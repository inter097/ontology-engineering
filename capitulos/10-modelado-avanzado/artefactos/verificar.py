"""
Reproduce las afirmaciones del caso de estudio del capítulo 10.

Dos partes:

A. **Vaguedad** (§10.1) — «menor de edad» tiene una frontera exacta; «joven» no.
   En OWL, que es nítido, la única salida es inventarse un umbral. Aquí se mide
   qué pasa con quien está justo al lado de ese umbral, y qué pasa cuando dos
   ontologías eligen umbrales distintos y se alinean.

B. **Tiempo** (§10.2) — una ontología atemporal no puede decir «fue estudiante y
   ahora es profesora» sin contradecirse. Se comprueba el problema y las dos
   salidas habituales: relaciones indexadas por tiempo y partes temporales.

    python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
    ./.venv/bin/python verificar.py

Necesita Java en el PATH: owlready2 invoca HermiT, que es un jar.
"""

import os
import sys

from owlready2 import (
    AllDisjoint,
    ConstrainedDatatype,
    DataProperty,
    FunctionalProperty,
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


# ===========================================================================
# A. Vaguedad: «joven» con un umbral inventado
# ===========================================================================
print("\nA. Vaguedad (§10.1) — «menor de edad» frente a «joven»")


def poblacion(umbral, edades):
    """Joven ≡ Persona ⊓ ∃edad.(entero ≤ umbral). Nítido, porque OWL lo es."""
    mundo = World()
    onto = mundo.get_ontology("http://ontologias.eliuth.dev/edades.owl")
    with onto:

        class Persona(Thing):
            pass

        class edad(DataProperty, FunctionalProperty):
            domain = [Persona]
            range = [int]

        class Joven(Persona):
            pass

        Joven.equivalent_to = [
            Persona & edad.some(ConstrainedDatatype(int, max_inclusive=umbral))]

        for nombre, valor in edades.items():
            p = Persona(nombre)
            p.edad = valor

        sync_reasoner(mundo, infer_property_values=False, debug=0)
    return onto


def es(onto, individuo, clase):
    return any(getattr(c, "name", None) == clase
               for c in getattr(onto, individuo).INDIRECT_is_a)


onto = poblacion(30, {"ana": 30, "bea": 31})
afirmar("con el umbral en 30: ana (30) es Joven", es(onto, "ana", "Joven"))
afirmar("y bea (31) NO lo es — un año de diferencia, dos clases distintas",
        not es(onto, "bea", "Joven"))

onto = poblacion(35, {"ana": 30, "bea": 31})
afirmar("moviendo el umbral a 35, bea pasa a ser Joven sin que nada del mundo "
        "haya cambiado", es(onto, "bea", "Joven"))


def dos_umbrales_alineados():
    """Dos ontologías con umbrales distintos, alineadas como equivalentes."""
    mundo = World()
    onto = mundo.get_ontology("http://ontologias.eliuth.dev/alineacion.owl")
    with onto:

        class Persona(Thing):
            pass

        class edad(DataProperty, FunctionalProperty):
            domain = [Persona]
            range = [int]

        class JovenA(Persona):
            pass

        class JovenB(Persona):
            pass

        JovenA.equivalent_to = [
            Persona & edad.some(ConstrainedDatatype(int, max_inclusive=30))]
        JovenB.equivalent_to = [
            Persona & edad.some(ConstrainedDatatype(int, max_inclusive=35))]
        # el alineamiento ingenuo: «joven es joven»
        JovenA.equivalent_to.append(JovenB)

        bea = Persona("bea")
        bea.edad = 31
    return mundo, onto


afirmar("alinear como equivalentes dos «Joven» con umbrales distintos (30 y 35) "
        "vuelve la ontología INCONSISTENTE en cuanto hay alguien en medio",
        not es_consistente(*dos_umbrales_alineados()))
print("   La frontera no está en el mundo: la puso quien modeló.")


# ===========================================================================
# B. Tiempo: «fue estudiante y ahora es profesora»
# ===========================================================================
print("\nB. Tiempo (§10.2) — un cambio de estado en una ontología atemporal")


def carrera(enfoque):
    """
    enfoque='atemporal'  : Estudiante(nadia) y Profesora(nadia), disjuntas
    enfoque='indexado'   : relaciones con índice temporal (una clase de estado)
    enfoque='partes'     : partes temporales del individuo (perdurantismo)
    """
    mundo = World()
    onto = mundo.get_ontology(f"http://ontologias.eliuth.dev/tiempo-{enfoque}.owl")
    with onto:

        class Persona(Thing):
            pass

        class Estudiante(Persona):
            pass

        class Profesora(Persona):
            pass

        AllDisjoint([Estudiante, Profesora])

        if enfoque == "atemporal":
            nadia = Estudiante("nadia")
            nadia.is_a.append(Profesora)

        elif enfoque == "indexado":

            class Intervalo(Thing):
                pass

            class Estado(Thing):
                pass

            class deQuien(ObjectProperty):
                domain = [Estado]
                range = [Persona]

            class durante(ObjectProperty):
                domain = [Estado]
                range = [Intervalo]

            class EstadoEstudiante(Estado):
                pass

            class EstadoProfesora(Estado):
                pass

            nadia = Persona("nadia")
            for clase, cuando in ((EstadoEstudiante, "2015_2019"),
                                  (EstadoProfesora, "2020_2026")):
                e = clase(f"estado_{cuando}")
                e.deQuien = [nadia]
                e.durante = [Intervalo(cuando)]

        elif enfoque == "partes":

            class parteTemporalDe(ObjectProperty):
                pass

            nadia = Persona("nadia")
            joven = Estudiante("nadia_2015_2019")
            madura = Profesora("nadia_2020_2026")
            joven.parteTemporalDe = [nadia]
            madura.parteTemporalDe = [nadia]

    return mundo, onto


afirmar("atemporal: afirmar que la misma persona es Estudiante y Profesora "
        "—clases disjuntas— es INCONSISTENTE",
        not es_consistente(*carrera("atemporal")))
afirmar("con relaciones indexadas por tiempo: consistente, y el cambio queda "
        "representado", es_consistente(*carrera("indexado")))
afirmar("con partes temporales del individuo: también consistente",
        es_consistente(*carrera("partes")))


def partes_sin_disyuncion():
    """El precio de las partes temporales: la persona ya no es la clase."""
    mundo, onto = carrera("partes")
    with onto:
        sync_reasoner(mundo, infer_property_values=False, debug=0)
    return onto


onto = partes_sin_disyuncion()
afirmar("pero el individuo «nadia» NO es Estudiante ni Profesora: lo son sus "
        "partes temporales, y cualquier consulta sobre personas tiene que saberlo",
        not any(getattr(c, "name", None) in ("Estudiante", "Profesora")
                for c in onto.nadia.INDIRECT_is_a))
print("   Las dos salidas funcionan y las dos cambian a qué se le pregunta.")


# --- resultado --------------------------------------------------------------
print()
if fallos:
    print(f"{len(fallos)} afirmación(es) del caso de estudio no se reproducen:")
    for f in fallos:
        print(f"  - {f}")
    sys.exit(1)
print("Todas las afirmaciones del caso de estudio se reproducen.")
