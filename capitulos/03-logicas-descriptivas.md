---
titulo: 'Description Logics: el motor que hay debajo de OWL'
capitulo: 3
descripcion: 'La familia de lógicas que decide qué puede inferir un razonador y en cuánto tiempo. El ejercicio del libro sobre veganos y vegetarianos resuelto con HermiT — y las tres consecuencias del cuantificador universal que el ejercicio no menciona.'
keet: 'cap. 3 (Description Logics), §3.1–3.4'
hallazgo: 'Degradar dos clases definidas a primitivas no «pierde precisión»: destruye por completo la subsunción que el propio ejercicio del libro pide demostrar.'
cifras:
  - valor: '3'
    etiqueta: 'cajas: TBox, ABox, RBox'
  - valor: '5'
    etiqueta: 'servicios de razonamiento'
  - valor: '9'
    etiqueta: 'comprobaciones'
---

El capítulo 3 es el que explica **por qué** el razonador infiere lo que infiere.
Las lógicas descriptivas son fragmentos decidibles de la lógica de primer orden, y
OWL 2 no es más que una sintaxis para una de ellas. Todo lo que en el capítulo 4
parecerá una peculiaridad de la herramienta, aquí es una decisión de diseño con
nombre y coste computacional.

> Si `⊑`, `≡`, `∀`, `∃` o `⊤` todavía no se leen solos, están uno a uno en el
> [capítulo 0](/capitulos/00-simbolos/).

## Tres tipos de entidades, tres cajas (§3.1.1)

En una lógica descriptiva solo hay tres clases de cosas: **conceptos** (conjuntos de
individuos), **roles** (relaciones binarias) y **nombres de individuo**. En lógica de
primer orden serían predicados unarios, binarios y constantes.

Los axiomas se agrupan por costumbre —no por obligación lógica— en tres cajas:

| Caja | Qué contiene | Ejemplo |
|---|---|---|
| **ABox** | hechos sobre individuos con nombre | `Mother(julia)`, `parentOf(julia, john)` |
| **TBox** | terminología: relaciones entre conceptos | `Mother ≡ Female ⊓ Parent` |
| **RBox** | axiomas sobre los roles | `parentOf ⊑ ancestorOf`, `parentOf⁻ ≡ childOf` |

Keet insiste en un punto que conviene no perder: *«unlike a database, a DL ontology
does not fully describe a particular situation»*. Los axiomas capturan conocimiento
**parcial**, y hay muchos estados del mundo compatibles con la ontología. Es la misma
idea del capítulo 2 —cuantificar sobre todos los modelos— dicha en el vocabulario que
se usará de aquí en adelante.

## Constructores: dónde empieza a doler (§3.1.2)

Los booleanos son los esperables: `C ⊓ D`, `C ⊔ D`, `¬C`, más `⊤` y `⊥`.

Lo que de verdad cambia cómo modelas son las **restricciones de rol**, y en concreto
la pareja `∃R.C` / `∀R.C`:

| Construcción | Se lee | Trampa |
|---|---|---|
| `∃eats.Plant` | come **al menos una** planta | no dice que solo coma plantas |
| `∀eats.Plant` | **todo** lo que come es planta | **cierto si no come nada** |

Esa última casilla es el contenido entero del caso de estudio de esta página.

<details class="peras">
<summary>¿Y esto qué quiere decir? Sin jerga</summary>

Piensa en una caja de fruta y en dos frases sobre ella.

*«En la caja hay alguna manzana»* — para comprobarlo tienes que encontrar una
manzana. Si la caja está vacía, la frase es **falsa**.

*«En la caja, todo lo que hay es manzana»* — para comprobarlo vas sacando cosas y
miras que ninguna desentone. Si la caja está **vacía**, no sacas nada, no encuentras
ninguna que desentone… y la frase es **verdadera**.

Suena a truco, pero es exactamente cómo funciona: *«todo lo que hay es X»* se cumple
de sobra cuando no hay nada.

