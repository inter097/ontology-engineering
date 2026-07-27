---
titulo: 'Capítulo 0: los símbolos, antes de empezar'
capitulo: 0
descripcion: 'Por qué hay dos juegos de símbolos distintos, cómo se lee cada uno en voz alta, y las cuatro ideas que hay que tener claras antes del capítulo 1. Página propia, no del libro.'
keet: 'ninguno — página propia, con enlaces a §2.1 y §3.1 donde el libro lo formaliza'
hallazgo: 'Dos notaciones para lo mismo: la descriptiva es primer orden recortado para que el razonamiento siempre termine.'
cifras:
  - valor: '2'
    etiqueta: 'juegos de símbolos'
  - valor: '4'
    etiqueta: 'ideas base'
  - valor: '0'
    etiqueta: 'capítulos del libro'
---

Esta página no es del libro. Está aquí porque el libro da por sabidas cosas que
conviene tener a mano, y porque hay una pregunta que confunde a todo el mundo la
primera vez:

> **¿Por qué hay dos juegos de símbolos distintos?**

Al principio salen `∀`, `∃`, `→`, `∧`. Más tarde salen `⊑`, `⊓`, `∃come.Planta`.
Parecen dos lenguajes rivales. No lo son.

## La respuesta: son el mismo idioma, uno abreviado

El primero es **lógica de primer orden** (FOL). Es el lenguaje general de las
matemáticas: sirve para hablar de cualquier cosa.

El segundo es **lógica descriptiva** (DL). Es un **subconjunto** de la lógica de
primer orden, recortado a propósito, con una notación más corta.

Mismo significado, distinta forma de escribirlo:

| En lógica de primer orden | En lógica descriptiva |
|---|---|
| `∀x(León(x) → Animal(x))` | `León ⊑ Animal` |
| `∀x(León(x) → ∃y(come(x,y) ∧ Carne(y)))` | `León ⊑ ∃come.Carne` |
| `∀x(León(x) → ∀y(come(x,y) → Carne(y)))` | `León ⊑ ∀come.Carne` |

Fíjate en la tercera fila: la versión larga necesita dos `∀`, una `→` anidada y
tres apariciones de variables. La corta cabe en once caracteres.

### ¿Y por qué molestarse en recortar el lenguaje?

Porque la lógica de primer orden completa es **indecidible**: existen preguntas para
las que ningún programa puede garantizar una respuesta. Puede quedarse pensando para
siempre y no hay forma de saber si va a terminar.

Las lógicas descriptivas se diseñaron eligiendo qué dejar fuera para que **siempre
termine**. Ese es todo el truco, y es la razón de que exista OWL: OWL 2 DL *es* una
lógica descriptiva concreta con ropa de estándar web.

> **La regla mental:** lógica de primer orden = todo lo expresable. Lógica
> descriptiva = lo que además se puede calcular en tiempo finito. Se paga
> expresividad a cambio de que el razonador conteste.

El capítulo 2 desarrolla la primera. El capítulo 3, la segunda. Esta página es solo
para que los símbolos no estorben mientras tanto.

---

## Los símbolos, uno a uno

### Los de lógica de primer orden

| Símbolo | Se lee | Ejemplo |
|---|---|---|
| `∀x` | «todo x» | `∀x(León(x) → Animal(x))` — todo león es un animal |
| `∃x` | «existe algún x» | `∃x(León(x))` — hay al menos un león |
| `→` | «si… entonces» | `León(x) → Animal(x)` |
| `∧` | «y» | `León(x) ∧ Hambriento(x)` |
| `∨` | «o» (vale que sean las dos) | `León(x) ∨ Tigre(x)` |
| `¬` | «no» | `¬León(x)` |
| `⊨` | «se sigue de» | `T ⊨ α` — de mis reglas se sigue α |

El paréntesis con variable —`León(x)`— se lee «x es un león». Y `come(x,y)` se lee
«x come y». Nada más: **una palabra con un hueco es una propiedad, con dos huecos es
una relación**.

### Los de lógica descriptiva (los de OWL)

| Símbolo | Se lee | Ejemplo |
|---|---|---|
| `⊑` | «es un tipo de» | `León ⊑ Animal` |
| `≡` | «es exactamente» | define una clase, no solo la describe |
| `⊓` | «y a la vez» | `León ⊓ Hambriento` — leones que además tienen hambre |
| `⊔` | «o» | `León ⊔ Tigre` |
| `¬` | «no» | `¬León` — todo lo que no es un león |
| `⊤` | «cualquier cosa» | |
| `⊥` | «imposible, no existe» | `A ⊓ B ⊑ ⊥` — nada puede ser A y B a la vez |
| `∃come.Carne` | «come carne» | |
| `∀come.Carne` | «no come otra cosa que carne» | |

