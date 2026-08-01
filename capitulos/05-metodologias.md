---
titulo: 'Methods and Methodologies: las preguntas de competencia son las pruebas'
capitulo: 5
descripcion: 'Metodologías de macro y micro nivel, y los cuatro tipos de método para mejorar una ontología. Las once preguntas de competencia del libro ejecutadas contra la ontología de ejemplo — contesta cuatro.'
keet: 'cap. 5 (Methods and Methodologies), §5.1–5.3'
hallazgo: 'De las once preguntas de competencia que el propio libro propone, la ontología de ejemplo contesta cuatro; tres devuelven vacío —que no es un «no»— y una parece contestada solo porque la ontología está rota.'
cifras:
  - valor: '4/11'
    etiqueta: 'CQ que la AWO contesta'
  - valor: '4'
    etiqueta: 'familias de método'
  - valor: '17'
    etiqueta: 'comprobaciones'
---

Este es el capítulo por el que el libro manda empezar un proyecto real, y el que
contiene la única cosa de todo el libro que funciona como una prueba de software:
las **preguntas de competencia**.

## Macro y micro (§5.1)

Dos niveles distintos, y confundirlos es lo que hace que una metodología parezca
inútil.

- **Macro-nivel**: el proceso completo, de la idea al despliegue. **Methontology**
  es el ejemplo canónico —cinco pasos con sabor a cascada: especificación,
  conceptualización, formalización, implementación, mantenimiento— y **NeOn** el
  representante moderno, con escenarios de reutilización en vez de un único camino.
- **Micro-nivel**: cómo se pasa de una descripción informal a axiomas. Ahí viven
  **OntoSpec**, **OD101** y **DiDOn**: elegir lenguaje, elegir ontología fundacional,
  decidir si un atributo es propiedad o clase, y qué servicios de razonamiento hacen
  falta.

Keet no compara metodologías y da una recomendación seca que vale más que la
comparación: *«it is better to pick one of them to structure your activities than
using none at all»* (cap. 5, §5.1.1). No usar ninguna es reinventar la rueda y
tropezar con los mismos errores.

**Enfoques ágiles.** El libro los da por «en flujo» en el momento de escribirse, y
menciona OntoMaven con casos de prueba, *eXtreme Design* dentro de NeOn y un
bosquejo de desarrollo dirigido por pruebas. *Criterio propio: es exactamente lo que
hace este repositorio — cada capítulo tiene su `verificar.py`, y una afirmación que
no se puede ejecutar no se escribe.*

### Las preguntas de competencia

En la fase de requisitos, la pregunta que la metodología obliga a contestar es:
**¿qué preguntas debería poder responder la ontología?** No es documentación. Es la
especificación ejecutable del alcance:

> Una CQ es una consulta más una respuesta esperada. Si la consulta deja de devolver
> la respuesta esperada, la ontología ha dejado de cumplir su requisito. Es una
> prueba unitaria con otro nombre.

<details class="peras">
<summary>¿Y esto qué quiere decir? Sin jerga</summary>

Antes de construir un armario, alguien pregunta: *«¿va a caber la aspiradora?»*.

Esa pregunta no es documentación del armario. Es lo que decide si el armario está
bien o mal hecho. Cuando esté montado, se prueba: se mete la aspiradora. Si entra,
el armario cumple; si no entra, no cumple — por bonito que haya quedado.

Una ontología funciona igual. Antes de escribir nada se apuntan las preguntas que
tendrá que saber contestar. Después se comprueba una por una si las contesta. Y hay
tres resultados posibles, no dos:

- **la contesta** — bien;
- **no la contesta porque le falta vocabulario** — no sabe ni de qué le hablas;
- **contesta «nada»** — y esto es lo traicionero, porque «nada» se parece muchísimo
  a «no», y casi siempre significa «no me lo has contado».

El tercer caso es el que hunde proyectos: alguien pregunta *«¿quién se come a los
rockdassies?»*, la ontología devuelve una lista vacía, y el equipo apunta en el
informe que los rockdassies no tienen depredadores.

</details>

## Cuatro familias de método (§5.2)

Keet los agrupa en cuatro, y de cada uno da un ejemplo:

