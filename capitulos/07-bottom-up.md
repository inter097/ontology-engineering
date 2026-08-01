---
titulo: 'Bottom-up: reutilizar lo que ya hay, y lo que se pierde al hacerlo'
capitulo: 7
descripcion: 'De bases de datos, modelos conceptuales, tesauros y texto a una ontología. El modelo UML del ejercicio 7.2 razonado con HermiT: una clase insatisfacible y dos subsunciones que nadie dibujó.'
keet: 'cap. 7 (Bottom-up Ontology Development), §7.1–7.7'
hallazgo: 'Un NOT NULL de base de datos no sobrevive a la traducción: ni como domain, ni como ∃. La fila que la base de datos rechazaría, la ontología la acepta sin decir nada.'
cifras:
  - valor: '1'
    etiqueta: 'clase insatisfacible en el modelo UML'
  - valor: '2'
    etiqueta: 'subsunciones no dibujadas'
  - valor: '12'
    etiqueta: 'comprobaciones'
---

El capítulo 6 empezaba por arriba. Este empieza por abajo: **ya existe material** —una
base de datos, un modelo UML, un tesauro, un corpus de texto— y la pregunta es qué
parte se puede reaprovechar. La respuesta corta del capítulo: casi todo se puede
convertir, y casi nada significa lo mismo después.

## Bases de datos y modelos conceptuales (§7.1)

La tentación es una tabla → una clase, una columna → una propiedad. Keet dedica la
primera *review question* del capítulo a desmontarlo, y hay tres razones distintas:

1. **En la base de datos hay cosas que no son del dominio**: tablas puente de
   relaciones muchos-a-muchos, claves subrogadas, tablas de auditoría, campos
   desnormalizados por rendimiento.
2. **Falta lo que la base de datos nunca necesitó**: jerarquías, disyunciones,
   definiciones. Un esquema relacional no distingue entre subclase y clave foránea.
3. **Las restricciones cambian de naturaleza.** Una base de datos **valida**; una
   ontología **infiere**. Es la parte C del caso de estudio y es la que más daño hace.

Con los modelos conceptuales (UML, ER, ORM) el punto de partida es mejor: ya tienen
jerarquías, disyunción, completitud y cardinalidades. Pero traen dos decisiones
propias (Review question 7.2): **qué hacer con los atributos** —¿propiedad de datos, o
una clase de cualidad al estilo de la fundacional del capítulo 6?— y **qué hacer con
las relaciones n-arias**, que en OWL hay que reificar porque solo hay binarias.

## Tesauros (§7.3)

Un tesauro tiene tres tipos de relación: **BT/NT** (*broader term* / *narrower term*),
**RT** (*related term*) y **USE/UF** (término preferente y sus sinónimos). El estándar
del W3C para publicarlos es **SKOS**.

Y aquí está la trampa del capítulo (Review question 7.4): **`broader` no es
`subClassOf`**. En un tesauro, «más amplio» significa lo que le pareció al
documentalista: unas veces es «es un tipo de», otras «es parte de», otras «tiene que
ver con». Convertirlo mecánicamente produce una jerarquía de clases que deduce cosas
falsas.

<details class="peras">
<summary>¿Y esto qué quiere decir? Sin jerga</summary>

Un tesauro es una lista de palabras con flechas de «más general» a «más específico».
Sirve para buscar: si buscas *coche*, te sugiere mirar también *vehículo*.

Para buscar funciona de maravilla, porque a un humano le da igual **por qué** están
conectadas dos palabras: le basta con que le lleve a documentos parecidos.

Pero al convertirlo en ontología, esa flecha pasa a significar algo muy concreto:
*«todo lo que sea esto, es también aquello»*. Y entonces las flechas que estaban ahí
por otro motivo empiezan a mentir.

En el tesauro, *motor* cuelga de *coche* porque quien lo escribió pensó «los motores
salen al buscar coches». Al convertirlo, esa flecha pasa a decir **«todo motor es un
coche»**. Y como *coche* cuelga de *vehículo*, la máquina concluye que **todo motor es
un vehículo**.

Nadie escribió esa frase. Salió sola.

</details>

## Texto y otros métodos semiautomáticos (§7.4, §7.5)

Keet abre la sección del texto con un *«if all else fails…»* que conviene tomarse en
serio: el texto no está estructurado y el lenguaje natural es ambiguo. Hay **dos
formas** de usar NLP (Review question 7.5):

