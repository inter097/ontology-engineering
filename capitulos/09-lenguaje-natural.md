---
titulo: 'Ontologías y lenguas naturales: el nombre no es el concepto'
capitulo: 9
descripcion: 'Ontologías multilingües, lemon y verbalización. El ejemplo del propio libro —fleuve, rivière y river— alineado de las dos maneras: una es consistente y la otra revienta la ontología.'
keet: 'cap. 9 (Ontologies and natural languages), §9.1–9.3'
hallazgo: 'Traducir bien no basta: alinear fleuve y rivière con river como equivalentes vuelve la ontología inconsistente, porque las dos lenguas no cortan el mundo por el mismo sitio.'
cifras:
  - valor: '2'
    etiqueta: 'formalizaciones de una misma frase'
  - valor: '0'
    etiqueta: 'inferencias que cambian al traducir los IRI'
  - valor: '9'
    etiqueta: 'comprobaciones'
---

Este capítulo trata de la distancia entre **el concepto** y **la palabra**. Es un
tema que parece de presentación —etiquetas, idiomas, cómo se lee una ontología— y no
lo es: los problemas que trae son de modelado, y algunos rompen ontologías.

## Nombrar clases cuando hay más de una lengua (§9.1)

La costumbre es poner los IRI en inglés y las traducciones en `rdfs:label`. Los
problemas empiezan enseguida (Review question 9.1):

- **El IRI parece legible y no lo es.** `#Lion` sugiere significado a un humano y no
  significa nada para el razonador. Toda la semántica está en los axiomas.
- **No hay una traducción neutra.** Elegir inglés no es neutral: importa la
  conceptualización de esa lengua junto con las palabras.
- **`rdfs:label` no basta.** Una clase puede necesitar varias formas —singular,
  plural, género, declinaciones— y una anotación plana no las estructura.
- **No siempre hay palabra.** Un concepto que en una lengua es una palabra en otra es
  una frase, o no existe.

La solución teórica que propone el capítulo es **lemon** (hoy OntoLex-lemon):
separar en tres capas —la ontología, el léxico y el enlace entre ambos— de modo que
cada entrada léxica tenga su forma escrita, su categoría gramatical y sus variantes,
y **apunte** al concepto en vez de ser el concepto. En monolingüe sirve para tener
varias formas de nombrar lo mismo; en multilingüe, para que cada lengua tenga su
léxico completo sobre una única ontología compartida.

**Localizar a lenguas no inglesas** (Review question 9.3) trae dificultades que el
inglés esconde: lenguas aglutinantes donde una palabra equivale a una frase, sistemas
de clases nominales como el de isiZulu que condicionan la concordancia, pluralización
no regular, y conceptos que sencillamente no tienen término.

## Verbalización (§9.2)

Es el camino inverso: convertir axiomas en frases legibles. Sirve (Review question
9.4) para que un experto del dominio **valide** lo que se ha escrito sin saber lógica,
para documentar, para interfaces de usuario y para escribir ontologías desde un
lenguaje natural controlado.

El enfoque más común es **por plantillas**: a cada patrón de axioma le corresponde una
frase con huecos.

| Axioma | Plantilla |
|---|---|
| `C ⊑ D` | *Cada `C` es un `D`.* |
| `C ⊓ D ⊑ ⊥` | *Nada puede ser a la vez un `C` y un `D`.* |
| `∃R.C ⊑ D` | *Todo lo que `R` algún `C` es un `D`.* |
| `C ⊑ ∀R.D` | *Si un `C` `R` algo, ese algo es un `D`.* |

Barato y controlable, pero rígido: las plantillas dependen de la lengua, y en lenguas
con concordancia rica hay que generar morfología, no solo rellenar huecos.

---

# Caso de estudio: traducir bien y aun así romperlo

Reproducible con:

```bash
cd capitulos/09-lenguaje-natural/artefactos
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
./.venv/bin/python verificar.py     # necesita Java en el PATH
```

