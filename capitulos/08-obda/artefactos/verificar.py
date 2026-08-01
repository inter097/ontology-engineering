"""
Reproduce las afirmaciones del caso de estudio del capítulo 8.

Se monta el Example 8.1 del libro, que es el argumento entero del capítulo:

    Professor(Mkhize)      dato, en la base de datos
    Professor ⊑ Employee   conocimiento, en la ontología

    consulta: «lista todos los empleados»

Solo base de datos → {} ; solo ontología → no sabe si hay alguno ;
base de datos + ontología → {Mkhize}.

Y después, las dos cosas que un sistema OBDA **no** hace y que se confunden con
lo anterior: la negación en la consulta sigue siendo de mundo cerrado sobre lo
materializado, y el conocimiento existencial de la TBox no produce filas.

    python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
    ./.venv/bin/python verificar.py

Necesita Java en el PATH: owlready2 invoca HermiT, que es un jar.
"""

import os
import sys

from owlready2 import ObjectProperty, Thing, World, sync_reasoner

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = "http://ontologias.eliuth.dev/obda.owl"

fallos = []


def afirmar(descripcion, condicion):
    print(f"  [{'ok ' if condicion else 'FALLA'}] {descripcion}")
    if not condicion:
        fallos.append(descripcion)


def universidad(con_tbox=True, con_existencial=False):
    """
    Datos (la «base de datos»):  Professor(Mkhize), Cleaner(Naidoo),
                                 worksFor(Mkhize, Informatica)
    Conocimiento (la ontología): Professor ⊑ Employee,  Cleaner ⊑ Employee
    """
    mundo = World()
    onto = mundo.get_ontology(BASE)
    with onto:

        class Employee(Thing):
            pass

        class Department(Thing):
            pass

        class Professor(Thing):
            pass

        class Cleaner(Thing):
            pass

        class worksFor(ObjectProperty):
            pass

        if con_tbox:
            Professor.is_a.append(Employee)
            Cleaner.is_a.append(Employee)

        if con_existencial:
            Employee.is_a.append(worksFor.some(Department))

        informatica = Department("Informatica")
        mkhize = Professor("Mkhize")
        mkhize.worksFor = [informatica]
        Cleaner("Naidoo")

    return mundo, onto


def consulta_directa(mundo):
    """«Lista todos los empleados», tal cual, contra los datos."""
    filas = list(mundo.sparql(
        "SELECT ?x WHERE { ?x a <%sEmployee> . }" % (BASE + "#")))
    return sorted(f[0].name for f in filas)


def consulta_reescrita(mundo):
    """La misma pregunta con la TBox incorporada a la consulta: es la opción v1
    de §8.2 —«incorporate the relevant parts of the TBox into the query»— y es
    lo que hace por dentro un sistema OBDA."""
    filas = list(mundo.sparql(
        "SELECT ?x WHERE { ?x a/rdfs:subClassOf* <%sEmployee> . }" % (BASE + "#")))
    return sorted(f[0].name for f in filas)


def completar_abox(mundo, onto):
    """La opción v2 de §8.2: incorporar la TBox a la ABox y consultar después."""
    with onto:
        sync_reasoner(mundo, infer_property_values=True, debug=0)
        for individuo in onto.individuals():
            for madre in list(individuo.is_a):
                for antepasado in madre.ancestors():
                    if antepasado not in individuo.is_a:
                        individuo.is_a.append(antepasado)
    return mundo


# --- 1. Example 8.1, las tres situaciones ----------------------------------
print("\n1. Example 8.1 — «lista todos los empleados»")

mundo, onto = universidad(con_tbox=False)
afirmar("solo datos, sin ontología: la consulta devuelve {}",
        consulta_directa(mundo) == [])

mundo, onto = universidad(con_tbox=True)
afirmar("con la ontología cargada, la consulta TAL CUAL sigue devolviendo {}: "
        "el conocimiento está escrito, pero la consulta no lo usa",
        consulta_directa(mundo) == [])

mundo, onto = universidad(con_tbox=True)
afirmar("reescribiendo la consulta con la TBox (opción v1 de §8.2): "
        "{Mkhize, Naidoo}", consulta_reescrita(mundo) == ["Mkhize", "Naidoo"])

mundo, onto = universidad(con_tbox=True)
afirmar("o completando la ABox y preguntando lo mismo (opción v2 de §8.2): "
        "también {Mkhize, Naidoo}",
        consulta_directa(completar_abox(mundo, onto)) == ["Mkhize", "Naidoo"])
print("   Misma pregunta, mismos datos, tres respuestas distintas.")


# --- 2. Lo que OBDA NO arregla: la negación de la consulta ------------------
print("\n2. La negación en la consulta sigue siendo de mundo cerrado")


def sin_departamento(mundo):
    filas = list(mundo.sparql("""
        SELECT ?x WHERE {
            ?x a <%(b)sEmployee> .
            FILTER NOT EXISTS { ?x <%(b)sworksFor> ?d . }
        }
    """ % {"b": BASE + "#"}))
    return sorted(f[0].name for f in filas)


mundo, onto = universidad(con_tbox=True)
afirmar("«empleados sin departamento» devuelve {Naidoo}: en los datos no consta "
        "el suyo", sin_departamento(completar_abox(mundo, onto)) == ["Naidoo"])

mundo, onto = universidad(con_tbox=True, con_existencial=True)
afirmar("y añadiendo Employee ⊑ ∃worksFor.Department a la TBox, la consulta "
        "SIGUE devolviendo {Naidoo}: el razonador sabe que su departamento "
        "existe, pero no puede ponerlo en una fila",
        sin_departamento(completar_abox(mundo, onto)) == ["Naidoo"])
print("   NOT EXISTS pregunta por lo materializado, no por lo que se sigue.")


# --- 3. Por qué la TBox tiene que ser pequeña (§8.2) ------------------------
print("\n3. Qué parte del conocimiento llega a las filas")

mundo, onto = universidad(con_tbox=True, con_existencial=True)
with onto:
    sync_reasoner(mundo, infer_property_values=True, debug=0)
departamentos = list(mundo.sparql("""
    SELECT ?d WHERE { <%(b)sNaidoo> <%(b)sworksFor> ?d . }
""" % {"b": BASE + "#"}))
afirmar("el departamento de Naidoo no aparece como valor: un existencial de la "
        "TBox no crea individuos en los datos", departamentos == [])

mundo, onto = universidad(con_tbox=True)
completar_abox(mundo, onto)
tipos = list(mundo.sparql("""
    SELECT ?c WHERE { <%(b)sMkhize> a ?c . }
""" % {"b": BASE + "#"}))
afirmar("lo que sí llega a las filas son las subsunciones: completada la ABox, "
        "Mkhize aparece con los dos tipos, Professor y Employee",
        {"Professor", "Employee"} <= {t[0].name for t in tipos
                                      if hasattr(t[0], "name")})
print("   Por eso la TBox de un sistema OBDA se limita a OWL 2 QL (§8.2).")


# --- resultado --------------------------------------------------------------
print()
if fallos:
    print(f"{len(fallos)} afirmación(es) del caso de estudio no se reproducen:")
    for f in fallos:
        print(f"  - {f}")
    sys.exit(1)
print("Todas las afirmaciones del caso de estudio se reproducen.")