- **poblar la TBox** — sacar términos candidatos a clase: *ontology learning*;
- **poblar la ABox** — sacar entidades nombradas: *ontology population*.

Del resto de métodos semiautomáticos, los que importan conceptualmente son dos
servicios de razonamiento **no estándar** (Review question 7.7):

| Servicio | Qué hace | Para qué sirve |
|---|---|---|
| **Least common subsumer** | dados varios conceptos, el concepto más específico que los subsume a todos | proponer la superclase que falta en una jerarquía |
| **Most specific concept** | dado un individuo, la descripción más específica que lo captura | subir de la ABox a la TBox: generalizar ejemplos |

Los dos van de abajo arriba, y los dos son **inducción**, no deducción — con lo que
eso implica desde el [capítulo 2](/capitulos/02-logica-primer-orden/): lo que
proponen es una hipótesis, no una consecuencia. El aprendizaje automático aplicado a
ontologías está en la misma categoría.

## Patrones de diseño (§7.6)

Los **ODP** (*Ontology Design Patterns*) son soluciones reutilizables a problemas de
modelado recurrentes: relaciones n-arias, participación, transformación material,
listas. Son lo más parecido que hay a reutilizar sin heredar una ontología entera, y
la vía por la que el capítulo 7 se conecta con el 6: un patrón de contenido suele
venir ya alineado con una fundacional.

---

<h2 class="caso">Caso de estudio: lo que sobrevive a la conversión y lo que no</h2>

Reproducible con:

```bash
cd capitulos/07-bottom-up/artefactos
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
./.venv/bin/python verificar.py     # necesita Java en el PATH
```

## A. Exercise 7.2(a): el modelo UML que esconde dos cosas

El enunciado describe la Figura 7.7: `Employee` **particionado** (disjunto y
completo) en `Clerk` y `Manager`; `RichEmployee` y `PoorEmployee` como subclases de
`Employee`, disjuntas de `Clerk` y de `Manager` respectivamente; el atributo `salary`
restringido a cadena de 8 en todas las subclases **salvo** en `Clerk`, que la tiene de
5. El ejercicio avisa: hay una clase inconsistente y una subsunción nueva.

```
[ok] el modelo por sí solo es consistente: el problema no se ve sin razonar
[ok] PoorEmployee es INSATISFACIBLE
[ok] RichEmployee sí es satisfacible
[ok] subsunción nueva: RichEmployee ⊑ Manager
[ok] PoorEmployee ni aparece bajo Clerk: ya es equivalente a ⊥
[ok] quitando SOLO la longitud del salario aparece PoorEmployee ⊑ Clerk, y nada es insatisfacible
```

<p class="evidencia">modelo 7.7 ⊨ RichEmployee ⊑ Manager, y PoorEmployee ⊑ ⊥</p>

La cadena, entera:

1. `Employee ≡ Clerk ⊔ Manager` (la partición es **completa**: no hay empleados de
   otro tipo).
2. `RichEmployee` es disjunta de `Clerk`, luego todo `RichEmployee` es `Manager`.
   **Nadie dibujó esa flecha**, y es una afirmación fuerte sobre la empresa.
3. Simétricamente, `PoorEmployee ⊑ Clerk`.
4. Pero `PoorEmployee` tiene salario de 8 caracteres y `Clerk` de 5. Con el atributo
   obligatorio y único, no hay valor posible: `PoorEmployee` no puede tener
   instancias.

La última comprobación es la que hace útil el ejercicio: al quitar **solo** la
restricción de longitud, la insatisfacibilidad desaparece y aflora la subsunción
`PoorEmployee ⊑ Clerk` que estaba tapada. Mientras una clase es insatisfacible,
**equivale a `⊥`** y el razonador la mete debajo de todo, así que la jerarquía
inferida no dice nada de ella. Es la razón de que se reparen las insatisfacibilidades
**una a una y de abajo arriba**: hasta que no se arregla la primera, no se ve la
siguiente.

Y sobre el apartado (c) —*«are there any problems with the original conceptual data
model?»*— la respuesta es sí, y de dos tipos: uno lógico (`PoorEmployee` es
imposible) y otro de modelado (la partición completa convierte «rico» y «pobre» en
sinónimos encubiertos de «directivo» y «administrativo», que casi seguro no era la
intención).

## B. El tesauro convertido término a término

```
Motor  broader  Coche  broader  Vehículo
```