Aquí las clases van sin hueco: se escribe `León`, no `León(x)`. La variable está
implícita — es una de las cosas que se ahorra la notación corta.

---

## Las cuatro ideas que hay que tener claras

Si te quedas solo con esto, ya puedes leer el resto.

### 1. `∃` promete; `∀` prohíbe

La confusión número uno, y la que rompe ontologías de verdad.

Piensa en un amigo vegetariano:

- **«come verdura»** — promete que hay verdura de por medio. Si lleva tres días sin
  probar bocado, es **falso**. Esto es `∃`.
- **«no come otra cosa que verdura»** — no dice que coma. Dice qué **no** hace. Esto
  es `∀`.

Y ahora el detalle incómodo: si lleva tres días **sin comer nada**, sigue siendo
verdad que «no come otra cosa que verdura». Y también que «no come otra cosa que
carne». Y que «no come otra cosa que piedras». **Las tres a la vez**, porque no hay
ni un solo contraejemplo que puedas señalar.

Se le llama cumplirse **de forma vacía**, y el razonador lo aplica sin piedad.

| Lo que quieres decir | Hace falta |
|---|---|
| «come verdura» | `∃` |
| «no come otra cosa» | `∀` |
| «come verdura, y nada más» | **los dos juntos** |

La tercera fila es la que casi nadie escribe. Y es casi siempre la que hacía falta.
En el [capítulo 1](/capitulos/01-introduccion/) esto tumba la ontología de ejemplo
del propio libro.

### 2. «Se sigue» significa «en todas las situaciones posibles»

Describes una habitación por teléfono: *«hay una mesa, hay una silla, la silla está
junto a la mesa»*. Quien te escucha se imagina la habitación — pero no una,
**miles**. Con mesa de madera o de cristal. Con una silla o con cinco.

Le preguntas: *«¿la silla es de madera?»* Y te dice **«no lo sé»**. Puede imaginarse
las dos versiones, y las dos encajan con lo que le contaste.

Para que te conteste que sí, tendría que ser de madera en **todas** las habitaciones
que puede imaginar.

> Eso es lo único que significa `T ⊨ α`: es cierto en **todas** las situaciones que
> encajan con lo que escribiste. No solo en la que tú tenías en la cabeza.

Por eso el razonador te lleva la contraria tanto. Y cuando no deduce algo «obvio»,
no está roto: te está diciendo *«me puedo imaginar una situación que cumple tus
reglas y donde eso es falso»*. Casi siempre significa que te faltó escribir una
regla.

### 3. Lo que no está escrito no es falso; es desconocido

En una base de datos, si no hay fila, no existe. Es **mundo cerrado**.

En una ontología es al revés: lo que no está escrito simplemente **no se sabe**.
Puede ser cierto y nadie lo anotó. Es **mundo abierto**, y es el supuesto por
defecto.

Consecuencia directa, que sorprende a todo el que viene de programar: **en OWL nada
valida datos**. No puede haber un dato «incorrecto», solo desconocido. Las
construcciones que parecen validaciones —`domain`, `range`— en realidad **infieren
tipos en silencio**.

### 4. Definir no es lo mismo que describir

| | Símbolo | Qué hace |
|---|---|---|
| **Clase primitiva** | `⊑` | describe: *todo león es un animal*, pero ser animal no te hace león |
| **Clase definida** | `≡` | define: *ser exactamente esto* — y entonces cualquier cosa que cumpla la condición **entra en la clase automáticamente** |

La diferencia importa mucho más de lo que parece. Con `⊑` el razonador comprueba;
con `≡` el razonador **clasifica**: mete cosas dentro de la clase sin que se lo
pidas.

Ahí es donde el error del `∀` vacío pasa de curiosidad a catástrofe. Si defines
`Herbívoro ≡ ∀come.Planta` y algo no come nada, ese algo **es** un herbívoro por
definición. Y también un carnívoro. Y si has declarado que no pueden coincidir, la
ontología entera se cae.

---

## Cómo leer un axioma entero

Con lo anterior ya se lee la línea que atraviesa todo el libro:

```
lion ⊑ ∀eats.herbivore ⊓ ∃eats.Impala
```

De izquierda a derecha:

