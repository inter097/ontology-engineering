---
titulo: 'Modularización: partir una ontología sin romper lo que deducía'
capitulo: 11
descripcion: 'Las cinco dimensiones de un módulo y el marco que las relaciona. Tres formas de extraer el mismo módulo, medidas: la ingenua conserva todos los nombres pedidos y pierde una consecuencia.'
keet: 'cap. 11 (Ontology modularisation), §11.1–11.4, 1ª ed. v1.5'
hallazgo: 'Un módulo que contiene los tres nombres pedidos y ningún axioma inventado deja de deducir que un león no puede ser un impala. Correcto y a la vez incompleto.'
cifras:
  - valor: '5'
    etiqueta: 'dimensiones de un módulo'
  - valor: '3'
    etiqueta: 'clases frente a 7 en el módulo bueno'
  - valor: '12'
    etiqueta: 'comprobaciones'
---

Una ontología grande —SNOMED CT, la FMA, DOLCE— no se usa entera casi nunca. Este
capítulo trata de cómo partirla, y sobre todo de **qué significa que la parte esté
bien**.

> **Nota de edición.** Corresponde al capítulo 11 de la **1ª edición, v1.5 (2020)**.
> En la 2ª edición la numeración difiere a partir del 10.

## Cinco dimensiones (§11.2)

Un módulo se describe por cinco cosas, y el error habitual es hablar solo de la
tercera:

| Dimensión | Pregunta que contesta |
|---|---|
| **Caso de uso** | ¿para qué se parte? mantenimiento, rendimiento, reutilización, privacidad, comprensión |
| **Tipo** | ¿qué clase de módulo es? cobertura de dominio, subdominio, rama aislada, patrón de diseño, sublenguaje, abstracción, privacidad |
| **Técnica** | ¿cómo se obtiene? partición del grafo, **por localidad**, a priori, manual, abstracción |
| **Propiedades** | ¿qué garantiza? preservación de consecuencias, autocontención, disyunción con otros módulos |
| **Criterios de evaluación** | ¿es un buen módulo? métricas estructurales, lógicas y relacionales |

Las dos métricas **lógicas** son las que deciden (§11.2):

- **Corrección** — todo axioma del módulo está en la ontología original. No se
  inventa nada.
- **Completitud** — el significado de cada entidad del módulo se preserva: lo que la
  ontología original deducía sobre ella, el módulo lo sigue deduciendo.

Y son **independientes**. El caso de estudio de esta página es un módulo perfectamente
correcto e incompleto — que es justo el par de valores que nadie comprueba, porque
«no he añadido nada» suena a garantía y no lo es.

<details class="peras">
<summary>¿Y esto qué quiere decir? Sin jerga</summary>

Alguien pide una copia de tres fichas de un archivo: la de «impala», la de «león» y la
de «animal».

La forma rápida: buscar esas tres palabras, fotocopiar las fichas donde aparecen, y
entregar el montón. Nadie ha inventado nada — todo lo entregado estaba en el archivo.
Eso es **corrección**.

Pero en el archivo original, la ficha del león remitía a «carnívoro», y la de
carnívoro decía «un carnívoro nunca es un herbívoro», y la del impala remitía a
«herbívoro». Encadenando esas fichas se sabía que **un león no puede ser un impala**.
Ninguna de esas fichas intermedias menciona las tres palabras pedidas, así que no
entraron en la fotocopia.

Quien recibe el montón lo tiene todo lo que pidió y ya no puede llegar a esa
conclusión. Eso es lo que falla: la **completitud**.

Lo incómodo del caso es que el error no se ve mirando el resultado. No falta ninguna
ficha de las pedidas y no sobra ninguna. Solo se detecta preguntando algo y viendo que
ahora la respuesta es distinta.

</details>

**Técnicas** (Review question 11.2): **partición del grafo** —cortar por donde la
estructura está poco conectada—, **modularización por localidad** —cerrar la
signatura hasta que ningún axioma quede colgando, que es la que da garantías
lógicas— y los enfoques **a priori o manuales**, donde el módulo se decide antes de
mirar los axiomas.

## El marco (§11.3)

Lo que aporta el capítulo no es una técnica más, sino **las dependencias entre
dimensiones**: el caso de uso determina qué tipos de módulo tienen sentido, el tipo
determina qué técnicas sirven, y de ahí salen las propiedades exigibles y los
criterios con los que se evalúa. Se recorre en ese orden, y el orden importa: elegir
la técnica primero —«vamos a partirlo por ramas»— es como elegir la respuesta antes de
la pregunta.

