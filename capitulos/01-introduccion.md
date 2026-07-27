---
titulo: 'Introduction: qué es una ontología y por qué no es una base de datos'
capitulo: 1
descripcion: 'El capítulo que fija el vocabulario. Cuatro definiciones, la hipótesis de mundo abierto, y un error semántico real en la ontología de ejemplo del propio libro — comprobado con un razonador.'
keet: 'cap. 1 (Introduction), §1.1–1.5'
---

El capítulo 1 no enseña a construir nada. Fija el vocabulario y responde una sola
pregunta con varias capas de profundidad: **qué es una ontología**. Casi todos los
malentendidos que se arrastran después nacen aquí.

Lo que sigue está ordenado por lo que de verdad cambia cómo modelas. Lo rutinario
va comprimido; lo que muerde, extendido.

## Las definiciones, rápido

Cuatro, en orden histórico, cada una arreglando a la anterior (§1.2.1, «The definition game»):

| Definición | Problema |
|---|---|
| **Gruber (1993)** — *«a specification of a conceptualization»* | la más citada y la más vaga: ni «especificación» ni «conceptualización» están definidas |
| **Studer et al. (1998)** — *«a formal, explicit specification of a shared conceptualization»* | añade formal, explícita y compartida; no dice qué significa «compartida» |
| **Guarino (1998)** — *«una teoría lógica que da cuenta del significado pretendido de un vocabulario formal»* | la útil de verdad |
| **Desarrolladores de OWL (2003)** — *«equivale a una base de conocimiento en lógica descriptiva»* | Keet la marca como indebidamente restrictiva |

**Quédate con la de Guarino**, porque es la única que explica qué estás haciendo
cuando añades un axioma: **cada axioma recorta el espacio de interpretaciones
posibles**. Una ontología sin axiomas admite cualquier interpretación y por tanto no
dice nada. No estás documentando: estás tachando mundos donde las cosas no son como
quieres.

De ahí sale también que el dibujito de cajas y flechas no es la ontología. Es una
foto de la ontología. La ontología es la teoría lógica.

### Ontology vs. ontology, en dos líneas

**Ontology** (mayúscula) es la disciplina filosófica: qué existe. **ontology**
(minúscula) es el artefacto computable. No es homonimia — la primera da los
criterios con los que decides qué merece ser una clase en la segunda.

Keet lista tres posturas, y sí cambian lo que metes en el archivo: **empirista**
(los términos refieren a entidades reales: infección por VIH, jacarandá),
**conceptualista** (a conceptos mentales: flogisto, unicornio) y **universalista**
(a universales que explican el parecido entre individuos). Si eres empirista,
`Unicornio` no entra. Decisión a tomar y sostener, no a dejar implícita.

---

## Lo que sí importa: mundo abierto

Aquí está la diferencia real con una base de datos, y el motivo de la mayoría de
las sorpresas con OWL.

| | Ontología | Modelo conceptual / esquema relacional |
|---|---|---|
| Alcance | independiente de la aplicación, reutilizable | específico de una aplicación |
| Formalización | teoría lógica explícita | diagramas informales de cajas y líneas |
| Razonamiento | inferencia automatizada | solo consultas |
| Supuesto | **mundo abierto (OWA)** | **mundo cerrado (CWA)** |

**CWA** (bases de datos): lo que no está afirmado ni es derivable, **es falso**. No
hay fila, no existe. Fin.

**OWA** (ontologías): la ausencia de información **no implica falsedad**. No está
escrito, luego no se sabe. Puede ser cierto y simplemente nadie lo anotó.

Si vienes de SQL o de TypeScript, este es el reflejo que hay que desprogramar, y
tiene una consecuencia inmediata:

> **En OWL, `domain` y `range` no validan nada.** No pueden: bajo mundo abierto no
> existe el dato «malo», solo el dato desconocido. Lo único que hacen es **inferir
> tipos en silencio**. Declaras un `domain` esperando un error y lo que obtienes es
> una clasificación que nadie pidió.