La primera frase es `∃`. La segunda es `∀`. Y por eso una persona de la que consta
que no come nada encaja perfectamente en la definición de vegana: todo lo que come
es vegetal, porque no come nada.

---

**Y hay una segunda vuelta.** Para que el razonador saque esa conclusión, no basta
con que no sepas qué come esa persona. Tienes que **decirle** que no come nada.

Que en tu ontología no haya un dato no significa que ese dato no exista: significa
que no consta. Silencio no es negación. Si quieres que el razonador trate la caja
como vacía, hay que escribir «esta caja está vacía» — no basta con no escribir nada.

</details>

También están los **nominales** (`{julia}`, enumerar individuos como concepto) y las
**cardinalidades cualificadas** (`≥2 parentOf.Person`). Cada uno tiene su letra en el
nombre de la lógica y su factura en complejidad.

## Semántica: interpretaciones, otra vez (§3.1.3)

Idéntica maquinaria que en el capítulo 2, con notación propia. Una interpretación
`I` es un dominio no vacío `Δᴵ` más una función `·ᴵ` que manda cada concepto a un
subconjunto de `Δᴵ`, cada rol a un subconjunto de `Δᴵ × Δᴵ` y cada individuo a un
elemento de `Δᴵ`.

<details class="peras">
<summary>La versión formal, para cuando haga falta citarla</summary>

Tal como las da §3.2.1 para `ALC`:

| Sintaxis | Semántica |
|---|---|
| `(¬C)ᴵ` | `Δᴵ \ Cᴵ` |
| `(C ⊓ D)ᴵ` | `Cᴵ ∩ Dᴵ` |
| `(C ⊔ D)ᴵ` | `Cᴵ ∪ Dᴵ` |
| `(∀R.C)ᴵ` | `{x \| ∀y. Rᴵ(x,y) → Cᴵ(y)}` |
| `(∃R.C)ᴵ` | `{x \| ∃y. Rᴵ(x,y) ∧ Cᴵ(y)}` |

Con `⊤ᴵ = Δᴵ` y `⊥ᴵ = ∅`. `I` satisface `C ⊑ D` si `Cᴵ ⊆ Dᴵ`, y satisface `C ≡ D`
si `Cᴵ = Dᴵ`. Una `KB` es **satisfacible** si admite un modelo.

Mirando la fila de `∀R.C`: si no hay ningún `y` con `Rᴵ(x,y)`, el condicional es
verdadero para todos ellos —no hay ninguno— y `x` pertenece a `(∀R.C)ᴵ`. La
vacuidad no es una excepción del sistema: **es la definición**.

</details>

## Cuál es cuál: `ALC`, `SROIQ`, y los fragmentos (§3.2)

`ALC` —*Attributive Language with Concept negation*— es la base: conceptos, roles,
`⊓ ⊔ ¬`, `∀ ∃`, `⊤ ⊥`. Todo el caso de estudio de esta página cabe en `ALC`.

A partir de ahí se añaden letras: `I` inversas, `H` jerarquía de roles, `Q`
cardinalidades cualificadas, `O` nominales, `R` inclusiones complejas de roles y
`S` la abreviatura de `ALC` con roles transitivos. `SROIQ` es la suma de todas, y es
la lógica que hay debajo de OWL 2 DL.

En la otra dirección están los **fragmentos**, que quitan expresividad para ganar
tiempo de respuesta: `EL` (solo `⊓` y `∃`, razonamiento en tiempo polinómico) y
`DL-Lite` (pensada para consultar bases de datos, y la que reaparece en el capítulo
8). Son los que en el capítulo 4 se llamarán **perfiles** de OWL 2.

> Que existan varias lógicas descriptivas y no una sola es exactamente lo que dice
> Keet: *«the best balance between expressivity of the language and complexity of
> reasoning depends on the intended application»* (cap. 3, §3.1).

## Los cinco servicios estándar (§3.3.1)

