---
titulo: 'Modelado avanzado: lo que OWL no sabe decir'
capitulo: 10
descripcion: 'Incertidumbre, vaguedad y tiempo. Tres cosas del mundo que un lenguaje nítido y atemporal no representa — y las salidas, medidas: el umbral inventado de «joven» y las dos formas de decir «fue estudiante».'
keet: 'cap. 10 (Advanced Modelling with Additional Language Features), §10.1–10.3, 1ª ed. v1.5'
hallazgo: 'Alinear como equivalentes dos ontologías que ponen el umbral de «joven» en 30 y en 35 vuelve la ontología inconsistente en cuanto aparece alguien de 31.'
cifras:
  - valor: '2'
    etiqueta: 'formas de meter tiempo en OWL'
  - valor: '0'
    etiqueta: 'grados de pertenencia en OWL 2'
  - valor: '8'
    etiqueta: 'comprobaciones'
---

Los capítulos anteriores dan por bueno un supuesto que el mundo no cumple: que todo
es **nítido** —o se pertenece a una clase o no— y **atemporal** —lo que es cierto, lo
es siempre—. Este capítulo mira qué pasa cuando eso no vale.

> **Nota de edición.** Esta página cubre el capítulo 10 de la **1ª edición, v1.5
> (2020)**: *Advanced Modelling with Additional Language Features*. En la 2ª edición
> el 10 es *Rough, Temporal, and Fuzzy Modelling* y el 11 pasa a ser *More Topics to
> Explore*. La numeración coincide hasta el 9 (ver [README](https://github.com/inter097/ontology-engineering)).

## Incertidumbre y vaguedad no son lo mismo (§10.1)

Es la primera *review question* del capítulo y la distinción que ordena todo lo demás:

| | **Incertidumbre** | **Vaguedad** |
|---|---|---|
| Qué pasa | el hecho es nítido, **no se sabe** si se cumple | el concepto **no tiene frontera** exacta |
| Ejemplo | «probablemente llueva mañana» | «es alto», «es joven», «está calvo» |
| Se trata con | probabilidad | lógica difusa (grados de pertenencia) |
| Al saber más | se resuelve | **no se resuelve**: sigue siendo vago |

La prueba para distinguirlas: **si toda la información del mundo eliminara la duda,
era incertidumbre; si no, era vaguedad**. Nadie deja de dudar si alguien de 31 años es
joven por medir más.

<details class="peras">
<summary>¿Y esto qué quiere decir? Sin jerga</summary>

Dos frases que parecen del mismo tipo y no lo son.

*«No sé si el paquete llegó ayer.»* — El paquete llegó o no llegó. Hay una respuesta
exacta ahí fuera; lo que falta es que yo la sepa. Una llamada y se acabó la duda.

*«No sé si Bea es joven.»* — Aquí no hay ninguna llamada que hacer. Sé que tiene 31
años, sé todo lo que hay que saber, y la duda **sigue igual de viva**. No falta
información: falta frontera. «Joven» no tiene un borde donde termina.

La primera es incertidumbre: se arregla sabiendo más. La segunda es vaguedad: no se
arregla nunca.

Y esto importa porque en un lenguaje como OWL solo hay dos opciones, dentro o fuera.
Así que la vaguedad hay que resolverla a martillazos: eligiendo un número. Y ese
número no está en el mundo, lo pone quien modela — con las consecuencias que se
comprueban abajo.

</details>

**Conceptos difusos** son los del ejemplo del libro: *joven*, *alto*, *caro*, *cerca*,
*grande*. Frente a ellos, *menor de edad* es **nítido**: la ley pone la frontera en un
número exacto. Los dos suenan parecido y son animales distintos.

**Ontologías rough.** Cuando un concepto no se puede definir con precisión pero sí
acotar, se aproxima por arriba y por abajo (Review question 10.3): una clase
**aproximación inferior** —lo que seguro pertenece—, una **aproximación superior** —lo
que podría pertenecer— y el concepto en medio. En OWL se representa con dos clases
normales y `Inferior ⊑ Concepto ⊑ Superior`, sin salir del lenguaje. Lo que queda
entre las dos es la **región frontera**.

## Tiempo (§10.2)

Hay **dos formas conceptualmente distintas** de meter tiempo (Review question 10.4):

1. **Extender el lenguaje.** Lógicas descriptivas temporales —`DLR_US`, `TDL-Lite`—
   con operadores del tipo «siempre», «alguna vez», «hasta». Se gana expresividad y
   se pierde soporte: no hay razonadores estándar ni es OWL.
2. **Quedarse en OWL y modelar el tiempo como contenido.** Reificar: convertir la
   relación temporal en una clase con su intervalo, o usar **partes temporales** del
   individuo. Se conserva toda la infraestructura y se paga en vocabulario y en
   consultas más complicadas.

La **Time Ontology** del W3C (OWL-Time) es la pieza estándar para la segunda vía:
aporta intervalos, instantes y las relaciones de Allen entre ellos, pero no cambia la
lógica — no permite decir «siempre», permite decir «durante este intervalo».

---

# Caso de estudio: la frontera inventada y el cambio de estado

Reproducible con:

```bash
cd capitulos/10-modelado-avanzado/artefactos
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
./.venv/bin/python verificar.py     # necesita Java en el PATH
```

## A. «Joven» en un lenguaje nítido

`Joven ≡ Persona ⊓ ∃edad.(entero ≤ 30)`. Es lo único que OWL deja escribir, y ya es
una decisión.

```
[ok] con umbral 30: ana (30) es Joven
[ok] y bea (31) NO lo es
[ok] moviendo el umbral a 35, bea pasa a ser Joven sin que nada haya cambiado
[ok] alinear dos «Joven» con umbrales 30 y 35 como equivalentes: INCONSISTENTE
```

<p class="evidencia">JovenA ≡ JovenB con umbrales distintos: ontología inconsistente</p>

Las tres primeras líneas muestran el problema conocido: **un año de diferencia produce
dos clases distintas**, y la frontera es arbitraria. Nada nuevo — todo el mundo lo
acepta como un mal menor.

La cuarta es la que muerde, y es donde la vaguedad deja de ser una incomodidad
filosófica y se convierte en un fallo de ingeniería. Dos organizaciones modelan
«joven», una con 30 y otra con 35; ambas ontologías son impecables por separado. Al
alinearlas —`JovenA ≡ JovenB`, que es lo que cualquiera escribiría, porque *es la
misma palabra*— basta **una sola persona de 31 años** para que todo se vuelva
inconsistente.

<details class="errata">
<summary>Por qué esto no se ve venir</summary>

Porque cada ontología, sola, es correcta. El razonador no tiene nada que decir de
ninguna de las dos. El error solo existe **en la unión**, y aparece cuando llegan
datos — no al alinear.

Y el diagnóstico apunta al sitio equivocado: la inconsistencia se atribuye al dato
(«esta persona tiene una edad rara») o al alineamiento («habrá que revisar el
mapping»), cuando el problema es que **se alineó como equivalente algo que nunca fue
equivalente**. Las dos clases se llamaban igual; eso es todo lo que tenían en común.
Es la misma lección de *fleuve*/*rivière* del
[capítulo 9](/capitulos/09-lenguaje-natural/), ahora provocada por un umbral en vez de
por un idioma.

Lo defendible, si hay que quedarse en OWL 2:

- **no alinear conceptos vagos con `≡`** — como mucho, subsunción en la dirección que
  se pueda justificar (`JovenA ⊑ JovenB`, que sí es cierto con 30 ≤ 35);
- **documentar el umbral como decisión**, no como hecho del dominio: es una
  *encoding peculiarity* en el sentido del [capítulo 5](/capitulos/05-metodologias/);
- **conservar el dato crudo** —la edad— para que quien reutilice la ontología pueda
  poner su propia frontera.

</details>

Lo que una ontología difusa aportaría aquí es un **grado de pertenencia** en vez de un
sí/no: Bea sería joven en grado 0,7 y la alineación entre las dos ontologías sería una
relación entre funciones, no una equivalencia que revienta. El precio es salir de OWL
2 y quedarse sin razonadores estándar.

## B. «Fue estudiante y ahora es profesora»

```
[ok] atemporal: Estudiante(nadia) y Profesora(nadia), disjuntas → INCONSISTENTE
[ok] con relaciones indexadas por tiempo: consistente
[ok] con partes temporales del individuo: consistente
[ok] …pero «nadia» ya no es ni Estudiante ni Profesora: lo son sus partes
```

<p class="evidencia">las dos salidas funcionan; las dos cambian a qué hay que preguntar</p>

La primera línea es el problema entero: **en una ontología atemporal, un cambio de
estado es una contradicción**. Y es correcto que lo sea: si `Estudiante` y `Profesora`
son disjuntas, decir que alguien es las dos es decir algo falso — falta el «cuándo»,
que el lenguaje no tiene dónde poner.

Las dos salidas funcionan y no son intercambiables:

- **Relaciones indexadas**: se reifica el estado (`EstadoEstudiante`, con su `deQuien`
  y su `durante`). La persona sigue siendo una sola. El coste: cada relación que pueda
  cambiar en el tiempo se convierte en una clase, y las consultas dejan de ser
  directas.
- **Partes temporales** (perdurantismo, cap. 6): `nadia_2015_2019` es estudiante,
  `nadia_2020_2026` es profesora, y las dos son partes temporales de `nadia`. El
  coste está en la última comprobación: **`nadia` ya no pertenece a ninguna de las dos
  clases**. Una consulta de «dame las profesoras» no la devuelve, y toda la ontología
  tiene que estar escrita sabiéndolo.

La cuarta línea es la que conviene tener verificada, porque es el argumento decisivo
al elegir: **no se elige entre dos notaciones, se elige a qué entidad se le pregunta**.

## Qué deja el caso

1. **Vaguedad ≠ incertidumbre.** La primera no se arregla con más datos.
2. **Todo umbral en OWL es una decisión de modelado**, y hay que documentarla como
   tal.
3. **Los conceptos vagos no se alinean con `≡`.** Es una bomba de relojería que
   estalla al llegar los datos.
4. **El tiempo en OWL se paga siempre**: en vocabulario, o en que el individuo deje de
   ser el sujeto de las consultas.

---

## Los ejercicios (§10.3)

**Review question 10.1.** *«What is the difference between uncertainty and
vagueness?»* — La incertidumbre es epistémica: el hecho es nítido y no se sabe si se
cumple; se trata con probabilidad y **se resuelve** al saber más. La vaguedad es del
concepto: no tiene frontera precisa; se trata con lógica difusa y **no se resuelve**
con información adicional.

**Review question 10.2.** *«Name some examples of fuzzy concepts.»* — *Joven*, *viejo*,
*alto*, *caro*, *cerca*, *grande*, *calvo*, *tibio*. Frente a ellos, *menor de edad*,
*mayor de 65 años* o *nacido en 1990* son **nítidos**: tienen frontera legal o
aritmética exacta.

**Review question 10.3.** *«How are rough concepts approximated in an OWL ontology?»* —
Con dos clases nítidas: la **aproximación inferior** (lo que con seguridad pertenece) y
la **superior** (lo que podría pertenecer), y el concepto entre las dos:
`Inferior ⊑ Concepto ⊑ Superior`. Lo que queda entre ambas es la región frontera. No
hace falta salir de OWL 2: el precio es que la incertidumbre queda representada como
estructura, no como grado.

**Review question 10.4.** *«Name two conceptually distinct ways how time can be dealt
with.»* — (1) **Extender el lenguaje** con lógicas descriptivas temporales (`DLR_US`,
`TDL-Lite`) y sus operadores. (2) **Modelar el tiempo como contenido** dentro de OWL:
reificación con intervalos —una ontología del tiempo como OWL-Time— o partes
temporales. La primera cambia la lógica; la segunda, el vocabulario. **Las dos están
verificadas en la parte B del caso de estudio**, en su variante implementable.

**Review question 10.5.** *«State for each whether it refers to uncertainty or
vagueness.»* — El criterio, aplicado: cualquier enunciado sobre lo que *puede* o
*probablemente* ocurra, sobre un diagnóstico no confirmado o sobre una medición con
error es **incertidumbre**; cualquier predicado gradual —tamaño, edad, precio,
proximidad, temperatura— es **vaguedad**. La prueba rápida: *si toda la información
del mundo despejara la duda, era incertidumbre*.

**Exercise 10.1.** *«Devise an example similar to ‘minor’ and ‘young’, but for ‘senior
citizen’, ‘old’ and ‘old person’.»* — `SeniorCitizen` es **nítido**: lo define una
norma —65 años en muchos sistemas— y es exactamente representable en OWL. `Old` es
**vago**: no hay frontera, y además depende del contexto (un coche viejo, un perro
viejo y una persona vieja no comparten escala). `OldPerson` hereda la vaguedad de
`Old` y añade una trampa: parece nítido porque suele implementarse con un umbral, que
es justo lo que se verifica en la parte A.

*Sobre las dos preguntas del enunciado, criterio propio:* (1) frente a los sistemas de
información, las ontologías difusas encajan mal — la infraestructura entera (OWL 2,
razonadores, perfiles, OBDA) presupone pertenencia nítida, y salir de ahí cuesta todo
el ecosistema; (2) frente al **objetivo original** de las ontologías, que es compartir
una conceptualización, encajan mejor de lo que parece, porque hacen **explícito** el
grado en vez de esconderlo dentro de un umbral arbitrario que cada organización elige
distinto. La parte A mide exactamente ese coste: dos umbrales razonables y una sola
persona bastan para volver inconsistente la unión.

**Exercise 10.2.** *«There are a few temporal reasoners for DLs and OWL. Find them and
assess what technology they use.»* — Los razonadores temporales quedan fuera de lo que
`verificar.py` puede ejecutar con la cadena owlready2+HermiT, así que **no se afirma
aquí ningún resultado obtenido con ellos**. Lo que sí está ejecutado es la alternativa
realista: las dos codificaciones del tiempo **dentro** de OWL 2, con sus consecuencias
medidas.

**Exercise 10.3.** *«The Time Ontology was standardised recently. Can this be a viable
alternative to `DLR_US`?»* — *Criterio propio: no como alternativa, sí como sustituto
práctico.* No es alternativa porque no es lo mismo: OWL-Time aporta **vocabulario**
—instantes, intervalos, relaciones de Allen— dentro de una lógica atemporal, mientras
que `DLR_US` aporta **operadores temporales** en la lógica misma, con lo que se pueden
escribir restricciones del tipo «siempre que…» que OWL-Time no expresa. Es sustituto
práctico porque conserva todo el ecosistema —razonadores, perfiles, herramientas— que
`DLR_US` no tiene, y para la mayoría de los proyectos eso pesa más. El coste está
medido en la parte B: el tiempo entra como estructura, y cambia a qué entidad se le
pregunta.

**Exercise 10.4.** *«BFO draft v2.1 has all those indications of time in the names of
the object properties. What would your advice to its developers be?»* — *Criterio
propio: el tiempo en el **nombre** de la propiedad es la peor de las tres opciones.*
Propiedades como `part-of-at-some-time` y `part-of-at-all-times` meten el índice
temporal en un sitio donde el razonador no lo ve —los nombres no razonan, verificado en
el [capítulo 9](/capitulos/09-lenguaje-natural/)—, de modo que no hay forma de deducir
nada de la relación entre ambas ni de comparar intervalos: el compromiso temporal queda
en la documentación, no en la lógica. El consejo sería reificar con OWL-Time cuando se
necesite el intervalo concreto, y dejar el par de propiedades solo como atajo
documentado; y si de verdad hace falta razonar sobre el tiempo, asumir que eso ya no
es OWL y usar una lógica temporal.

---

## Lo que hay que llevarse

1. **OWL 2 es nítido y atemporal.** Cualquier vaguedad o cambio de estado se
   representa deformándolo.
2. **Un umbral es una decisión, no un dato.** Documentarlo y conservar el valor
   crudo.
3. **No alinees conceptos vagos con `≡`.** Está verificado lo que pasa.
4. **Meter tiempo cambia el sujeto de las consultas.** Es la parte de la decisión que
   nadie mira hasta que las consultas dejan de funcionar.

<small>Salvo los enunciados citados, el análisis y las resoluciones de esta página
son criterio propio, verificados con HermiT. Numeración y enunciados tomados del PDF
en <a href="https://github.com/inter097/ontology-engineering/tree/main/libro">/libro</a>
(1ª edición, v1.5), no de ediciones web que renumeran las secciones.</small>

<details class="defensa">
<summary>Para la defensa — lo que te van a preguntar de aquí</summary>

**«Tu dominio tiene conceptos vagos. ¿Cómo los has tratado?»**

Con umbrales nítidos, porque OWL 2 no permite otra cosa, y **declarando el umbral como
decisión de modelado**, no como hecho del dominio. Además se conserva siempre el valor
crudo —la edad, la altura, el precio— para que quien reutilice la ontología pueda
poner su propia frontera sin rehacer nada.

*El matiz que conviene añadir:* una ontología difusa representaría el grado
explícitamente y sería más fiel, pero cuesta el ecosistema entero — OWL 2,
razonadores estándar, perfiles, OBDA. Es una decisión de ingeniería, no de precisión.

**«¿Qué diferencia hay entre incertidumbre y vaguedad, y por qué te importa?»**

La incertidumbre se resuelve sabiendo más; la vaguedad, no. Importa porque se tratan
con herramientas distintas —probabilidad frente a lógica difusa— y confundirlas lleva
a intentar arreglar con datos algo que no es un problema de datos. Nadie deja de dudar
si alguien de 31 años es joven por medir más.

**«¿Puedes alinear tu ontología con otra del mismo dominio?»**

Con cuidado, y **nunca con `≡` sobre conceptos vagos**.

*Por qué es una respuesta fuerte:* está medido. Dos ontologías que ponen el umbral de
«joven» en 30 y en 35 son impecables por separado; alineadas como equivalentes,
**basta una persona de 31 años para volver inconsistente el conjunto**. Y el fallo no
aparece al alinear, sino después, cuando llegan los datos — que es lo que hace tan
difícil diagnosticarlo. Lo defendible es alinear con subsunción en la dirección
justificable.

**«¿Cómo representas que algo cambia en el tiempo?»**

OWL 2 es atemporal: afirmar que la misma persona es estudiante y profesora, siendo
clases disjuntas, **es inconsistente** —verificado—, y es correcto que lo sea, porque
falta el «cuándo». Hay dos salidas dentro de OWL: reificar el estado con su intervalo,
o usar partes temporales del individuo. Las dos están verificadas como consistentes.

*El matiz decisivo:* con partes temporales, el individuo **deja de pertenecer a las
clases** — es `nadia_2020_2026` quien es profesora, no `nadia`. Está comprobado, y
significa que la elección no es de notación: cambia a qué entidad se le pregunta, y
por tanto cómo se escriben todas las consultas de competencia del proyecto.

**«¿Por qué no usas una lógica temporal si el tiempo importa tanto?»**

Porque `DLR_US` o `TDL-Lite` no son OWL: no hay razonadores estándar, ni perfiles, ni
herramientas, y este trabajo se apoya en lo que un razonador confirma. La alternativa
practicable es OWL-Time, que aporta vocabulario temporal sin cambiar la lógica — con
la limitación honesta de que permite decir «durante este intervalo», pero no «siempre».

</details>