---

<h2 class="caso">Caso de estudio: el mismo módulo, tres veces</h2>

Reproducible con:

```bash
cd capitulos/11-modularizacion/artefactos
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
./.venv/bin/python verificar.py     # necesita Java en el PATH
```

La ontología de partida:

```
Impala ⊑ Antelope ⊑ Bovidae ⊑ Herbivore ⊑ Animal
Herbivore ⊓ Carnivore ⊑ ⊥
Lion ⊑ Carnivore ⊓ ∃eats.Impala
Animal ⊓ Plant ⊑ ⊥ ,  Herbivore ⊑ ∃eats.Plant ,  Grass ⊑ Plant
```

Se pide un módulo para la **signatura** `{Impala, Animal, Lion}` —lo que necesita una
aplicación que solo habla de esos tres términos— de tres maneras: el **corte
ingenuo** (solo los axiomas que mencionan esos nombres), el **módulo por localidad**
(cerrando la signatura hacia arriba hasta que nada quede colgando) y la **ontología
entera** como referencia.

## Lo que los tres conservan

```
[ok] [completa]  ⊨ Impala ⊑ Animal   ⊨ Lion ⊑ ∃eats.Impala
[ok] [localidad] ⊨ Impala ⊑ Animal   ⊨ Lion ⊑ ∃eats.Impala
[ok] [ingenuo]   ⊨ Impala ⊑ Animal   ⊨ Lion ⊑ ∃eats.Impala
```

Hasta aquí, los tres módulos parecen intercambiables. Es exactamente la comprobación
que se hace en la práctica —«están las clases que pedí y las relaciones evidentes
funcionan»— y es la que no sirve para nada.

## Lo que el corte ingenuo pierde

```
[ok] [completa]  ⊨ Lion ⊓ Impala ⊑ ⊥
[ok] [localidad] ⊨ Lion ⊓ Impala ⊑ ⊥
[ok] [ingenuo]   NO lo deduce
```

<p class="evidencia hipotesis">módulo ingenuo: T ⊭ Lion ⊓ Impala ⊑ ⊥</p>

En el módulo ingenuo, **un león puede ser un impala**. La consecuencia se apoyaba en
una cadena de clases —`Carnivore`, `Herbivore`, `Bovidae`, `Antelope`— y en la
disyunción entre las dos primeras; ninguna de ellas menciona los nombres de la
signatura, así que el corte las tiró. Los tres términos pedidos están todos. La
consecuencia, no.

Ese módulo es **correcto** —cada axioma que contiene estaba en el original— e
**incompleto**. Es el mismo fallo del `Example 11.4` del libro, donde un módulo de
rama de DOLCE se queda sin uno de los axiomas de `endurant` y por tanto suspende la
métrica de completitud.

<details class="errata">
<summary>Por qué el corte ingenuo es tan tentador</summary>

Porque es lo que hace cualquiera con un editor de texto y quince minutos, y porque su
resultado **supera todas las comprobaciones informales**: están las clases pedidas,
no sobra nada, la ontología carga, el razonador no protesta y las consultas obvias
funcionan.

Y porque el fallo es silencioso en la peor dirección posible. Un módulo incompleto no
deduce de menos en abstracto: **deja de detectar contradicciones**. La aplicación que
use ese módulo aceptará datos que la ontología completa habría rechazado — un
individuo que sea león e impala a la vez entra sin protesta. No falla al razonar:
falla al no fallar.

Se detecta solo de una forma, y hay que decidirlo antes de partir nada: **fijar el
conjunto de consecuencias que el módulo debe preservar y comprobarlas después** — es
decir, las preguntas de competencia del [capítulo 5](/capitulos/05-metodologias/)
aplicadas al módulo en vez de a la ontología. Si no hay esa lista, no hay forma de
saber si el módulo está bien.

</details>

## Qué cuesta conservarla

```
[ok] módulo por localidad: 7 clases   frente a  9 de la ontología completa
[ok] corte ingenuo: 3 clases          — y eso es exactamente lo que le pasa
[ok] la rama de plantas, que la signatura no toca, no hace falta
```

<p class="evidencia">7 de 9 clases conservan las tres consecuencias; 3 de 9, no</p>

El módulo por localidad **sí** es más pequeño que la ontología completa: la rama
entera de plantas desaparece sin que se pierda ninguna de las tres consecuencias,
porque nada de lo que se pregunta la atraviesa. Modularizar funciona; lo que no
funciona es cortar por los nombres.

