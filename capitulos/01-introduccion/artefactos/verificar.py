"""
Reproduce las afirmaciones del caso de estudio del capítulo 1 sobre
AfricanWildlifeOntology1.owl, la ontología de ejemplo del libro de Keet.

    python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
    ./.venv/bin/python verificar.py

Necesita Java en el PATH: owlready2 invoca HermiT, que es un jar.
"""

import os
import sys

from owlready2 import (
    Nothing,
    OwlReadyInconsistentOntologyError,
    Thing,
    get_ontology,
    sync_reasoner,
)

RUTA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "AfricanWildlifeOntology1.owl")

fallos = []


def afirmar(descripcion, condicion):
    print(f"  [{'ok ' if condicion else 'FALLA'}] {descripcion}")
    if not condicion:
        fallos.append(descripcion)


def cargar():
    """Carga limpia. Cada prueba parte de cero: sync_reasoner muta la ontología."""
    return get_ontology("file://" + RUTA).load(reload=True)


def clase(onto, nombre):
    return onto.search_one(iri="*#" + nombre)


# --- 1. inventario, sin razonador -------------------------------------------
print("\n1. El archivo, tal como viene")
onto = cargar()
clases = list(onto.classes())
props = list(onto.object_properties())
individuos = list(onto.individuals())
print(f"  {len(clases)} clases · {len(props)} propiedades de objeto · "
      f"{len(individuos)} individuos")
afirmar("no hay ABox: es una ontología puramente de esquema", len(individuos) == 0)

definidas = [c.name for c in clases if c.equivalent_to]
print(f"  clases definidas (necesarias y suficientes): {sorted(definidas)}")
afirmar("solo herbivore, carnivore y Omnivore están definidas",
        sorted(definidas) == ["Omnivore", "carnivore", "herbivore"])

herbivore, carnivore = clase(onto, "herbivore"), clase(onto, "carnivore")
print(f"  herbivore ≡ {herbivore.equivalent_to[0]}")
print(f"  carnivore ≡ {carnivore.equivalent_to[0]}")

disjuntas = [sorted(e.name for e in d.entities) for d in onto.disjoint_classes()]
print(f"  {len(disjuntas)} axiomas de disyunción: {disjuntas}")
afirmar("carnivore y herbivore están declaradas disjuntas",
        ["carnivore", "herbivore"] in disjuntas)


# --- 2. la ontología, tal cual, es consistente -------------------------------
print("\n2. Con el razonador (HermiT), sin tocar nada")
onto = cargar()
try:
    with onto:
        sync_reasoner(infer_property_values=False, debug=0)
    consistente = True
except OwlReadyInconsistentOntologyError:
    consistente = False
afirmar("la ontología es consistente", consistente)

insatisfacibles = [c.name for c in onto.classes() if Nothing in c.is_a]
afirmar(f"no hay clases insatisfacibles (encontradas: {insatisfacibles})",
        not insatisfacibles)

# clasificación inferida
padres = {c.name: [str(p) for p in c.is_a] for c in onto.classes()}
afirmar("giraffe se clasifica como herbivore",
        any("herbivore" in p for p in padres["giraffe"]))
afirmar("lion se clasifica como carnivore",
        any("carnivore" in p for p in padres["lion"]))
afirmar("Impala NO se clasifica como herbivore, pese a que "
        "lion ⊑ ∀eats.herbivore ⊓ ∃eats.Impala",
        not any("herbivore" in p for p in padres["Impala"]))


# --- 3. el defecto: un individuo que no come nada ---------------------------
print("\n3. Se añade un individuo que no come nada")
onto = cargar()
eats = onto.search_one(iri="*#eats")
Grass = clase(onto, "Grass")
with onto:
    brizna = Grass("brizna_de_hierba_1")
    brizna.is_a.append(eats.exactly(0, Thing))   # una brizna no come

try:
    with onto:
        sync_reasoner(infer_property_values=False, debug=0)
    rompe = False
except OwlReadyInconsistentOntologyError:
    rompe = True

afirmar("afirmar que una brizna de hierba no come vuelve INCONSISTENTE la "
        "ontología (satisfacción vacua de ∀ en una clase definida, más la "
        "disyunción carnivore/herbivore)", rompe)


# --- 4. la corrección -------------------------------------------------------
print("\n4. Se corrigen las definiciones y se vuelve a probar")
onto = cargar()
eats, ipo = onto.search_one(iri="*#eats"), onto.search_one(iri="*#is-part-of")
animal, plant = clase(onto, "animal"), clase(onto, "plant")
herbivore, carnivore = clase(onto, "herbivore"), clase(onto, "carnivore")
Grass, giraffe, leaf = clase(onto, "Grass"), clase(onto, "giraffe"), clase(onto, "leaf")

with onto:
    # el ⊔ dentro del alcance del ∀, y un ∃ que impide la satisfacción vacua
    herbivore.equivalent_to = [
        animal & eats.some(Thing) & eats.only(plant | ipo.some(plant))
    ]
    carnivore.equivalent_to = [
        animal & eats.some(Thing) & eats.only(animal | ipo.some(animal))
    ]
    brizna = Grass("brizna_de_hierba_1")
    brizna.is_a.append(eats.exactly(0, Thing))

try:
    with onto:
        sync_reasoner(infer_property_values=False, debug=0)
    sigue_rota = False
except OwlReadyInconsistentOntologyError:
    sigue_rota = True

afirmar("con las definiciones corregidas, la brizna ya no rompe nada",
        not sigue_rota)

padres = {c.name: [str(p) for p in c.is_a] for c in onto.classes()}
afirmar("lion sigue clasificándose como carnivore",
        any("carnivore" in p for p in padres["lion"]))
afirmar("PERO giraffe pierde la clasificación: solo se dijo qué come *si* come",
        not any("herbivore" in p for p in padres["giraffe"]))


# --- 5. el precio de la corrección ------------------------------------------
print("\n5. Se afirma además que la jirafa come alguna hoja")
with onto:
    giraffe.is_a.append(eats.some(leaf))
    sync_reasoner(infer_property_values=False, debug=0)

afirmar("con ∃eats.leaf, giraffe vuelve a clasificarse como herbivore",
        any("herbivore" in str(p) for p in giraffe.is_a))


# --- resultado --------------------------------------------------------------
print()
if fallos:
    print(f"{len(fallos)} afirmación(es) del caso de estudio no se reproducen:")
    for f in fallos:
        print(f"  - {f}")
    sys.exit(1)
print("Todas las afirmaciones del caso de estudio se reproducen.")