Cualquier consejo de modelado que trate estas construcciones como validación es
sencillamente incorrecto.

---

## El `∀` que no obliga a nada

La trampa que más caro sale en OWL, y la que hace posible el caso de estudio de más
abajo.

En §1.1 aparece la **African Wildlife Ontology (AWO)**, el ejemplo que atraviesa
todo el libro, con un mismo axioma escrito de cuatro maneras —*los leones comen
solo herbívoros, y comen algún impala*—:

| Notación | El axioma |
|---|---|
| Lógica de primer orden | `∀x(Lion(x) → ∀y(eats(x,y) → Herbivore(y)) ∧ ∃z(eats(x,z) ∧ Impala(z)))` |
| Lógica descriptiva | `Lion ⊑ ∀eats.Herbivore ⊓ ∃eats.Impala` |
| Lenguaje controlado | «Each lion eats only herbivore and eats some Impala» |
| RDF/XML | `owl:allValuesFrom`, `owl:someValuesFrom`, `rdfs:subClassOf` |

Mira los dos cuantificadores de esa única línea:

```
∀eats.Herbivore   →  "si come algo, es herbívoro"   NO obliga a comer
∃eats.Impala      →  "come al menos un impala"      SÍ obliga
```

`∀eats.plant` **lo cumple una piedra**. Una piedra no come nada, luego «todo lo que
come es planta» es verdad de forma vacía. `∀` no dice «come plantas», dice «no come
nada que no sea planta».

**Regla práctica: un `∀` casi nunca va solo.** Suele necesitar un `∃` al lado que
diga «y además come algo». Cuando el `∀` va dentro de una **clase definida**
(equivalencia, condiciones necesarias y suficientes), olvidarlo deja de ser una
curiosidad y se vuelve una bomba. Lo vemos funcionando en un minuto.

---

## Qué hace buena a una ontología

Dos ejes: **precisión** (¿representa solo lo pretendido?) y **cobertura**
(¿representa todo lo pretendido?).

| | Cobertura máxima | Cobertura limitada |
|---|---|---|
| **Precisión alta** | buena | mala — falta contenido necesario |
| **Precisión baja** | menos buena — admite modelos no pretendidos | peor |

Y tres niveles de error, de barato a caro:

| Error | Quién lo detecta |
|---|---|
| **sintáctico** — el archivo no parsea | el parser |
| **lógico** — inconsistencia, clases insatisfacibles | el razonador |
| **semántico** — formalizaste impecablemente **otra cosa** | **nadie** |

Que un razonador diga «consistente y sin clases insatisfacibles» significa *«lo que
dijiste no se contradice»*. No significa *«dijiste lo que querías decir»*.

Esa frase suena a advertencia genérica. No lo es, y lo que sigue lo demuestra
contra la ontología del propio libro.

---

# Caso de estudio: la brizna de hierba que rompe la ontología del libro

Todo lo que sigue se reproduce con:

```bash
cd capitulos/01-introduccion/artefactos
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
./.venv/bin/python verificar.py     # necesita Java en el PATH
```

El script razona con **HermiT** vía owlready2 y sale con código 1 si alguna
afirmación de esta página deja de cumplirse.

## El punto de partida: todo verde

`AfricanWildlifeOntology1.owl` —el archivo de material suplementario del libro—
tiene 31 clases, 5 propiedades de objeto y **cero individuos**: es TBox pura, sin
ABox. Solo tres clases están **definidas** (`owl:equivalentClass`): `herbivore`,
`carnivore` y `Omnivore`.

Se ejecuta el razonador:

```
[ok] la ontología es consistente
[ok] no hay clases insatisfacibles
[ok] giraffe se clasifica como herbivore
[ok] lion se clasifica como carnivore
```

Clasificación no trivial, cero errores. En un proyecto de software esto sería verde
en CI y se mergearía.

## La primera grieta: lo que *no* se infiere

