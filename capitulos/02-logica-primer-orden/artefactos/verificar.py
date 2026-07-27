"""
Reproduce las afirmaciones del caso de estudio del capítulo 2.

La idea que se comprueba: el razonador hace **deducción** y solo deducción. Lo que
en el capítulo 1 parecía un fallo —que `Impala` no se clasificara como herbívoro—
es que aquella inferencia no era una deducción, sino una **abducción**.

Todo se decide con el método que describe el propio libro (§2.2.3):

    T |= α   si y solo si   T ∪ {¬α} es inconsistente

    python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
    ./.venv/bin/python verificar.py

Necesita Java en el PATH: owlready2 invoca HermiT, que es un jar.

Nota de implementación: cada comprobación usa su propio `World`. `sync_reasoner`
razona sobre todo el mundo cargado, así que compartirlo entre pruebas mezclaría
teorías distintas —y, con la aritmética de cardinalidades, se cuelga.
"""

import os
import sys

from owlready2 import (
    Not,
    ObjectProperty,
    OwlReadyInconsistentOntologyError,
    Thing,
    World,
    sync_reasoner,
)

AWO = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "AfricanWildlifeOntology1.owl")

fallos = []


def afirmar(descripcion, condicion):
    print(f"  [{'ok ' if condicion else 'FALLA'}] {descripcion}")
    if not condicion:
        fallos.append(descripcion)


def es_consistente(mundo, onto):
    """True si la teoría admite al menos un modelo."""
    try:
        with onto:
            sync_reasoner(mundo, infer_property_values=False, debug=0)
        return True
    except OwlReadyInconsistentOntologyError:
        return False


def c(onto, nombre):
    return onto.search_one(iri="*#" + nombre)


# --- 1. Deducción: el ejemplo de la tarántula (§2.2.3) ----------------------
print("\n1. Deducción — «cada tarántula tiene 8 patas»")
print("   T = { Arachnid ⊑ =8 hasPart.Leg ,  Tarantula ⊑ Arachnid }")


def aracnidos(negar_conclusion):
    mundo = World()
    onto = mundo.get_ontology("http://ontologias.eliuth.dev/aracnidos.owl")
    with onto:
        class Leg(Thing):
            pass

        class Arachnid(Thing):
            pass

        class Tarantula(Arachnid):
            pass

        class hasPart(ObjectProperty):
            pass

        # «cada arácnido tiene exactamente 8 patas como parte»
        Arachnid.is_a.append(hasPart.exactly(8, Leg))

        if negar_conclusion:
            # ¬α, con α = «cada tarántula tiene exactamente 8 patas»
            t = Tarantula("tarantula_1")
            t.is_a.append(Not(hasPart.exactly(8, Leg)))
    return mundo, onto


afirmar("T por sí sola es consistente", es_consistente(*aracnidos(False)))
afirmar("T ∪ {¬α} es inconsistente, luego T |= «Tarantula ⊑ =8 hasPart.Leg»",
        not es_consistente(*aracnidos(True)))
print("   La deducción no aporta conocimiento nuevo: ya estaba implícito en T.")


# --- 2. La inferencia del impala, revisada ---------------------------------
print("\n2. El impala del capítulo 1 — ¿deducción o abducción?")
print("   T = AfricanWildlifeOntology1.owl, con lion ⊑ ∀eats.herbivore ⊓ ∃eats.Impala")


def awo(construir):
    mundo = World()
    onto = mundo.get_ontology("file://" + AWO).load()
    with onto:
        construir(onto)
    return mundo, onto


def neg_impala_es_herbivoro(onto):
    Impala, herbivore = c(onto, "Impala"), c(onto, "herbivore")
    x = Impala("impala_de_prueba")
    x.is_a.append(Not(herbivore))


def neg_leon_come_impala_herbivoro(onto):
    lion, Impala = c(onto, "lion"), c(onto, "Impala")
    herbivore, eats = c(onto, "herbivore"), c(onto, "eats")
    x = lion("leon_de_prueba")
    x.is_a.append(Not(eats.some(Impala & herbivore)))


afirmar("T ∪ {¬α} es INCONSISTENTE con α = «lion ⊑ ∃eats.(Impala ⊓ herbivore)»: "
        "esto SÍ es una deducción",
        not es_consistente(*awo(neg_leon_come_impala_herbivoro)))

afirmar("T ∪ {¬α} es CONSISTENTE con α = «Impala ⊑ herbivore»: "
        "esto NO se sigue de T",
        es_consistente(*awo(neg_impala_es_herbivoro)))


# --- 3. La hipótesis abductiva ---------------------------------------------
print("\n3. Abducción — «Impala ⊑ herbivore» como explicación, no como consecuencia")


def hipotesis_fuerte(onto):
    c(onto, "Impala").is_a.append(c(onto, "herbivore"))


def hipotesis_debil(onto):
    """Basta con que algún impala sea herbívoro; no hace falta que lo sean todos."""
    Impala, herbivore = c(onto, "Impala"), c(onto, "herbivore")
    x = Impala("un_impala_herbivoro")
    x.is_a.append(herbivore)


afirmar("H = «Impala ⊑ herbivore» es una explicación admisible: T ∪ {H} consistente",
        es_consistente(*awo(hipotesis_fuerte)))
afirmar("H' = «algún impala es herbívoro» también lo es, y es más débil — "
        "la abducción no da una respuesta única",
        es_consistente(*awo(hipotesis_debil)))


# --- 4. Inducción ----------------------------------------------------------
print("\n4. Inducción — generalizar desde individuos no es válido")


def gatos(afirmar_generalizacion):
    mundo = World()
    onto = mundo.get_ontology("http://ontologias.eliuth.dev/gatos.owl")
    with onto:
        class Cat(Thing):
            pass

        class Tail(Thing):
            pass

        class hasPart(ObjectProperty):
            pass

        tibbles = Cat("tibbles")
        tibbles.hasPart = [Tail("cola_de_tibbles")]

        if afirmar_generalizacion:
            # el salto inductivo: «todos los gatos tienen cola»
            Cat.is_a.append(hasPart.some(Tail))
            # …y el contraejemplo que el mundo real sí tiene
            manx = Cat("manx")
            manx.is_a.append(Not(hasPart.some(Tail)))
    return mundo, onto


afirmar("de «tibbles es un gato con cola» NO se sigue «todos los gatos tienen cola»: "
        "sin la generalización, T es consistente", es_consistente(*gatos(False)))
afirmar("al afirmarla, un solo gato sin cola (un manx) la vuelve inconsistente",
        not es_consistente(*gatos(True)))


# --- resultado --------------------------------------------------------------
print()
if fallos:
    print(f"{len(fallos)} afirmación(es) del caso de estudio no se reproducen:")
    for f in fallos:
        print(f"  - {f}")
    sys.exit(1)
print("Todas las afirmaciones del caso de estudio se reproducen.")