```
[ok] con broader → subClassOf se deduce «todo motor es un vehículo»
[ok] separando la parte-todo del es-un, la deducción falsa desaparece
[ok] y al declarar Motor y Vehículo disjuntos, la conversión ingenua vuelve la ontología INCONSISTENTE
```

<p class="evidencia hipotesis">deducción falsa: Motor ⊑ Vehiculo</p>

Las dos flechas del tesauro son relaciones **distintas** escritas igual: la primera es
parte-todo, la segunda es subsunción. Encadenadas bajo `subClassOf`, producen una
falsedad. Y la tercera línea es la más útil en la práctica: en cuanto la ontología
crece lo suficiente como para tener la disyunción correcta —un motor no es un
vehículo— la conversión ingenua deja de ser un error silencioso y pasa a ser una
inconsistencia. **El error no cambió; cambió que ahora hay suficiente teoría para
detectarlo.**

Es la misma lección del [capítulo 6](/capitulos/06-top-down/) desde el otro lado: allí
la mezcla venía de declarar transitiva una propiedad que llevaba dentro dos
relaciones; aquí viene heredada de una fuente que nunca distinguió.

## C. Lo que no sobrevive: la restricción de la base de datos

Tabla `Empleado`, columna `departamento` NOT NULL con su clave foránea. Se inserta un
empleado sin departamento:

```
[ok] traducido a domain/range: NO produce ningún error
[ok] traducido a ∃trabajaEn.Departamento: TAMPOCO
[ok] lo único que OWL rechaza es una contradicción lógica
```

<p class="evidencia">OWL acepta la fila que la base de datos rechazaría — en las dos traducciones</p>

Las dos traducciones habituales del NOT NULL fallan, y por motivos distintos:

- **`domain`/`range` no validan**: clasifican. Es la trampa que este trabajo verifica
  también en el [capítulo 5](/capitulos/05-metodologias/).
- **`∃trabajaEn.Departamento` sí es una restricción de verdad**, pero bajo mundo
  abierto se satisface suponiendo que existe un departamento **que no consta**. El
  razonador no exige que esté en los datos: exige que sea posible.

Lo único que OWL rechaza es una contradicción lógica —un individuo que sea empleado y
departamento a la vez, siendo disjuntas—, y eso no es lo que un NOT NULL quiere decir.

<details class="errata">
<summary>Por qué esto es la mitad de los proyectos fallidos de integración</summary>

El proyecto típico: hay una base de datos con integridad referencial cuidada durante
años, alguien la convierte a OWL, y a partir de ahí **se da por hecho** que la
ontología conserva esas garantías. No conserva ninguna.

Lo que se pierde no es la información: es la **capacidad de rechazar**. Un esquema
relacional es un filtro —lo que no encaja no entra—; una ontología es una teoría —lo
que no encaja se convierte en una deducción nueva, o en nada—.

Y hay una consecuencia que suele sorprender: la ontología no da error **precisamente
porque es más permisiva**, así que la conversión parece un éxito. El fallo aparece
meses después, en forma de consulta que devuelve resultados que no deberían existir.

Lo defendible es no fingir: si hacen falta garantías de integridad sobre los datos,
se dejan en la base de datos y se accede a ella desde la ontología —que es
exactamente el planteamiento del [capítulo 8](/capitulos/08-obda/)— o se añade una
capa de validación aparte, tipo SHACL, que es mundo cerrado y sí rechaza.

</details>

## Qué deja el caso

1. **Convertir es fácil; conservar el significado, no.** Cada fuente pierde algo
   distinto al pasar a OWL.
2. **Un modelo conceptual razonado dice más de lo que dibuja.** Dos subsunciones y
   una clase imposible salieron de una figura que nadie consideraba problemática.
3. **Repara de una en una:** una clase insatisfacible tapa lo que hay debajo.
4. **Las restricciones de integridad no se traducen.** Ni con `domain`, ni con `∃`.

---

## Los ejercicios (§7.7)

**Review question 7.1.** *«Why can one not simply convert each database table into an
OWL class?»* — Porque el esquema contiene artefactos de implementación (tablas puente,
claves subrogadas, desnormalizaciones), le falta lo que una ontología necesita
(jerarquías, disyunciones, definiciones) y, sobre todo, porque **sus restricciones
validan y las de OWL no**: verificado en la parte C del caso de estudio.