| Servicio | Pregunta | Formalmente |
|---|---|---|
| **Consistencia** | ¿la KB se contradice a sí misma? | `KB ⊭ ⊤ ⊑ ⊥` |
| **Satisfacibilidad** de concepto | ¿puede `C` tener instancias? | `KB ⊭ C ⊑ ⊥` |
| **Subsunción** | ¿toda instancia de `C` lo es de `D`? | `KB ⊨ C ⊑ D` |
| **Instance checking** | ¿es `a` un `C`? | `KB ⊨ C(a)` |
| **Instance retrieval** | ¿quiénes son los `C`? | `{a \| KB ⊨ C(a)}` |

Los cinco se reducen a una única llamada —comprobar consistencia— por el método de
refutación del capítulo 2. La técnica concreta es el **tableau** (§3.3.2): se niega
lo que se quiere probar, se descompone según las conectivas ramificando en las
disyunciones, y si **todas** las ramas se cierran con una contradicción, lo original
se deduce.

---

# Caso de estudio: el ejercicio de los veganos, y lo que el ejercicio no dice

Reproducible con:

```bash
cd capitulos/03-logicas-descriptivas/artefactos
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
./.venv/bin/python verificar.py     # necesita Java en el PATH
```

La TBox es literalmente la del **Exercise 3.2** del libro:

```
Vegan      ≡ Person ⊓ ∀eats.Plant
Vegetarian ≡ Person ⊓ ∀eats.(Plant ⊔ Dairy)
```

El ejercicio pide demostrar a mano, con un tableau, si `T ⊢ Vegan ⊑ Vegetarian`.
Aquí se decide con HermiT y el método de refutación, que es lo que el tableau hace
por dentro.

## Lo que pide el ejercicio

```
[ok] T sola es consistente
[ok] T ∪ {¬(Vegan ⊑ Vegetarian)} INCONSISTENTE
[ok] T ∪ {¬(Vegetarian ⊑ Vegan)} CONSISTENTE
```

<p class="evidencia">T ⊨ Vegan ⊑ Vegetarian</p>

Sí se deduce, y la razón es puramente semántica: `∀eats.Plant` obliga a que todo lo
comido caiga en `Plant`, que está contenido en `Plant ⊔ Dairy`. Cuanto más grande es
el concepto del `∀`, más débil es la restricción — el `∀` es **antimonótono** en su
argumento. El recíproco no se sigue, y no hace falta intuición para saberlo: al
negarlo la teoría aguanta.

## Lo que el ejercicio no dice: el vegano que no come

Si la definición de vegano es «todo lo que come es vegetal», entonces alguien de
quien conste que **no come nada** la cumple. Y el razonador lo clasifica:

```
[ok] «nadia» (persona, y se afirma que no come nada) → se clasifica como Vegan
[ok] «perico» (persona, sin ningún dato sobre lo que come) → NO se clasifica
```

<p class="evidencia">KB ⊨ Vegan(nadia)</p>

Las dos comprobaciones juntas son el punto entero:

1. **El `∀` se satisface vacuamente.** No es un fallo del razonador: es la fila
   `(∀R.C)ᴵ` de la tabla de semántica aplicada al caso en que no hay ningún `y`.
   Una definición escrita solo con `∀` deja entrar a todo lo que no hace nada.
   Lo que se quería decir casi siempre era `∃eats.Plant ⊓ ∀eats.Plant`: que coma, y
   que lo que coma sea vegetal.
2. **Y aun así, no basta con no decir nada.** A `perico` no se le clasifica, porque
   en mundo abierto que no conste qué come no significa que no coma. Para que
   `nadia` cuente hubo que **cerrar el mundo explícitamente** sobre ella:
   `¬∃eats.⊤`.

Es la misma pareja de errores en direcciones opuestas: el `∀` es más permisivo de lo
que se cree, y el silencio de la ontología es más débil de lo que se cree.

