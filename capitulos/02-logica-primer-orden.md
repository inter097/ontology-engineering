---
titulo: 'First order logic: por qué el razonador no adivina'
capitulo: 2
descripcion: 'Sintaxis, semántica y las tres formas de inferir. El capítulo explica lo que quedó abierto en el 1: aquella inferencia sobre el impala no era un fallo del razonador, era una abducción disfrazada de deducción.'
keet: 'cap. 2 (First order logic and automated reasoning in a nutshell), §2.1–2.3'
hallazgo: 'Aquella inferencia sobre el impala nunca fue una deducción: es una abducción, y hay otra hipótesis más débil que explica lo mismo.'
cifras:
  - valor: '3'
    etiqueta: 'formas de inferir'
  - valor: '1'
    etiqueta: 'que hace el razonador'
  - valor: '8'
    etiqueta: 'comprobaciones'
---

El capítulo 2 es la maquinaria. No hay ontologías aquí: hay lógica de primer orden,
teoría de modelos y tres formas distintas de sacar conclusiones. Es corto y el libro
lo llama explícitamente *in a nutshell* — no pretende sustituir un curso de lógica.

> Si los símbolos (`∀`, `∃`, `⊑`, `⊨`) todavía no te dicen nada, están todos
> explicados uno a uno en el [capítulo 0](/capitulos/00-simbolos/).

Pero resuelve algo que quedó suelto en el capítulo 1. Allí el razonador se negó a
deducir que los impalas son herbívoros, y quedó como una rareza del mundo abierto.
No lo es. Es que **aquello nunca fue una deducción**.

## Sintaxis y semántica: la distinción que hay que tener clara

**Sintaxis** es qué cadenas de símbolos están bien formadas. **Semántica** es qué
significan. Son independientes: una fórmula puede ser sintácticamente impecable y
no decir nada de lo que creías.

Para darle significado a una frase hace falta describir **una situación concreta**
donde mirarla. El libro le llama *estructura*; puedes pensarlo como «un mundo
posible». Tiene tres partes, y ninguna es complicada:

- **las cosas que hay** en ese mundo;
- **las palabras** que te dejas usar;
- **a qué apunta cada palabra** — qué cosa es «la mesa», qué grupo de cosas son
  «sillas».

Un **modelo** de tu teoría es un mundo donde **todo** lo que escribiste sale
verdadero.

<details class="peras">
<summary>¿Y esto qué quiere decir? Sin jerga</summary>

Imagina que describes una habitación por teléfono a alguien que no la ve.

Le dices tres cosas: *«hay una mesa», «hay una silla», «la silla está junto a la
mesa»*.

Esa persona ahora se imagina la habitación. Pero no hay **una** habitación posible:
hay miles. Con la mesa de madera o de cristal. Con una silla o con cinco. Con una
ventana, o sin ella. **Todas encajan con lo que dijiste.**

Cada una de esas habitaciones imaginadas es lo que la lógica llama un **modelo**:
una manera concreta de que todo lo que dijiste sea verdad.

Las tres piezas raras de la tabla de arriba son solo las partes de esa habitación
imaginada:

- **el conjunto de cosas que hay** — la mesa, la silla, lo que sea que haya dentro;
- **las palabras que usas** — «mesa», «silla», «junto a»;
- **a qué apunta cada palabra** — cuál de las cosas es la mesa, cuáles parejas de
  cosas están «junto a» otra.

Y ya está. Una habitación imaginada = las cosas + qué nombre lleva cada una.

---

**Lo importante viene ahora.**

Le preguntas a esa persona: *«¿la silla es de madera?»*

Y te responde: **«no lo sé»**. No porque sea tonta, sino porque puede imaginarse una
habitación con silla de madera y otra con silla de plástico, y **las dos encajan con
lo que le contaste**.

Para que pueda contestarte que sí, tendría que ser de madera en **todas** las
habitaciones que puede imaginar. En todas, sin excepción.

Eso es lo único que quiere decir la frase «se sigue de la teoría»:

> es cierto en **todas** las situaciones que encajan con lo que escribiste, no solo
> en la que tú tenías en la cabeza.

---

