---
titulo: 'Top-down: ontologías fundacionales y la parte que no es una parte'
capitulo: 6
descripcion: 'DOLCE, BFO y por qué elegir una es una decisión filosófica con consecuencias lógicas. Y las relaciones parte-todo: el rockdassie del capítulo 5 por fin clasificado, y una deducción falsa que aparece sola al mezclar «parte» con «miembro».'
keet: 'cap. 6 (Top-down Ontology Development), §6.1–6.3'
hallazgo: 'Meter la pertenencia a un grupo dentro de la misma propiedad transitiva que la parte estructural produce una deducción falsa que nadie escribió: la hoja pasa a ser parte del bosque.'
cifras:
  - valor: '2'
    etiqueta: 'axiomas para clasificar el rockdassie'
  - valor: '0'
    etiqueta: 'mereologías completas que caben en OWL 2 DL'
  - valor: '9'
    etiqueta: 'comprobaciones'
---

Top-down significa empezar por arriba: tomar una **ontología fundacional** ya hecha
—con sus categorías más generales y sus relaciones básicas— y colgar de ahí el
dominio propio. La alternativa, empezar por los datos, es el capítulo 7.

## Por qué usar una ontología fundacional (§6.1)

Tres razones, y ninguna es teórica:

1. **Da respuestas ya tomadas** a preguntas que hay que contestar sí o sí: ¿un
   proceso es una cosa? ¿el color es una entidad o un atributo? ¿los roles son
   clases?
2. **Hace interoperables** dos ontologías de dominios distintos que comparten
   raíz.
3. **Impone disciplina**: las categorías superiores traen axiomas que hacen que un
   error de modelado se convierta en una contradicción detectable, en vez de en una
   opinión.

El precio: expresividad y tamaño. Alinear con DOLCE puede sacar la ontología del
perfil elegido en el capítulo 4.

## DOLCE frente a BFO

| | **DOLCE** | **BFO** |
|---|---|---|
| Postura filosófica | **descriptiva**: captura las categorías del lenguaje natural y el sentido común | **realista**: solo lo que existe en la realidad, tal como la describe la ciencia |
| Corte principal | endurante / perdurante | continuante / ocurrente |
| Cualidades | entidades de primera clase, con su espacio de valores | no hay cualidades reificadas del mismo modo; hay *dispositions* y *qualities* dependientes |
| Tamaño | grande, muy axiomatizada | deliberadamente pequeña |
| Entidades sin correlato real | admite `Set`, entidades sociales, ficciones | las rechaza por principio |

<details class="peras">
<summary>¿Y esto qué quiere decir? Sin jerga</summary>

Dos formas de organizar el mundo antes de empezar a describir nada.

**La descriptiva (DOLCE)** pregunta: *«¿de qué habla la gente?»*. Si la gente habla
de deudas, de países y de personajes de novela, esas cosas entran en el catálogo,
existan o no en algún sentido fuerte. El objetivo es encajar con cómo pensamos.

**La realista (BFO)** pregunta: *«¿qué hay ahí fuera de verdad?»*. Si algo solo
existe porque lo hemos acordado entre todos —una deuda, un cargo, un equipo— no
entra como entidad de pleno derecho. El objetivo es encajar con lo que la ciencia
describe.

Ninguna es «la correcta». Son dos apuestas distintas, y **cambian qué se puede
escribir**. Una ontología de administración pública está llena de cosas que existen
solo por convenio social; con la realista se pelea todo el rato. Una de anatomía o de
química no tiene ese problema y agradece lo pequeña que es.

El otro corte —endurante/perdurante, continuante/ocurrente— es esta pregunta: *«¿esto
está entero cada vez que lo miras, o va pasando por partes?»*. Una silla está entera
ahora. Un concierto, no: ahora está pasando el segundo movimiento, y el primero ya no
está. La silla es endurante; el concierto, perdurante. Y una misma cosa no puede ser
las dos, que es de donde salen las contradicciones útiles.

</details>

La pregunta de Exercise 6.2 —qué fundacional para qué dominio— tiene una respuesta
razonable justo con esa tabla, y el libro señala **ONSET** como herramienta para
tomar la decisión con criterios explícitos en vez de por costumbre.

## Relaciones parte-todo (§6.2)

