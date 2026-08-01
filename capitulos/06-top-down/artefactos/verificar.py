"""
Reproduce las afirmaciones del caso de estudio del capítulo 6.

Tres partes, las tres atadas a ejercicios del capítulo:

A. **Exercise 6.6(a)** — añadir a la AWO el conocimiento suficiente para que
   `RockDassie` se clasifique **automáticamente** como herbívoro. Es la CQ2 que
   el capítulo 5 dejó sin contestar.

B. **§6.2, relaciones parte-todo** — qué pasa cuando se mete la pertenencia a un
   grupo dentro de la misma propiedad transitiva que la parte estructural. La
   respuesta es una deducción falsa que nadie escribió.

C. **Review question 6.6** — por qué la mereología básica no cabe entera en OWL 2
   DL: la parte propia necesita ser transitiva y asimétrica a la vez, y eso el
   estándar lo prohíbe.

    python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
    ./.venv/bin/python verificar.py

Necesita Java en el PATH: owlready2 invoca HermiT, que es un jar.
"""

import os
import sys

from owlready2 import (
    AsymmetricProperty,
    ObjectProperty,
    OwlReadyInconsistentOntologyError,
    OwlReadyJavaError,
    Thing,
    TransitiveProperty,
    World,
    sync_reasoner,
)

AQUI = os.path.dirname(os.path.abspath(__file__))
AWO = os.path.join(AQUI, "AfricanWildlifeOntology1.owl")

fallos = []


def afirmar(descripcion, condicion):
    print(f"  [{'ok ' if condicion else 'FALLA'}] {descripcion}")
    if not condicion:
        fallos.append(descripcion)


def es_consistente(mundo, onto):
    try:
        with onto:
            sync_reasoner(mundo, infer_property_values=False, debug=0)
        return True
    except OwlReadyInconsistentOntologyError:
        return False


def c(onto, nombre):
    return onto.search_one(iri="*#" + nombre)


# ===========================================================================
# A. Exercise 6.6(a) — que RockDassie se clasifique como herbívoro
# ===========================================================================
print("\nA. Exercise 6.6(a) — clasificar RockDassie como herbivore")


def awo(arreglo=None):
    mundo = World()
    onto = mundo.get_ontology("file://" + AWO).load()
    if arreglo is not None:
        with onto:
            arreglo(onto)
    with onto:
        sync_reasoner(mundo, infer_property_values=False, debug=0)
    return onto


def es_subclase_de(onto, hija, madre):
    return c(onto, madre) in c(onto, hija).ancestors()


onto = awo()
afirmar("de partida NO se clasifica: la AWO solo dice RockDassie ⊑ animal",
        not es_subclase_de(onto, "RockDassie", "herbivore"))


def arreglo_ingenuo(onto):
    """El primer intento de todo el mundo: «come plantas»."""
    c(onto, "RockDassie").is_a.append(c(onto, "eats").some(c(onto, "plant")))


onto = awo(arreglo_ingenuo)
afirmar("con RockDassie ⊑ ∃eats.plant TAMPOCO: herbivore está definida con ∀, y "
        "«come alguna planta» no excluye que coma otras cosas",
        not es_subclase_de(onto, "RockDassie", "herbivore"))


def arreglo_correcto(onto):
    """∀ para entrar en la definición, ∃ para no entrar por vacuidad."""
    eats, plant = c(onto, "eats"), c(onto, "plant")
    c(onto, "RockDassie").is_a.append(eats.only(plant))
    c(onto, "RockDassie").is_a.append(eats.some(plant))


onto = awo(arreglo_correcto)
afirmar("con RockDassie ⊑ ∀eats.plant ⊓ ∃eats.plant SÍ se clasifica como herbivore",
        es_subclase_de(onto, "RockDassie", "herbivore"))
afirmar("y NO se clasifica además como carnivore: el ∃ es lo que impide la "
        "vacuidad que hunde a la AWO",
        not es_subclase_de(onto, "RockDassie", "carnivore"))


# ===========================================================================
# B. §6.2 — mezclar parte estructural y pertenencia a un grupo
# ===========================================================================
print("\nB. Relaciones parte-todo: qué se deduce al meterlas todas en una")


def bosque(una_sola_propiedad):
    """
    hoja  —parte de→  rama  —parte de→  árbol  —¿?→  bosque

    una_sola_propiedad=True: todo cuelga de un único partOf transitivo.
    False: la pertenencia al grupo va por memberOf, que no es parte-todo.
    """
    mundo = World()
    onto = mundo.get_ontology("http://ontologias.eliuth.dev/mereologia.owl")
    with onto:

        class partOf(ObjectProperty, TransitiveProperty):
            pass

        class memberOf(ObjectProperty):
            pass

        if una_sola_propiedad:
            memberOf.is_a.append(partOf)

        hoja = Thing("hoja")
        rama = Thing("rama")
        arbol = Thing("arbol")
        bosque_ = Thing("bosque")

        hoja.partOf = [rama]
        rama.partOf = [arbol]
        arbol.memberOf = [bosque_]

        sync_reasoner(mundo, infer_property_values=True, debug=0)
    return onto


onto = bosque(una_sola_propiedad=True)
afirmar("con una sola propiedad transitiva se deduce «la hoja es parte del "
        "bosque» — nadie lo escribió y es falso",
        onto.bosque in onto.hoja.partOf)

onto = bosque(una_sola_propiedad=False)
afirmar("separando memberOf de partOf, la deducción falsa desaparece",
        onto.bosque not in onto.hoja.partOf)
afirmar("y lo que sí es parte-todo se sigue propagando: la hoja es parte del árbol",
        onto.arbol in onto.hoja.partOf)


# ===========================================================================
# C. Review question 6.6 — la mereología básica no cabe en OWL 2 DL
# ===========================================================================
print("\nC. Por qué la mereología básica no cabe entera en OWL 2 DL")


def parte_propia(asimetrica):
    """Parte propia = transitiva + asimétrica. OWL 2 DL no admite las dos."""
    mundo = World()
    onto = mundo.get_ontology("http://ontologias.eliuth.dev/parte-propia.owl")
    with onto:
        if asimetrica:

            class properPartOf(ObjectProperty, TransitiveProperty,
                               AsymmetricProperty):
                pass
        else:

            class properPartOf(ObjectProperty, TransitiveProperty):
                pass

        a, b = Thing("a"), Thing("b")
        a.properPartOf = [b]
    try:
        with onto:
            sync_reasoner(mundo, infer_property_values=False, debug=0)
        return True
    except (OwlReadyJavaError, OwlReadyInconsistentOntologyError):
        return False


afirmar("transitiva sola: aceptada", parte_propia(asimetrica=False))
afirmar("transitiva + asimétrica: RECHAZADA. Una propiedad transitiva no es "
        "simple, y la asimetría solo se admite en propiedades simples (cap. 4)",
        not parte_propia(asimetrica=True))


# --- resultado --------------------------------------------------------------
print()
if fallos:
    print(f"{len(fallos)} afirmación(es) del caso de estudio no se reproducen:")
    for f in fallos:
        print(f"  - {f}")
    sys.exit(1)
print("Todas las afirmaciones del caso de estudio se reproducen.")