**Y por eso el razonador te lleva la contraria.**

Tú describes tu ontología pensando en tu habitación. Él se imagina todas las
habitaciones posibles que encajan con tu descripción. Si encuentra **una sola** donde
tu conclusión falle, te dice que no se sigue.

Es exactamente lo que pasó con el impala en el capítulo 1. Tú te imaginabas el
mundo donde todos los impalas son herbívoros. El razonador se imaginó otro —con
impalas que ningún león se come, y que no son herbívoros— que también encajaba con
lo escrito. Con encontrar ese, ya no lo deduce.

**Cuando el razonador no deduce algo obvio, no está roto.** Te está diciendo: *«me
puedo imaginar una situación que cumple tus reglas y donde eso es falso»*. Y casi
siempre significa lo mismo — te faltó escribir una regla.

</details>

<details class="peras">
<summary>La versión formal, para cuando haga falta citarla</summary>

Las definiciones tal cual las da §2.1.2:

| Pieza | Definición |
|---|---|
| **Vocabulario** `V` | un conjunto de símbolos de función, relación y constante (Def. 2.5) |
| **`V`-estructura** `M` | un conjunto no vacío `Δ` más una interpretación de `V`: a cada constante le asigna un elemento de `Δ`; a cada relación de `n` huecos, un subconjunto de `Δⁿ` — o sea, qué grupos de `n` cosas cumplen esa relación (Def. 2.6) |
| **Modelo de `Γ`** | una `V`-estructura que modela cada sentencia de `Γ` (Def. 2.9) |
| **Teoría de `M`** | el conjunto de todas las `V`-sentencias verdaderas en `M` (Def. 2.8) |
| **Teoría completa** | para toda sentencia, contiene esa sentencia o su negación, pero no ambas (Def. 2.10) |

`M ⊨ φ` se lee «`M` es un modelo de `φ`»: la sentencia `φ` es verdadera en esa
estructura.

</details>

Y de aquí sale la noción que de verdad usas todos los días:

> `T ⊨ α` — la teoría `T` **implica** `α` — significa que **en todos los modelos de
> `T`, `α` es verdadera**. No en el que tú tenías en la cabeza: en todos.

Ahí está el nudo de casi todo. Cuando dices «pero es evidente que el impala es
herbívoro», estás pensando en *tu* modelo. El razonador comprueba **todos**, y le
basta encontrar uno donde no lo sea para no deducirlo.

## Las tres formas de inferir (§2.2.3)

| | Qué hace | ¿Conserva la verdad? |
|---|---|---|
| **Deducción** | `T ⊨ α`: `α` ya estaba implícita en `T` | **sí** |
| **Abducción** | busca `a` como *explicación* de una observación `b` | no — es una hipótesis |
| **Inducción** | generaliza desde individuos a una regla | no — puede ser falsa con premisas verdaderas |

De la deducción, Keet dice algo que conviene no olvidar: *«strictly speaking, a
deduction does not reveal novel knowledge»*. Solo saca a la luz lo que ya estaba.
Que a un experto del dominio le parezca nuevo es un problema de tamaño de la
teoría, no de creatividad del razonador.

**Los razonadores de ontologías hacen deducción. Solo deducción.** La abducción
está mucho menos automatizada (se usa, por ejemplo, en detección de fallos: dado el
sistema y el estado defectuoso, encontrar la avería probable). La inducción es lo
que hace el aprendizaje automático, y por eso da respuestas de otro tipo.

## Cómo se demuestra `T ⊨ α`

Dos caminos, y el segundo es el que usan las herramientas:

1. **Deducción natural** — construir la prueba hacia adelante desde las premisas.
2. **Refutación** — suponer lo contrario y buscar la contradicción:

> `T ⊨ α` **si y solo si** `T ∪ {¬α}` es **inconsistente**.

Sobre esto se montan resolución, métodos de conexión y **tableaux**. Es también,
literalmente, la única llamada que ofrece un razonador OWL: preguntarle si algo es
consistente. Todo lo demás —clasificación, satisfacibilidad, comprobar una
implicación— se reduce a eso.