Aquí está el contenido que más se usa en la práctica. «Parte de» en lenguaje natural
tapa varias relaciones distintas, y tratarlas como una sola es el error del capítulo:

| Relación | Ejemplo | ¿Transitiva? |
|---|---|---|
| **parte estructural** (mereológica) | rama – árbol | **sí** |
| **miembro de** un colectivo | músico – orquesta | **no** |
| **porción de** una masa | rebanada – pan | sí, con cuidado |
| **constituido por** | estatua – bronce | **no**: no es parte-todo |
| **participa en** | músico – concierto | **no**: es endurante en perdurante |
| **ubicado en** | león – reserva natural | **no** |

Las tres últimas ni siquiera son parte-todo, aunque el lenguaje las diga igual. La
distinción endurante/perdurante de la fundacional es justo lo que permite verlo:
un músico no es *parte* de una actuación, **participa** en ella.

**Y la mereología no cabe entera en OWL 2 DL** (Review question 6.6). La parte propia
debería ser transitiva y **asimétrica**; los axiomas de suplementación exigen
cuantificar sobre variables compartidas, que las DLs no tienen. Lo que se implementa
siempre es una aproximación, y conviene saber cuál.

---

<h2 class="caso">Caso de estudio: el rockdassie, y la hoja que acabó siendo parte del bosque</h2>

Reproducible con:

```bash
cd capitulos/06-top-down/artefactos
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
./.venv/bin/python verificar.py     # necesita Java en el PATH
```

## A. Exercise 6.6(a): clasificar el rockdassie

El enunciado: *«Add enough knowledge so that RockDassie will be classified
automatically as a subclass of Herbivore.»* Es la **CQ2 que el
[capítulo 5](/capitulos/05-metodologias/) dejó sin contestar**.

```
[ok] de partida NO se clasifica: la AWO solo dice RockDassie ⊑ animal
[ok] con RockDassie ⊑ ∃eats.plant TAMPOCO se clasifica
[ok] con RockDassie ⊑ ∀eats.plant ⊓ ∃eats.plant SÍ
[ok] y no se clasifica además como carnivore
```

<p class="evidencia">AWO + 2 axiomas ⊨ RockDassie ⊑ herbivore</p>

La línea que importa es la segunda. El arreglo intuitivo —«el rockdassie come
plantas»— **no funciona**, porque `herbivore` está definida con `∀`: para entrar hay
que garantizar que *todo* lo que come es vegetal, y «come alguna planta» no excluye
nada. Hacen falta los dos cuantificadores, y cada uno hace un trabajo distinto:

- el `∀` es lo que **mete** al rockdassie en la definición;
- el `∃` es lo que impide que entre **por vacuidad** — sin él, el rockdassie sería
  también carnívoro (capítulos [3](/capitulos/03-logicas-descriptivas/) y
  [5](/capitulos/05-metodologias/)) y la ontología se caería.

**La pareja `∀ + ∃` es la forma canónica de una definición por lo que se come, se
tiene o se hace.** Escribir solo una de las dos es el error más repetido de todo el
libro.

## B. Cuando «parte» y «miembro» son la misma propiedad

Cuatro individuos y tres hechos:

```
hoja —partOf→ rama —partOf→ árbol —memberOf→ bosque
```

```
[ok] con memberOf ⊑ partOf (transitiva), se deduce partOf(hoja, bosque)
[ok] separando las dos propiedades, la deducción falsa desaparece
[ok] y lo verdadero sigue: partOf(hoja, árbol)
```

<p class="evidencia hipotesis">deducción falsa: partOf(hoja, bosque)</p>

Nadie escribió que la hoja fuera parte del bosque. Lo produjo la transitividad al
atravesar una relación que **no es parte-todo**: un árbol no es *parte* de un bosque,
es un **miembro** de él. Y una vez dentro de la misma propiedad transitiva, la lógica
no tiene forma de saber dónde estaba la frontera.

<details class="errata">
<summary>Por qué esto se cuela siempre</summary>

Porque «parte de» funciona en español para las dos cosas, y porque juntar todo en una
sola propiedad **parece** más limpio: menos vocabulario, menos axiomas, una jerarquía
más ordenada.

El síntoma tarda en aparecer. La ontología es consistente, no hay clases
insatisfacibles, OOPS! no dice nada. La deducción falsa solo se ve si alguien
pregunta —una CQ— o si mira la lista de hechos inferidos, que casi nadie mira.

