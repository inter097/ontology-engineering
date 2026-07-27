---
titulo: Ejercicios del capítulo 1, resueltos
capitulo: 1
seccion: ejercicios
descripcion: 'Los cinco ejercicios de la sección 1.E, resueltos y explicados. El quinto —¿es buena la ontología de ejemplo?— se responde con un razonador, no con opinión.'
keet: cap. 1, §1.E (Exercises)
---

Los cinco ejercicios tal como los plantea el libro, resueltos paso a paso. El
enunciado va citado literal; la resolución es propia salvo donde se indica.

---

## Ejercicio 1

> *«There are several terms in the preceding sections that were highlighted in bold
> in the text. Find them, and try to describe them in your own words, in particular:
> ontology-driven information system, Ontology, ontology, and ontology engineering.»*

**ontology-driven information system** — un sistema de información donde la
ontología no es documentación adjunta sino una pieza en ejecución: el sistema
consulta la ontología y un razonador deriva conocimiento que nadie escribió en la
base de datos. La distinción operativa: si borrar la ontología no cambia el
comportamiento del sistema, no es un sistema dirigido por ontologías, es un
sistema con un glosario.

**Ontology** (mayúscula) — la rama de la filosofía que estudia qué existe y cómo
se estructura la realidad. No produce archivos; produce los criterios con los que
se decide qué merece ser una clase.

**ontology** (minúscula) — el artefacto: una teoría lógica, computable, sobre un
dominio, pensada para ser reutilizada por más de una aplicación.

**ontology engineering** — la disciplina de construir, evaluar y mantener esos
artefactos: métodos, metodologías, lenguajes y herramientas. La palabra
*engineering* está puesta a propósito, en oposición a que cada quien modele por
intuición.

Un matiz que Keet subraya y conviene no perder: la relación entre las dos
*ontolog(í)as* no es de homonimia. La disciplina filosófica es la que da los
criterios —¿los universales existen?, ¿un rol es una entidad?— con los que se toman
decisiones concretas en el archivo.

---

## Ejercicio 2

> *«List several uses of ontologies.»*

| Uso | Qué aporta la ontología | Ejemplo del libro |
|---|---|---|
| Integración de datos a nivel de **esquema** | vocabulario común por encima de los modelos conceptuales de cada sistema | fusión de universidades u hospitales; `Flower` ≡ `Bloem` |
| Integración a nivel de **instancia** | identificadores compartidos para anotar tuplas | Gene Ontology: KEGG e InterPro anotan con `GO:0004619` |
| **e-learning** | adaptar contenido al perfil y las preferencias del estudiante | sistemas educativos adaptativos |
| **Pregunta-respuesta** | clasificar entidades y localizar respuestas en fuentes heterogéneas | Watson en *Jeopardy!* |
| **Humanidades digitales** (OBDA) | consultar datos federados en el vocabulario del dominio, no en SQL | ánforas y comercio de alimentos |
| **Flujos de trabajo científicos** | orquestar pipelines, repetibilidad y procedencia | Taverna |
| **Descubrimiento científico** | generar hipótesis sobre grandes volúmenes | moléculas candidatas de caucho; descubrimiento de enzimas que superó a expertos |

El patrón detrás de todos: la ontología aporta valor donde hay **heterogeneidad
semántica** —varias fuentes que hablan del mismo dominio con vocabularios
distintos— o donde hace falta **conocimiento no explícito en los datos**. Si hay
una sola base de datos, bajo control, y no se necesita inferencia, una ontología
es sobreingeniería.

---

## Ejercicio 3

> *«Describe the difference between schema vs. instance-level data integration.»*

La diferencia es **a qué nivel se pega la ontología**.

**A nivel de esquema** se integran los *tipos*. La ontología se sitúa por encima
de los modelos conceptuales (EER, UML) de cada sistema y establece
correspondencias entre ellos: la clase `Student` de un sistema y
`AdvancedLearners` de otro se mapean al mismo término de la ontología. Los datos
siguen donde estaban; lo que se armoniza es el significado de las estructuras.

**A nivel de instancia** se integran los *registros individuales*. Nadie armoniza
esquemas: cada base de datos, con su modelo propio, anota sus tuplas con
identificadores de un vocabulario controlado compartido. Dos registros de KEGG e
InterPro quedan conectados porque ambos citan `GO:0004619`, no porque sus tablas
se parezcan.