Y tiene un corolario práctico que vale oro: **puedes preguntarle a tu razonador si
algo NO se sigue.** Si añades la negación y la ontología sigue siendo consistente,
tienes la prueba de que tu teoría no dice lo que creías.

---

# Caso de estudio: el impala no era un fallo, era una abducción

Reproducible con:

```bash
cd capitulos/02-logica-primer-orden/artefactos
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
./.venv/bin/python verificar.py     # necesita Java en el PATH
```

Todas las preguntas se deciden con el método de refutación de §2.2.3: se añade `¬α`
y se mira si la teoría revienta.

## Primero, calibrar: una deducción de verdad

El ejemplo del propio libro. `T` = «cada arácnido tiene exactamente 8 patas» +
«cada tarántula es un arácnido». `α` = «cada tarántula tiene exactamente 8 patas».

```
[ok] T por sí sola es consistente
[ok] T ∪ {¬α} es inconsistente, luego T |= α
```

Funciona. Y no ha aparecido conocimiento nuevo: las patas de la tarántula ya
estaban en `T`, solo que nadie las había escrito.

## Ahora, el impala

En la ontología del libro está declarado:

```
lion ⊑ ∀eats.herbivore ⊓ ∃eats.Impala
```

Se prueban dos afirmaciones por refutación:

```
[ok] T ∪ {¬α} INCONSISTENTE  con α = lion ⊑ ∃eats.(Impala ⊓ herbivore)
[ok] T ∪ {¬α} CONSISTENTE    con α = Impala ⊑ herbivore
```

<p class="evidencia">T ⊨ lion ⊑ ∃eats.(Impala ⊓ herbivore)</p>

<p class="evidencia hipotesis">T ⊭ Impala ⊑ herbivore — abducción, no deducción</p>

La primera **sí** se deduce. La segunda **no**, y ahora hay una prueba formal, no
una observación de que «el razonador no lo sacó».

La diferencia es exactamente dónde cae el cuantificador. De `∀eats.herbivore` y
`∃eats.Impala` se sigue que **el impala concreto que ese león se come** es un
herbívoro. La clase `Impala` entera no entra en el argumento: nada impide un modelo
con impalas que ningún león toca y que no son herbívoros. Como `T ⊨ α` exige que
`α` valga en **todos** los modelos, basta ese para que no se deduzca.

## Entonces, ¿qué era?

Una **abducción**: `Impala ⊑ herbivore` no es una consecuencia de `T`, es una
*explicación* candidata de lo que observas.

```
[ok] H  = «Impala ⊑ herbivore»          → T ∪ {H} consistente: explicación admisible
[ok] H' = «algún impala es herbívoro»   → T ∪ {H'} consistente: también lo explica
```

Y aquí está lo que hace peligrosa a la abducción: **no da una respuesta única**.
`H'` es estrictamente más débil que `H` y explica lo mismo. Elegir `H` porque «suena
bien» es meter en la ontología un compromiso mucho más fuerte del que los datos
justifican — y en biología es además falso, porque hay impalas que ningún león se
come.

Un razonador no elige por ti. Ni siquiera te avisa de que estás eligiendo.

## Y la inducción, de paso

```
[ok] de «tibbles es un gato con cola» NO se sigue «todos los gatos tienen cola»
[ok] al afirmarlo, un solo gato sin cola (un manx) vuelve la teoría inconsistente
```

El salto inductivo es lo que casi todo el mundo hace al modelar: mira cinco
ejemplos, escribe la regla universal. Funciona hasta que aparece el manx. La
diferencia con el machine learning es que allí la regla es probabilística y aquí es
un axioma duro: un contraejemplo no baja la precisión, **destruye la ontología
entera**.

## Qué deja el caso

1. **`T ⊨ α` es cuantificación sobre modelos, no sobre tu intuición.** Un solo
   modelo donde `α` falle basta para que no se deduzca.
2. **El razonador solo deduce.** Cuando esperas una inferencia y no llega, la
   pregunta no es «¿qué le pasa al razonador?» sino «¿esto es realmente una
   deducción, o estoy abduciendo?».
3. **Puedes probar la ausencia.** Añade `¬α`; si sigue consistente, tu teoría no
   dice lo que creías. Es la herramienta de diagnóstico más barata que existe y casi
   nadie la usa.