| Familia | Ejemplo | Qué detecta |
|---|---|---|
| **Solo lógica** | explicación y justificación de deducciones | por qué una clase se volvió insatisfacible: el conjunto mínimo de axiomas culpable |
| **Solo filosofía** | **OntoClean** | jerarquías «sucias»: una subclase que no puede serlo por rigidez, identidad o unidad |
| **Lógica + filosofía** | **RBox Compatibility** | jerarquías de propiedades incoherentes: una subpropiedad cuyo dominio no encaja con el de su padre |
| **Heurísticas** | **OOPS!** con TIPS | *pitfalls* frecuentes: sin dominio, sin disyunciones, ciclos, nombres inconsistentes |

**OntoClean** en una línea: se anotan las clases con metapropiedades filosóficas
—**rigidez** (¿se deja de ser eso alguna vez?), **identidad** (¿cómo se reconoce que
son la misma cosa?), **unidad** (¿se reconocen todas sus partes?)— y de ahí salen
reglas duras. La más útil: **una clase rígida no puede ser subclase de una
antirrígida**. `Persona` (rígida) bajo `Estudiante` (antirrígida) es un error, aunque
el razonador nunca proteste.

Y el punto que Keet subraya: OOPS! mira **el lado negativo** —qué errores hay—
mientras OntoClean y RBox Compatibility miran si el modelado es **ontológicamente**
correcto. No se sustituyen entre sí.

---

<h2 class="caso">Caso de estudio: las once preguntas del libro contra la ontología del libro</h2>

Reproducible con:

```bash
cd capitulos/05-metodologias/artefactos
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
./.venv/bin/python verificar.py     # necesita Java en el PATH
```

Dos ejercicios del propio capítulo, ejecutados en vez de razonados.

## A. Exercise 5.1 — evaluar la AWO contra once CQ

El enunciado da once preguntas de competencia y pregunta: *«If these were the
requirements for the content, is it a ‘good’ ontology?»*

**Las que sí contesta:**

```
[ok] CQ6  ¿qué plantas comen animales?      → CarnivorousPlant ≡ plant ⊓ ∃eats.animal
[ok] CQ7  ¿qué animales comen impalas?      → lion ⊑ ∃eats.Impala
[ok] CQ1  ¿qué animal come a qué animal?    → sí, pero solo en la TBox: 0 individuos
[ok] CQ4  ¿come el león plantas?            → NO, y es deducción: lion ⊓ ∃eats.plant insatisfacible
```

<p class="evidencia">AWO ⊨ lion ⊓ ∃eats.plant ⊑ ⊥</p>

Solo la CQ4 se contesta con una **deducción**. Las otras tres se contestan leyendo
axiomas: útil, pero es lo que haría un `grep`.

**Las que devuelven vacío — y vacío no es «no»:**

```
[ok] CQ2  ¿es herbívoro un rockdassie?      → no se deduce: T ∪ {¬α} consistente
[ok] CQ8  ¿quién depreda al rockdassie?     → vacío; añadir un depredador NO da inconsistencia
```

Estas dos son el corazón del capítulo. La ontología no dice que el rockdassie no sea
herbívoro: **no dice nada**. Y la prueba de que es ignorancia y no negación es que se
puede añadir lo contrario sin romper nada. Un informe que apunte «la ontología
confirma que el rockdassie no tiene depredadores» está inventando.

**La que parece contestada y no lo está:**

```
[ok] CQ3  la AWO deduce que toda jirafa come algo: T ∪ {¬∃eats.⊤} INCONSISTENTE
[ok] …pero le pasa igual a un `animal` cualquiera
```

<p class="evidencia hipotesis">falso positivo: la deducción viene de una grieta, no de un axioma sobre jirafas</p>

Aquí la CQ3 aparenta funcionar. No funciona: la inconsistencia no viene de ningún
axioma sobre jirafas, sino de que `herbivore` y `carnivore` están **definidas solo
con `∀`** y son disjuntas. Quien no come nada satisface las dos por vacuidad y
revienta la ontología. Es exactamente el fallo documentado en el
[capítulo 1](/capitulos/01-introduccion/), visto ahora desde el lado del requisito:
**una ontología rota puede pasar una CQ por la razón equivocada.**

**Las que no se pueden contestar — falta el vocabulario:**

```
[ok] CQ5     ¿hay un animal que no beba agua?          → no existe «beber» ni «agua»
[ok] CQ9/10  ¿monos en Sudáfrica? ¿a qué país ir?      → no existe ni Monkey ni país
[ok] CQ11    ¿comparten hábitat jirafa y cebra?        → existen Habitat y Distribution…
             …pero ninguna propiedad las conecta con nada
```