## Definida frente a primitiva, medido

Ahora el mismo texto en lenguaje natural, pero con las dos clases declaradas como
**primitivas** (`⊑`, condiciones solo necesarias) en vez de **definidas** (`≡`,
necesarias y suficientes):

```
[ok] con Vegan primitiva, «nadia» ya NO se clasifica como Vegan
[ok] con ambas primitivas, T ∪ {¬(Vegan ⊑ Vegetarian)} vuelve a ser CONSISTENTE
```

<p class="evidencia hipotesis">con clases primitivas: T ⊭ Vegan ⊑ Vegetarian</p>

La segunda línea es el hallazgo del capítulo, y no era la previsión de partida —la
primera versión de `verificar.py` afirmaba que la subsunción sobrevivía, y HermiT la
tumbó. Tiene razón: para deducir que un vegano es vegetariano hace falta la
condición **suficiente** de `Vegetarian`, y una clase primitiva no la tiene. Sin
ella, nada obliga a que nadie entre en `Vegetarian`.

<details class="errata">
<summary>Lo que se dio por supuesto y era falso</summary>

Suposición de partida: *«degradar a primitiva solo hace que se clasifiquen menos
individuos; las relaciones entre clases se mantienen»*.

Es falso, y por una razón que se ve mejor al revés: **`⊑` no es media `≡`**. Una
clase primitiva no dice nada sobre quién pertenece a ella, solo sobre qué cumplen
los que ya pertenecen. Toda inferencia que necesite meter algo *dentro* de una clase
—clasificar un individuo, o probar una subsunción cuyo lado derecho es esa clase—
desaparece al degradarla.

La regla práctica que queda: si en algún momento se espera que el razonador
**meta** algo en una clase, esa clase tiene que ser definida. Si solo se espera que
saque consecuencias de estar dentro, basta con primitiva.

</details>

## Satisfacibilidad de un concepto

```
[ok] Vegan ⊓ ∃eats.Dairy INSATISFACIBLE      (con Plant ⊓ Dairy ⊑ ⊥)
[ok] Vegan ⊓ ∃eats.Dairy SATISFACIBLE        (sin declarar la disyunción)
```

Sin el axioma de disyunción, nada impide un modelo donde un mismo objeto sea planta
y lácteo a la vez. La disyunción entre hermanos **no es gratis y no es automática**;
es lo que convierte una taxonomía en una teoría con contenido.

## Qué deja el caso

1. **`∀R.C` es cierto por vacuidad.** Una definición hecha solo de universales admite
   a todo el que no participa en la relación.
2. **Y el mundo abierto lo tapa.** Esa vacuidad solo se activa cerrando el mundo
   explícitamente, así que el error se cuela silenciosamente en cuanto llegan datos
   completos.
3. **`≡` frente a `⊑` no es un matiz de estilo.** Cambia qué se deduce, incluido lo
   que no tiene nada que ver con clasificar individuos.
4. **La disyunción hay que escribirla.** Sin ella, conceptos que parecen
   incompatibles son perfectamente satisfacibles juntos.

---

## Los ejercicios (§3.4)

**Review question 3.1.** *«How are DLs typically different from full FOL?»* — Son
**fragmentos decidibles**: se renuncia a expresividad (predicados n-arios, variables
libres, cuantificación arbitraria) a cambio de que el razonamiento termine siempre.
Se limitan a predicados unarios y binarios y a un conjunto fijo de constructores.

**Review question 3.2.** *«What are the components of a DL knowledge base?»* —
**TBox** (terminología), **ABox** (hechos sobre individuos) y **RBox** (axiomas sobre
roles). La separación es convención: lógicamente son todos axiomas.

**Review question 3.3.** *«What are the concept and role constructors?»* — Para
`ALC`: de concepto, `¬C`, `C ⊓ D`, `C ⊔ D`, `∀R.C`, `∃R.C`, más `⊤` y `⊥`; de rol,
ninguno. `SROIQ` añade nominales `{a}`, cardinalidades cualificadas `≥n R.C`,
inversas `R⁻`, jerarquías y cadenas de roles, `Self` y roles disjuntos.