## A. `fleuve`, `rivière` y `river`

El ejemplo es del propio libro (§9.1): el francés tiene **dos** palabras donde el
inglés tiene una. Un *fleuve* desemboca en el mar; una *rivière*, no.

```
Fleuve  ≡ River ⊓ ∃desembocaEn.Mar
Riviere ≡ River ⊓ ¬∃desembocaEn.Mar
```

```
[ok] con Fleuve ⊑ River y Riviere ⊑ River: CONSISTENTE
[ok] con la alineación ingenua (ambas ≡ River): INCONSISTENTE
```

<p class="evidencia">alinear las dos traducciones como equivalencias: ontología inconsistente</p>

Un diccionario dice, correctamente, que *fleuve* se traduce por *river* y que
*rivière* también. Volcar eso a la ontología como dos equivalencias hace que `Fleuve`
y `Riviere` acaben siendo la misma clase — y se distinguen justo por lo contrario.

**No es un error de traducción: es que las dos lenguas no cortan el mundo por el mismo
sitio.** La relación correcta entre los tres términos no es de equivalencia sino de
subsunción, y el resultado es que la ontología en francés es **más fina** que la
inglesa. Ninguna de las dos está mal.

<details class="peras">
<summary>¿Y esto qué quiere decir? Sin jerga</summary>

Un diccionario no promete lo que la gente cree que promete.

Cuando dice que *rivière* se traduce por *river*, quiere decir: «si te encuentras esta
palabra, esta otra es la que más se le parece». No dice «estas dos palabras significan
exactamente lo mismo», porque casi nunca es verdad.

En francés hay dos palabras distintas para dos cosas distintas: el río que acaba en el
mar y el que acaba en otro río. En inglés hay una sola palabra para las dos. No es que
el inglés esté mal ni que le falte vocabulario: es que **esa distinción no le hace
falta** para hablar.

El problema aparece al escribirlo en una ontología, donde «se traduce por» hay que
convertirlo en una afirmación exacta. Si se escribe *«fleuve es lo mismo que river»* y
*«rivière es lo mismo que river»*, la máquina hace lo evidente: concluye que *fleuve* y
*rivière* son lo mismo. Y como una desemboca en el mar y la otra no, todo se cae.

Lo correcto es más humilde: *fleuve* y *rivière* son **dos tipos** de *river*. Nadie se
equivocó traduciendo; simplemente traducir palabras no es alinear conceptos.

</details>

## B. Los nombres no razonan

```
[ok] «Lion ⊑ ∀eats.Animal» con un león que come una planta: INCONSISTENTE
[ok] la misma teoría con los nombres en español: INCONSISTENTE igual
[ok] dos clases disjuntas con la MISMA etiqueta «banco»: consistente, sin queja
```

<p class="evidencia">traducir todos los identificadores no cambia ni una deducción</p>

Las dos primeras líneas confirman lo obvio y conviene tenerlo comprobado: **el
razonador no lee los identificadores**. Un IRI en español, en inglés o en isiZulu
produce exactamente las mismas inferencias, porque todo el significado está en los
axiomas.

La tercera es la que muerde. Dos clases **disjuntas** con la etiqueta «banco» —el
asiento y la entidad financiera— conviven sin que nada proteste. Es correcto: la
etiqueta es una anotación. Y tiene una consecuencia incómoda: **la homonimia no la
detecta ninguna herramienta lógica**. Si dos clases se llaman igual y significan cosas
distintas, o si dos clases distintas modelan sin querer el mismo concepto, eso solo lo
encuentra una persona leyendo — o una verbalización que se la ponga delante.

## C. Una frase, dos formalizaciones

*«Los leones comen herbívoros.»* En español es una sola frase. En lógica son dos
axiomas distintos, y ni siquiera se implican:

| | `Leon ⊑ ∀come.Herbivoro` | `Leon ⊑ ∃come.Herbivoro` |
|---|---|---|
| un león que no come nada | **admisible** | **inconsistente** |
| un león que come un carnívoro | **inconsistente** | **admisible** |

```
[ok] con ∀: león que no come nada, admisible
[ok] con ∃: el mismo león, inconsistente
[ok] con ∀: león que come un no-herbívoro, inconsistente
[ok] con ∃: ese mismo león, admisible
```

Cuatro resultados, opuestos dos a dos, para la misma frase. Los dos axiomas son
lecturas legítimas del español — y no dicen lo mismo en ningún caso.

<details class="errata">
<summary>Lo que esto significa para la validación con expertos</summary>

La escena habitual: se verbaliza la ontología, se le enseña al experto del dominio,
el experto dice «sí, eso es correcto», y se da por validada.

Pero si la frase que ha leído es *«los leones comen herbívoros»*, **el experto no ha
validado nada**: ha confirmado una frase compatible con dos axiomas que se contradicen
en los casos límite. Y los casos límite —el león que no come nada— son justo donde
fallan las ontologías, como se ve en los capítulos
[3](/capitulos/03-logicas-descriptivas/), [5](/capitulos/05-metodologias/) y
[6](/capitulos/06-top-down/) de este mismo trabajo.

Por eso una plantilla de verbalización decente **no** dice «los leones comen
herbívoros». Dice:

- para `∀`: *«si un león come algo, ese algo es un herbívoro»* — y deja ver que no
  obliga a comer;
- para `∃`: *«todo león come al menos un herbívoro»* — y deja ver que no excluye lo
  demás.

Son más feas y son las correctas. Una verbalización que suena natural y pierde el
cuantificador convierte la validación en un trámite: el experto está de acuerdo con
algo que no es lo que hay escrito.

</details>

## Qué deja el caso

1. **Traducir palabras no es alinear conceptos.** El diccionario da equivalencias
   aproximadas; la ontología exige afirmaciones exactas.
2. **Los IRI no aportan semántica.** Se pueden traducir enteros sin que cambie una
   sola deducción — y por eso tampoco protegen de nada.
3. **La homonimia y la sinonimia son invisibles al razonador.** Se cazan leyendo.
4. **Una frase natural no determina un axioma.** La verbalización tiene que exponer
   el cuantificador aunque quede fea, o no sirve para validar.

---

## Los ejercicios (§9.3)

**Review question 9.1.** *«Name some of the problems with naming the classes in an OWL
file, when considering multiple languages.»* — El IRI parece legible pero no tiene
semántica; elegir inglés importa una conceptualización concreta; `rdfs:label` no
estructura las variantes morfológicas ni distingue registros; y hay conceptos sin
término en la lengua de destino. Se añade el problema de gestión: si el IRI lleva la
palabra inglesa dentro, traducir de verdad obliga a cambiar los IRI y a romper todo lo
que apuntaba a ellos.

**Review question 9.2.** *«Describe the theoretical solution that lemon exhibits.»* —
Separar el **léxico** de la **ontología** y unirlos con una capa de enlace. En
monolingüe permite varias entradas léxicas —con su forma escrita, categoría y
variantes— apuntando a un mismo concepto, y por tanto tratar sinónimos sin duplicar
clases. En multilingüe, cada lengua tiene su léxico completo sobre **una sola**
ontología: se traduce el léxico, no la teoría. *Criterio propio: esa es la respuesta
directa al problema de la parte A del caso de estudio — solo hasta donde las
conceptualizaciones coincidan; cuando el francés distingue lo que el inglés no,
ningún léxico arregla que hagan falta clases distintas.*

**Review question 9.3.** *«Name some of the challenges for localising an ontology into
a language that is not English.»* — Lenguas aglutinantes donde una palabra equivale a
una frase entera; sistemas de clases nominales con concordancia obligatoria, como en
isiZulu; pluralización irregular; ausencia de término para conceptos técnicos; y
direccionalidad o registro distintos que hacen que la plantilla de verbalización no se
traduzca palabra por palabra.