| | Esquema | Instancia |
|---|---|---|
| Qué se alinea | tipos, clases, atributos | tuplas concretas |
| Requiere tocar los esquemas | sí (mapeo) | no |
| Requiere almacenamiento central | no necesariamente | no |
| Ontología típica | rica en axiomas | vocabulario controlado ligero |
| Ejemplo | fusión de dos hospitales | Gene Ontology |

**Criterio propio, no del libro:** la integración a nivel de instancia escala mejor
socialmente —cada base mantiene su autonomía y solo hay que ponerse de acuerdo en
las etiquetas— y por eso es la que triunfó en biología. La de esquema da respuestas
más ricas pero exige un acuerdo político que rara vez existe.

---

## Ejercicio 4

> *«You may like to get a practical 'feel' of ontologies and how they look like in an
> ontology development environment. To this end, install an ODE, such as Protégé,
> load the AfricanWildlifeOntology1.owl from the book's supplementary material page
> at http://www.meteck.org/teaching/OEbook/ in the tool and browse around. Download
> the AfricanWildlifeOntology1.owl file (right-click, save as) and open it in your
> text editor, such as notepad.»*

El archivo está en este repositorio en
[`capitulos/01-introduccion/artefactos/AfricanWildlifeOntology1.owl`](https://github.com/inter097/ontology-engineering/blob/main/capitulos/01-introduccion/artefactos/AfricanWildlifeOntology1.owl),
descargado de la página de material suplementario del libro.

**Lo que se ve al abrirlo en un editor de texto.** Es RDF/XML. Verboso hasta lo
cómico: el axioma «cada león come solo herbívoros» ocupa una decena de líneas
anidadas. Un `∀` es un `owl:Restriction` con `owl:onProperty` y `owl:allValuesFrom`.
Esto es exactamente lo que decía §1.2: la sintaxis de intercambio está hecha para
máquinas, y por eso hace falta Protégé o la sintaxis Manchester para trabajar.

**Inventario del archivo,** contado sobre el propio XML:

```
31 clases        5 propiedades de objeto     0 individuos
50 rdfs:subClassOf      26 someValuesFrom (∃)     9 allValuesFrom (∀)
 6 equivalentClass       7 axiomas de disyunción   2 rdfs:range   0 rdfs:domain
36 rdfs:comment
```

Cero individuos: es una ontología puramente de nivel de esquema — TBox, sin ABox.

**Lo que se ve al abrirlo en Protégé.** Sin ejecutar el razonador, la jerarquía es
plana y aburrida: `animal` con sus subclases, `plant` con las suyas, `PlantParts`
colgando de `owl:Thing`. `herbivore`, `carnivore` y `Omnivore` aparecen con el
icono de **clase definida** (equivalencia, condiciones necesarias y suficientes),
no primitiva — son las tres únicas.

Al pulsar «start reasoner» la jerarquía cambia, y ahí está lo interesante:

| Clase | Se declaró | El razonador infiere |
|---|---|---|
| `giraffe` | `⊑ animal`, `⊑ ∀eats.(Twig ⊔ leaf)` | **`⊑ herbivore`** |
| `lion` | `⊑ animal`, `⊑ ∀eats.herbivore ⊓ ∃eats.Impala` | **`⊑ carnivore`** |
| `Impala` | `⊑ animal` | nada — **sigue siendo solo `animal`** |

Verificado con HermiT (vía owlready2). Que `Impala` **no** se clasifique como
herbívoro, pese a que los leones comen solo herbívoros y comen algún impala, es el
resultado más instructivo del ejercicio, y se explica en el
[caso de estudio](/capitulos/01-introduccion/caso-de-estudio/).

**Detalle de modelado que salta a la vista.** Las propiedades mereológicas están
mejor cuidadas que el resto: `is-part-of` es transitiva y reflexiva, `has-part` es
su inversa y también transitiva, y `is-proper-part-of` es subpropiedad de
`is-part-of` e **irreflexiva** — que es la manera correcta de distinguir parte de
parte propia. Contrasta con la nomenclatura del resto del archivo, que es un
desastre (ver ejercicio 5).

---

## Ejercicio 5

> *«Having inspected the AfricanWildlifeOntology1.owl, is it a good, less good, bad,
> or even worse ontology? Why?»*

Usando la matriz de §1.3 —precisión × cobertura—: **menos buena**. Precisión baja
con cobertura razonable. Admite modelos que no se pretendían.

La respuesta corta es que el archivo es consistente, no tiene ninguna clase
insatisfacible, clasifica correctamente jirafas y leones… y aun así contiene un
error semántico que lo vuelve inconsistente en cuanto se le añade un individuo
perfectamente razonable.

### Lo que está bien

- Es una teoría lógica de verdad, no una taxonomía: hay cuantificación,
  disyunción, clases definidas y características de propiedades.
- Las tres clases definidas (`herbivore`, `carnivore`, `Omnivore`) hacen que el
  razonador trabaje de verdad y produzca clasificación no trivial.
- La mereología (`is-part-of` transitiva y reflexiva, `is-proper-part-of`
  irreflexiva) está bien pensada.
- 36 `rdfs:comment`: está documentada.

### Lo que está mal

**1. Nomenclatura incoherente.** `lion`, `giraffe`, `herbivore`, `plant`, `animal`,
`leaf`, `branch`, `tree` en minúscula, junto a `Impala`, `Elephant`, `Warthog`,
`RockDassie`, `Grass`, `Palmtree`, `Omnivore` en CamelCase. Y `tasty-plant` con
guion. En una ontología pensada para ser compartida, esto solo es cosmético hasta
que alguien tiene que alinearla con otra.

**2. `tasty-plant` no es una clase del dominio.** Está definida como una planta
comida por algún carnívoro y por algún herbívoro. «Sabrosa» es una propiedad
epistémica y subjetiva, y la definición dada ni siquiera habla de sabor: habla de
quién se la come. Es un error semántico de manual — la formalización es válida y
dice otra cosa distinta de lo que el nombre promete.

**3. Casi no hay disyunción.** Siete axiomas para 31 clases:
`animal`/`plant`, `carnivore`/`herbivore`, `Omnivore`/`carnivore`,
`Omnivore`/`herbivore`, `Palmtree`/`tree`, `giraffe`/`lion`, y
`Twig`/`branch`/`leaf`. Nada impide que un `Warthog` sea también un `RockDassie`,
ni que un `Root` sea un `Stem`. Bajo OWA, lo que no se declara disjunto se
considera posiblemente solapado, y el razonador deja de poder detectar errores.

**4. Cero `rdfs:domain`, dos `rdfs:range`.** Aquí conviene no equivocarse de queja:
el problema *no* es que falte validación —en OWL nunca la hubo—, sino que se está
desaprovechando la inferencia de tipos que sí darían.

**5. `Palmtree ⊑ ∃has-part.¬branch`** — «toda palmera tiene alguna parte que no es
una rama». Es literalmente cierto (tiene hojas, tiene raíces) y es completamente
inútil: lo que se quería decir es que las palmeras **no tienen** ramas, o sea
`Palmtree ⊑ ¬∃has-part.branch`. Confundir «tiene alguna parte que no es X» con «no
tiene ninguna parte X» es el mismo error de alcance de cuantificador que el del
punto siguiente, y es el error semántico más frecuente en OWL.

**6. El defecto grave: las definiciones de `herbivore` y `carnivore`.**

```
herbivore ≡ ∀eats.plant  ⊔  ∀eats.(∃is-part-of.plant)
carnivore ≡ ∀eats.animal ⊔  ∀eats.(∃is-part-of.animal)
carnivore ⊓ herbivore ⊑ ⊥
```

Dos problemas encadenados, ambos por poner el `⊔` en el sitio equivocado:

- *Alcance del cuantificador.* Un animal que coma una planta entera **y** un trozo
  de planta no cumple ninguno de los dos disyuntos, y por tanto **no** se clasifica
  como herbívoro. Lo que se quería decir era
  `∀eats.(plant ⊔ ∃is-part-of.plant)` — el `⊔` dentro del alcance del `∀`, no
  fuera.
- *Satisfacción vacua.* `∀eats.plant` se cumple de forma vacía para cualquier cosa
  que no coma nada. Como es una **equivalencia** (necesaria y suficiente),
  cualquier entidad que no coma queda clasificada como herbívoro **y** como
  carnívoro a la vez — y esas dos clases están declaradas disjuntas.

La ontología, tal cual viene, es consistente: bajo OWA el razonador nunca puede
asumir que algo no come. Pero basta afirmar un individuo que no come nada para que
todo se venga abajo. Está comprobado, y es el
[caso de estudio](/capitulos/01-introduccion/caso-de-estudio/).

### Veredicto

**Menos buena** — y casi con seguridad a propósito. `AfricanWildlifeOntology1.owl`
es la versión número 1 de una serie que el libro va corrigiendo capítulo a
capítulo. Su función pedagógica es ser la foto del «antes». Responder «es buena
porque el razonador no se queja» sería precisamente caer en la trampa: el capítulo
1 acaba de explicar que los errores semánticos no los detecta ninguna herramienta.