Está declarado que el león come **solo** herbívoros y que come **algún** impala:

```
lion ⊑ ∀eats.herbivore ⊓ ∃eats.Impala
```

En lenguaje natural, de ahí se sigue que los impalas son herbívoros. El razonador
no lo infiere:

```
[ok] Impala NO se clasifica como herbivore
```

Y hace bien. Lo que se sigue es que *el impala concreto que se come ese león
concreto* es herbívoro — formalmente `lion ⊑ ∃eats.(Impala ⊓ herbivore)`. Nada dice
sobre la clase `Impala` entera: puede haber impalas que ningún león se coma.

No es un fallo, es OWA funcionando. Pero es la primera señal de que la intuición
del modelador y lo que el archivo dice no son lo mismo.

## El defecto

Las dos definiciones centrales:

```
herbivore ≡ ∀eats.plant   ⊔  ∀eats.(∃is-part-of.plant)
carnivore ≡ ∀eats.animal  ⊔  ∀eats.(∃is-part-of.animal)
carnivore ⊓ herbivore ⊑ ⊥
```

**El `⊔` está fuera del alcance del `∀`.** Se quería decir «come solo plantas o
partes de plantas». Lo que dice es «(come solo plantas) **o** (come solo partes de
plantas)». Un animal que coma una planta entera *y* una hoja no cumple ninguno de
los dos disyuntos y no es herbívoro. Lo correcto sería
`∀eats.(plant ⊔ ∃is-part-of.plant)`.

Pero la consecuencia grave es la otra. **`∀eats.plant` se satisface de forma vacía**
para cualquier cosa que no coma nada. Y como es una *equivalencia*, la implicación
va en los dos sentidos: cualquier entidad que no coma **es**, por definición, un
herbívoro. Y por el mismo argumento, un carnívoro. Y esas dos clases están
declaradas disjuntas.

## La prueba

La ontología, tal como viene, es consistente — porque bajo mundo abierto el
razonador nunca puede asumir que algo no come; siempre puede inventarle un
alimento. La contradicción solo aparece cuando se le cierra esa puerta.

Se añade un individuo que ningún biólogo discutiría: una brizna de hierba que no
come nada.

```python
brizna = Grass("brizna_de_hierba_1")
brizna.is_a.append(eats.exactly(0, Thing))   # una brizna no come
```

```
[ok] afirmar que una brizna de hierba no come vuelve INCONSISTENTE la ontología
```

Toda la ontología. No una clase insatisfacible: **inconsistente**, que es la avería
total — a partir de ahí el razonador deriva cualquier cosa y ninguna respuesta
sirve.

Mide el desastre contra su causa. La causa es **un paréntesis mal puesto** en dos
líneas. La ontología pasaba el razonador. Habría pasado cualquier suite que solo
comprobara consistencia. Y revienta con el primer dato real que alguien cargue.

## La corrección, y su precio

Meter el `⊔` dentro del `∀`, y añadir un `∃` que impida la satisfacción vacía:

```
herbivore ≡ animal ⊓ ∃eats.⊤ ⊓ ∀eats.(plant  ⊔ ∃is-part-of.plant)
carnivore ≡ animal ⊓ ∃eats.⊤ ⊓ ∀eats.(animal ⊔ ∃is-part-of.animal)
```

```
[ok] con las definiciones corregidas, la brizna ya no rompe nada
[ok] lion sigue clasificándose como carnivore
[ok] PERO giraffe pierde la clasificación de herbivore
```

**La jirafa deja de ser herbívora.** No es un fallo de la corrección: sobre la
jirafa solo estaba declarado `∀eats.(Twig ⊔ leaf)` — *si* come, come ramitas u
hojas. Nunca se declaró que coma. Antes se colaba como herbívora **justamente por
el bug que se acaba de arreglar**: era una inferencia correcta por la razón
equivocada.

Se declara lo que faltaba y vuelve:

```python
giraffe.is_a.append(eats.some(leaf))     # las jirafas comen alguna hoja
```