La regla que queda: **la transitividad no es una propiedad de la palabra, sino de la
relación**. Antes de declarar `Trans(R)` hay que comprobar el encadenamiento en los
dos sentidos con ejemplos del dominio, y en cuanto uno solo chirríe, la relación son
dos relaciones y hay que partirlas.

Corolario incómodo: `is-part-of` es lo primero que todo el mundo declara transitivo,
y casi siempre acaba llevando varias relaciones distintas dentro.

</details>

## C. La mereología no cabe en OWL 2 DL

```
[ok] properPartOf transitiva sola: aceptada
[ok] properPartOf transitiva + asimétrica: RECHAZADA
```

<p class="evidencia">transitiva + asimétrica: fuera de OWL 2 DL</p>

Es la respuesta a Review question 6.6, y enlaza directamente con el
[capítulo 4](/capitulos/04-owl-2/): una propiedad transitiva **no es simple**, y la
asimetría solo se admite en propiedades simples. Lo que la mereología pide como
mínimo —parte propia transitiva y asimétrica— el estándar no lo deja escribir. Ni
siquiera es una limitación de expresividad: es una restricción global de sintaxis.

Y la antisimetría (`x ⊑ y ∧ y ⊑ x → x = y`), que es la que de verdad quiere la
mereología, **no existe en OWL 2** en ninguna forma. Lo que se implementa siempre es
una aproximación: transitividad y punto, confiando en que nadie escriba el ciclo.

## Qué deja el caso

1. **Una definición se cierra con `∀ + ∃`.** El `∀` clasifica; el `∃` impide la
   vacuidad. Falta cualquiera de los dos y la ontología miente en una dirección o en
   la otra.
2. **«Parte de» son varias relaciones.** La fundacional sirve exactamente para eso:
   dar nombres distintos a lo que el idioma confunde.
3. **La transitividad se comprueba con ejemplos antes de declararse**, en los dos
   sentidos.
4. **La mereología completa no es representable en OWL 2 DL.** Cualquier ontología
   parte-todo es una aproximación, y hay que documentar cuál.

---

## Los ejercicios (§6.3)

**Review question 6.1.** *«Why would one want to at least consider using a
foundational ontology?»* — Por interoperabilidad, por no volver a decidir desde cero
cuestiones ya resueltas (procesos, roles, cualidades, participación) y porque sus
axiomas convierten errores de modelado en contradicciones detectables. El coste es
expresividad y tamaño.

**Review question 6.2.** *«Name at least three fundamental ontological design
decisions.»* — (1) Descriptiva o realista. (2) Multiplicativa o reduccionista: ¿pueden
coexistir dos entidades en el mismo sitio a la vez —la estatua y el bronce— o son la
misma? (3) Endurantismo/perdurantismo: ¿las cosas persisten enteras en el tiempo o
por partes temporales? Se añaden el tratamiento de universales frente a
particulares y si se admiten entidades abstractas.

**Review question 6.3.** *«Major differences between DOLCE and BFO in philosophical
approach?»* — DOLCE es **descriptiva** y con sesgo cognitivo/lingüístico: modela las
categorías implícitas en el lenguaje natural y el sentido común, admitiendo entidades
que existen por convención. BFO es **realista**: solo entidades que existen en la
realidad según la ciencia. La consecuencia práctica es qué se puede meter dentro.

**Review question 6.4.** *«Major difference in type of contents?»* — DOLCE es grande y
muy axiomatizada, con cualidades y espacios de valores reificados, y admite conjuntos
y entidades sociales. BFO es deliberadamente pequeña, pensada como esqueleto
compartido para ontologías biomédicas, y deja el contenido a las ontologías de
dominio.

**Review question 6.5.** *«Name at least 2 common relations in the OWLized DOLCE, GFO
and RO.»* — **Parthood** (`part-of` / `has-part`, con sus variantes temporalizadas) y
**participation** (un endurante participa en un perdurante). Añadiría la
**inherencia**/dependencia de cualidad respecto a su portador, presente en las tres
con nombres distintos. *Criterio propio: la que más problemas da al alinear no es
`part-of` sino la participación, porque en OWL se aplana a una propiedad binaria y se
pierde el índice temporal.*