**Review question 9.4.** *«What can ontology verbalisation be used for?»* — Para que un
experto del dominio valide sin saber lógica, para documentar automáticamente, para
interfaces de usuario y para escribir ontologías desde un lenguaje natural controlado.
*Criterio propio: con la salvedad que verifica la parte C — una verbalización que no
expone el cuantificador convierte la validación en un trámite vacío.*

**Review question 9.5.** *«Describe how the template-based approach works.»* — A cada
patrón de axioma le corresponde una plantilla de frase con huecos, que se rellenan con
las etiquetas de las entidades implicadas y se ajustan morfológicamente. Es la tabla de
§9.2 de más arriba. Barato y predecible; su límite es que el número de patrones crece
con la expresividad y que la morfología no es sustitución de cadenas.

**Exercise 9.1.** *«The AWO has been translated into Spanish, Afrikaans, isiZulu and
Dutch… What are the IRI issues?»* — Requiere inspeccionar los cuatro archivos
traducidos, que no están en este repositorio, así que **no se afirma aquí nada sobre
su contenido**. *Criterio propio sobre la pregunta (b), que sí es general: la opción
defendible es **mantener el IRI original y traducir solo las etiquetas**. Un IRI es un
identificador, no un nombre legible; cambiarlo por la traducción crea una entidad
distinta a ojos de la máquina y rompe el enlace con la ontología original — que es
justo lo que pregunta el apartado (c). Si aun así se cambian los IRI, el enlace hay
que reconstruirlo explícitamente con `owl:equivalentClass`, y ahí reaparece el riesgo
verificado en la parte A: la equivalencia solo vale si las dos lenguas conceptualizan
igual.*

**Exercise 9.2.** *«Create a Lemon file for the ontology of your choice.»* — Pendiente
hasta que exista la ontología propia del trabajo; hacerlo sobre una ontología ajena
sería un ejercicio de sintaxis sin decisiones que defender.

**Exercise 9.3.** *«Devise templates in English for the following axiom types.»* — En
inglés, y en español al lado, evitando deliberadamente la formulación bonita:

| Axioma | Inglés | Español |
|---|---|---|
| `C ⊓ D ⊑ ⊥` | *Nothing can be both a `C` and a `D`.* | *Nada puede ser a la vez un `C` y un `D`.* |
| `∃R.C ⊑ D` | *Everything that `R` at least one `C` is a `D`.* | *Todo lo que `R` al menos un `C` es un `D`.* |
| `C ⊑ ∀R.D` | *If a `C` `R` something, then that something is a `D`.* | *Si un `C` `R` algo, entonces ese algo es un `D`.* |

*Criterio propio: la tercera es la que importa. La traducción natural —«un `C` solo `R`
`D`»— se lee como si obligara a `R` algo, y no obliga; la formulación condicional es
más torpe y es la única que transmite la vacuidad del universal. Es la conclusión
directa de la parte C del caso de estudio.*

**Exercise 9.4.** *«Devise a software architecture that would solve multilingualism
with respect to maintenance.»* — *Criterio propio:* una **única** ontología con IRI
opacos —identificadores sin palabras dentro, tipo `AWO_0000123`— y los léxicos por
lengua en archivos separados en OntoLex-lemon, enlazados por IRI. Ventajas: la teoría
se mantiene en un solo sitio, añadir una lengua no toca ni un axioma, y ninguna lengua
queda privilegiada. Inconvenientes: los archivos se vuelven ilegibles a ojo, se
depende por completo de la herramienta, y **no resuelve** los casos en que las lenguas
conceptualizan distinto — ahí siguen haciendo falta clases distintas, como en la parte
A. Es el patrón que usan las ontologías biomédicas grandes, y por esa razón.

