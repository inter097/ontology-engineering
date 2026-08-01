---
titulo: 'OBDA: la ontología encima de la base de datos, no en lugar de ella'
capitulo: 8
descripcion: 'Acceso a datos mediado por ontologías: reescritura de consultas, mappings y por qué la TBox tiene que ser pequeña. El ejemplo del libro ejecutado — la misma pregunta y los mismos datos devuelven tres respuestas distintas.'
keet: 'cap. 8 (Ontology-Based Data Access), §8.1–8.5'
hallazgo: 'La misma consulta sobre los mismos datos devuelve {} o {Mkhize, Naidoo} según se reescriba o no con la TBox; y ni siquiera razonando aparece en una fila el departamento cuya existencia la ontología garantiza.'
cifras:
  - valor: '3'
    etiqueta: 'respuestas a la misma consulta'
  - valor: 'QL'
    etiqueta: 'perfil de la TBox'
  - valor: '8'
    etiqueta: 'comprobaciones'
---

Los capítulos anteriores tratan la ontología como el sitio donde vive todo. Aquí no:
los datos se quedan **en la base de datos** —gigas o teras que no caben en un archivo
OWL— y la ontología queda encima como capa semántica. Es la forma en que las
ontologías entran en sistemas que ya existen.

Keet lo resume desde los dos lados: para el ingeniero del conocimiento es
*«representación del conocimiento + muchos datos»*; para el de bases de datos,
*«base de datos + conocimiento de fondo»*.

## El ejemplo que justifica el capítulo entero (§8.2)

```
Professor(Mkhize)        dato, en la base de datos
Professor ⊑ Employee     conocimiento, en la ontología
```

Consulta: *«lista todos los empleados»*.

- **Solo base de datos**: `{}`. No hay ninguna fila marcada como empleado.
- **Solo ontología**: no sabría si hay alguno.
- **Las dos juntas**: `{Mkhize}`, que es lo que cualquiera esperaría al leerlo.

## Dos maneras de conseguirlo (§8.2)

La complejidad de OWL 2 DL respecto a los datos es decidible pero abierta, y respecto
a la consulta ni siquiera se sabe si es decidible (cap. 4). Traducido: **no se puede
hacer con la lógica entera**. Hay dos vías para volverlo tratable, y la primera tiene
dos variantes:

1. **Restringir la TBox** hasta un lenguaje minimalista —`DL-Lite`, o sea **OWL 2
   QL**— y entonces:
   - **v1**: meter la parte relevante de la TBox **en la consulta** y evaluarla contra
     los datos tal como están;
   - **v2**: completar la ABox con lo que la TBox implica y luego consultar.
2. **Restringir las consultas** a aquellas cuya respuesta no dependa de qué modelo se
   elija.

La arquitectura que describe el capítulo es la opción **1-v1**: la ontología no toca
los datos, **transforma la pregunta**.

<details class="peras">
<summary>¿Y esto qué quiere decir? Sin jerga</summary>

Tienes un fichero enorme de personal donde cada ficha pone el puesto: *profesor*,
*limpiadora*, *conserje*. En ninguna pone «empleado».

Alguien pide la lista de empleados. Hay dos formas de resolverlo.

**La primera**: coger el fichero entero y añadir a mano la etiqueta «empleado» a cada
ficha. Funciona, pero hay que tocar el fichero, tarda, y hay que repetirlo cada vez
que entra una ficha nueva.

**La segunda**: no tocar nada y **cambiar la pregunta**. En vez de buscar «empleado»,
buscar «profesor o limpiadora o conserje», porque ya se sabe que esos son los tipos
de empleado que hay. El fichero se queda como está y la respuesta es la misma.

La segunda es lo que hace un sistema OBDA. Y explica de golpe dos cosas: por qué la
ontología puede ser pequeña —solo necesita saber lo justo para reescribir la
pregunta— y por qué tiene que serlo — si la ontología dijera cosas muy complicadas,
la pregunta reescrita sería impracticable, o directamente no existiría.

</details>

## Componentes (§8.3, §8.4)

**Estáticos:** un lenguaje de ontologías (de la familia `DL-Lite`, ≈ OWL 2 QL); un
**lenguaje de mappings**, que declara qué consulta SQL produce las instancias de cada
clase o propiedad de la ontología; y los datos, en un gestor relacional normal.

