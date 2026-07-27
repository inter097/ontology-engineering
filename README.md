# ontology-engineering

Proyecto de ingeniería de ontologías siguiendo el método de:

> **Keet, C.M.** *An Introduction to Ontology Engineering*, v1.5 (2020).
> Libro abierto: https://people.cs.uct.ac.za/~mkeet/OEbook/

---

## ⚠️ Numeración de capítulos — verificada

**La numeración que circula suele estar corrida +1** (por contar el prefacio o el
*"How to Use the Book"* como capítulo 1). Esta es la real, confirmada contra el índice
del autor y la edición en LibreTexts:

| Cap. | Título |
|---|---|
| 1 | Introduction |
| 2 | First-Order Logic and Automated Reasoning in a Nutshell |
| 3 | **Description Logics** |
| 4 | **The Web Ontology Language OWL 2** |
| 5 | **Methods and Methodologies** |
| 6 | **Top-down Ontology Development** |
| 7 | Bottom-up Ontology Development |
| 8 | Ontology-Based Data Access |
| 9 | Ontologies and Natural Languages |
| 10 | **Advanced Modeling with Additional Language Features** |

La 2ª edición mantiene esta numeración hasta el capítulo 9; a partir del 10 difiere
(10 = *Rough, Temporal, and Fuzzy Modelling*, 11 = *More Topics to Explore*).
**Al citar, indicar la edición.**

---

## Ruta de lectura

```
cap. 4 (OWL 2)  →  cap. 3 (lógicas descriptivas)  →  cap. 6 (top-down)
      →  cap. 5 (metodologías)  →  cap. 10 (modelado avanzado)
```

Herramienta primero, teoría después. Es una ruta pragmática y defendible.

**El riesgo asumido:** las lógicas descriptivas son lo que explica *por qué* el
razonador infiere lo que infiere. El error clásico de quien las pospone es tratar
`domain` y `range` como restricciones que validan datos, cuando en OWL son **reglas de
inferencia** — no rechazan nada, infieren tipos. Se declara un `domain` y en vez de un
error aparece una clasificación silenciosa que nadie esperaba.

Conviene al menos hojear el capítulo 3 antes de modelar en serio.

---

## Convención de trabajo

**Toda decisión de modelado se cita contra el capítulo correspondiente de Keet.**

El objetivo es que cada elección sea rastreable a una fuente metodológica citable, no
a intuición. Formato:

> Se usa una clase definida en vez de una primitiva para `X` porque las condiciones
> son necesarias y suficientes (Keet, cap. 4, §4.x).

Si una decisión no tiene respaldo en el libro, se dice explícitamente que es criterio
propio. **No inventar referencias ni números de capítulo** — verificarlos contra el
índice.

---

## Qué hace verificable a una ontología

A diferencia de un proyecto de machine learning, aquí **no hay una métrica única** que
zanje las discusiones. No existe el RMSE de una ontología. Pero sí hay artefactos que
se pueden automatizar y que sirven de suite de pruebas:

| Verificación | Qué comprueba | Falla si |
|---|---|---|
| **Razonador** (HermiT, ELK, Pellet) | Consistencia y satisfacibilidad | Hay clases insatisfacibles o la ontología es inconsistente |
| **Preguntas de competencia** | Que responda lo que debía responder | Una consulta deja de devolver el resultado esperado |
| **OOPS!** | Errores comunes de modelado | Aparecen pitfalls críticos |
| **Métricas estructurales** | Expresividad DL, conteo de clases/axiomas | Se dispara la complejidad sin justificación |

**Las preguntas de competencia son el equivalente real de las pruebas unitarias.** Se
formalizan como consultas con respuesta esperada; si un cambio en el modelo rompe una,
se sabe de inmediato.

---

## Estructura

Los capítulos son la fuente única: el mismo Markdown se lee en GitHub y genera el
sitio en **[ontologias.eliuth.dev](https://ontologias.eliuth.dev)**. Nada se duplica.

```
.
├── capitulos/
│   └── NN-nombre/
│       ├── resumen.md          # qué dice el libro
│       ├── ejercicios.md       # los del libro, resueltos paso a paso
│       ├── caso-de-estudio.md  # el cierre: algo verificable, no un programa
│       └── artefactos/         # .owl, scripts de verificación, requirements
├── src/                        # el sitio (Astro): layout, páginas, índice global
└── README.md
```

Cada capítulo cierra con un **caso de estudio**: no un ejercicio más, sino un
problema donde lo del capítulo se aplica a algo que un razonador puede confirmar o
desmentir. El del capítulo 1 encuentra un error semántico real en la ontología de
ejemplo del propio libro.

### Comandos

```bash
npm install
npm run dev      # sitio en local
npm run build    # build estático a dist/

# verificar los artefactos de un capítulo (necesita Java en el PATH)
cd capitulos/01-introduccion/artefactos
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
./.venv/bin/python verificar.py
```

## Estado

| Capítulo | Estado |
|---|---|
| 1 — Introduction | resumen · ejercicios · caso de estudio |
| 2–10 | pendientes |

Pendiente de definir: dominio de la ontología propia, alcance y preguntas de
competencia iniciales — que es justamente por donde manda empezar el capítulo 5.

---

## Referencias

- Keet, C.M. (2020). *An Introduction to Ontology Engineering*, v1.5.
  [Libro](https://people.cs.uct.ac.za/~mkeet/OEbook/) ·
  [PDF](https://people.cs.uct.ac.za/~mkeet/files/OEbook.pdf) ·
  [LibreTexts](https://eng.libretexts.org/Bookshelves/Computer_Science/Programming_and_Computation_Fundamentals/An_Introduction_to_Ontology_Engineering_(Keet))
- [OOPS! — OntOlogy Pitfall Scanner](https://oops.linkeddata.es/)
- [Protégé](https://protege.stanford.edu/)