Y de paso queda la medida honesta del ahorro: de 9 clases a 7, no a 3. **La reducción
real es siempre menor de lo que promete la intuición**, porque las cadenas de
subsunción y las disyunciones arrastran clases que nadie pidió.

## Qué deja el caso

1. **Correcto no implica completo.** Son dos métricas independientes y solo se mira
   la primera.
2. **La signatura no basta para decidir qué entra.** Los axiomas que importan pueden
   no mencionar ni un término pedido.
3. **Un módulo incompleto falla dejando de detectar errores**, que es la forma más
   difícil de darse cuenta.
4. **Modularizar sí reduce**, pero menos de lo esperado, y solo si se cierra la
   signatura.

---

## Los ejercicios (§11.4)

**Review question 11.1.** *«What are some of the dimensions specified for modules?»* —
Cinco: **casos de uso**, **tipos**, **técnicas**, **propiedades** y **criterios de
evaluación**. La tabla de §11.2 de más arriba.

**Review question 11.2.** *«Name three techniques for modularising a large
ontology.»* — **Partición del grafo** (cortar por zonas poco conectadas), **por
localidad** (cerrar la signatura hasta que ningún axioma quede colgando, con garantía
de preservación de consecuencias) y **a priori / manual** (el módulo se decide por
criterio humano antes de mirar los axiomas). Se añade la **abstracción**, que reduce
el nivel de detalle en vez de recortar el alcance.

**Review question 11.3.** *«Name five criteria that concern the structure of the
ontology and three that have to do with how one module relates to the others.»* —
Estructurales: **tamaño** del módulo (número de entidades), **tamaño relativo** frente
a la ontología de origen, **cohesión** interna (cuán conectadas están sus entidades
entre sí), **riqueza de atributos y relaciones**, y **profundidad o granularidad** de
la jerarquía que conserva. Relacionales: **solapamiento** entre módulos,
**acoplamiento** —cuántas referencias salen fuera del módulo— y **cobertura** conjunta
respecto a la ontología original. *Criterio propio en el reparto exacto de nombres; lo
que no es criterio propio son las dos métricas **lógicas** del capítulo, corrección y
completitud, que son las que se miden en el caso de estudio y las únicas con una
definición formal.*

**Review question 11.4.** *«Describe the framework and how you would use it to
modularise SNOMED CT, the FMA or DOLCE.»* — El marco encadena las cinco dimensiones:
del **caso de uso** salen los **tipos** admisibles, del tipo las **técnicas** posibles,
y de ahí las **propiedades** exigibles y los **criterios** con que se evalúa.
Aplicado: para **SNOMED CT** el caso de uso típico es rendimiento y alcance —una
especialidad clínica—, luego módulo de subdominio por **localidad**, porque hace falta
que las consecuencias clínicas se preserven. Para la **FMA**, reutilización parcial de
anatomía: módulo de cobertura de dominio, otra vez por localidad, con cuidado especial
en las relaciones parte-todo del [capítulo 6](/capitulos/06-top-down/), que arrastran
media ontología. Para **DOLCE**, comprensión y enseñanza: módulo de **rama aislada**,
técnica manual o a priori — y ahí el propio libro avisa (Example 11.4) de que sale
**incompleto**, lo cual es aceptable si el uso es didáctico y catastrófico si es
razonar.

**Exercise 11.1.** *«We have imported DOLCE and BFO into the AWO. What sort of
modularisation do we have there?»* — No es modularización sino **importación**: la AWO
alineada con una fundacional no parte nada, sino que compone. En el vocabulario del
capítulo, el resultado es una ontología con módulos por **cobertura de dominio**
—dominio arriba, fundacional abajo—, obtenidos **a priori** (existían antes de la
composición) y con la relación entre ellos gestionada por `owl:imports`. *Criterio
propio: y con una propiedad que conviene nombrar, porque es lo que hace útil la
importación — el módulo importado es **autocontenido**: se entiende sin la AWO,
mientras que la AWO ya no se entiende sin él.*

**Exercise 11.2.** *«Study the evaluation metrics to determine whether the set of QUDT
modules are a good set of modules.»* — Requiere descargar los módulos QUDT y calcular
sobre ellos la tabla de métricas del libro; no está en este repositorio, así que **no
se afirma aquí ningún resultado sobre QUDT**. *Criterio propio sobre el método, que sí
es transferible: en un conjunto de módulos como QUDT —cantidades, unidades,
dimensiones— lo primero que hay que mirar no es el tamaño sino el **acoplamiento**,
porque unidades y dimensiones se referencian mutuamente sin parar, y un conjunto de
módulos con acoplamiento alto ofrece las desventajas de estar partido sin las
ventajas.*

