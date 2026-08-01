"""
Reproduce las afirmaciones del caso de estudio del capítulo 3.

Se construye la TBox del Exercise 3.2 del libro:

    Vegan      ≡ Person ⊓ ∀eats.Plant
    Vegetarian ≡ Person ⊓ ∀eats.(Plant ⊔ Dairy)

y se comprueba con HermiT lo que el ejercicio pide demostrar a mano con un
tableau, más las tres consecuencias que el ejercicio no menciona y que son las
que de verdad cambian cómo se modela:

  - el ∀ se satisface **vacuamente**: quien no come nada es vegano;
  - eso solo se infiere si el mundo se cierra explícitamente (mundo abierto);
  - con una clase **primitiva** (⊑) en lugar de **definida** (≡) no se clasifica
    nadie, aunque los axiomas «digan lo mismo» al leerlos.

    python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
    ./.venv/bin/python verificar.py

Necesita Java en el PATH: owlready2 invoca HermiT, que es un jar.

Nota de implementación: cada comprobación usa su propio `World`. `sync_reasoner`
razona sobre todo el mundo cargado, así que compartirlo mezclaría teorías.
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
    sync_reasoner,
)

AQUI = os.path.dirname(os.path.abspath(__file__))

fallos = []


def afirmar(descripcion, condicion):
    print(f"  [{'ok ' if condicion else 'FALLA'}] {descripcion}")
    if not condicion:
        fallos.append(descripcion)


def es_consistente(mundo, onto):
    """True si la teoría admite al menos un modelo (KB ⊭ ⊤ ⊑ ⊥)."""
    try:
        with onto:
            sync_reasoner(mundo, infer_property_values=False, debug=0)
        return True
    except OwlReadyInconsistentOntologyError:
        return False


def teoria(definida=True, disjuntas=True):
    """La TBox del Exercise 3.2.

    definida=False la degrada a clases primitivas: mismo texto en lenguaje
    natural, condiciones solo necesarias.
    """
    mundo = World()
    onto = mundo.get_ontology("http://ontologias.eliuth.dev/vegetarianos.owl")
    with onto:

        class Person(Thing):
            pass

        class Plant(Thing):
            pass

        class Dairy(Thing):
            pass

        class eats(ObjectProperty):
            pass

        class Vegan(Person):
            pass

        class Vegetarian(Person):
            pass

        if disjuntas:
            AllDisjoint([Plant, Dairy])

        if definida:
            Vegan.equivalent_to = [Person & eats.only(Plant)]
            Vegetarian.equivalent_to = [Person & eats.only(Plant | Dairy)]
        else:
            Vegan.is_a.append(eats.only(Plant))
            Vegetarian.is_a.append(eats.only(Plant | Dairy))

    return mundo, onto


# --- 1. Lo que pide el Exercise 3.2 ----------------------------------------
print("\n1. Exercise 3.2 — ¿T ⊢ Vegan ⊑ Vegetarian?")
print("   Se decide por refutación (§2.2.3): T ∪ {¬α} inconsistente sii T ⊨ α")


def negar_vegan_sub_vegetarian(onto):
    x = onto.Vegan("un_vegano")
    x.is_a.append(Not(onto.Vegetarian))


def negar_vegetarian_sub_vegan(onto):
    x = onto.Vegetarian("un_vegetariano")
    x.is_a.append(Not(onto.Vegan))


def con(construir, **kwargs):
    mundo, onto = teoria(**kwargs)
    with onto:
        construir(onto)
    return mundo, onto


afirmar("T sola es consistente", es_consistente(*teoria()))
afirmar("T ∪ {¬(Vegan ⊑ Vegetarian)} es INCONSISTENTE, luego T ⊨ Vegan ⊑ Vegetarian",
        not es_consistente(*con(negar_vegan_sub_vegetarian)))
afirmar("T ∪ {¬(Vegetarian ⊑ Vegan)} es CONSISTENTE: el recíproco NO se sigue",
        es_consistente(*con(negar_vegetarian_sub_vegan)))


# --- 2. El ∀ vacío ----------------------------------------------------------
print("\n2. El cuantificador universal se satisface vacuamente")


def persona_que_no_come(onto):
    p = onto.Person("nadia")
    # cierre explícito del mundo: nadia no come NADA
    p.is_a.append(Not(eats_de(onto).some(Thing)))
    return p


def eats_de(onto):
    return onto.search_one(iri="*#eats")


def clasificar(construir, **kwargs):
    mundo, onto = teoria(**kwargs)
    with onto:
        individuo = construir(onto)
        sync_reasoner(mundo, infer_property_values=False, debug=0)
    return individuo


nadia = clasificar(persona_que_no_come)
afirmar("una persona de la que se afirma que no come nada se clasifica como Vegan "
        "(∀eats.Plant es cierto por vacuidad)",
        any(c.name == "Vegan" for c in nadia.INDIRECT_is_a if hasattr(c, "name")))


def persona_sin_datos(onto):
    return onto.Person("perico")


perico = clasificar(persona_sin_datos)
afirmar("una persona SIN afirmar nada sobre lo que come NO se clasifica como Vegan: "
        "mundo abierto, no es lo mismo «no consta» que «no come»",
        not any(c.name == "Vegan" for c in perico.INDIRECT_is_a if hasattr(c, "name")))


# --- 3. Definida frente a primitiva ----------------------------------------
print("\n3. Clase definida (≡) frente a primitiva (⊑)")

nadia_prim = clasificar(persona_que_no_come, definida=False)
afirmar("con Vegan PRIMITIVA, la misma persona ya no se clasifica como Vegan: "
        "la condición es necesaria, no suficiente",
        not any(c.name == "Vegan" for c in nadia_prim.INDIRECT_is_a
                if hasattr(c, "name")))
afirmar("y con ambas primitivas, el resultado del Exercise 3.2 se PIERDE: "
        "T ∪ {¬(Vegan ⊑ Vegetarian)} vuelve a ser consistente",
        es_consistente(*con(negar_vegan_sub_vegetarian, definida=False)))


# --- 4. Satisfacibilidad de conceptos --------------------------------------
print("\n4. Satisfacibilidad de un concepto (KB ⊭ C ⊑ ⊥)")


def vegano_que_come_lacteo(onto):
    x = onto.Vegan("vegano_con_queso")
    x.is_a.append(eats_de(onto).some(onto.Dairy))


afirmar("Vegan ⊓ ∃eats.Dairy es INSATISFACIBLE cuando Plant y Dairy son disjuntas",
        not es_consistente(*con(vegano_que_come_lacteo)))
afirmar("sin declarar la disyunción, es SATISFACIBLE: nada impide un modelo donde "
        "algo sea planta y lácteo a la vez",
        es_consistente(*con(vegano_que_come_lacteo, disjuntas=False)))


# --- artefacto inspeccionable en Protégé ------------------------------------
mundo, onto = teoria()
onto.save(file=os.path.join(AQUI, "vegetarianos.owl"), format="rdfxml")


# --- resultado --------------------------------------------------------------
print()
if fallos:
    print(f"{len(fallos)} afirmación(es) del caso de estudio no se reproducen:")
    for f in fallos:
        print(f"  - {f}")
    sys.exit(1)
print("Todas las afirmaciones del caso de estudio se reproducen.")
