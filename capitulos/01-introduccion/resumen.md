---
titulo: Qué es una ontología y por qué no es una base de datos
capitulo: 1
seccion: resumen
descripcion: 'El capítulo que fija el vocabulario. Cuatro definiciones de «ontología», la diferencia con un esquema relacional, y la razón de fondo de casi todo lo que viene después: la hipótesis de mundo abierto.'
keet: cap. 1 (Introduction), §1.1–1.5
---

El capítulo 1 no enseña a construir nada. Fija el vocabulario y responde una sola
pregunta con cuatro capas de profundidad: **qué es una ontología**. Vale la pena
leerlo despacio porque los malentendidos que se arrastran después casi siempre
nacen aquí.

## 1.1 — El problema que motiva todo

Keet abre con una definición deliberadamente pobre: una ontología es *«un archivo
de texto con conocimiento estructurado sobre un dominio»*, usado dentro de un
**sistema de información dirigido por ontologías** (*ontology-driven information
system*) — que describe, medio en broma, como una base de datos *on steroids*
(Keet, §1.1).

El problema concreto es la integración de datos. Dos sistemas de la misma
universidad: uno tiene `Student`, otro tiene `AdvancedLearners`. Un `JOIN` no
sirve, porque el problema no es de formato, es de significado. Hace falta un
**vocabulario común y acordado** que diga que ambos denotan lo mismo.

Los ejemplos de aplicación que da van bastante más allá del CRUD: sistemas de
pregunta-respuesta sobre literatura científica, identificación de moléculas
candidatas de caucho, y descubrimiento automatizado de enzimas que superó a
expertos humanos.

## 1.2 — Cómo se ve una ontología

Aquí aparece la **African Wildlife Ontology (AWO)**, el ejemplo que atraviesa todo
el libro. Un mismo axioma —*los leones comen solo herbívoros, y comen algún
impala*— escrito de cuatro maneras:

| Notación | El axioma |
|---|---|
| Lógica de primer orden | `∀x(Lion(x) → ∀y(eats(x,y) → Herbivore(y)) ∧ ∃z(eats(x,z) ∧ Impala(z)))` |
| Lógica descriptiva | `Lion ⊑ ∀eats.Herbivore ⊓ ∃eats.Impala` |
| Lenguaje controlado | «Each lion eats only herbivore and eats some Impala» |
| RDF/XML | `owl:allValuesFrom`, `owl:someValuesFrom`, `rdfs:subClassOf` |

La idea que Keet quiere dejar clavada: **la representación gráfica o textual es
para el humano; la ontología real es la teoría lógica**. El diagrama bonito no es
la ontología, es una vista de ella.

Vale detenerse en el contraste `∀` / `∃` de esa sola línea, porque es el 80% de
los errores de principiante:

- `∀eats.Herbivore` — *si* come algo, es herbívoro. **No obliga a comer nada.** Se
  satisface de forma vacía.
- `∃eats.Impala` — obliga a que exista al menos un impala comido.

## 1.3 — Qué es una ontología (en serio)

Cuatro definiciones, en orden histórico, cada una arreglando a la anterior:

1. **Gruber (1993)** — *«An ontology is a specification of a conceptualization.»*
   La más citada y la más vaga: ni «especificación» ni «conceptualización» están
   definidas.
2. **Studer et al. (1998)** — *«a formal, explicit specification of a shared
   conceptualization.»* Añade *formal*, *explícita* y *compartida*, pero deja sin
   responder qué significa «compartida».
3. **Guarino (1998)** — *«una teoría lógica que da cuenta del significado
   pretendido de un vocabulario formal.»* La más útil operativamente: introduce el
   **compromiso ontológico** y la idea de que los axiomas **restringen los modelos**
   hacia los pretendidos.
4. **Los desarrolladores de OWL (2003)** — *«una ontología equivale a una base de
   conocimiento en lógica descriptiva.»* Keet la marca como indebidamente
   restrictiva: hay ontologías en otros lenguajes formales.

La definición de Guarino es la que conviene interiorizar, porque explica qué se
está haciendo al añadir un axioma: **cada axioma recorta el espacio de
interpretaciones posibles**. Una ontología sin axiomas admite cualquier
interpretación y por tanto no dice nada.

### Ontology con O mayúscula ≠ ontology con o minúscula

- **Ontology** — la disciplina filosófica, milenaria: qué existe y cómo se
  estructura la realidad.
- **ontology** — el artefacto computable.

No es pedantería. Keet lista tres posturas filosóficas que sí cambian lo que uno
mete en el archivo:

| Postura | Los términos refieren a… | Ejemplo |
|---|---|---|
| **Doctrina empirista** | entidades reales independientes de la mente | infección por VIH, jacarandá |
| **Visión conceptualista** | conceptos dependientes de la mente | flogisto, unicornio |
| **Doctrina universalista** | universales que explican el parecido entre individuos | — |