4. **Cuidado al convertir una abducción en axioma.** Suele haber una hipótesis más
   débil que explica lo mismo, y esa es casi siempre la correcta.

---

## Los ejercicios (§2.3)

**Review question 2.1.** *«What is the difference between syntax and semantics for
a logic?»* — La sintaxis dice qué cadenas están bien formadas; la semántica, qué
significan, vía estructuras que asignan un dominio `Δ` e interpretan cada símbolo.
Una fórmula puede ser sintácticamente correcta y semánticamente decir algo distinto
de lo que pretendías: el capítulo 1 entero fue un ejemplo de eso.

**Review question 2.2.** *«What is a theory?»* — Un conjunto de sentencias. Dado un
`M`, la teoría de `M` es el conjunto de todas las `V`-sentencias verdaderas en `M`
(Def. 2.8). Una teoría es **completa** si para toda sentencia `φ` contiene `φ` o
`¬φ`, pero no ambas (Def. 2.10).

**Review question 2.3.** *«Name the four core components for automated
reasoning.»* — El lenguaje lógico (sintaxis), su semántica, un cálculo con reglas de
deducción, y un algoritmo que lo implemente. *Criterio propio: lo que hay que
retener es que las dos propiedades que se le exigen a esa combinación son ser
**correcta** (lo que deduce es verdadero) y **completa** (deduce todo lo verdadero);
sin ambas, el silencio del razonador no significa nada.*

**Review question 2.4.** *«Describe the procedure for tableau reasoning in four
short sentences.»* — Se niega lo que se quiere probar y se añade a la teoría. Se
descompone cada fórmula según su conectiva, ramificando en las disyunciones. Una
rama se cierra cuando contiene una fórmula y su negación. Si **todas** las ramas
cierran, la teoría con la negación es insatisfacible, luego lo original se deduce.

**Exercise 2.1.** *«Write in one natural language sentence what the following
sentences in First-Order Logic state.»*

| Fórmula | En español |
|---|---|
| `∀x(Lion(x) → Mammal(x))` | Todo león es un mamífero. |
| `∀x(PC(x) → ∃y,z(hasPart(x,y) ∧ connected(x,z) ∧ CPU(y) ∧ Monitor(z)))` | Todo PC tiene como parte alguna CPU y está conectado a algún monitor. |
| `∀x,y(hasProperPart(x,y) → ¬hasProperPart(y,x))` | Si algo es parte propia de otra cosa, esa otra no es parte propia de la primera: la parte propia es **asimétrica**. |

La tercera merece un apunte: asimetría no es lo mismo que irreflexividad, aunque en
mereología vayan juntas. La asimetría prohíbe el ciclo de longitud 2; la
irreflexividad prohíbe el de longitud 1. En OWL 2 son dos declaraciones distintas.

**Exercise 2.2.** *«Formalise the following natural language sentence into
First-Order Logic.»*

```
a.  ∀x(Car(x) → Vehicle(x))

b.  ∀x((Human(x) ∧ Parent(x)) → ∃y(hasChild(x,y) ∧ Human(y)))

c.  ¬∃x,y(Person(x) ∧ Course(y) ∧ lecturerOf(x,y) ∧ studentEditorOf(x,y))
    equivalente:  ∀x,y((lecturerOf(x,y) ∧ Person(x) ∧ Course(y)) → ¬studentEditorOf(x,y))
```

En (c) el «del mismo curso» es lo que obliga a que `y` sea la misma variable en
ambas relaciones. Escribirlo como dos restricciones sueltas —«no es profesor» y «no
es editor estudiante»— sería una formalización distinta y más fuerte, que prohíbe
las dos cosas incluso en cursos diferentes. *Criterio propio: este es el error de
formalización más común del ejercicio, y es la misma clase de error de alcance que
rompió la ontología del capítulo 1.*

**Exercise 2.3.** *«Consider the structures in Figure 2.6, which are graphs.»* — El
ejercicio depende de una figura del libro; lo relevante para lo que viene después es
el apartado (a): dos dibujos distintos pueden tener exactamente la misma descripción
en vértices y aristas. Es la misma idea de §1.1 — **el dibujo no es la teoría**. La
estructura es lo que la interpretación fija, no lo que se ve en el papel.

