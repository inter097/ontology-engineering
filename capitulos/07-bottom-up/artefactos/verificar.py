"""
Reproduce las afirmaciones del caso de estudio del capítulo 7.

Tres partes, atadas a los ejercicios del capítulo:

A. **Exercise 7.2(a)** — el modelo conceptual de la Figura 7.7 pasado a OWL. El
   propio enunciado avisa de que hay una clase inconsistente y una subsunción
   nueva; aquí se localizan las dos con el razonador en vez de a ojo.

B. **Review questions 7.3 y 7.4** — un tesauro convertido término a término. La
   relación `broader` de un tesauro **no** es `rdfs:subClassOf`: mezcla «es un
   tipo de» con «es parte de», y al convertirla se deduce una falsedad.

C. **Review question 7.1** — por qué no basta con convertir cada tabla en una
   clase: las restricciones de la base de datos (NOT NULL, claves) **validan**, y
   sus traducciones a OWL no.

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
# A. Exercise 7.2(a) — el modelo conceptual de la Figura 7.7
# ===========================================================================
print("\nA. Exercise 7.2(a) — modelo conceptual UML pasado a OWL")


def figura_77(salarios=True):
    """
    Employee particionado (disjunto y completo) en Clerk y Manager.
    RichEmployee ⊑ Employee, disjunta de Clerk.
    PoorEmployee ⊑ Employee, disjunta de Manager.
    salary: obligatorio y único; cadena de 8 salvo en Clerk, que es de 5.
    """
    mundo = World()
    onto = mundo.get_ontology("http://ontologias.eliuth.dev/figura77.owl")
    with onto:

        class Employee(Thing):
            pass

        class Clerk(Employee):
            pass

        class Manager(Employee):
            pass

        class RichEmployee(Employee):
            pass

        class PoorEmployee(Employee):
            pass

        class salary(DataProperty, FunctionalProperty):
            domain = [Employee]
            range = [str]

        # partición: disjuntas y completas
        AllDisjoint([Clerk, Manager])
        Employee.equivalent_to = [Clerk | Manager]
        # los dos «cuadrados con cruz» del diagrama
        AllDisjoint([RichEmployee, Clerk])
        AllDisjoint([PoorEmployee, Manager])

        # el atributo es obligatorio en un modelo conceptual
        Employee.is_a.append(salary.exactly(1, str))
        # «cadena de 8 en todas las subclases, salvo Clerk, que la tiene de 5»
        if salarios:
            for clase in (Manager, RichEmployee, PoorEmployee):
                clase.is_a.append(
                    salary.only(ConstrainedDatatype(str, min_length=8)))
            Clerk.is_a.append(salary.only(ConstrainedDatatype(str, max_length=5)))

    return mundo, onto


def con_instancia(clase):
    mundo, onto = figura_77()
    with onto:
        onto[clase](f"un_{clase}")
    return mundo, onto


afirmar("el modelo por sí solo es consistente: el problema no se ve sin razonar",
        es_consistente(*figura_77()))
afirmar("PoorEmployee es INSATISFACIBLE: al ser disjunta de Manager cae dentro de "
        "Clerk, y ahí el salario tendría que medir 5 y 8 a la vez",
        not es_consistente(*con_instancia("PoorEmployee")))
afirmar("RichEmployee sí es satisfacible", es_consistente(*con_instancia("RichEmployee")))

mundo, onto = figura_77()
with onto:
    sync_reasoner(mundo, infer_property_values=False, debug=0)
afirmar("subsunción nueva, no declarada en el diagrama: RichEmployee ⊑ Manager",
        onto.Manager in onto.RichEmployee.ancestors())
afirmar("PoorEmployee no aparece como subclase de Clerk porque ya es equivalente "
        "a ⊥: el razonador la lista entre las clases insatisfacibles",
        onto.PoorEmployee in list(mundo.inconsistent_classes()))

mundo, onto = figura_77(salarios=False)
with onto:
    sync_reasoner(mundo, infer_property_values=False, debug=0)
afirmar("quitando SOLO la restricción de longitud del salario aparece la otra "
        "subsunción oculta, PoorEmployee ⊑ Clerk, y ya nada es insatisfacible",
        onto.Clerk in onto.PoorEmployee.ancestors()
        and not list(mundo.inconsistent_classes()))


# ===========================================================================
# B. Un tesauro convertido término a término
# ===========================================================================
print("\nB. broader de un tesauro NO es subClassOf")


def tesauro(broader_como_subclase):
    """
    Tesauro:  Motor  broader  Coche  broader  Vehículo

    El primer `broader` es una relación parte-todo; el segundo, un «es un tipo
    de». En un tesauro las dos se escriben igual.
    """
    mundo = World()
    onto = mundo.get_ontology("http://ontologias.eliuth.dev/tesauro.owl")
    with onto:

        class Vehiculo(Thing):
            pass

        class Coche(Vehiculo):
            pass

        class Motor(Thing):
            pass

        class parteDe(ObjectProperty):
            pass

        if broader_como_subclase:
            Motor.is_a.append(Coche)
        else:
            Motor.is_a.append(parteDe.some(Coche))
            AllDisjoint([Motor, Vehiculo])

        Motor("motor_de_prueba")
        sync_reasoner(mundo, infer_property_values=False, debug=0)
    return onto


onto = tesauro(broader_como_subclase=True)
afirmar("convirtiendo broader en subClassOf se deduce «todo motor es un "
        "vehículo» — falso, y nadie lo escribió",
        onto.Vehiculo in onto.Motor.ancestors())

onto = tesauro(broader_como_subclase=False)
afirmar("distinguiendo la parte-todo del es-un, la deducción falsa desaparece",
        onto.Vehiculo not in onto.Motor.ancestors())


def tesauro_incoherente():
    """La versión ingenua más la disyunción que el dominio exige: revienta."""
    mundo = World()
    onto = mundo.get_ontology("http://ontologias.eliuth.dev/tesauro2.owl")
    with onto:

        class Vehiculo(Thing):
            pass

        class Coche(Vehiculo):
            pass

        class Motor(Thing):
            pass

        Motor.is_a.append(Coche)
        AllDisjoint([Motor, Vehiculo])
        Motor("motor_de_prueba")
    return mundo, onto


afirmar("y si además se declara que motor y vehículo son disjuntos —que es la "
        "verdad del dominio— la conversión ingenua vuelve la ontología "
        "INCONSISTENTE", not es_consistente(*tesauro_incoherente()))


# ===========================================================================
# C. Review question 7.1 — la restricción de la base de datos no sobrevive
# ===========================================================================
print("\nC. Una tabla no es una clase: NOT NULL no se traduce")


def empleados(con_existencial):
    """
    Tabla Empleado con columna departamento NOT NULL, más su clave foránea.

    con_existencial=True traduce el NOT NULL como Empleado ⊑ ∃trabajaEn.Departamento.
    En los dos casos se inserta un empleado SIN departamento.
    """
    mundo = World()
    onto = mundo.get_ontology("http://ontologias.eliuth.dev/empleados.owl")
    with onto:

        class Departamento(Thing):
            pass

        class Empleado(Thing):
            pass

        class trabajaEn(ObjectProperty):
            domain = [Empleado]
            range = [Departamento]

        if con_existencial:
            Empleado.is_a.append(trabajaEn.some(Departamento))

        Empleado("empleado_sin_departamento")
    return mundo, onto


afirmar("traduciendo la columna a domain/range, un empleado sin departamento NO "
        "produce ningún error: la fila que la base de datos rechazaría, OWL la "
        "acepta", es_consistente(*empleados(con_existencial=False)))
afirmar("y traducido como ∃trabajaEn.Departamento TAMPOCO: el razonador se limita "
        "a suponer que existe un departamento que no consta",
        es_consistente(*empleados(con_existencial=True)))


def dato_que_contradice(onto_mundo):
    """Lo único que OWL sí rechaza: un dato que contradiga un axioma."""
    mundo, onto = onto_mundo
    with onto:
        d = onto.Departamento("ventas")
        e = onto.empleado_sin_departamento
        e.trabajaEn = [d]
        e.is_a.append(onto.Departamento)
        AllDisjoint([onto.Empleado, onto.Departamento])
    return mundo, onto


afirmar("lo único que OWL rechaza es una contradicción lógica: un individuo que "
        "sea empleado y departamento a la vez, siendo disjuntos",
        not es_consistente(*dato_que_contradice(empleados(True))))


# --- resultado --------------------------------------------------------------
print()
if fallos:
    print(f"{len(fallos)} afirmación(es) del caso de estudio no se reproducen:")
    for f in fallos:
        print(f"  - {f}")
    sys.exit(1)
print("Todas las afirmaciones del caso de estudio se reproducen.")
