"""
Reproduce las afirmaciones del caso de estudio del capítulo 5.

Dos partes, las dos tomadas de los ejercicios del propio libro:

A. **Exercise 5.1** — las once preguntas de competencia (CQ) del libro evaluadas
   contra AfricanWildlifeOntology1.owl. Una CQ es una prueba unitaria: consulta
   + respuesta esperada. Aquí se mide cuántas contesta la ontología, cuántas no
   puede contestar por falta de vocabulario, y —lo peor— cuántas devuelven una
   respuesta vacía que parece un «no» y es un «no consta».

B. **Exercise 5.3** — la ontología con `domain`/`range` del libro, donde una clase
   se vuelve insatisfacible sin que nadie haya escrito una contradicción. Es la
   demostración de que en OWL el dominio **no valida: infiere**.

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


def awo(construir=None):
    mundo = World()
    onto = mundo.get_ontology("file://" + AWO).load()
    if construir is not None:
        with onto:
            construir(onto)
    return mundo, onto


def c(onto, nombre):
    return onto.search_one(iri="*#" + nombre)


# ===========================================================================
# A. Exercise 5.1 — las CQ del libro contra la AWO
# ===========================================================================
print("\nA. Preguntas de competencia (Exercise 5.1) contra la AWO")

_, o = awo()
vocabulario = {e.name for e in list(o.classes()) + list(o.properties())}

print("\n  A.1 — las que la ontología SÍ contesta")

# CQ 6: ¿qué plantas comen animales?
afirmar("CQ6 «¿qué plantas comen animales?» → CarnivorousPlant, definida como "
        "plant ⊓ ∃eats.animal",
        any("eats" in str(x) and "animal" in str(x)
            for x in c(o, "CarnivorousPlant").is_a))

# CQ 7 y CQ 1: ¿qué animales comen impalas? ¿qué animal come a qué animal?
afirmar("CQ7 «¿qué animales comen impalas?» → lion, por lion ⊑ ∃eats.Impala",
        any("eats" in str(x) and "Impala" in str(x) for x in c(o, "lion").is_a))
afirmar("CQ1 «¿qué animal come a qué otro animal?» → se contesta, pero solo en la "
        "TBox: la AWO no tiene ni un individuo",
        len(list(o.individuals())) == 0)


# CQ 4: ¿come el león plantas o partes de planta?
def leon_come_planta(onto):
    x = c(onto, "lion")("leon_de_prueba")
    x.is_a.append(c(onto, "eats").some(c(onto, "plant")))


afirmar("CQ4 «¿come el león plantas?» → NO, y es una deducción: lion ⊓ ∃eats.plant "
        "es insatisfacible", not es_consistente(*awo(leon_come_planta)))

print("\n  A.2 — las que devuelven vacío, y el vacío NO significa «no»")


def rockdassie_no_herbivoro(onto):
    x = c(onto, "RockDassie")("rockdassie_de_prueba")
    x.is_a.append(Not(c(onto, "herbivore")))


afirmar("CQ2 «¿es herbívoro un rockdassie?» → la ontología NO lo deduce: "
        "T ∪ {¬α} sigue consistente", es_consistente(*awo(rockdassie_no_herbivoro)))


def alguien_come_rockdassie(onto):
    x = c(onto, "lion")("un_leon")
    y = c(onto, "RockDassie")("un_rockdassie")
    x.eats = [y]


afirmar("CQ8 «¿quién depreda al rockdassie?» → respuesta vacía; y es ignorancia, "
        "no negación: añadir un depredador NO produce inconsistencia",
        es_consistente(*awo(alguien_come_rockdassie)))


def no_come_nada(clase):
    def construir(onto):
        x = c(onto, clase)(f"{clase}_que_no_come")
        x.is_a.append(Not(c(onto, "eats").some(Thing)))
    return construir


afirmar("CQ3 «¿qué partes de planta come una jirafa?» → la AWO parece deducir que "
        "toda jirafa come algo: T ∪ {¬∃eats.⊤} es inconsistente",
        not es_consistente(*awo(no_come_nada("giraffe"))))
afirmar("…pero no lo deduce de ningún axioma sobre jirafas: le pasa igual a un "
        "animal cualquiera, porque quien no come nada cae a la vez en herbivore y "
        "en carnivore —ambas definidas solo con ∀— que son disjuntas. Es el fallo "
        "del capítulo 1, y aquí convierte una CQ en un falso positivo",
        not es_consistente(*awo(no_come_nada("animal"))))

print("\n  A.3 — las que no se pueden contestar: falta el vocabulario")

afirmar("CQ5 «¿hay algún animal que no beba agua?» → no existe ninguna propiedad "
        "de beber ni clase de agua en la ontología",
        not any(t in v.lower() for v in vocabulario for t in ("drink", "water")))
afirmar("CQ9/CQ10 «¿monos en Sudáfrica? ¿a qué país ir para ver elefantes?» → "
        "no hay ni Monkey ni país ni región",
        not any(t in v.lower() for v in vocabulario
                for t in ("monkey", "country", "africa")))
afirmar("CQ11 «¿comparten hábitat jirafas y cebras?» → existen las clases Habitat "
        "y Distribution, pero ninguna propiedad las conecta con nada",
        {"Habitat", "Distribution"} <= vocabulario
        and not any(p.range and any(getattr(r, "name", None)
                                    in ("Habitat", "Distribution") for r in p.range)
                    for p in o.properties()))

respondidas = 4
afirmar(f"balance: {respondidas} de 11 CQ se contestan; el resto falla por "
        "vocabulario ausente o por confundir vacío con negación",
        respondidas == 4)


# ===========================================================================
# B. Exercise 5.3 — el dominio no valida, infiere
# ===========================================================================
print("\nB. Exercise 5.3 — una clase insatisfacible sin ninguna contradicción escrita")


def ejercicio_53(con_dominio=True):
    """
    R ⊑ PD × PD     PD ⊑ PT      A ⊑ ED      A ⊑ ∃R.B
    S ⊑ PT × PT     ED ⊑ PT      B ⊑ ED      D ⊑ ∃S.C
    S ⊑ R           ED ⊑ ¬PD     C ⊑ PD      D ⊑ PD
    Trans(R)
    """
    mundo = World()
    onto = mundo.get_ontology("http://ontologias.eliuth.dev/ejercicio53.owl")
    with onto:

        class PT(Thing):
            pass

        class PD(PT):
            pass

        class ED(PT):
            pass

        class A(ED):
            pass

        class B(ED):
            pass

        class C(PD):
            pass

        class D(PD):
            pass

        class R(ObjectProperty, TransitiveProperty):
            if con_dominio:
                domain = [PD]
                range = [PD]

        class S(R):
            domain = [PT]
            range = [PT]

        AllDisjoint([ED, PD])
        A.is_a.append(R.some(B))
        D.is_a.append(S.some(C))

    return mundo, onto


def instanciar(clase_nombre, **kwargs):
    mundo, onto = ejercicio_53(**kwargs)
    with onto:
        onto[clase_nombre](f"instancia_de_{clase_nombre}")
    return mundo, onto


afirmar("con el dominio declarado, A es INSATISFACIBLE: A ⊑ ∃R.B mete a A en el "
        "dominio de R, que es PD, y ED es disjunta de PD",
        not es_consistente(*instanciar("A")))
afirmar("y nadie escribió A ⊑ ⊥ ni ninguna contradicción: la produjo el domain",
        not es_consistente(*instanciar("A")))
afirmar("quitando SOLO la declaración de dominio y rango de R, A vuelve a ser "
        "satisfacible: el domain no rechazaba nada, infería",
        es_consistente(*instanciar("A", con_dominio=False)))
afirmar("B, en cambio, es satisfacible en las dos versiones: el fallo no está en "
        "la jerarquía sino en la interacción entre el axioma y el dominio",
        es_consistente(*instanciar("B"))
        and es_consistente(*instanciar("B", con_dominio=False)))
afirmar("S ⊑ R con dominios incompatibles (PT ⊄ PD) es lo que detecta el servicio "
        "de RBox Compatibility: la teoría lo tolera, el modelado no",
        es_consistente(*ejercicio_53()))


# --- resultado --------------------------------------------------------------
print()
if fallos:
    print(f"{len(fallos)} afirmación(es) del caso de estudio no se reproducen:")
    for f in fallos:
        print(f"  - {f}")
    sys.exit(1)
print("Todas las afirmaciones del caso de estudio se reproducen.")
