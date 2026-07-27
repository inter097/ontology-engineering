---
titulo: 'Caso de estudio: la brizna de hierba que rompe la ontología del libro'
capitulo: 1
seccion: caso-de-estudio
descripcion: 'Un error semántico real en la ontología de ejemplo de Keet. El razonador dice que todo está bien, y basta un individuo perfectamente razonable para volverla inconsistente. Todo comprobable ejecutando un script.'
keet: cap. 1, §1.2–1.3 · AfricanWildlifeOntology1.owl
---

El capítulo 1 termina con una afirmación fácil de leer y difícil de creer: que los
**errores semánticos** —formalizar impecablemente algo distinto de lo que se quería
decir— no los detecta ninguna herramienta. Este caso de estudio la pone a prueba
contra la propia ontología de ejemplo del libro.

Todo lo que sigue se reproduce con:

```bash
cd capitulos/01-introduccion/artefactos
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
./.venv/bin/python verificar.py     # necesita Java en el PATH
```

El script razona con **HermiT** a través de owlready2 y falla con código 1 si
alguna afirmación de esta página deja de cumplirse.

## El punto de partida: todo verde

`AfricanWildlifeOntology1.owl` tiene 31 clases, 5 propiedades de objeto y cero
individuos. Solo tres clases están **definidas** (condiciones necesarias y
suficientes, `owl:equivalentClass`): `herbivore`, `carnivore` y `Omnivore`.

Se ejecuta el razonador y el resultado es el que cualquiera firmaría:

```
[ok] la ontología es consistente
[ok] no hay clases insatisfacibles
[ok] giraffe se clasifica como herbivore
[ok] lion se clasifica como carnivore
```

Clasificación no trivial, cero errores. En un proyecto de software esto sería
verde en CI y se mergearía.

## La primera grieta: lo que *no* se infiere

Está declarado que el león come **solo** herbívoros, y que come **algún** impala:

```
lion ⊑ ∀eats.herbivore ⊓ ∃eats.Impala
```

De ahí se sigue, en lenguaje natural, que los impalas son herbívoros. El razonador
no lo infiere:

```
[ok] Impala NO se clasifica como herbivore
```

Y hace bien. `∀eats.herbivore ⊓ ∃eats.Impala` implica que *el impala concreto que
se come ese león concreto* es un herbívoro — formalmente,
`lion ⊑ ∃eats.(Impala ⊓ herbivore)`. No dice nada sobre la clase `Impala` entera.
Puede haber impalas que ningún león se coma y que no sean herbívoros.

Esto no es un fallo: es OWA funcionando. Pero es la primera señal de que la
intuición del modelador y lo que el archivo dice no son lo mismo.

## El defecto

Las dos definiciones centrales del archivo:

```
herbivore ≡ ∀eats.plant   ⊔  ∀eats.(∃is-part-of.plant)
carnivore ≡ ∀eats.animal  ⊔  ∀eats.(∃is-part-of.animal)
```

más un axioma que parece inofensivo:

```
carnivore ⊓ herbivore ⊑ ⊥
```

**El `⊔` está fuera del alcance del `∀`.** Se quería decir «come solo plantas o
partes de plantas»; lo que dice es «(come solo plantas) o (come solo partes de
plantas)». Un animal que coma una planta entera *y* una hoja no cumple ninguno de
los dos disyuntos y no es herbívoro. La formalización correcta sería
`∀eats.(plant ⊔ ∃is-part-of.plant)`.

Pero la consecuencia grave es otra. **`∀eats.plant` se satisface de forma vacía**
para cualquier cosa que no coma nada. Como la definición es una *equivalencia*, la
implicación va en los dos sentidos: cualquier entidad que no coma **es**, por
definición, un herbívoro. Y por el mismo argumento, un carnívoro. Y esas dos
clases son disjuntas.

## La prueba

La ontología, tal como viene, es consistente — porque bajo mundo abierto el
razonador nunca puede asumir que algo no come; siempre puede inventar un alimento.
La contradicción solo aparece cuando se le cierra esa puerta.

