"""
Reproduce las afirmaciones del caso de estudio del capítulo 11.

Se modulariza una ontología pequeña de tres formas y se mide qué se conserva:

    Impala ⊑ Antelope ⊑ Bovidae ⊑ Herbivore ⊑ Animal
    Herbivore ⊓ Carnivore ⊑ ⊥
    Lion ⊑ Carnivore ⊓ ∃eats.Impala

Se pide un módulo para la **signatura** {Impala, Animal, Lion}:

  a. **corte ingenuo** — quedarse solo con los axiomas que mencionan esos
     nombres;
  b. **módulo por localidad (aproximado)** — cerrar la signatura hacia arriba
     hasta que ningún axioma quede colgando;
  c. la ontología entera, como referencia.

Un módulo sirve si **preserva las consecuencias sobre su signatura**. Aquí se
comprueba cuál lo hace y qué se pierde exactamente con el otro.

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


# --- las tres versiones -----------------------------------------------------
def construir(version):
    """version ∈ {'completa', 'ingenuo', 'localidad'}"""
    mundo = World()
    onto = mundo.get_ontology(f"http://ontologias.eliuth.dev/modulo-{version}.owl")
    with onto:

        class Animal(Thing):
            pass

        class Impala(Animal):
            pass

        class Lion(Animal):
            pass

        class eats(ObjectProperty):
            pass

        if version == "ingenuo":
            # solo los axiomas que mencionan literalmente {Impala, Animal, Lion}
            Lion.is_a.append(eats.some(Impala))
            return mundo, onto

        class Herbivore(Animal):
            pass

        class Carnivore(Animal):
            pass

        class Bovidae(Herbivore):
            pass

        class Antelope(Bovidae):
            pass

        AllDisjoint([Herbivore, Carnivore])
        Impala.is_a = [Antelope]
        Lion.is_a = [Carnivore, eats.some(Impala)]

        if version == "completa":
            # una rama entera que la signatura no toca
            class Plant(Thing):
                pass

            class Grass(Plant):
                pass

            AllDisjoint([Animal, Plant])
            Herbivore.is_a.append(eats.some(Plant))

    return mundo, onto


def entails(version, negacion):
    """T ⊨ α  sii  T ∪ {¬α} inconsistente (§2.2.3)."""
    mundo, onto = construir(version)
    with onto:
        negacion(onto)
    return not es_consistente(mundo, onto)


def impala_no_es_animal(onto):
    x = onto.Impala("un_impala")
    x.is_a.append(Not(onto.Animal))


def leon_come_algo_que_no_es_impala(onto):
    x = onto.Lion("un_leon")
    x.is_a.append(Not(onto.eats.some(onto.Impala)))


def leon_es_impala(onto):
    x = onto.Lion("un_leon")
    x.is_a.append(onto.Impala)


# --- 1. lo que los tres conservan ------------------------------------------
print("\n1. Consecuencias sobre la signatura {Impala, Animal, Lion}")

for version in ("completa", "localidad", "ingenuo"):
    afirmar(f"[{version}] ⊨ Impala ⊑ Animal",
            entails(version, impala_no_es_animal))
    afirmar(f"[{version}] ⊨ Lion ⊑ ∃eats.Impala",
            entails(version, leon_come_algo_que_no_es_impala))


# --- 2. lo que el corte ingenuo pierde -------------------------------------
print("\n2. La consecuencia que el corte ingenuo se deja por el camino")

afirmar("[completa]  ⊨ Lion ⊓ Impala ⊑ ⊥ — un león no puede ser un impala",
        entails("completa", leon_es_impala))
afirmar("[localidad] ⊨ Lion ⊓ Impala ⊑ ⊥ — el módulo lo conserva",
        entails("localidad", leon_es_impala))
afirmar("[ingenuo]   NO lo deduce: sin Carnivore, Herbivore y la disyunción "
        "entre ambas, un león puede ser un impala",
        not entails("ingenuo", leon_es_impala))
print("   Los tres nombres de la signatura estaban; la consecuencia, no.")


# --- 3. tamaño frente a fidelidad ------------------------------------------
print("\n3. Qué cuesta conservarla")


def tamano(version):
    mundo, onto = construir(version)
    return len(list(onto.classes()))


afirmar("el módulo por localidad es más pequeño que la ontología completa: "
        f"{tamano('localidad')} clases frente a {tamano('completa')}",
        tamano("localidad") < tamano("completa"))
afirmar(f"y el corte ingenuo es aún más pequeño ({tamano('ingenuo')} clases), "
        "pero eso es exactamente lo que le pasa",
        tamano("ingenuo") < tamano("localidad"))
afirmar("la rama de plantas, que la signatura no toca, no hace falta: sin ella "
        "se siguen deduciendo las tres consecuencias",
        entails("localidad", impala_no_es_animal)
        and entails("localidad", leon_come_algo_que_no_es_impala)
        and entails("localidad", leon_es_impala))


# --- resultado --------------------------------------------------------------
print()
if fallos:
    print(f"{len(fallos)} afirmación(es) del caso de estudio no se reproducen:")
    for f in fallos:
        print(f"  - {f}")
    sys.exit(1)
print("Todas las afirmaciones del caso de estudio se reproducen.")