**En tiempo de consulta:** razonamiento **sobre la TBox** (no sobre los datos),
**reescritura** de la consulta con lo que dice la TBox, **desdoblado** (*unfolding*)
de esa consulta usando los mappings hasta convertirla en SQL, y la base de datos
haciendo lo que sabe hacer.

Lo importante de ese reparto: **el razonamiento pesado ocurre sobre la TBox, que es
pequeña; los datos los mueve el gestor relacional, que para eso está.** Ninguna de las
dos partes hace el trabajo de la otra.

---

# Caso de estudio: la misma pregunta, tres respuestas

Reproducible con:

```bash
cd capitulos/08-obda/artefactos
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
./.venv/bin/python verificar.py     # necesita Java en el PATH
```

Los datos —el papel de la base de datos— son tres hechos: `Professor(Mkhize)`,
`Cleaner(Naidoo)`, `worksFor(Mkhize, Informatica)`. La ontología añade
`Professor ⊑ Employee` y `Cleaner ⊑ Employee`. La consulta, en SPARQL, es siempre la
misma pregunta: *«lista todos los empleados»*.

## A. Example 8.1, ejecutado

```
[ok] solo datos, sin ontología:                          {}
[ok] con la ontología cargada, consulta tal cual:        {}
[ok] consulta REESCRITA con la TBox (v1 de §8.2):        {Mkhize, Naidoo}
[ok] ABox COMPLETADA y consulta tal cual (v2 de §8.2):   {Mkhize, Naidoo}
```

<p class="evidencia">misma pregunta, mismos datos: {} frente a {Mkhize, Naidoo}</p>

La segunda línea es la que enseña algo. **Tener la ontología cargada no sirve de
nada por sí solo**: mientras la consulta pregunte literalmente por `Employee` y los
datos digan `Professor`, la respuesta es vacía. El conocimiento tiene que entrar
*por algún sitio* — o en la consulta, o en los datos. No hay una tercera forma, y esa
disyuntiva es exactamente v1 frente a v2 de §8.2.

La reescritura es literal: la consulta pasa de preguntar por `Employee` a preguntar
por `Employee` **y todo lo que esté por debajo suyo en la jerarquía**. En un sistema
real ese paso lo hace el motor OBDA con la TBox en `DL-Lite`, y después el *unfolding*
lo convierte en SQL contra las tablas reales.

## B. Lo que OBDA no arregla: la negación

```
[ok] «empleados sin departamento» → {Naidoo}
[ok] añadiendo Employee ⊑ ∃worksFor.Department → SIGUE devolviendo {Naidoo}
```

<p class="evidencia hipotesis">la ontología garantiza que Naidoo tiene departamento; la consulta lo lista como si no</p>

Aquí hay dos mundos chocando. La consulta con `NOT EXISTS` es **de mundo cerrado**:
pregunta por lo que está materializado. La ontología es **de mundo abierto**: al
añadir `Employee ⊑ ∃worksFor.Department` afirma que el departamento de Naidoo
**existe** — sencillamente no consta cuál.

Las dos afirmaciones son ciertas a la vez y se contradicen en la práctica. El sistema
devuelve a Naidoo en la lista de «empleados sin departamento» aunque la ontología
acaba de garantizar que tiene uno.

## C. Qué parte del conocimiento llega a las filas

```
[ok] el departamento de Naidoo NO aparece como valor
[ok] las subsunciones SÍ: completada la ABox, Mkhize tiene los dos tipos
```

Y aquí está la razón de fondo de por qué la TBox de un sistema OBDA se limita a
**OWL 2 QL**:

- una **subsunción** se traduce a una consulta más ancha — es una unión, y SQL sabe
  hacer uniones;
- un **existencial** no se traduce a nada: afirma que hay un objeto que **no está en
  ninguna tabla**, y ninguna consulta SQL puede devolver una fila que no existe.

<details class="errata">
<summary>El malentendido que este caso deshace</summary>

La expectativa razonable al montar un sistema OBDA es: *«la ontología añade
conocimiento, así que las consultas devolverán más y mejores respuestas»*.