Se añade entonces un individuo que ningún biólogo discutiría: una brizna de hierba
que no come nada.

```python
brizna = Grass("brizna_de_hierba_1")
brizna.is_a.append(eats.exactly(0, Thing))   # una brizna no come
```

```
[ok] afirmar que una brizna de hierba no come vuelve INCONSISTENTE la ontología
```

Toda la ontología. No una clase insatisfacible: **inconsistente**, que es la avería
total — a partir de ahí el razonador deriva cualquier cosa y ninguna respuesta
sirve.

Merece la pena ver el tamaño del desastre frente al tamaño de la causa. La causa
es un paréntesis mal puesto en dos líneas. La ontología pasó el razonador. Habría
pasado cualquier suite de tests que solo comprobara consistencia. Y el desastre lo
dispara el primer dato real que alguien intente cargar.

## La corrección, y su precio

El arreglo es meter el `⊔` dentro del `∀` y añadir un `∃` que impida la
satisfacción vacua:

```
herbivore ≡ animal ⊓ ∃eats.⊤ ⊓ ∀eats.(plant  ⊔ ∃is-part-of.plant)
carnivore ≡ animal ⊓ ∃eats.⊤ ⊓ ∀eats.(animal ⊔ ∃is-part-of.animal)
```

Resultado:

```
[ok] con las definiciones corregidas, la brizna ya no rompe nada
[ok] lion sigue clasificándose como carnivore
[ok] PERO giraffe pierde la clasificación de herbivore
```

**La jirafa deja de ser herbívora.** No es un fallo de la corrección: es que sobre
la jirafa solo estaba declarado `∀eats.(Twig ⊔ leaf)` — *si* come, come ramitas u
hojas. Nunca se declaró que coma. Antes se colaba como herbívora justamente por el
bug que se acaba de arreglar; era una inferencia correcta por la razón equivocada.

Se declara lo que faltaba y vuelve:

```python
giraffe.is_a.append(eats.some(leaf))     # las jirafas comen alguna hoja
```

```
[ok] con ∃eats.leaf, giraffe vuelve a clasificarse como herbivore
```

## Qué deja este caso

**1. El razonador comprueba coherencia, no verdad.** Consistente y sin clases
insatisfacibles significa «lo que dijiste no se contradice», no «dijiste lo que
querías decir». La matriz de §1.3 lo llamaba precisión baja: se admiten modelos no
pretendidos, y todos son perfectamente consistentes.

**2. Bajo OWA, los errores se esconden hasta que llegan los datos.** El mundo
abierto es tan permisivo que absorbe modelado defectuoso durante todo el desarrollo
y lo devuelve en producción, cuando alguien afirma algo negativo o cerrado. Probar
la TBox sola no basta: **hay que probarla contra individuos**.

**3. `∀` no obliga a nada.** Es la trampa que más caro sale en OWL. `∀eats.plant`
no dice «come plantas», dice «no come nada que no sea planta» — y no comer nada lo
cumple. En una clase **definida** eso deja de ser una curiosidad y se vuelve una
bomba: la equivalencia arrastra a toda entidad que no coma hacia dentro de la
clase. Regla práctica: **un `∀` casi nunca debe ir solo; suele necesitar un `∃` al
lado**.

**4. Esto es el argumento a favor de las preguntas de competencia.** Ninguna
herramienta iba a preguntar «¿sigue siendo herbívora la jirafa?». Esa pregunta la
tiene que escribir una persona, antes de modelar, y quedar automatizada. Es
exactamente lo que el capítulo 5 manda hacer desde el principio, y lo que aquí se
está haciendo a mano en `verificar.py`.

**5. La versión 1 es la foto del «antes».** `AfricanWildlifeOntology1.owl` es la
primera de una serie que el libro va corrigiendo capítulo a capítulo. Encontrarle
defectos no es contradecir a Keet: es el ejercicio.

---

*Salvo los enunciados citados y la ontología de ejemplo, el análisis de esta página
es criterio propio, verificado con HermiT.*