**Review question 3.4.** *«What distinguishes one DL from another?»* — El conjunto de
constructores que admite, y con él la clase de complejidad de sus servicios de
razonamiento. Todas comparten la semántica de teoría de modelos; lo que cambia es
qué se puede escribir y qué cuesta decidirlo.

**Review question 3.5.** *«Explain in your own words what the following reasoning
tasks involve.»*

| Tarea | Qué es | Por qué importa |
|---|---|---|
| **Instance checking** | ¿`KB ⊨ C(a)`? | es lo que puebla la ontología con datos: el `Vegan(nadia)` del caso |
| **Subsumption checking** | ¿`KB ⊨ C ⊑ D`? | construye la jerarquía inferida; es lo que detecta que la taxonomía escrita a mano no es la que se dedujo |
| **Concept satisfiability** | ¿`KB ⊭ C ⊑ ⊥`? | una clase insatisfacible es un error de modelado, no un resultado: casi siempre una disyunción que choca con una restricción |

**Exercise 3.1.** *«Consider again the natural language sentences from Exercise 2.6.
Formalise them into a suitable DL, where possible.»* — Las del capítulo 2 quedan:

```
Car ⊑ Vehicle
Human ⊓ Parent ⊑ ∃hasChild.Human
```

La tercera —«nadie es a la vez profesor y editor estudiante *del mismo curso*»— **no
se puede formalizar en una DL estándar**. Exige comparar dos roles sobre el mismo
par de individuos, y eso es una restricción de disyunción de roles con variables
compartidas que `ALC` no tiene. `SROIQ` sí admite roles disjuntos
(`Disjoint(lecturerOf, studentEditorOf)`), que es una aproximación **más fuerte**:
prohíbe la coincidencia en cualquier par, no solo la que interesaba. *Criterio
propio: el «where possible» del enunciado apunta justo a esto — que en lógica
descriptiva hay frases del capítulo 2 que sencillamente no caben.*

**Exercise 3.2.** *«Consider the following TBox… We want to know if
`T ⊢ Vegan ⊑ Vegetarian`.»* — Es el caso de estudio de esta página; ahí está
resuelto y verificado. En negación normal, la fórmula del enunciado queda:

```
Person ⊓ ∀eats.Plant ⊓ (¬Person ⊔ ∃eats.(¬Plant ⊓ ¬Dairy))
```

La rama con `¬Person` cierra contra `Person`. La otra rama genera un `y` con
`eats(a,y)`, `¬Plant(y)`, `¬Dairy(y)`; pero `∀eats.Plant` fuerza `Plant(y)`, y
choca con `¬Plant(y)`. **Todas las ramas cierran**, luego
`T ⊢ Vegan ⊑ Vegetarian`. Es el mismo resultado que devuelve HermiT.

**Exercise 3.3.** *«Download and install Protégé 5.x… load the AWO, click on Lion,
and inspect the DL axioms.»* — Ejercicio de herramienta. El artefacto de esta página
guarda `vegetarianos.owl` precisamente para poder abrirlo y ver la TBox del ejercicio
en notación DL en vez de en RDF/XML. *Criterio propio: leer los axiomas en notación
DL en Protégé es la forma más rápida de descubrir que una clase que se creía
definida está declarada como primitiva — se ve de un vistazo si el símbolo es `≡` o
`⊑`.*

---

## Lo que hay que llevarse

1. **OWL no tiene semántica propia: la toma de una DL.** Cualquier «rareza» del
   capítulo 4 tiene su explicación aquí.
2. **`∀R.C` no obliga a nada si no hay `R`.** Es el error de modelado más silencioso
   del capítulo, y solo aparece cuando llegan datos completos.