La CQ11 es la más instructiva de las tres: **las clases están, y aun así la pregunta
es incontestable**. Tener el sustantivo no sirve de nada si no está la relación. Es
el síntoma clásico de una ontología construida enumerando conceptos en vez de
partiendo de las preguntas.

**Balance: 4 de 11.** Y la respuesta al *«is it a ‘good’ ontology?»* del enunciado es
**no** —para estos requisitos—, con un matiz que importa: no es mala por estar mal
razonada, sino por estar construida **sin las preguntas delante**.

## B. Exercise 5.3 — el dominio no valida, infiere

La ontología del enunciado, tal cual:

```
R ⊑ PD × PD     PD ⊑ PT      A ⊑ ED      A ⊑ ∃R.B
S ⊑ PT × PT     ED ⊑ PT      B ⊑ ED      D ⊑ ∃S.C
S ⊑ R           ED ⊑ ¬PD     C ⊑ PD      D ⊑ PD
Trans(R)
```

Pregunta (a): *«Is A consistent? Verify this with the reasoner and explain why.»*

```
[ok] A es INSATISFACIBLE
[ok] y nadie escribió A ⊑ ⊥ ni ninguna contradicción
[ok] quitando SOLO el domain/range de R, A vuelve a ser satisfacible
[ok] B es satisfacible en las dos versiones
```

<p class="evidencia">AWO-53 ⊨ A ⊑ ⊥, y desaparece al quitar domain(R)</p>

La cadena es corta y devastadora: `A ⊑ ∃R.B` mete a todo `A` en el **dominio** de
`R`; el dominio de `R` es `PD`; luego todo `A` es un `PD`. Pero `A ⊑ ED` y
`ED ⊑ ¬PD`. Contradicción. `A` no puede tener instancias.

<details class="errata">
<summary>La trampa que este ejercicio existe para enseñar</summary>

La intuición de quien viene de bases de datos es: *«declaro `domain(R) = PD` para
que el sistema me avise si alguien usa `R` con algo que no sea `PD`»*.

En OWL eso **no pasa nunca**. `domain` no rechaza: **clasifica**. Ante un uso que no
encaja, el razonador no da un error — deduce que el sujeto también es un `PD`, y
sigue tan tranquilo. Solo si esa deducción choca contra una disyunción declarada
aparece un problema, y entonces lo que aparece no es *«has usado mal la
propiedad»*, sino *«la clase `A` es insatisfacible»*, señalando a un sitio que no
tiene la culpa.

Peor aún: quitar la disyunción `ED ⊑ ¬PD` «arregla» el síntoma y deja el error de
modelado intacto, ahora invisible. El error real estaba en `S ⊑ R` con dominios
incompatibles —`PT` no está contenido en `PD`—, que es justo lo que detecta el
servicio de **RBox Compatibility** de §5.2.3, y que la lógica **tolera sin
inmutarse**: la teoría con esa jerarquía es perfectamente consistente.

Que una teoría sea consistente no significa que el modelado sea correcto. Esa
distancia es toda la razón de ser de §5.2.

</details>

## Qué deja el caso

1. **Las CQ se escriben antes y se ejecutan después.** Sin ellas, «buena ontología»
   no significa nada, porque no hay criterio contra el que fallar.
2. **Hay tres formas de fallar una CQ, no una**: no se contesta, se contesta vacío,
   o se contesta por accidente. Solo la primera es evidente.
3. **Una respuesta vacía es mundo abierto, no negación.** Y se prueba: si añadir lo
   contrario no genera inconsistencia, la ontología no lo estaba negando.
4. **`domain` y `range` no validan.** Producen clasificación silenciosa, y sus
   errores aparecen lejos de donde se cometieron.

---

## Los ejercicios (§5.3)

**Review question 5.1.** *«List the main high-level tasks in a ‘waterfall’ ontology
development methodology.»* — Los cinco pasos de Methontology: especificación,
conceptualización, formalización, implementación y mantenimiento, más las
actividades transversales de gestión (planificación, control, aseguramiento de
calidad) y de soporte (documentación).

**Review question 5.2.** *«Explain the difference between macro and micro level
development.»* — El macro-nivel ordena el **proceso** completo; el micro-nivel guía
el paso de una descripción informal a **axiomas concretos**: qué lenguaje, qué
ontología fundacional, si un atributo se modela como propiedad o como clase, qué
servicios de razonamiento hacen falta.

