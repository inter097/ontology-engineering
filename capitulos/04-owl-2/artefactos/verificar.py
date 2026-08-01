"""
Reproduce las afirmaciones del caso de estudio del capítulo 4.

Es el Exercise 4.2 del libro: una lesión en un hueso de la mano es también una
lesión en la mano, y se quiere que el razonador lo infiera **para cualquier parte
anatómica**, no caso por caso. La característica que hace falta es nueva de OWL 2:
las **cadenas de propiedades**.

    injuryOf ∘ partOf ⊑ injuryOf

Lo que se comprueba aquí, además de que funciona, es su precio: la cadena vuelve
`injuryOf` una propiedad **no simple**, y las propiedades no simples no pueden
aparecer en restricciones de cardinalidad, ni ser funcionales, ni irreflexivas, ni
asimétricas. Es una restricción global de OWL 2 DL, no un capricho del razonador.

    python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
    ./.venv/bin/python verificar.py

Necesita Java en el PATH: owlready2 invoca HermiT, que es un jar.
"""

import os
import sys

from owlready2 import (
    Not,
    ObjectProperty,
    OwlReadyInconsistentOntologyError,
    OwlReadyJavaError,
    PropertyChain,
    Thing,
    TransitiveProperty,
    World,
    sync_reasoner,
)

AQUI = os.path.dirname(os.path.abspath(__file__))

fallos = []


def afirmar(descripcion, condicion):
    print(f"  [{'ok ' if condicion else 'FALLA'}] {descripcion}")
    if not condicion:
        fallos.append(descripcion)


def anatomia(cadena=True, cardinalidad=False):
    """Ontología mínima de lesiones y partes anatómicas.

    cadena=True añade  injuryOf ∘ partOf ⊑ injuryOf  (OWL 2, §4.2.1).
    cardinalidad=True añade  Injury ⊑ =1 injuryOf.BodyPart, que solo es legal
    si injuryOf es simple.
    """
    mundo = World()
    onto = mundo.get_ontology("http://ontologias.eliuth.dev/anatomia.owl")
    with onto:

        class BodyPart(Thing):
            pass

        class Injury(Thing):
            pass

        class partOf(ObjectProperty, TransitiveProperty):
            domain = [BodyPart]
            range = [BodyPart]

        class injuryOf(ObjectProperty):
            domain = [Injury]
            range = [BodyPart]

        if cadena:
            injuryOf.property_chain = [PropertyChain([injuryOf, partOf])]

        if cardinalidad:
            Injury.is_a.append(injuryOf.exactly(1, BodyPart))

        hueso = BodyPart("hueso_escafoides")
        mano = BodyPart("mano_derecha")
        brazo = BodyPart("brazo_derecho")
        hueso.partOf = [mano]
        mano.partOf = [brazo]

        fractura = Injury("fractura_del_escafoides")
        fractura.injuryOf = [hueso]

    return mundo, onto


def razonar(**kwargs):
    mundo, onto = anatomia(**kwargs)
    with onto:
        sync_reasoner(mundo, infer_property_values=True, debug=0)
    return onto


def es_consistente(mundo, onto):
    try:
        with onto:
            sync_reasoner(mundo, infer_property_values=False, debug=0)
        return True
    except OwlReadyInconsistentOntologyError:
        return False


def negar_lesion_de_la_mano(onto):
    """¬α, con α = injuryOf(fractura_del_escafoides, mano_derecha)."""
    onto.fractura_del_escafoides.is_a.append(
        Not(onto.injuryOf.value(onto.mano_derecha)))


def con(construir, **kwargs):
    mundo, onto = anatomia(**kwargs)
    with onto:
        construir(onto)
    return mundo, onto


# --- 1. Sin la cadena, no se infiere nada ----------------------------------
print("\n1. Sin cadena de propiedades")
print("   partOf(hueso, mano), partOf(mano, brazo), injuryOf(fractura, hueso)")

onto = razonar(cadena=False)
afirmar("la lesión NO llega a la mano: injuryOf(fractura, mano) no se infiere",
        onto.mano_derecha not in onto.fractura_del_escafoides.injuryOf)
afirmar("y se prueba por refutación: T ∪ {¬α} sigue siendo CONSISTENTE",
        es_consistente(*con(negar_lesion_de_la_mano, cadena=False)))


# --- 2. Con la cadena, se propaga por toda la mereología -------------------
print("\n2. Con  injuryOf ∘ partOf ⊑ injuryOf  (§4.2.1)")

onto = razonar()
afirmar("injuryOf(fractura, mano_derecha) se infiere",
        onto.mano_derecha in onto.fractura_del_escafoides.injuryOf)
afirmar("injuryOf(fractura, brazo_derecho) también: se propaga al todo indirecto",
        onto.brazo_derecho in onto.fractura_del_escafoides.injuryOf)
afirmar("y ahora T ∪ {¬α} es INCONSISTENTE, luego T ⊨ injuryOf(fractura, mano)",
        not es_consistente(*con(negar_lesion_de_la_mano)))
afirmar("un solo axioma cubre cualquier parte anatómica: no hay reglas por caso",
        len(onto.fractura_del_escafoides.injuryOf) == 3)


# --- 3. El precio: la propiedad deja de ser simple -------------------------
print("\n3. La restricción global de OWL 2 DL sobre propiedades no simples")


def acepta(**kwargs):
    """True si el razonador acepta la ontología; False si la rechaza por violar
    una restricción global del lenguaje (no por inconsistencia lógica)."""
    mundo, onto = anatomia(**kwargs)
    try:
        with onto:
            sync_reasoner(mundo, infer_property_values=False, debug=0)
        return True
    except OwlReadyJavaError:
        return False


afirmar("Injury ⊑ =1 injuryOf.BodyPart es legal mientras injuryOf sea simple",
        acepta(cadena=False, cardinalidad=True))
afirmar("con la cadena declarada, la MISMA restricción sale de OWL 2 DL y el "
        "razonador rechaza la ontología: injuryOf ya no es simple",
        not acepta(cadena=True, cardinalidad=True))


# --- artefacto inspeccionable en Protégé ------------------------------------
mundo, onto = anatomia()
onto.save(file=os.path.join(AQUI, "anatomia.owl"), format="rdfxml")


# --- resultado --------------------------------------------------------------
print()
if fallos:
    print(f"{len(fallos)} afirmación(es) del caso de estudio no se reproducen:")
    for f in fallos:
        print(f"  - {f}")
    sys.exit(1)
print("Todas las afirmaciones del caso de estudio se reproducen.")