```
[ok] con ∃eats.leaf, giraffe vuelve a clasificarse como herbivore
```

## Qué deja el caso

1. **El razonador comprueba coherencia, no verdad.** Precisión baja, en la matriz de
   §1.2.3: se admiten modelos no pretendidos y todos son perfectamente consistentes.
2. **Bajo OWA los errores se esconden hasta que llegan los datos.** El mundo abierto
   absorbe modelado defectuoso durante todo el desarrollo y lo devuelve en
   producción, cuando alguien afirma algo negativo o cerrado. Probar la TBox sola no
   basta: **hay que probarla contra individuos**.
3. **Ninguna herramienta iba a preguntar «¿sigue siendo herbívora la jirafa?».** Esa
   pregunta la escribe una persona, antes de modelar, y queda automatizada. Son las
   **preguntas de competencia**, el equivalente real de los tests unitarios, y es lo
   que el capítulo 5 manda hacer desde el minuto cero.
4. **La versión 1 es la foto del «antes».** `AfricanWildlifeOntology1.owl` es la
   primera de una serie que el libro va corrigiendo capítulo a capítulo. Encontrarle
   defectos no es contradecir a Keet: es el ejercicio.

---

## Para qué sirven, sin humo

§1.3, comprimido:

| Uso | Ejemplo del libro |
|---|---|
| Integración a nivel de **esquema** — vocabulario común sobre los modelos de cada sistema | fusión de universidades u hospitales; `Flower` ≡ `Bloem` |
| Integración a nivel de **instancia** — identificadores compartidos para anotar tuplas | Gene Ontology: KEGG e InterPro anotan con `GO:0004619` |
| e-learning | contenido adaptado al perfil del estudiante |
| Pregunta-respuesta | Watson en *Jeopardy!* |
| Humanidades digitales (OBDA) | ánforas y comercio de alimentos, consultados sin SQL |
| Flujos de trabajo científicos | Taverna: repetibilidad y procedencia |
| Descubrimiento científico | moléculas candidatas de caucho; enzimas, superando a expertos humanos |

La diferencia entre las dos primeras es **a qué nivel se pega la ontología**: al
esquema (qué tipos de cosas hay) o a las tuplas (esta fila concreta trata de esto).
La de instancia no obliga a armonizar esquemas ni a centralizar nada, y por eso es
la que triunfó en biología — *criterio propio: escala mejor socialmente, porque
cada base conserva su autonomía y solo hay que acordar etiquetas.*

El patrón detrás de todos: aportan valor donde hay **heterogeneidad semántica** o
donde hace falta **conocimiento que no está en los datos**. Una sola base de datos
bajo tu control y sin inferencia → una ontología es sobreingeniería. Conviene
saberlo antes de enamorarse del tema.

---

## Los ejercicios (§1.5)

El libro trae dos series distintas por capítulo y conviene no mezclarlas al
citar: **Review question N.x** (conceptuales) y **Exercise N.x** (prácticos).
Enunciados citados literal; resolución propia.

**Review question 1.1.** *«…describe them in your own words, in particular: ontology-driven
information system, Ontology, ontology, and ontology engineering.»*

**ontology-driven information system**: la ontología no es documentación adjunta,
es una pieza en ejecución. La prueba operativa — si borrarla no cambia el
comportamiento del sistema, no es un sistema dirigido por ontologías, es un sistema
con un glosario. **Ontology / ontology / ontology engineering**: ya arriba; la
tercera es la disciplina de construir, evaluar y mantener el artefacto — la palabra
*engineering* está puesta en oposición a modelar por intuición.

**Review question 1.2.** *«List several uses of ontologies.»* → la tabla de la sección anterior.

**Review question 1.3.** *«Describe the difference between schema vs.
instance-level data integration.»*