---

## Lo que hay que llevarse

1. **`T ⊨ α` cuantifica sobre todos los modelos.** Tu intuición es un modelo entre
   muchos.
2. **Los razonadores deducen y nada más.** Abducción e inducción se parecen a
   razonar, pero no conservan la verdad.
3. **`T ⊨ α` sii `T ∪ {¬α}` inconsistente.** Sirve tanto para probar como para
   **refutar**, y refutar es lo que casi nunca se hace.
4. Una deducción **no aporta nada nuevo**. Si esperabas que el razonador
   «descubriera» algo, lo que buscabas era abducción o inducción, y ninguna de las
   dos vive en un razonador OWL.

<small>Salvo los enunciados citados, el análisis y las resoluciones de esta página
son criterio propio, verificados con HermiT. Numeración y enunciados tomados del PDF
en <a href="https://github.com/inter097/ontology-engineering/tree/main/libro">/libro</a>,
no de ediciones web que renumeran las secciones.</small>

<details class="defensa">
<summary>Para la defensa — lo que te van a preguntar de aquí</summary>

**«¿Qué significa exactamente `T ⊨ α`?»**

Que en **todos** los modelos de `T`, `α` es verdadera. Es una cuantificación sobre
modelos, no una afirmación sobre el modelo que uno tiene en mente. La consecuencia
práctica es que basta **un solo** modelo donde `α` falle para que no se siga — y ese
modelo puede ser uno que el modelador nunca consideró.

**«¿Qué diferencia hay entre deducción, abducción e inducción? ¿Cuál hace un
razonador OWL?»**

Solo **deducción**, y solo esa. La deducción conserva la verdad: si las premisas son
verdaderas, la conclusión lo es. La abducción propone una hipótesis que *explicaría*
una observación, y la inducción generaliza desde individuos; ninguna de las dos
conserva la verdad, y por tanto ninguna está en un razonador de ontologías.

*El matiz que conviene añadir:* una deducción, estrictamente, no aporta conocimiento
nuevo — solo hace explícito lo que ya estaba. Que a un experto le parezca un
descubrimiento es una cuestión del tamaño de la teoría, no de creatividad del
sistema.

**«¿Cómo demuestras que algo NO se sigue de tu ontología?»**

Por **refutación**, que es el método del propio capítulo: `T ⊨ α` si y solo si
`T ∪ {¬α}` es inconsistente. Luego para probar que `α` **no** se sigue, se añade
`¬α` y se comprueba que la ontología sigue siendo consistente. Es una prueba, no la
ausencia de un resultado.

*Por qué es una respuesta fuerte:* casi todo el mundo mira solo qué salió
clasificado, y de ahí no se puede concluir nada — el silencio de un razonador no es
evidencia sin esta comprobación. En este trabajo se usa para demostrar que
`Impala ⊑ herbivore` no es una consecuencia de la ontología del libro, sino una
abducción.

**«¿Por qué te fías del razonador?»**

Por dos propiedades que hay que nombrar juntas: **corrección** (todo lo que deduce
es verdadero en la teoría) y **completitud** (deduce todo lo que es verdadero en
ella). Sin corrección, lo que afirma no vale; sin completitud, **su silencio no
significa nada** — podría haber una consecuencia que simplemente no encuentra.

*Aquí es donde conectar con los perfiles de OWL 2:* un razonador puede ser completo
para un fragmento del lenguaje e incompleto si la ontología usa construcciones fuera
de él. Por eso importa saber en qué perfil está una ontología antes de interpretar
lo que el razonador no dijo.

**«Si tu ontología es consistente pero no deduce lo que esperabas, ¿qué haces?»**

Primero comprobar por refutación si realmente es una deducción o estaba abduciendo.
Si no se sigue, la pregunta correcta no es «¿qué le pasa al razonador?» sino «¿qué
axioma me falta?». Y al añadirlo, vigilar no meter una hipótesis más fuerte de lo
que los datos justifican: casi siempre existe una versión más débil que explica lo
mismo.

</details>