**Review question 5.3.** *«What is meant by ‘encoding peculiarities’ of an
ontology?»* — Las decisiones impuestas por el lenguaje y no por el dominio: qué hacer
con las relaciones n-arias en un lenguaje que solo tiene binarias, cómo representar
atributos, cómo simular lo que el perfil elegido no soporta. Se reconocen porque no
sobreviven a un cambio de lenguaje.

**Review question 5.4.** *«Methods were grouped into four categories.»* — La tabla de
§5.2 de más arriba: solo lógica (justificación de deducciones), solo filosofía
(OntoClean), la combinación (RBox Compatibility) y las heurísticas (OOPS! con TIPS).
La diferencia es **contra qué se contrasta**: contra la teoría, contra la naturaleza
de las cosas, contra ambas, o contra la experiencia acumulada.

**Review question 5.5.** *«Give two examples of types of modelling flaws.»* — (1)
Confundir `∀` con `∃` en una definición, que deja entrar a todo el que no participa
en la relación —los capítulos 3 y 5 de este trabajo lo verifican dos veces—. (2)
Declarar `domain`/`range` esperando validación y provocar una clasificación que
choca con una disyunción: el Exercise 5.3 de esta misma página.

**Review question 5.6.** *«Compare the older Methontology with the newer NeOn
methodology.»* — Methontology es de ontología única y en cascada: un camino, de la
especificación al mantenimiento. NeOn parte de que la ontología **casi nunca se
construye desde cero** y ofrece varios escenarios —reutilizar recursos no
ontológicos, reutilizar y reingeniar ontologías, alinearlas, modularizarlas— más
soporte para desarrollo colaborativo y en red. *Criterio propio: la diferencia de
fondo no es la agilidad sino la unidad de trabajo — para Methontology es «la
ontología», para NeOn es «la red de ontologías», y eso cambia qué decisiones son
importantes.*

**Exercise 5.1.** *«Consider the following CQs and evaluate the
AfricanWildlifeOntology1.owl against them.»* — Es la parte A del caso de estudio de
esta página: 4 de 11, con el desglose y las pruebas de por qué falla cada una.

**Exercise 5.2.** *«Take the Pizza ontology and submit it to the OOPS! portal.»* —
OOPS! es un servicio web y no se puede meter dentro de `verificar.py`, así que **no
se afirma aquí ningún resultado suyo**. *Criterio propio: los pitfalls que OOPS!
marca como críticos y que este trabajo ya comprueba por otra vía son P19 (relaciones
sin dominio o rango declarados), P11 (falta de disyunción entre hermanos, verificado
en el capítulo 3) y P24 (definiciones recursivas). Queda pendiente pasar la ontología
propia por el portal cuando exista.*

**Exercise 5.3.** *«Is A consistent? Verify this with the reasoner and explain
why.»* — Parte B del caso de estudio: **no**, `A` es insatisfacible, y la causa es la
declaración de dominio de `R`, no ninguna contradicción escrita. Sobre (b), el
servicio de RBox Compatibility señalaría `S ⊑ R` con `S ⊑ PT × PT` frente a
`R ⊑ PD × PD`: para que una subpropiedad sea coherente, su dominio y rango deben
estar **contenidos** en los del padre, y `PT` contiene a `PD`, no al revés. Sí, el
conocimiento está ontológicamente mal formado — y verificado queda que la lógica no
protesta por ello.

**Exercise 5.4.** *«Apply the OntoClean rules to the flawed ontology of Figure
5.7.»* — Depende de una figura del libro. Lo transferible son las reglas: si `q`
subsume a `p`, entonces si `q` es antirrígida `p` también debe serlo; los criterios de
identidad y unidad incompatibles son disyuntos; en corto, `+R ⊄ ∼R`, `−I ⊄ +I`,
`−U ⊄ +U`, `+U ⊄ ∼U`, `−D ⊄ +D`. El caso típico que cazan: `Persona` (rígida) colgada
bajo `Estudiante` (antirrígida), que ningún razonador marcará jamás como error.

**Exercise 5.6.** *«Pick a topic and step through one of the methodologies.»* —
*Criterio propio: pendiente, y es la deuda declarada de este repositorio. Es el
ejercicio que debería producir la ontología propia del trabajo —dominio, alcance y
preguntas de competencia— y hasta que exista, los capítulos siguientes se apoyan en
las ontologías del libro.*

