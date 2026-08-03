// Guía de portada: construir una ontología de cero, en el orden en que el libro
// manda hacerlo. No resume capítulos —eso es RESUMEN— sino que los ordena en un
// procedimiento.
//
// Regla de mantenimiento: el ejemplo del taller de bicicletas es ILUSTRATIVO y no
// tiene `verificar.py`. Por eso ninguna `trampa` afirma un resultado de razonador
// sobre el ejemplo: cada una remite al capítulo donde ese fallo SÍ está verificado.
// Si se escribe aquí una afirmación nueva, o remite a un capítulo verificado o no
// se escribe.

export interface Paso {
  n: number;
  titulo: string;
  /** capítulos que respaldan el paso, en el orden en que se consultan */
  donde: { n: number; slug: string }[];
  /** qué se hace, en imperativo */
  hacer: string;
  /** el mismo paso aplicado al ejemplo del taller */
  ejemplo: string;
  /** el error caro de este paso, con el capítulo que lo verifica */
  trampa: string;
}

export const EJEMPLO = {
  titulo: 'El ejemplo que se sigue de principio a fin',
  texto:
    'Un taller de bicicletas con una base de datos de inventario que ya funciona y una pregunta que la base de datos no sabe contestar: <b>«¿qué piezas de las que tengo son compatibles con esta bici?»</b>. Es el caso típico —hay datos, falta significado— y toca casi todos los capítulos. Es un ejemplo <b>ilustrativo</b>: lo verificado con razonador vive en cada capítulo enlazado, no aquí.',
};