**Review question 6.6.** *«Why can one not represent Ground Mereology fully in OWL 2
DL?»* — Porque la parte propia necesita transitividad **y** asimetría a la vez, y OWL
2 DL prohíbe la asimetría en propiedades no simples; **verificado en la parte C del
caso de estudio**. Además, la antisimetría no existe en el lenguaje, y los axiomas de
suplementación (*si algo tiene una parte propia, tiene otra disjunta de la primera*)
exigen cuantificación sobre variables compartidas que ninguna DL admite.

**Review question 6.7.** *«Which part-whole relation is appropriate?»*

| Par | Relación | Por qué |
|---|---|---|
| Plant – Twig | **parte estructural** | la ramita es parte de la planta; transitiva |
| Tusk/Ivory – Apatite | **constituido por** | el marfil no es parte del colmillo: es de lo que está hecho |
| Musician – Performance | **participa en** | endurante en perdurante; no es parte-todo |
| Musician – Orchestra | **miembro de** | colectivo; no transitiva — es el caso verificado en la parte B |

**Exercise 6.1.** *«Match the DOLCE classes to a class in BFO.»* — Encajan bien
`Endurant`→`Continuant`, `Process`→`Process`, `Quality`→`Quality`,
`Amount of Matter`→`Object Aggregate`/porción de materia,
`Spatial Region`→`Spatial Region`, `Accomplishment`→`Process` (BFO no distingue
logros de procesos por su telicidad). **`Set` no es mapeable**: es una entidad
abstracta y BFO, por realista, no la admite. *Criterio propio: `Agentive Physical
Object` tampoco tiene equivalente limpio — la agentividad en BFO no es una categoría
de objeto sino una disposición realizada en procesos, así que el mapeo cambia de tipo
de entidad.*

**Exercise 6.2 y 6.4.** *«Which foundational ontology would you choose?»* — *Criterio
propio, con la tabla de §6.1 como base:*

- *Administración pública y aspectos sociológicos: **DOLCE**. El dominio es casi todo
  entidades sociales —cargos, competencias, expedientes— que existen por convención;
  con una fundacional realista se pelea en cada clase.*
- *Fisiología y química de plantas medicinales: **BFO**. Es el terreno para el que se
  diseñó, hay ontologías biomédicas alineadas de sobra que reutilizar, y su tamaño
  reducido no estorba.*
- *El escenario bancario del Exercise 6.4: **DOLCE**. El enunciado pide
  explícitamente entidades abstractas (préstamos), procesos (retiradas, depósitos),
  fechas y transacciones pasadas, y supuestos ontológicos «basados en el sentido común
  humano» — que es la definición misma de una fundacional descriptiva. La exigencia de
  OWL 2 DL obliga además a usar la versión OWLizada, no la de primer orden, y a
  aceptar que la mereología quedará aproximada, como se verifica en este capítulo.*

**Exercise 6.3.** *«Use ONSET and re-do Exercise 6.2.»* — ONSET es una herramienta de
escritorio y no entra en `verificar.py`, así que **no se afirma aquí ningún resultado
suyo**. *Criterio propio: lo valioso del ejercicio no es si ONSET coincide, sino que
obliga a escribir los criterios de la elección —expresividad requerida, dominio,
necesidad de razonamiento, reutilización disponible— en vez de elegir por costumbre o
por lo que use el laboratorio de al lado.*

**Exercise 6.6.** *«Modify the AWO so that…»* — El apartado (a) es la parte A del caso
de estudio. Sobre (b) y (c), *criterio propio*: para «los leones residen en reservas
naturales situadas en un país» hace falta vocabulario nuevo —`NatureReserve`,
`Country`, y una relación de **ubicación**, que **no** es parte-todo (§6.2)—; y
`located-in` sí encadena bien (si el león está en la reserva y la reserva en Kenia, el
león está en Kenia), así que es un caso legítimo de propiedad transitiva, al revés que
el `memberOf` de la parte B. Para (c), «guardabosques» es un **rol** que desempeña un
humano, no una subclase de humano: es antirrígido en el sentido de OntoClean (cap. 5)
y colgarlo de `Human` es el error que ese método existe para cazar. Aquí sí ayuda la
fundacional, que ya tiene la categoría de rol y la relación de desempeño.