Si se es empirista, `Unicornio` no entra en la ontología. Si se es conceptualista,
sí. La decisión hay que tomarla y sostenerla, no dejarla implícita.

### Ontología vs. base de datos / modelo conceptual

La tabla que hay que memorizar:

| | Ontología | Modelo conceptual / esquema relacional |
|---|---|---|
| Alcance | independiente de la aplicación, orientado al dominio, reutilizable | específico de una aplicación |
| Formalización | teoría lógica explícita | diagramas informales de cajas y líneas |
| Razonamiento | inferencia automatizada de conocimiento nuevo | solo consultas |
| Supuesto | **mundo abierto (OWA)** | **mundo cerrado (CWA)** |

**El supuesto de mundo abierto es la línea que más consecuencias tiene.**

- **CWA** (bases de datos): lo que no está afirmado ni es derivable, es falso. Si
  no hay fila, no existe.
- **OWA** (ontologías): la ausencia de información no implica falsedad. Que no esté
  afirmado no significa que no sea cierto — puede ser cierto y simplemente no
  registrado.

De ahí sale directo el error que este repositorio trae en su propio README:
`domain` y `range` en OWL **no validan datos**. Bajo OWA no pueden rechazar nada;
lo único que pueden hacer es inferir tipos. Declarar `domain` sobre una propiedad
no produce un error ante un dato que no encaja: produce una clasificación
silenciosa que nadie pidió.

### Qué hace buena a una ontología

Keet propone dos ejes —**precisión** (¿representa solo lo pretendido?) y
**cobertura** (¿representa todo lo pretendido?)— y sale una matriz:

| | Cobertura máxima | Cobertura limitada |
|---|---|---|
| **Precisión alta** | buena | mala (falta contenido necesario) |
| **Precisión baja** | menos buena (admite modelos no pretendidos) | peor |

Y tres niveles de error, de más barato a más caro de detectar:

1. **sintáctico** — el archivo no parsea;
2. **lógico** — inconsistencia, clases insatisfacibles; lo detecta el razonador;
3. **semántico** — la formalización es impecable y dice algo distinto de lo que se
   quería decir. Ningún razonador lo detecta. Este es el caro.

## 1.4 — Para qué sirve

**Integración a nivel de esquema.** La ontología es la capa de mapeo autorizada,
por encima de modelos como EER o UML. Cuando se fusionan dos hospitales o dos
universidades, es lo que establece que `Flower` y `Bloem` denotan lo mismo.

**Integración a nivel de instancia.** El ejemplo canónico es la **Gene Ontology**:
vocabularios controlados ligeros con los que bases de datos independientes (KEGG,
InterPro) anotan sus registros con el mismo identificador —`GO:0004619` para
*Phosphoglycerate Mutase Activity*—. La interoperabilidad ocurre *a través de la
GO*, sin armonizar esquemas ni centralizar el almacenamiento.

La diferencia entre ambas es el nivel al que se pega la ontología: al **esquema**
(qué tipos de cosas hay) o a las **tuplas** (esta fila concreta trata de esto).

Otros usos que enumera: **e-learning** (contenido adaptado al perfil del
estudiante), **pregunta-respuesta** (el motor de Watson en *Jeopardy!* combinaba
ontologías con NLP y métodos estadísticos), **humanidades digitales** (OBDA para
que historiadores consulten datos federados de ánforas y comercio de alimentos en
el vocabulario del dominio en vez de SQL), y **flujos de trabajo científicos**
(Taverna, con ontologías de dominio y de minería de datos, para repetibilidad y
procedencia).

## 1.5 — Cómo está armado el libro

Capítulos con referencias cruzadas, recomendaciones de lectura y bibliografía por
capítulo. Es un libro de texto de universidad: da la lógica antes que las recetas
de herramienta.

---

## Lo que hay que llevarse

1. Una ontología es una **teoría lógica**, no un diagrama ni un archivo de
   configuración. Cada axioma restringe modelos.
2. **OWA, no CWA.** No valida; infiere. Este solo punto explica la mayoría de las
   sorpresas con OWL.
3. Los errores **semánticos** —formalizar bien algo distinto de lo que se quería—
   no los detecta ninguna herramienta. Es lo que justifica escribir preguntas de
   competencia.
4. `∀` no obliga a nada; se cumple de forma vacía. Ver el
   [caso de estudio](/capitulos/01-introduccion/caso-de-estudio/), donde eso rompe
   la propia ontología de ejemplo del libro.

## Nota de numeración

Este es el capítulo **1** en la numeración del autor. En LibreTexts aparece bajo
`02%3A_Introduction_to_Ontology_Engineering`, porque esa edición cuenta *«How to
Use the Book»* como capítulo 1. Las secciones citadas aquí como §1.1–1.5 son las
2.1–2.5 de LibreTexts.