**Exercise 11.3.** *«The developer wishes to extract only the specific Book-toy entity
and the generalised Toy-property entity. Determine the use-case, the type of module,
the technique…»* — *Criterio propio, recorriendo el marco en su orden:* el **caso de
uso** es reutilización parcial en una aplicación; el **tipo**, módulo de cobertura de
dominio sobre una signatura dada (no una rama, porque se piden dos entidades de
niveles distintos); la **técnica**, **por localidad**, que es la única con garantía de
preservar consecuencias; y las **propiedades** exigibles, corrección y completitud
sobre esa signatura. La comprobación que este caso de estudio añade al ejercicio es
que la alternativa evidente —extraer solo los axiomas que mencionan `Book-toy` y
`Toy-property`— produce un módulo correcto, incompleto y aparentemente sano.

---

## Lo que hay que llevarse

1. **Modularizar empieza por el caso de uso**, no por la técnica.
2. **Corrección y completitud son independientes**, y la que se comprueba es la que
   no importa.
3. **Por localidad, no por nombres.** Cerrar la signatura es lo que da la garantía.
4. **Un módulo se valida con consecuencias esperadas**, igual que una ontología se
   valida con preguntas de competencia.

<small>Salvo los enunciados citados, el análisis y las resoluciones de esta página
son criterio propio, verificados con HermiT. Numeración y enunciados tomados del PDF
en <a href="https://github.com/inter097/ontology-engineering/tree/main/libro">/libro</a>
(1ª edición, v1.5), no de ediciones web que renumeran las secciones.</small>

<details class="defensa">
<summary>Para la defensa — lo que te van a preguntar de aquí</summary>

**«¿Por qué modularizar? ¿No basta con importar la ontología entera?»**

Depende del caso de uso, que es la primera dimensión del marco. Se modulariza por
rendimiento del razonamiento, por mantenimiento, por reutilizar solo una parte, por
privacidad o por comprensión. Si ninguno de esos motivos aplica, importar entera es la
respuesta correcta y modularizar es trabajo perdido con riesgo añadido.

**«¿Cómo sabes que tu módulo es correcto?»**

«Correcto» y «completo» son dos cosas distintas, y esa distinción es el capítulo
entero. **Corrección**: todo axioma del módulo estaba en el original — fácil de
comprobar y casi siempre cierta. **Completitud**: lo que la ontología deducía sobre
las entidades del módulo, el módulo lo sigue deduciendo — que es lo que de verdad
importa y casi nadie mide.

*Por qué es una respuesta fuerte:* está medido en el caso de estudio. El módulo
extraído por nombres contiene las tres clases pedidas, ningún axioma inventado, carga
sin errores y responde bien a las consultas evidentes — y **deja de deducir que un
león no puede ser un impala**. Es correcto e incompleto a la vez.

**«¿Qué técnica de modularización usas?»**

**Por localidad**: se cierra la signatura hacia arriba hasta que ningún axioma queda
colgando. Es la única de las técnicas del capítulo con garantía de preservación de
consecuencias; la partición del grafo optimiza estructura y la manual depende del ojo
de quien corta.

*El matiz que conviene añadir:* el ahorro real es menor de lo que se espera. En el
caso de estudio se pasa de 9 clases a 7, no a 3, porque las cadenas de subsunción y
las disyunciones arrastran clases que nadie pidió. Un módulo que reduce muchísimo casi
siempre está incompleto.

**«¿Qué riesgo concreto corre una aplicación que use un módulo mal extraído?»**

Aceptar datos que la ontología completa habría rechazado. Un módulo incompleto no da
respuestas equivocadas: **deja de detectar contradicciones**. En el caso de estudio,
un individuo que fuera león e impala a la vez pasa sin protesta. El sistema no falla;
simplemente deja de avisar, que es peor.

**«¿Cómo validas un módulo?»**

Con una lista de consecuencias que debe preservar, fijada **antes** de partir, y
comprobada después con el razonador. Son las preguntas de competencia del capítulo 5
aplicadas al módulo. Sin esa lista no hay criterio: los tres módulos del caso de
estudio superan cualquier inspección informal y solo uno de ellos sirve.

</details>
