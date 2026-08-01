"""
Reproduce las afirmaciones del caso de estudio del capítulo 9.

Tres partes:

A. El ejemplo del propio libro (§9.1): el inglés tiene *river* y el francés
   distingue *fleuve* (desemboca en el mar) de *rivière* (no). Alinear las
   traducciones como equivalencias produce una contradicción — y la produce
   porque las dos lenguas **no conceptualizan igual**, no porque nadie se haya
   equivocado traduciendo.

B. Las etiquetas son invisibles para el razonador. Cambiar los IRI a otro idioma
   no cambia ni una deducción; poner la misma `rdfs:label` a dos clases
   disjuntas tampoco molesta a nadie.

C. La ambigüedad del lenguaje natural, medida: una sola frase en español admite
   dos formalizaciones que **no** son equivalentes.

    python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
    ./.venv/bin/python verificar.py

Necesita Java en el PATH: owlready2 invoca HermiT, que es un jar.
"""

import os
import sys

from owlready2 import (
    AllDisjoint,
    Not,
    ObjectProperty,
    OwlReadyInconsistentOntologyError,
    Thing,
    World,
    locstr,
    sync_reasoner,
)

AQUI = os.path.dirname(os.path.abspath(__file__))

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


# ===========================================================================
# A. fleuve / rivière / river
# ===========================================================================
print("\nA. Alinear traducciones: fleuve, rivière y river (§9.1)")


def rios(alineacion):
    """
    alineacion='ingenua'  : Fleuve ≡ River  y  Riviere ≡ River
    alineacion='correcta' : Fleuve ⊑ River  y  Riviere ⊑ River
    """
    mundo = World()
    onto = mundo.get_ontology("http://ontologias.eliuth.dev/rios.owl")
    with onto:

        class Mar(Thing):
            pass

        class River(Thing):
            pass

        class desembocaEn(ObjectProperty):
            pass

        class Fleuve(Thing):
            """río que desemboca en el mar"""

        class Riviere(Thing):
            """río que NO desemboca en el mar"""

        Fleuve.equivalent_to = [River & desembocaEn.some(Mar)]
        Riviere.equivalent_to = [River & Not(desembocaEn.some(Mar))]

        if alineacion == "ingenua":
            # «fleuve se traduce por river» y «rivière se traduce por river»
            Fleuve.equivalent_to.append(River)
            Riviere.equivalent_to.append(River)

        River("un_rio")
    return mundo, onto


afirmar("con Fleuve ⊑ River y Riviere ⊑ River la ontología es consistente",
        es_consistente(*rios("correcta")))
afirmar("con la alineación ingenua (ambas ≡ River) la ontología se vuelve "
        "INCONSISTENTE: fleuve y rivière acabarían siendo lo mismo, y se "
        "diferencian justo en desembocar o no en el mar",
        not es_consistente(*rios("ingenua")))
print("   No es un error de traducción: las dos lenguas no cortan el mundo igual.")


# ===========================================================================
# B. Las etiquetas no razonan
# ===========================================================================
print("\nB. Etiquetas e IRI: invisibles para el razonador")


def zoo(idioma):
    """La misma teoría con los nombres en inglés o en español."""
    nombres = {
        "en": ("Animal", "Plant", "Lion", "eats"),
        "es": ("Animal", "Planta", "Leon", "come"),
    }[idioma]
    mundo = World()
    onto = mundo.get_ontology(f"http://ontologias.eliuth.dev/zoo-{idioma}.owl")
    with onto:
        animal = type(nombres[0], (Thing,), {})
        planta = type(nombres[1], (Thing,), {})
        leon = type(nombres[2], (animal,), {})
        come = type(nombres[3], (ObjectProperty,), {})
        AllDisjoint([animal, planta])
        leon.is_a.append(come.only(animal))
        x = leon("x")
        x.is_a.append(come.some(planta))
    return mundo, onto


afirmar("«Lion ⊑ ∀eats.Animal» con un león que come una planta: INCONSISTENTE",
        not es_consistente(*zoo("en")))
afirmar("y exactamente igual con los nombres en español: el razonador no lee "
        "los identificadores", not es_consistente(*zoo("es")))


def etiquetas_iguales():
    """Dos clases disjuntas con la MISMA rdfs:label."""
    mundo = World()
    onto = mundo.get_ontology("http://ontologias.eliuth.dev/etiquetas.owl")
    with onto:

        class Banco_asiento(Thing):
            pass

        class Banco_entidad(Thing):
            pass

        Banco_asiento.label = [locstr("banco", "es")]
        Banco_entidad.label = [locstr("banco", "es")]
        AllDisjoint([Banco_asiento, Banco_entidad])
        Banco_asiento("uno")
        Banco_entidad("otro")
    return mundo, onto


afirmar("dos clases disjuntas con la MISMA etiqueta «banco» conviven sin "
        "problema: la etiqueta es una anotación, no un axioma",
        es_consistente(*etiquetas_iguales()))
print("   Corolario: la homonimia no la detecta ninguna herramienta lógica.")


# ===========================================================================
# C. Una frase, dos formalizaciones
# ===========================================================================
print("\nC. «Los leones comen herbívoros»: ∀ o ∃, y no son lo mismo")


def leones(cuantificador):
    mundo = World()
    onto = mundo.get_ontology("http://ontologias.eliuth.dev/leones.owl")
    with onto:

        class Animal(Thing):
            pass

        class Herbivoro(Animal):
            pass

        class Leon(Animal):
            pass

        class come(ObjectProperty):
            pass

        if cuantificador == "universal":
            Leon.is_a.append(come.only(Herbivoro))
        else:
            Leon.is_a.append(come.some(Herbivoro))
    return mundo, onto


def con(cuantificador, construir):
    mundo, onto = leones(cuantificador)
    with onto:
        construir(onto)
    return mundo, onto


def leon_que_no_come_nada(onto):
    x = onto.Leon("simba")
    x.is_a.append(Not(onto.come.some(Thing)))


def leon_que_come_un_carnivoro(onto):
    otro = onto.Animal("otro_animal")
    otro.is_a.append(Not(onto.Herbivoro))
    x = onto.Leon("simba")
    x.come = [otro]


afirmar("con ∀: un león que no come nada es admisible",
        es_consistente(*con("universal", leon_que_no_come_nada)))
afirmar("con ∃: el mismo león ya NO lo es",
        not es_consistente(*con("existencial", leon_que_no_come_nada)))
afirmar("con ∀: un león que come algo que no es herbívoro es INCONSISTENTE",
        not es_consistente(*con("universal", leon_que_come_un_carnivoro)))
afirmar("con ∃: ese mismo león es perfectamente admisible",
        es_consistente(*con("existencial", leon_que_come_un_carnivoro)))
print("   Cuatro resultados, dos y dos opuestos, para la MISMA frase en español.")


# --- resultado --------------------------------------------------------------
print()
if fallos:
    print(f"{len(fallos)} afirmación(es) del caso de estudio no se reproducen:")
    for f in fallos:
        print(f"  - {f}")
    sys.exit(1)
print("Todas las afirmaciones del caso de estudio se reproducen.")