**Exercise 9.5.** *«If there were an ‘OWL 3’, what would you propose for
internationalisation?»* — *Criterio propio: incorporar al estándar un modelo léxico
—lo que hoy es OntoLex-lemon, que vive fuera de OWL— para que las formas, categorías
gramaticales y variantes por lengua sean parte del lenguaje y no de una convención de
anotación. Y añadir una anotación estándar que declare la lengua de origen de la
conceptualización, porque hoy nada obliga a documentar que una jerarquía corta el
mundo como lo corta el inglés.*

---

## Lo que hay que llevarse

1. **El nombre no es el concepto**, y el razonador lo demuestra: se pueden traducir
   todos los identificadores sin cambiar nada.
2. **Alinear traducciones con equivalencias es peligroso.** Casi siempre lo correcto
   es subsunción.
3. **lemon separa léxico de ontología**, que es la única forma de escalar a varias
   lenguas sin duplicar la teoría.
4. **Verbalizar sin el cuantificador no es verbalizar**: es hacer que el experto
   valide una frase que admite dos axiomas incompatibles.

<small>Salvo los enunciados citados, el análisis y las resoluciones de esta página
son criterio propio, verificados con HermiT. Numeración y enunciados tomados del PDF
en <a href="https://github.com/inter097/ontology-engineering/tree/main/libro">/libro</a>,
no de ediciones web que renumeran las secciones.</small>

<details class="defensa">
<summary>Para la defensa — lo que te van a preguntar de aquí</summary>

**«¿En qué idioma está tu ontología y por qué?»**

La pregunta correcta es doble: los **IRI** y las **etiquetas** son cosas distintas. Los
IRI son identificadores y no aportan semántica —está verificado: traducir todos los
identificadores no cambia ni una inferencia—, así que lo defendible es mantenerlos
estables y no traducirlos nunca. Las etiquetas sí se traducen, con `rdfs:label` y su
marca de idioma, o mejor con un léxico OntoLex-lemon aparte.

**«¿Basta con traducir las etiquetas para tener una ontología multilingüe?»**

No, y es el hallazgo de este capítulo. Basta mientras las lenguas conceptualicen
igual. El ejemplo del propio libro: el francés distingue *fleuve* de *rivière* según
desemboque o no en el mar, y el inglés tiene solo *river*. Alinear las dos traducciones
como equivalentes —que es lo que dice el diccionario— **vuelve la ontología
inconsistente**, y está verificado con HermiT. La alineación correcta es de subsunción,
y deja la ontología francesa más fina que la inglesa.

**«¿Cómo detectas que dos clases significan lo mismo, o que una palabra está usada con
dos sentidos?»**

No con el razonador. Está comprobado que dos clases **disjuntas** con la misma
etiqueta «banco» conviven sin que nada proteste: las etiquetas son anotaciones. La
homonimia y la sinonimia se detectan leyendo, con revisión humana, verbalización o
alineamiento asistido — nunca con una comprobación de consistencia.

**«¿Cómo validas la ontología con expertos que no saben lógica?»**

Con verbalización por plantillas, y con una regla explícita: **la plantilla tiene que
exponer el cuantificador**, aunque la frase quede torpe.

*Por qué es una respuesta fuerte:* está medido. La frase *«los leones comen
herbívoros»* admite dos formalizaciones, `∀` y `∃`, y en el caso de estudio dan
resultados **opuestos** en los dos casos límite: el león que no come nada y el león que
come un carnívoro. Un experto que aprueba esa frase no ha validado ningún axioma. Por
eso las plantillas de este trabajo dicen *«si un león come algo, ese algo es un
herbívoro»*.

**«¿No es todo esto un problema de presentación?»**

No. La parte A produce una **inconsistencia lógica** a partir de una traducción
correcta, y la parte C produce dos teorías incompatibles a partir de una sola frase
española. Lo que empieza como una cuestión de etiquetas acaba decidiendo qué deduce el
razonador.

</details>