export const PASOS: Paso[] = [
  {
    n: 1,
    titulo: 'Escribe qué NO entra',
    donde: [{ n: 5, slug: '05-metodologias' }],
    hacer:
      'Antes que ninguna clase, un párrafo de dominio y alcance. El alcance se define mejor por exclusión: lo que queda fuera es lo que impide que la ontología crezca sin fin.',
    ejemplo:
      'Entra: piezas, montaje, compatibilidad. <b>No entra</b>: precio, cliente, stock, proveedor. El stock cambia cada hora; una ontología no es el sitio donde vive lo que cambia cada hora.',
    trampa:
      'Empezar enumerando conceptos «del dominio». Produce ontologías con todos los sustantivos y ninguna relación — el síntoma exacto de la <a href="/capitulos/05-metodologias/">CQ11 del capítulo 5</a>: las clases están y la pregunta sigue siendo incontestable.',
  },
  {
    n: 2,
    titulo: 'Escribe las preguntas de competencia, con su respuesta esperada',
    donde: [{ n: 5, slug: '05-metodologias' }],
    hacer:
      'Entre 8 y 15 preguntas que la ontología deberá contestar, cada una con la respuesta que se espera. <b>Son la especificación y son las pruebas.</b> Todo lo que no aparezca en ninguna CQ es vocabulario que no hace falta.',
    ejemplo:
      '<code>CQ1</code> ¿qué frenos valen para un cuadro de ruta? → los de llanta y los de disco con anclaje <i>flat mount</i>. <code>CQ2</code> ¿es esta bici eléctrica? → sí, si tiene motor. <code>CQ3</code> ¿qué piezas hay que quitar para sacar el eje? → las que son parte del conjunto de transmisión.',
    trampa:
      'Dar por buena una CQ que «funciona». Hay <b>tres formas de fallar</b> y dos parecen éxitos: contestar vacío —que bajo mundo abierto es «no consta», no «no»— y contestar por accidente. En el <a href="/capitulos/05-metodologias/">capítulo 5</a>, la ontología del libro contesta una CQ solo porque está rota.',
  },
  {
    n: 3,
    titulo: 'Busca lo que ya existe antes de escribir un axioma',
    donde: [
      { n: 7, slug: '07-bottom-up' },
      { n: 5, slug: '05-metodologias' },
    ],
    hacer:
      'Casi nada se construye desde cero: hay tesauros, esquemas de base de datos, modelos UML, vocabularios del sector. Reutilizar es un paso, no un atajo — es lo que separa NeOn de Methontology.',
    ejemplo:
      'La tabla <code>piezas</code> del taller ya tiene los tipos, los diámetros y las claves ajenas. De ahí sale el vocabulario inicial en una tarde; lo que no sale de ahí es el significado.',
    trampa:
      'Traducir el esquema tal cual y creer que las restricciones viajan con él. <a href="/capitulos/07-bottom-up/">Verificado en el capítulo 7</a>: un <code>NOT NULL</code> no sobrevive a la conversión ni como <code>domain</code> ni como <code>∃</code>. La fila que la base de datos rechazaría, OWL la acepta sin decir nada.',
  },
  {
    n: 4,
    titulo: 'Elige el perfil por la operación que debe ser barata',
    donde: [
      { n: 4, slug: '04-owl-2' },
      { n: 8, slug: '08-obda' },
    ],
    hacer:
      'No se elige el perfil más expresivo, se elige el que hace barata la operación que vas a repetir un millón de veces. <b>EL</b> si lo que importa es clasificar una jerarquía enorme; <b>QL</b> si vas a consultar sobre una base de datos; <b>DL</b> completo solo cuando algo lo exija de verdad.',
    ejemplo:
      'El taller consulta contra su inventario: la TBox se escribe en <b>OWL 2 QL</b>, para que la pregunta se pueda reescribir a SQL en vez de mover los datos a la ontología.',
    trampa:
      'Escribir en <code>SROIQ</code> «por si acaso» y descubrir tarde que cierra la puerta al acceso a datos. Y ojo al orden inverso: en el <a href="/capitulos/04-owl-2/">capítulo 4</a>, añadir una cadena de propiedades vuelve <b>ilegal</b> una restricción de cardinalidad que ya estaba escrita, y el razonador rechaza la ontología entera.',
  },
  {
    n: 5,
    titulo: 'Fija las categorías de arriba antes de tocar el dominio',
    donde: [{ n: 6, slug: '06-top-down' }],
    hacer:
      'Decide —y escribe— qué tipos de cosa hay: objetos, procesos, cualidades, roles. Se puede adoptar una ontología fundacional (DOLCE, BFO, GFO) o declarar las cuatro o cinco categorías propias, pero no se puede no decidirlo: elegir el nivel de arriba es elegir <b>qué existe</b>.',
    ejemplo:
      '<code>Pieza</code> es un objeto y <code>Montaje</code> es un proceso. Son categorías distintas, así que <code>Montaje</code> no cuelga de <code>Pieza</code> por muy natural que suene decir «el montaje del freno».',
    trampa:
      'Colgar un proceso de un objeto, o un rol de una clase rígida. Nada de eso produce contradicción: el razonador no protesta jamás. Se caza con OntoClean —<code>Persona</code> bajo <code>Estudiante</code> es el caso canónico— y por eso el <a href="/capitulos/05-metodologias/">capítulo 5</a> insiste en que consistente no es lo mismo que bien modelado.',
  },
  {
    n: 6,
    titulo: 'Modela las relaciones, no solo la taxonomía',
    donde: [{ n: 6, slug: '06-top-down' }],
    hacer:
      'La taxonomía es la parte fácil y la que menos deduce. El trabajo está en las propiedades: cuáles son transitivas, cuáles funcionales, cuál es subpropiedad de cuál, y sobre todo <b>cuántas relaciones distintas esconde la palabra «parte de»</b>.',
    ejemplo:
      'Tres relaciones separadas: <code>parteEstructuralDe</code> (el radio es parte de la rueda, transitiva), <code>montadoEn</code> (la rueda va montada en el cuadro, desmontable) y <code>miembroDe</code> (la bici pertenece a la flota de alquiler).',
    trampa:
      'Meterlas todas en una propiedad transitiva. <a href="/capitulos/06-top-down/">Verificado en el capítulo 6</a>: juntar pertenencia a un grupo con parte estructural hace que el razonador deduzca que la hoja es parte del bosque. La deducción es impecable; la ontología, falsa.',
  },
  {
    n: 7,
    titulo: 'Distingue clase primitiva de clase definida',
    donde: [
      { n: 3, slug: '03-logicas-descriptivas' },
      { n: 4, slug: '04-owl-2' },
    ],
    hacer:
      'Usa <code>≡</code> solo cuando las condiciones sean <b>necesarias y suficientes</b>; en cualquier otro caso, <code>⊑</code>. Esa elección decide qué puede clasificar el razonador solo: con <code>⊑</code> tienes que decir a mano a qué clase pertenece cada cosa.',
    ejemplo:
      '<code>Bicicleta</code> es primitiva: no hay lista cerrada de condiciones que baste. <code>BiciEléctrica ≡ Bicicleta ⊓ ∃tieneParte.Motor</code> es definida — y por eso el razonador etiqueta solo cualquier bici a la que se le añada un motor.',
    trampa:
      'Definir con <code>∀</code> a secas. <code>∀tieneParte.Motor</code> lo cumple también la bici que no tiene ninguna parte: se satisface <b>por vacuidad</b>. La forma correcta es <code>∀ + ∃</code>, y está verificado en los capítulos <a href="/capitulos/01-introduccion/">1</a>, <a href="/capitulos/03-logicas-descriptivas/">3</a> y <a href="/capitulos/05-metodologias/">5</a>. Degradar una definida a primitiva tampoco «pierde precisión»: destruye la subsunción, según el <a href="/capitulos/03-logicas-descriptivas/">capítulo 3</a>.',
  },
  {
    n: 8,
    titulo: 'Corre el razonador desde el tercer axioma, no al final',
    donde: [
      { n: 2, slug: '02-logica-primer-orden' },
      { n: 5, slug: '05-metodologias' },
    ],
    hacer:
      'Clasificar después de cada tanda de axiomas, no cuando esté «terminada». Y cuando algo salga insatisfacible, pedir la <b>justificación</b>: el conjunto mínimo de axiomas culpable. Sin eso, la reparación es a ciegas.',
    ejemplo:
      'Declarar <code>domain(montadoEn) = Cuadro</code> y ver qué se clasifica solo. Si aparece algo raro, mirar la justificación antes de tocar nada.',
    trampa:
      'Reparar donde señala el error. <a href="/capitulos/05-metodologias/">Verificado en el capítulo 5</a>: una clase resulta insatisfacible sin que nadie escribiera una contradicción, y la causa está en un <code>domain</code> lejano. Peor: quitar la disyunción hace desaparecer el síntoma y deja el error de modelado intacto y ya invisible. <code>domain</code> y <code>range</code> <b>no validan</b>, clasifican en silencio.',
  },
  {
    n: 9,
    titulo: 'Conecta los datos donde ya viven',
    donde: [{ n: 8, slug: '08-obda' }],
    hacer:
      'Si los datos están en una base de datos que funciona, no los copies a una ABox: pon la ontología encima y declara los <b>mapeos</b>. La pregunta se reescribe con la TBox y baja a SQL; los datos no se mueven ni se duplican.',
    ejemplo:
      'La tabla <code>piezas</code> se queda donde está. La consulta «¿qué frenos valen para este cuadro?» se reescribe usando la jerarquía de tipos de freno y devuelve filas que ninguna consulta SQL directa habría encontrado.',
    trampa:
      'Consultar sin reescribir y creer que el resultado es el mismo. <a href="/capitulos/08-obda/">Verificado en el capítulo 8</a>: la misma consulta sobre los mismos datos devuelve <code>{}</code> o dos resultados según se use la TBox o no.',
  },
  {
    n: 10,
    titulo: 'Convierte las CQ en un script que falle',
    donde: [{ n: 5, slug: '05-metodologias' }],
    hacer:
      'Cada CQ, una comprobación ejecutable: consulta más respuesta esperada, y salida con código 1 si deja de reproducirse. Es lo más parecido a CI que admite una ontología, y es lo que convierte «buena ontología» en algo que se puede fallar.',
    ejemplo:
      'Un <code>verificar.py</code> que afirma lo que <b>debe</b> deducirse (la bici con motor se clasifica como eléctrica) y también lo que <b>no</b> debe deducirse (el radio no es parte de la flota).',
    trampa:
      'Comprobar solo lo que debe salir. La mitad del valor está en las afirmaciones negativas: son las que detectan que una propiedad se volvió transitiva de más. Y para distinguir «no» de «no consta», la prueba es afirmar lo contrario: si la ontología sigue consistente, era ignorancia —<a href="/capitulos/01-introduccion/">capítulo 1</a>, <a href="/capitulos/05-metodologias/">capítulo 5</a>—.',
  },
  {
    n: 11,
    titulo: 'Pásale los métodos que el razonador no sustituye',
    donde: [{ n: 5, slug: '05-metodologias' }],
    hacer:
      'Cuatro fuentes de evidencia independientes, y ninguna basta sola: razonador (sin insatisfacibles), CQ ejecutadas, <b>OOPS!</b> (pitfalls frecuentes), y <b>OntoClean</b> más <b>RBox Compatibility</b> (errores ontológicos que la lógica tolera sin inmutarse).',
    ejemplo:
      'Comprobar que <code>montadoEn ⊑ parteEstructuralDe</code> tiene dominios <b>contenidos</b> en los del padre, no al revés — es justo lo que detecta RBox Compatibility.',
    trampa:
      'Leer «0 clases insatisfacibles» como aprobado. La ontología del propio libro está consistente y contesta 4 de 11 requisitos: <a href="/capitulos/05-metodologias/">capítulo 5</a>.',
  },
  {
    n: 12,
    titulo: 'Publica en módulos, y con las etiquetas fuera del razonamiento',
    donde: [
      { n: 11, slug: '11-modularizacion' },
      { n: 9, slug: '09-lenguaje-natural' },
    ],
    hacer:
      'IRI estable, versionado, y si la ontología se reparte en módulos, decidir explícitamente qué garantiza cada uno. Las etiquetas en varios idiomas van como anotaciones: no razonan y no deben razonar.',
    ejemplo:
      'Un módulo de <i>piezas y compatibilidad</i> para publicar al proveedor, sin el módulo de montaje. Y <code>rdfs:label</code> en español e inglés sobre los mismos IRI.',
    trampa:
      'Dar por hecho que un módulo correcto conserva las deducciones. <a href="/capitulos/11-modularizacion/">Verificado en el capítulo 11</a>: <b>correcto</b> (no inventa axiomas) y <b>completo</b> (conserva las consecuencias) son independientes, y solo se comprueba el primero. Y alinear términos por el diccionario rompe: en el <a href="/capitulos/09-lenguaje-natural/">capítulo 9</a>, igualar <i>fleuve</i> y <i>rivière</i> con <i>river</i> deja la ontología inconsistente.',
  },
];