**Exercise 5.7.** *«Antelope is a “wastebasket taxon”… What do modelling guidelines
say about that?»* — Las guías tipo TIPS desaconsejan las clases «cajón de sastre» y
las categorías «otros»: no tienen condiciones necesarias y suficientes, cambian
cuando cambia el resto de la clasificación, y no son rígidas en el sentido de
OntoClean. *Criterio propio: para la AWO, lo defendible es no crear `Antelope` como
clase y colgar `Impala` directamente de `Bovidae`, dejando «antílope» como
anotación o etiqueta alternativa. Se pierde una etiqueta cómoda y se gana que ningún
razonador deduzca algo a partir de un grupo que solo existe por descarte.*

---

## Lo que hay que llevarse

1. **Las preguntas de competencia son la especificación**, y son lo único del
   proceso que se puede ejecutar. En este repositorio viven dentro de cada
   `verificar.py`.
2. **Una CQ puede fallar de tres maneras**, y dos de ellas parecen éxitos.
3. **Consistente ≠ bien modelado.** OntoClean y RBox Compatibility existen porque el
   razonador es ciego a errores ontológicos.
4. **Elegir una metodología cualquiera es mejor que no elegir ninguna** — es la
   recomendación literal de Keet, y la única del capítulo que no admite matices.

<small>Salvo los enunciados citados, el análisis y las resoluciones de esta página
son criterio propio, verificados con HermiT. Numeración y enunciados tomados del PDF
en <a href="https://github.com/inter097/ontology-engineering/tree/main/libro">/libro</a>,
no de ediciones web que renumeran las secciones.</small>

<details class="defensa">
<summary>Para la defensa — lo que te van a preguntar de aquí</summary>

**«¿Qué metodología has seguido y por qué?»**

Un esqueleto de micro-nivel guiado por preguntas de competencia, con verificación
ejecutable en cada paso. La razón está en §5.1.1: cualquier metodología es mejor que
ninguna, porque evita repetir errores conocidos. Lo que se ha añadido por criterio
propio es el rasgo ágil que el libro solo esboza —cada capítulo tiene un
`verificar.py` que falla con código 1 si una afirmación deja de reproducirse—, de
modo que las CQ funcionan como pruebas de regresión y no como documentación.

**«¿Cómo sabes que tu ontología es buena?»**

No hay métrica única, y decirlo es parte de la respuesta. Hay cuatro fuentes de
evidencia independientes: el razonador (sin clases insatisfacibles ni
inconsistencia), las preguntas de competencia (cada una con su respuesta esperada),
OOPS! (ausencia de pitfalls críticos) y las métricas estructurales. Ninguna basta
sola: el caso de estudio de este capítulo enseña una ontología **consistente** que
contesta 4 de 11 requisitos.

**«¿Por qué insistes tanto en que una respuesta vacía no es un “no”?»**

Porque bajo mundo abierto la ausencia de una respuesta significa «no consta», no «no
existe», y **es comprobable cuál de las dos es**: si al afirmar lo contrario la
ontología sigue siendo consistente, era ignorancia.

*Por qué es una respuesta fuerte:* está medido en este capítulo. A la CQ8 —«¿quién
depreda al rockdassie?»— la AWO responde vacío, y se demuestra que es ignorancia
añadiendo un depredador sin que nada se rompa. Un informe que hubiera leído ese
vacío como un «no tiene depredadores» habría afirmado algo que la ontología jamás
dijo.

**«¿Qué aporta OntoClean si el razonador no encuentra nada?»**

Precisamente eso: encuentra lo que el razonador no puede encontrar. Una jerarquía
puede ser lógicamente impecable y ontológicamente falsa —`Persona` bajo
`Estudiante` es el ejemplo canónico— y ninguna cantidad de razonamiento la detecta,
porque no hay contradicción. OntoClean aporta el criterio externo: rigidez,
identidad y unidad.

**«En tu caso de estudio la clase `A` es insatisfacible. ¿Dónde está el error?»**

No donde señala el razonador. `A` es insatisfacible porque `A ⊑ ∃R.B` la mete en el
dominio declarado de `R`, que es disjunto de su superclase. El error de modelado
está en la RBox —`S ⊑ R` con dominios incompatibles— y la lógica lo tolera sin
protestar.

*El matiz que conviene añadir:* la tentación es «arreglarlo» quitando la disyunción,
que hace desaparecer el síntoma y deja el error intacto y ya invisible. Por eso la
justificación de deducciones (§5.2.1) es un método en sí mismo: sin saber **qué
conjunto mínimo de axiomas** causa la insatisfacibilidad, la reparación es a ciegas.

</details>