**Exercise 6.7.** *«How would dispositions and realisations affect the AWO regarding
eats?»* — *Criterio propio: `eats` mezcla dos cosas distintas — la **disposición** de
un animal a comer cierto tipo de cosa (que tiene aunque ahora mismo no coma) y el
**proceso** concreto de comer, que ocurre en un tiempo y tiene participantes.
Modelarlas separadas resolvería de raíz la vacuidad del `∀` que rompe la AWO: la
definición de herbívoro pasaría a ser sobre la disposición —que todo animal tiene—
en vez de sobre los actos de comer registrados, que pueden ser cero. El coste es que
la ontología se llena de entidades intermedias y sube de perfil.*

---

## Lo que hay que llevarse

1. **Elegir fundacional es elegir qué existe.** Descriptiva o realista no es un
   matiz académico: decide si tu dominio cabe.
2. **`∀ + ∃`**, siempre juntos, en cualquier definición basada en una relación.
3. **La transitividad se hereda a lo largo de toda una jerarquía de propiedades**, y
   por ahí se cuela lo que no es parte-todo.
4. **En OWL 2 DL toda mereología es una aproximación.** Saber cuál se está usando es
   parte del trabajo, no un detalle.

<small>Salvo los enunciados citados, el análisis y las resoluciones de esta página
son criterio propio, verificados con HermiT. Numeración y enunciados tomados del PDF
en <a href="https://github.com/inter097/ontology-engineering/tree/main/libro">/libro</a>,
no de ediciones web que renumeran las secciones.</small>

<details class="defensa">
<summary>Para la defensa — lo que te van a preguntar de aquí</summary>

**«¿Usas ontología fundacional? ¿Cuál y por qué?»**

La decisión se toma con los criterios de §6.1 y se declara: **descriptiva (DOLCE)**
si el dominio está lleno de entidades que existen por convención social, **realista
(BFO)** si es un dominio científico con ontologías alineadas que reutilizar. Lo que
no es defendible es elegir por costumbre — y por eso el libro señala ONSET, que
obliga a escribir los criterios.

*El matiz que conviene añadir:* alinear con una fundacional tiene un coste medible en
expresividad, y puede sacar la ontología del perfil de OWL 2 elegido. Es una decisión
que se toma con la tabla de complejidad del capítulo 4 delante.

**«¿Por qué no declaras `part-of` transitiva y ya está?»**

Porque la transitividad atraviesa toda la jerarquía de propiedades y arrastra
relaciones que no son parte-todo.

*Por qué es una respuesta fuerte:* está verificado en este capítulo. Con `memberOf`
como subpropiedad de un `partOf` transitivo, el razonador deduce que **la hoja es
parte del bosque** — algo que nadie escribió y que es falso, sin que la ontología sea
inconsistente ni haya clase insatisfacible alguna. Es un error que ningún razonador
señala como error: solo aparece si se pregunta.

**«¿Qué relaciones parte-todo distingues y con qué criterio?»**

Parte estructural, miembro de un colectivo y porción de una masa son parte-todo;
constitución, participación y ubicación **no lo son**, aunque el idioma las diga
igual. El criterio para separarlas viene de la fundacional: la participación relaciona
un endurante con un perdurante, y la constitución relaciona dos entidades que
coexisten sin que una sea parte de la otra.

**«¿Tu ontología implementa mereología?»**

Implementa una **aproximación**, y está documentado cuál. La mereología básica exige
parte propia transitiva y asimétrica, y OWL 2 DL lo prohíbe: una propiedad transitiva
no es simple y la asimetría solo se admite en simples — verificado en este capítulo, el
razonador rechaza la ontología entera. La antisimetría directamente no existe en el
lenguaje, y los axiomas de suplementación tampoco son expresables. Lo que queda es
transitividad y disciplina.

**«El capítulo 5 dejaba sin contestar si el rockdassie es herbívoro. ¿Se arregló?»**

Sí, y hicieron falta **dos** axiomas, no uno: `∀eats.plant` para entrar en la
definición y `∃eats.plant` para no entrar por vacuidad. El intento evidente
—`∃eats.plant` solo— está verificado que **no** clasifica, porque `herbivore` está
definida con un universal. Es el mismo patrón `∀ + ∃` que aparece en los capítulos 3 y
5; a estas alturas del trabajo es la firma del error más común del libro.

</details>
