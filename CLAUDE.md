# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Qué es esto

Un recorrido capítulo a capítulo por el libro de Keet. El repositorio **es** el
sitio: los mismos Markdown de `capitulos/` se leen en GitHub y generan
`ontologias.eliuth.dev` (Astro, salida estática, deploy en Vercel). No hay copia
del contenido en `src/` — si algo se duplica, está mal.

Capítulo 1 publicado. Los demás, pendientes. Sigue sin definirse la ontología
propia (dominio, alcance, preguntas de competencia), que es por donde manda
empezar el capítulo 5.

## Comandos

```bash
npm run dev      # sitio en local
npm run build    # estático a dist/ — falla si el frontmatter no valida
npm run check    # astro check (tipos)

# verificar los artefactos de un capítulo; sale con código 1 si algo no reproduce
cd capitulos/NN-nombre/artefactos
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
./.venv/bin/python verificar.py       # requiere Java: HermiT es un jar
```

## Arquitectura

- `capitulos/NN-nombre.md` — **una sola página por capítulo**. Frontmatter validado
  por Zod en `src/content.config.ts`; el `build` falla si no encaja.
- `capitulos/NN-nombre/artefactos/` — `.owl`, `verificar.py`, `requirements.txt`.
  El loader usa `pattern: '*.md'` (un nivel), así que esta carpeta hermana queda
  fuera de la colección a propósito.
- `src/capitulos.ts` — registro de los 10 capítulos con la numeración verificada.
  **Al añadir un capítulo se toca este archivo**, o el índice no lo enlaza; el
  loader de contenido no conoce los títulos ni el orden.
- `src/pages/capitulos/[...slug].astro` — una página por Markdown; el `slug` es el
  nombre del archivo sin extensión (`01-introduccion`).

**Frontmatter:** entrecomillar `descripcion` y `titulo` siempre. Llevan `:` y `«»`
y YAML rompe el build sin comillas.

## Cómo se trabaja un capítulo

Una página, con tres cosas dentro y **dosificadas por relevancia** — es la petición
explícita del autor: lo rutinario en tablas y párrafos cortos, lo que de verdad
cambia cómo modelas, extendido.

1. **Qué dice el libro**, con las secciones citadas (`§N.x`). Comprimir aquí.
2. **Caso de estudio** — el centro de la página, y lo que va extendido. No un
   programa: un problema donde lo del capítulo se aplica a algo que un razonador
   confirma o desmiente. Toda afirmación del texto debe corresponder a una
   comprobación en `verificar.py`. Si no se puede verificar, no se afirma.
3. **Ejercicios** del libro, enunciado citado literal + resolución propia. Marcar
   explícitamente lo que es criterio propio. Comprimir los rutinarios; si un
   ejercicio alimenta el caso de estudio, remitir en vez de repetir.

No repetir el mismo contenido en dos sitios de la página.

## Reglas de contenido (no negociables)

**Toda decisión de modelado se cita contra el capítulo correspondiente de Keet**
(*An Introduction to Ontology Engineering*, v1.5, 2020). Formato:

> Se usa una clase definida en vez de una primitiva para `X` porque las condiciones
> son necesarias y suficientes (Keet, cap. 4, §4.x).

Si una decisión no tiene respaldo en el libro, se declara explícitamente como criterio
propio. **No inventar referencias ni números de capítulo.**

**Numeración de capítulos.** La que circula suele estar corrida +1. La verificada está
en el README y es la que se usa: 3 = Description Logics, 4 = OWL 2, 5 = Methods and
Methodologies, 6 = Top-down, 10 = Advanced Modeling. La 2ª edición coincide hasta el 9
y difiere del 10 en adelante — al citar, indicar edición.

**Idioma.** README y documentación en español. Mantenerlo.

## Trampa recurrente del dominio

En OWL, `domain` y `range` **no validan** — son reglas de inferencia. Declarar un
`domain` no produce error ante datos que no encajan: produce una clasificación
silenciosa. Cualquier sugerencia de modelado que trate estas construcciones como
restricciones de validación es incorrecta.

## Verificación (equivalente a la suite de tests)

No hay métrica única. Los artefactos automatizables son:

| Verificación | Falla si |
|---|---|
| Razonador (HermiT, ELK, Pellet) | clases insatisfacibles o ontología inconsistente |
| Preguntas de competencia | una consulta deja de devolver el resultado esperado |
| [OOPS!](https://oops.linkeddata.es/) | aparecen pitfalls críticos |
| Métricas estructurales | se dispara expresividad DL / conteo de axiomas sin justificación |

**Las preguntas de competencia son las pruebas unitarias reales**: consulta +
respuesta esperada. Hoy viven dentro de los `verificar.py` de cada capítulo, como
afirmaciones sobre lo que el razonador debe y no debe inferir. Cuando exista la
ontología propia habrá que sacarlas a un directorio aparte.

**Toolchain actual:** owlready2 0.51 sobre HermiT (necesita Java). Un venv por
capítulo, en `artefactos/.venv`, ignorado por git. `verificar.py` sale con código 1
si alguna afirmación del texto deja de reproducirse — es lo más parecido a CI que
hay; ejecutarlo tras tocar cualquier `.owl` o cualquier afirmación de un caso de
estudio.

Aún sin usar, pero previstos: Protégé (inspección manual), ROBOT (CLI de
razonamiento y métricas), OOPS!.

## Bloque «para la defensa»

El repositorio es material de **tesis**. Cada capítulo cierra con un
`<details class="defensa">` con las preguntas que un tribunal haría sobre ese
capítulo y la respuesta corta y defendible. Reglas:

- Pregunta en negrita y entrecomillada, como la formularía el tribunal.
- Respuesta directa en la primera frase; el desarrollo después.
- Cuando haya una réplica previsible, anticiparla con *«si insisten:»* o
  *«el matiz que conviene añadir:»*.
- Apoyarse en lo verificado en el caso de estudio del propio capítulo. Una
  respuesta que cita una comprobación reproducible vale más que una correcta
  pero genérica.

Va **después** del cierre del capítulo, nunca en medio.

## Explicaciones en lenguaje llano

Los `<details class="peras">` explican notación y conceptos abstractos sin jerga.
Orden obligatorio: **primero la idea en lenguaje corriente con una situación
cotidiana, después la definición formal** — nunca al revés. La formal va en su
propio desplegable si hace falta citarla.

Los símbolos viven en `capitulos/00-simbolos.md` (capítulo 0, página propia, no del
libro). Los demás capítulos **enlazan ahí** en vez de repetir la tabla.

**Markdown dentro de `<details>`:** hace falta una línea en blanco después de
`</summary>`, o el bloque HTML se traga el markdown y las tablas salen en crudo.