| Trozo | Qué dice |
|---|---|
| `lion ⊑` | todo león es… |
| `∀eats.herbivore` | …algo que no come nada que no sea herbívoro… |
| `⊓` | …y a la vez… |
| `∃eats.Impala` | …algo que sí se come algún impala |

En español corriente: **«los leones comen solo herbívoros, y comen algún impala»**.

Y ahora la pregunta con la que arranca el capítulo 1: si el león solo come
herbívoros y se come algún impala, ¿son herbívoros los impalas?

Parece que sí. **No se deduce**, y el porqué está en el
[capítulo 2](/capitulos/02-logica-primer-orden/).

---

## Lo mínimo de vocabulario

Tres palabras que se usan sin avisar a partir del capítulo 3:

| Palabra | Qué es |
|---|---|
| **TBox** | las reglas generales: «todo león es un animal». La `T` es de *terminología* |
| **ABox** | los datos concretos: «Simba es un león». La `A` es de *aserción* |
| **Razonador** | el programa que saca conclusiones de las dos. HermiT, ELK y Pellet son razonadores |

Y dos que suenan parecido y no lo son:

- **Inconsistente** — tu ontología se contradice. Avería total: a partir de ahí se
  deduce cualquier cosa y ninguna respuesta vale.
- **Clase insatisfacible** — una clase concreta no puede tener miembros nunca. Es
  malo, pero es local: el resto sigue funcionando.

---

<small>Página propia, no del libro. Está aquí porque Keet formaliza esto en §2.1
(primer orden) y §3.1 (lógicas descriptivas), y viene bien tenerlo resumido antes.
Cualquier error de esta página es mío, no suyo.</small>

<details class="defensa">
<summary>Para la defensa — lo que te van a preguntar de aquí</summary>

**«¿Por qué usas lógica descriptiva y no lógica de primer orden, que es más
expresiva?»**

Por **decidibilidad**. La lógica de primer orden completa es indecidible: existen
preguntas para las que ningún algoritmo puede garantizar una respuesta en tiempo
finito. Las lógicas descriptivas son fragmentos elegidos precisamente para que todo
razonamiento termine siempre. Se renuncia a expresividad a cambio de que la
herramienta conteste — y sin esa garantía no hay razonador utilizable, luego no hay
ontología operativa.

*Si insisten:* el compromiso no es binario. Los perfiles de OWL 2 (EL, QL, RL)
recortan aún más para bajar de exponencial a polinómico, cada uno optimizado para un
caso de uso. Se elige el fragmento por el problema, no al revés.

**«¿Qué diferencia hay entre `∃R.C` y `∀R.C`?»**

`∃R.C` es una **condición de existencia**: obliga a que haya al menos un individuo
relacionado por `R` que sea del tipo `C`. `∀R.C` es una **restricción de tipo sobre
lo que haya**: no obliga a que exista nada, solo prohíbe que lo que exista sea de
otro tipo. Por eso `∀R.C` se satisface **de forma vacía** para cualquier individuo
sin relaciones `R`.

*La consecuencia que conviene mencionar tú antes de que te la saquen:* dentro de una
clase **definida** (`≡`), esa satisfacción vacía arrastra a la clase a todo
individuo sin esa relación. Es un error real y documentado; está el caso del
capítulo 1.

**«¿Qué implica el supuesto de mundo abierto para la validación de datos?»**

Que no hay validación. Bajo mundo abierto la ausencia de un dato no es una
violación, es desconocimiento, así que ninguna construcción del lenguaje puede
rechazar una instancia. `rdfs:domain` y `rdfs:range` no son restricciones de
integridad: son **axiomas de los que se infieren tipos**. Confundirlos con las
restricciones de un esquema relacional es el error de traslación más común entre
quien viene de bases de datos.

*Si quieren cerrar el mundo:* eso es otra cosa —SHACL, ShEx, o razonamiento con
supuesto de nombres únicos y mundo cerrado— y hay que decir explícitamente que se
sale de OWL.

**«¿Cuándo usas una clase primitiva y cuándo una definida?»**

Primitiva (`⊑`) cuando las condiciones son **necesarias pero no suficientes**: todo
león es un animal, pero ser animal no basta para ser león. Definida (`≡`) cuando son
**necesarias y suficientes**, y entonces el razonador clasifica automáticamente
dentro de esa clase todo lo que las cumpla.

La regla práctica: si no vas a querer que el razonador meta cosas ahí solo, no la
definas. Las clases definidas son potentes y son también donde se concentran los
errores, porque su efecto es automático y silencioso.

</details>