**Review question 7.2.** *«Name two modelling considerations going from conceptual
data model to ontology.»* — (1) **Los atributos**: si se representan como propiedades
de datos o se reifican como cualidades con su portador, que es lo que pide una
fundacional (cap. 6). (2) **Las relaciones n-arias**: OWL solo tiene binarias, así que
hay que reificarlas en una clase, con la pérdida de legibilidad que eso conlleva.
Añadiría una tercera: qué hacer con las **cardinalidades mínimas**, que en el modelo
conceptual son obligatoriedad de los datos y en OWL solo son una restricción
existencial satisfacible por objetos que no constan.

**Review question 7.3.** *«Name the type of relations in a thesaurus.»* — BT/NT
(broader/narrower term), RT (related term) y USE/UF (término preferente frente a sus
no preferentes).

**Review question 7.4.** *«What are some of the issues when developing an ontology
bottom-up using a thesaurus?»* — Que `broader` **no** es subsunción: mezcla «es un tipo
de», «es parte de» e incluso asociación temática, y al convertirla mecánicamente se
deducen falsedades —verificado en la parte B—. Además, los términos de un tesauro son
**palabras**, no conceptos: hay polisemia, términos compuestos que corresponden a
axiomas y no a clases, y `RT` no tiene ninguna traducción lógica.

**Review question 7.5.** *«What are the two ways one can use NLP for ontology
development?»* — Poblar la **TBox** extrayendo términos candidatos a clase (*ontology
learning*) y poblar la **ABox** extrayendo entidades nombradas (*ontology
population*).

**Review question 7.6.** *«Machine learning was said to use inductive methods.»* — La
inducción generaliza desde individuos a una regla y **no conserva la verdad**: puede
producir una regla falsa a partir de premisas verdaderas (cap. 2). La deducción sí la
conserva y no aporta conocimiento nuevo. Un razonador de ontologías solo deduce; todo
lo que salga de aprendizaje automático entra en la ontología como **hipótesis a
validar**, nunca como axioma directo.

**Review question 7.7.** *«Describe the least common subsumer and most specific
concept.»* — El **least common subsumer** de varios conceptos es el concepto más
específico que los subsume a todos: sugiere la superclase que falta. El **most
specific concept** de un individuo es la descripción más específica que lo captura:
sirve para generalizar de la ABox a la TBox. Los dos son servicios **no estándar** y
los dos producen candidatos, no consecuencias.

**Exercise 7.1.** *«Examine Figure 7.6 and answer…»* — Depende de una figura del libro
y del modelo concreto que muestra, así que **no se afirma aquí ningún resultado sobre
ella**. Lo transferible es el método, que es el del Exercise 7.2 y está ejecutado: pasar
el diagrama a OWL, razonar, y comparar lo inferido con lo dibujado. *Criterio propio: en
un modelo en ICom, lo que sistemáticamente no se puede representar son las
restricciones que cruzan varias relaciones a la vez —«el mismo empleado no puede ser
jefe y subordinado del mismo proyecto»— por la misma razón que en el capítulo 2 no
cabía en `ALC`.*

**Exercise 7.2.** *«Which class is inconsistent and what subsumes what?»* — Parte A del
caso de estudio: **`PoorEmployee` es insatisfacible**, y las subsunciones no dibujadas
son `RichEmployee ⊑ Manager` y `PoorEmployee ⊑ Clerk`. Sobre (b) —una ontología decente
que sirva para los dos modelos—, *criterio propio*: (i) sacar `RichEmployee` y
`PoorEmployee` de la partición, porque «rico» y «pobre» son **roles o estados**
dependientes del salario, no tipos de empleado, y colgarlos de `Employee` viola la regla
de rigidez de OntoClean (cap. 5); (ii) modelar el salario como cualidad con valor
numérico en vez de como cadena de longitud fija —la longitud de la cadena es una
`encoding peculiarity` (Review question 5.3), no un hecho del dominio—; y (iii) las
condiciones de proyectos, `Clerk ⊑ ≤3 worksOn.Project` y `Manager ⊑ ≥1 manages.Project`,
que son cardinalidades cualificadas y por tanto exigen OWL 2 (cap. 4).