| | Esquema | Instancia |
|---|---|---|
| Qué se alinea | tipos, clases, atributos | tuplas concretas |
| Requiere tocar los esquemas | sí (mapeo) | no |
| Ontología típica | rica en axiomas | vocabulario controlado ligero |
| Ejemplo | fusión de dos hospitales | Gene Ontology |

**Exercise 1.1.** *«…install an ODE, such as Protégé, load the AfricanWildlifeOntology1.owl…
and open it in your text editor.»*

El archivo está en
[`artefactos/AfricanWildlifeOntology1.owl`](https://github.com/inter097/ontology-engineering/blob/main/capitulos/01-introduccion/artefactos/AfricanWildlifeOntology1.owl).
En el editor de texto es RDF/XML, verboso hasta lo cómico: «cada león come solo
herbívoros» ocupa una decena de líneas anidadas, y un `∀` es un `owl:Restriction`
con `owl:allValuesFrom`. Justo lo que decía §1.1 — la sintaxis de intercambio está
hecha para máquinas. Inventario contado sobre el XML:

```
31 clases     5 propiedades de objeto    0 individuos
50 rdfs:subClassOf    26 someValuesFrom (∃)    9 allValuesFrom (∀)
 6 equivalentClass     7 axiomas de disyunción    2 rdfs:range    0 rdfs:domain
```

En Protégé, antes del razonador la jerarquía es plana y aburrida. Al pulsar «start
reasoner» aparece lo interesante — que es el caso de estudio de arriba.

Un detalle que salta a la vista: la mereología está mejor cuidada que el resto.
`is-part-of` transitiva y reflexiva, `has-part` su inversa y también transitiva,
`is-proper-part-of` subpropiedad suya e **irreflexiva** — que es la manera correcta
de distinguir parte de parte propia.

**Exercise 1.2.** *«…is it a good, less good, bad, or even worse ontology? Why?»*

**Menos buena**: precisión baja, cobertura razonable. Además del defecto del caso de
estudio:

- **Nomenclatura incoherente** — `lion`, `giraffe`, `plant` en minúscula junto a
  `Impala`, `Elephant`, `RockDassie` en CamelCase, y `tasty-plant` con guion.
  Cosmético hasta que hay que alinearla con otra ontología.
- **`tasty-plant` no es una clase del dominio** — definida como planta comida por
  algún carnívoro y algún herbívoro. «Sabrosa» es epistémico y subjetivo, y la
  definición ni siquiera habla de sabor. Error semántico de manual.
- **Casi no hay disyunción** — 7 axiomas para 31 clases. Nada impide que un
  `Warthog` sea también un `RockDassie`. Bajo OWA, lo que no se declara disjunto se
  considera posiblemente solapado, y el razonador deja de detectar errores.
- **`Palmtree ⊑ ∃has-part.¬branch`** — «toda palmera tiene alguna parte que no es
  una rama». Literalmente cierto (tiene hojas) y completamente inútil: se quería
  decir `Palmtree ⊑ ¬∃has-part.branch`. El mismo error de alcance de cuantificador.

Y casi con seguridad es **a propósito**: es la versión 1 de una serie que el libro
corrige capítulo a capítulo. Responder «es buena porque el razonador no se queja»
sería caer justo en la trampa que el capítulo acaba de explicar.

---

## Lo que hay que llevarse

1. Una ontología es una **teoría lógica**. Cada axioma recorta modelos.
2. **OWA, no CWA.** No valida; infiere. Este solo punto explica la mayoría de las
   sorpresas con OWL.
3. **`∀` no obliga a nada** y se cumple de forma vacía. En una clase definida, eso
   es una bomba.
4. Los errores **semánticos** no los detecta ninguna herramienta. Es lo que
   justifica escribir preguntas de competencia.
5. Probar el esquema solo no basta. **Hay que probarlo contra individuos.**

<small>Salvo los enunciados citados y la ontología de ejemplo, el análisis de esta
página es criterio propio, verificado con HermiT. Numeración del autor: este es el
capítulo 1; LibreTexts lo publica como «02».</small>