Devuelven más respuestas **de un solo tipo**: las que se consiguen ensanchando la
pregunta. Todo lo que la ontología sabe y no se puede expresar como «busca también
por aquí» simplemente no llega a los datos. El conocimiento existencial es el caso
claro: está en la teoría, es cierto, y es invisible desde SQL.

De ahí la observación del Exercise 8.1 —la «ontología» de un sistema OBDA se parece
sospechosamente a un modelo conceptual OWLizado—: no es dejadez de sus autores, es
que **el resto del conocimiento no serviría para nada ahí**. Lo que no reescribe la
consulta, sobra.

Consecuencia práctica al diseñar: la ontología de acceso a datos y la ontología de
dominio **no tienen por qué ser la misma**, y normalmente no deberían serlo. Una es
pequeña, en QL, y existe para reescribir; la otra es todo lo expresiva que el dominio
pida y existe para razonar.

</details>

## Qué deja el caso

1. **Cargar la ontología no cambia ninguna respuesta.** El conocimiento entra por la
   consulta (v1) o por los datos (v2), y hay que elegir cuál.
2. **La reescritura es una unión.** Por eso escala, y por eso solo funciona con un
   fragmento pequeño del lenguaje.
3. **La negación de la consulta y el mundo abierto de la ontología no se hablan.**
   Es la fuente más común de resultados absurdos en un sistema OBDA.
4. **QL no es OWL 2 DL recortado por capricho**: es exactamente lo que se puede
   convertir en SQL.

---

## Los ejercicios (§8.5)

**Review question 8.1.** *«Describe in your own words what an OBDA system is»* —en
menos de 30 segundos, como pide el enunciado—: **Una ontología puesta encima de una
base de datos que ya existe. Los datos no se mueven: cuando alguien pregunta en el
vocabulario de la ontología, el sistema usa lo que la ontología sabe para reescribir
esa pregunta en SQL contra las tablas reales. Así se consulta por conceptos que no
están en ninguna columna.**

**Review question 8.2.** *«What are the principal components?»* — Estáticos: lenguaje
de ontologías (`DL-Lite` ≈ OWL 2 QL), lenguaje de **mappings** entre el vocabulario de
la ontología y las consultas SQL que lo pueblan, y los datos en un gestor relacional.
En tiempo de consulta: razonamiento sobre la TBox, **reescritura**, **unfolding** con
los mappings, y la tecnología relacional de siempre.

**Review question 8.3.** *«How is querying in the OBDA setting different compared to a
plain relational database?»* — En tres cosas. (1) Se pregunta en el vocabulario de la
ontología, que no coincide con el esquema. (2) La respuesta son **certain answers**:
lo que se sigue en **todos** los modelos, no lo que hay en la tabla — es la noción de
consecuencia del [capítulo 2](/capitulos/02-logica-primer-orden/) aplicada a
consultas. (3) La misma consulta puede devolver más filas sin que los datos hayan
cambiado, porque el conocimiento la ensanchó; **verificado en la parte A del caso de
estudio**. *Criterio propio: y una cuarta que el enunciado no pide — la negación no
significa lo mismo, como enseña la parte B.*

**Exercise 8.1.** *«Why does the ‘ontology’ in an OBDA system look more like an
OWLized conceptual data model?»* — Porque en OBDA solo es útil el conocimiento que se
puede convertir en reescritura de consultas: jerarquías, dominios y rangos,
disyunciones, cardinalidades simples. Es justo el contenido de un modelo conceptual.
Todo lo demás —definiciones con condiciones suficientes, negación, existenciales
complejos, alineamiento con una fundacional del [capítulo 6](/capitulos/06-top-down/)—
no llega a los datos, **y está verificado en la parte C**: un existencial de la TBox
no produce ni una fila. A eso se suma el límite de expresividad de OWL 2 QL, que
directamente no admite buena parte de esas construcciones. *Criterio propio: la
conclusión defendible no es que esas ontologías sean pobres, sino que están
**optimizadas para otra cosa**; y que conviene mantener separadas la ontología de
acceso a datos y la de dominio.*