**Exercise 7.3.** *«Consider the small section of the ERIC thesaurus. In which
W3C-standardised language would you represent it, and why?»* — En **SKOS**, y la razón
es exactamente la del caso de estudio: SKOS existe para representar tesauros **sin**
comprometerse a que `broader` sea subsunción. `skos:broader` no es transitiva por
defecto ni implica pertenencia, así que no deduce nada falso. Pasarlo a OWL con
`rdfs:subClassOf` sería afirmar mucho más de lo que el documentalista quiso decir.
*Criterio propio: la ruta defendible es SKOS primero, y después una conversión
selectiva —término a término, con criterio humano— de la parte del tesauro que de
verdad sea taxonómica.*

---

## Lo que hay que llevarse

1. **Bottom-up es reutilizar, no convertir.** La conversión mecánica siempre
   introduce afirmaciones que la fuente nunca hizo.
2. **`broader` ≠ `subClassOf`.** Es el error más caro del capítulo, y SKOS existe
   justo para no cometerlo.
3. **Razonar un modelo conceptual sale barato y encuentra cosas**: aquí, dos
   subsunciones ocultas y una clase imposible.
4. **La integridad de los datos se queda en la base de datos.** Si hace falta
   rechazar filas, OWL no es la herramienta — el capítulo 8 explica la alternativa.

<small>Salvo los enunciados citados, el análisis y las resoluciones de esta página
son criterio propio, verificados con HermiT. Numeración y enunciados tomados del PDF
en <a href="https://github.com/inter097/ontology-engineering/tree/main/libro">/libro</a>,
no de ediciones web que renumeran las secciones.</small>

<details class="defensa">
<summary>Para la defensa — lo que te van a preguntar de aquí</summary>

**«Ya existe una base de datos del dominio. ¿Por qué no la conviertes y ya está?»**

Porque la conversión mecánica produce una ontología que afirma cosas que la base de
datos no decía y pierde las garantías que sí daba. El esquema contiene artefactos de
implementación que no son del dominio, y le falta todo lo que hace útil a una
ontología: jerarquías, disyunciones y definiciones. La base de datos es una **fuente**
de vocabulario y de instancias, no un borrador de la ontología.

**«¿Qué se pierde exactamente al convertir?»**

La capacidad de rechazar. Está verificado: un empleado sin departamento —la fila que
un NOT NULL impediría— no produce ningún error en OWL, ni traduciendo la columna a
`domain`/`range` ni traduciéndola a `∃trabajaEn.Departamento`. En el primer caso porque
el dominio infiere en vez de validar; en el segundo porque el mundo abierto permite
suponer un departamento que no consta.

*El matiz que conviene añadir:* si el proyecto necesita validación de datos, la
herramienta no es OWL. O se deja en la base de datos y se accede desde la ontología
(cap. 8), o se añade una capa tipo SHACL, que sí es de mundo cerrado.

**«¿Puedes reutilizar el tesauro que ya tiene la organización?»**

Sí, pero como SKOS, no como OWL. `skos:broader` no significa subsunción: en un tesauro
mezcla «es un tipo de», «es parte de» y simple asociación temática.

*Por qué es una respuesta fuerte:* está medido. En el caso de estudio, una cadena de
tres términos —motor, coche, vehículo— convertida término a término hace que el
razonador deduzca que **todo motor es un vehículo**, y en cuanto la ontología crece
hasta tener la disyunción correcta, esa conversión la vuelve **inconsistente**. El
error no aparece el día de la conversión: aparece el día que la ontología es lo bastante
buena para detectarlo.

**«¿Es fiable lo que sacan los métodos automáticos —NLP, aprendizaje— para una
ontología?»**

Como candidatos, sí; como axiomas, no. Son métodos **inductivos** y la inducción no
conserva la verdad (cap. 2): un solo contraejemplo no baja una precisión, vuelve la
ontología inconsistente. Lo mismo vale para el *least common subsumer* y el *most
specific concept*: proponen, no demuestran. Todo lo que entra por esa vía pasa por
revisión humana y por el razonador antes de quedarse.

**«Tu modelo conceptual de partida ya estaba validado por el equipo. ¿Qué aportó
razonarlo?»**

Tres cosas que nadie había visto en el diagrama: una clase que no puede tener
instancias (`PoorEmployee`) y dos relaciones de subsunción que nadie dibujó
(`RichEmployee ⊑ Manager` y su simétrica). Ninguna era visible a ojo, y las tres son
consecuencias de combinar una partición completa con dos disyunciones — que es
exactamente el tipo de interacción que un humano no calcula mentalmente y un razonador
resuelve en milisegundos.

</details>