3. **Definida (`≡`) o primitiva (`⊑`) decide qué puede deducirse**, no cuánto se
   deduce.
4. **Elegir una DL es elegir una factura.** Expresividad y complejidad son la misma
   decisión mirada por sus dos caras; los perfiles de OWL 2 son esa decisión ya
   tomada por el W3C.

<small>Salvo los enunciados citados, el análisis y las resoluciones de esta página
son criterio propio, verificados con HermiT. Numeración y enunciados tomados del PDF
en <a href="https://github.com/inter097/ontology-engineering/tree/main/libro">/libro</a>,
no de ediciones web que renumeran las secciones.</small>

<details class="defensa">
<summary>Para la defensa — lo que te van a preguntar de aquí</summary>

**«¿Por qué usar una lógica descriptiva y no lógica de primer orden completa?»**

Por **decidibilidad**. Las DLs son fragmentos de FOL elegidos para que el
razonamiento termine siempre y con una complejidad conocida. En FOL completa la
implicación es semidecidible: un razonador puede no terminar nunca, y eso hace
inviable la herramienta. Se paga con expresividad, y el Exercise 3.1 de este
capítulo es un ejemplo concreto: hay frases del capítulo 2 que no se pueden escribir
en `ALC`.

**«¿Qué diferencia hay entre una clase definida y una primitiva, y cuándo usa cada
una?»**

Primitiva (`⊑`) da condiciones **necesarias**; definida (`≡`), necesarias y
**suficientes**. La regla que se sigue en este trabajo: si se espera que el
razonador **meta** algo en la clase —clasificar individuos, o probar una subsunción
que termine en ella— tiene que ser definida.

*Por qué es una respuesta fuerte:* está medido en el caso de estudio, no razonado en
abstracto. Al degradar `Vegan` y `Vegetarian` a primitivas, no solo dejó de
clasificarse el individuo: **se perdió la subsunción `Vegan ⊑ Vegetarian` que el
propio ejercicio 3.2 del libro pide demostrar**. La primera versión de la
verificación daba por supuesto lo contrario y el razonador la desmintió.

**«¿Por qué se clasifica como vegano alguien que no come nada?»**

Porque `∀eats.Plant` es verdadero por **vacuidad** cuando no hay ningún `eats`: es
la semántica de `(∀R.C)ᴵ = {x | ∀y. Rᴵ(x,y) → Cᴵ(y)}` con el antecedente siempre
falso (cap. 3, §3.1.3). No es un fallo del razonador sino la definición.

*Si insisten en que entonces la definición está mal:* lo está, y la corrección es
añadir el existencial — `Vegan ≡ Person ⊓ ∃eats.Plant ⊓ ∀eats.Plant`. Una definición
hecha solo de universales casi nunca dice lo que su autor cree.

**«Si el `∀` es vacuo, ¿por qué no se clasifican todas las personas sin datos?»**

Porque la hipótesis de **mundo abierto** impide concluir que alguien no come solo
porque no conste qué come. En el caso de estudio hay dos individuos justo para
enseñar esto: al que se le afirma explícitamente `¬∃eats.⊤` se le clasifica, y al que
simplemente no tiene datos, no. Es un buen recordatorio de que los dos errores
—vacuidad del `∀` y silencio de la ABox— tiran en direcciones opuestas y por eso se
tapan mutuamente hasta que llegan datos completos.

**«¿Cómo se elige la lógica descriptiva de un proyecto?»**

Por el equilibrio entre lo que hay que poder decir y lo que cuesta razonarlo — es el
criterio explícito de Keet en §3.1. En la práctica no se elige una DL en abstracto
sino un **perfil de OWL 2** (cap. 4), que ya es esa decisión tomada: `EL` para
ontologías grandes y poco expresivas, `QL` para consultas sobre datos, `RL` para
reglas. Todo el caso de estudio de esta página cabe en `ALC`, la más simple de la
familia; nada de lo que se necesitó exigió `SROIQ`.

</details>