**Exercise 8.2.** *«You will set up an OBDA system»* con Ontop y los datos de ejemplo.
— Montar Ontop, PostgreSQL y sus mappings queda fuera de lo que `verificar.py` puede
reproducir sin infraestructura externa, así que **no se afirma aquí ningún resultado
obtenido con Ontop**. Lo que sí está ejecutado es el mecanismo que hay debajo: la
reescritura (v1) y la completitud de la ABox (v2) del §8.2, sobre el propio ejemplo
del libro. *Criterio propio: la pieza que falta por probar de verdad es el lenguaje de
mappings, que es donde se concentran los errores en un proyecto real — un mapping mal
escrito no da error, da filas de más o de menos, exactamente igual que un `domain` mal
puesto.*

---

## Lo que hay que llevarse

1. **Los datos se quedan donde están.** OBDA no migra: reescribe.
2. **La ontología aquí es una herramienta de consulta**, no un modelo del dominio, y
   por eso es pequeña y está en QL.
3. **Certain answers ≠ filas de una tabla.** Lo que se devuelve es lo que se sigue en
   todos los modelos.
4. **Mundo abierto y `NOT EXISTS` conviven mal.** Hay que saberlo antes de escribir
   informes con esas consultas.

<small>Salvo los enunciados citados, el análisis y las resoluciones de esta página
son criterio propio, verificados con HermiT y el motor SPARQL de owlready2.
Numeración y enunciados tomados del PDF en
<a href="https://github.com/inter097/ontology-engineering/tree/main/libro">/libro</a>,
no de ediciones web que renumeran las secciones.</small>

<details class="defensa">
<summary>Para la defensa — lo que te van a preguntar de aquí</summary>

**«¿Por qué no metes los datos en la ontología y te ahorras la complicación?»**

Porque no caben y porque no hace falta. Los volúmenes de un sistema real están en
gigas o teras y el razonamiento sobre ABox de ese tamaño no es viable —la complejidad
de OWL 2 DL respecto a los datos es decidible pero abierta (cap. 4)—. OBDA reparte el
trabajo: el razonamiento ocurre sobre la TBox, que es pequeña, y los datos los mueve
el gestor relacional. Además evita duplicar y desincronizar la fuente de verdad.

**«¿Qué gana el usuario si la base de datos ya responde a sus consultas?»**

Preguntar por conceptos que no están en ninguna columna. Está verificado con el
ejemplo del propio libro: la consulta «lista todos los empleados» devuelve `{}` sobre
los datos —nadie está marcado como empleado— y devuelve `{Mkhize, Naidoo}` en cuanto
la TBox entra en juego. Mismos datos, misma pregunta.

*El matiz que conviene añadir:* tener la ontología cargada **no basta**. Si la consulta
no se reescribe o la ABox no se completa, la respuesta sigue siendo `{}` — también
verificado. El conocimiento no se aplica solo.

**«¿Por qué OWL 2 QL y no la ontología completa?»**

Porque QL es exactamente el fragmento que se puede convertir en SQL. Una subsunción se
traduce a una unión; un existencial no se traduce a nada.

*Por qué es una respuesta fuerte:* está medido en el caso de estudio. Con
`Employee ⊑ ∃worksFor.Department` en la TBox, el departamento de Naidoo **no aparece
en ninguna fila**: la ontología garantiza que existe y ninguna consulta puede
devolverlo, porque no está en ninguna tabla. Ese es el límite, y no es de
implementación: es lógico.

**«¿Los resultados de un sistema OBDA son fiables para tomar decisiones?»**

Los positivos sí: son *certain answers*, lo que se sigue en todos los modelos. Las
**ausencias**, no. Una consulta con `NOT EXISTS` opera en mundo cerrado sobre lo
materializado, mientras la ontología razona en mundo abierto; en el caso de estudio,
Naidoo aparece en la lista de «empleados sin departamento» **justo después** de que la
ontología haya afirmado que tiene uno. Los informes basados en ausencias hay que
escribirlos sabiendo esto.

**«Tu ontología de OBDA parece un diagrama entidad-relación con otro nombre.»**

Lo parece, y es correcto que lo parezca. En OBDA solo es útil el conocimiento que se
convierte en reescritura de consultas, y eso es justo el contenido de un modelo
conceptual. La conclusión que se sigue —y que se aplica en este trabajo— es que la
ontología de acceso a datos y la ontología de dominio son **dos artefactos
distintos**: una pequeña y en QL para consultar, otra expresiva para razonar.

</details>
