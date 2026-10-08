# Libro de códigos: anotación de directivas en las guías de IA

Versión 1.0 · 28-09-2026

## Unidad de anotación
Una unidad es una oración ortográfica, un elemento de lista o un encabezado del
corpus, tal como la segmentó `01_limpiar_segmentar.py`. Cada unidad se anota
**leyéndola junto con su encabezado inmediato** (columna `encabezado`), porque muchas
guías colocan la fuerza deóntica en el epígrafe («Usos no permitidos») y dejan los
elementos de la lista sin verbo modal.

## Variable 1 · DIR: ¿contiene la unidad un acto directivo o compromisivo?
- **1**: la unidad, leída en su contexto, prescribe, prohíbe, permite o aconseja una
  acción a un agente humano (estudiantado, profesorado, personal, comunidad), o
  compromete a la propia institución a una acción.
- **0**: la unidad describe, explica, informa o valora sin orientar la conducta de
  nadie. También es 0:
  - la modalidad epistémica o dinámica: «la IA puede generar errores», «estas
    herramientas pueden resumir textos»;
  - las preguntas de los apartados de preguntas frecuentes («¿Está permitido…?»),
    salvo que la pregunta sea en sí una exhortación;
  - las instrucciones dirigidas a la máquina, dentro de un ejemplo de *prompt*
    («Simula una entrevista de trabajo…»). En cambio, la instrucción dirigida al
    lector sobre cómo usar la herramienta («Pide a ChatGPT que revise…») sí es
    directiva.
- Si una unidad contiene varias directivas, se anota **la de mayor fuerza**, en este
  orden: PROH > OBL > PERM > REC > COMP. La excepción es cuando una directiva es
  la condición de otra («puedes usarla siempre que lo declares»): entonces se
  anota la **principal**, en ese ejemplo PERM, y la condición queda recogida en
  el campo de ámbito.

## Variable 2 · FUERZA (solo si DIR = 1)
| Código | Definición | Formas típicas |
|---|---|---|
| **OBL** | Obligación: hay que hacer X | *deber* en presente o futuro («deben», «deberá»), *tener que*, *haber de*, *hay que*; «es obligatorio/necesario/imprescindible/preceptivo»; «se exige/requiere»; imperativo afirmativo bajo un epígrafe de normas u obligaciones |
| **PROH** | Prohibición: no se debe o no se permite hacer X | «no debe», «no se puede» (deóntico), «no está permitido», «prohibido», «queda prohibido»; imperativo o exhortativo negativo («no introduzcas», «no copiemos»); calificación sancionadora («se considerará plagio»); elemento de lista bajo «usos no permitidos» o «qué no hacer» |
| **PERM** | Permiso: se puede hacer X | *poder* deóntico con agente humano («el estudiantado puede utilizar…»), «se permite», «está permitido», «se autoriza»; elemento bajo «usos permitidos» o «qué se puede hacer» |
| **REC** | Recomendación: es aconsejable hacer (o no hacer) X | «se recomienda/aconseja/sugiere/anima/invita/alienta», «es recomendable/aconsejable/conveniente», «conviene», *debería* (condicional), *podría* con valor de sugerencia; «es importante/fundamental/esencial/crucial/clave + infinitivo o que»; «evita», «se desaconseja»; imperativo o exhortativo afirmativo fuera de un marco normativo; elemento bajo «recomendaciones» o «buenas prácticas» |
| **COMP** | Compromiso institucional: la universidad se obliga a sí misma | «la universidad se compromete a / promoverá / garantizará / ofrecerá» |

Reglas de decisión:
1. *deber* en condicional («debería») = REC; en presente o futuro = OBL; negado = PROH.
2. *poder* con agente humano y verbo de acción, con valor de licencia = PERM; negado
   = PROH; en condicional con valor de sugerencia («el profesorado podría pedir…»)
   = REC.
3. Los predicados de **necesidad** (necesario, imprescindible, obligatorio) = OBL.
   Los de **importancia** (importante, fundamental, esencial, crucial, clave) = REC.
   Esta división se mantiene en todo el corpus y se discute como decisión
   metodológica.
4. El imperativo afirmativo es REC por defecto; es OBL solo si el epígrafe o el
   contexto inmediato lo enmarcan como norma (p. ej., «Obligaciones», «Normas»).
   El imperativo negativo es PROH.
5. En un elemento de lista sin verbo modal propio, la fuerza es la del epígrafe.

## Variable 3 · DEST: destinatario de la directiva (solo si DIR = 1)
Se anota el agente **recuperable en el texto**, no el destinatario presumible del
documento.
| Código | Criterio |
|---|---|
| **EST** | estudiantado, alumnado, estudiantes, autor o autora de TFG/TFM/tesis; *tú* o *usted* en un documento o apartado dirigido al estudiantado |
| **DOC** | profesorado, docentes, PDI, tutores, directores de TFT, coordinadores; *tú* o *usted* en un documento o apartado dirigido al profesorado |
| **INV** | personal investigador, investigadores, autores de publicaciones científicas |
| **COM** | la comunidad universitaria en su conjunto, «los usuarios», «las personas», *nosotros* inclusivo |
| **INST** | la universidad, sus órganos o servicios (siempre en COMP y cuando la directiva recae en un órgano) |
| **NE** | no especificado: construcción impersonal o predicado evaluativo sin agente recuperable («se recomienda verificar», «es necesario declarar») |

## Variable 4 · ÁMBITO: aquello sobre lo que versa la directiva (solo si DIR = 1)
| Código | Contenido |
|---|---|
| **INTEG** | autoría, plagio, fraude, integridad académica, trabajo propio, exámenes |
| **TRANSP** | declarar, reconocer, citar o documentar el uso de IA |
| **DATOS** | privacidad, datos personales, confidencialidad, propiedad intelectual de lo que se introduce |
| **VERIF** | verificar, contrastar o supervisar los resultados; sesgos; alucinaciones; juicio humano |
| **DOCEN** | diseño docente, evaluación, guía docente, reglas de aula, acompañamiento del estudiantado |
| **APREND** | aprender con IA, no sustituir el esfuerzo, desarrollo de competencias, dependencia |
| **HERRAM** | elección o manejo de herramientas, *prompts*, licencias institucionales |
| **ETICA** | principios generales, bien común, equidad, sostenibilidad, responsabilidad genérica |
| **OTRO** | cualquier otro contenido |

## Formato de salida
Una línea por unidad: `unidad;DIR;FUERZA;DEST;ÁMBITO`. Si DIR = 0, los tres últimos
campos quedan vacíos.

## Validación
La persona experta anota a ciegas, con este mismo libro de códigos, una muestra
aleatoria estratificada por documento. Se calcula el acuerdo con el κ de Cohen en DIR,
FUERZA, DEST y ÁMBITO. Además se revisa una muestra de unidades **no candidatas**,
para estimar cuántas directivas se escapan del filtro automático (tasa de falsos
negativos).

## Reglas añadidas durante la anotación (lote 01)
6. **Condicional instrumental** («si queremos una respuesta correcta, debemos ser
   concretos»): la necesidad depende de un fin que elige el agente = REC.
7. ***Poder* de posibilidad técnica** («podemos construir chats con varios
   interlocutores»): describe lo que la herramienta permite hacer, no una licencia =
   DIR 0. *Poder* es PERM solo cuando concede una licencia de uso.
8. **Directiva incrustada**: la norma que el documento sugiere que otro establezca
   («marcar en el trabajo que se debe indicar el uso») no se cuenta aparte. Se anota
   la directiva principal, dirigida al lector (en ese ejemplo, REC al profesorado).
9. **Negación de una actitud inhibidora** («no debemos tener reparos en usarlas»): se
   anota la fuerza respecto de la acción que se promueve = REC.
10. **Recomendación de un organismo externo citada como pauta** («la UNESCO recomienda
    revisar…»): REC con DEST = NE.
11. **Duplicados** que produce la maquetación (llamadas de texto que repiten un párrafo)
    se anotan igual que el original y se eliminan en el cómputo
    (`03_analisis.py`).

## Reglas añadidas durante la anotación (lote 02)
12. **DEST se resuelve por el contexto**: si la construcción es impersonal («hay que
    declarar su uso», «es necesario verificar») pero el apartado o el documento se
    dirige a un colectivo (epígrafe «Recomendaciones para estudiantes», guía para el
    alumnado), se anota ese colectivo. Orden de decisión: (1) colectivo nombrado en la
    unidad; (2) colectivo del epígrafe o del apartado; (3) destinatario del documento;
    (4) si el documento se dirige a toda la comunidad y nada lo concreta, COM. NE se
    reserva para los casos en que ningún colectivo es identificable. La **expresión lingüística del agente** (explícito u
    omitido) no se anota a mano: se deriva automáticamente de la forma
    (`03_analisis.py`), para no confundir las dos variables.
13. **Advertencia de consecuencias** («puedes incurrir en plagio si copias
    literalmente») = REC (directiva indirecta), salvo que califique la conducta como
    fraude o plagio sin condiciones (= PROH, calificación sancionadora).
14. **Directivas cognitivas** («ten en cuenta que», «piensa que», «recordad que»,
    «no olvidéis que») = REC. Si van con *hay que* o *deber* («hay que tener en
    cuenta») = OBL, por la regla formal.

## Reglas añadidas durante la anotación (lote 03)
15. **Instrucción instrumental sobre el manejo de la herramienta** (cómo redactar un
    *prompt*, cómo darse de alta), cuya razón es la eficacia y no una norma
    = REC, con independencia de la polaridad o del modal («no cometas faltas de
    ortografía en el *prompt*», «la petición debe ser específica»).
16. **Texto generado por la IA y reproducido como ejemplo** (respuestas de ChatGPT,
    *prompts* de muestra, avisos que la propia herramienta añade al final) = DIR 0,
    aunque contenga imperativos o *deber*.
17. **Prueba licencia/posibilidad técnica para *poder***: se parafrasea con «está
    permitido que…» (licencia = PERM) o con «la herramienta hace posible que…»
    (posibilidad técnica = 0). «Con ayuda de ChatGPT, el docente puede diseñar
    actividades» = 0; «el docente puede crear foros de discusión» = PERM.
18. **Descripción del procedimiento de una actividad de ejemplo** («los compañeros
    deben comentar si observan algo incorrecto»): norma interna de la actividad
    descrita = DIR 0, salvo que se presente como pauta para el lector.

## Reglas añadidas durante la anotación (lote 04)
19. **Restricción con «solo/únicamente»**: si restringe el uso a una **autorización**
    («solo úsala cuando se autorice expresamente») = PROH, porque excluye el uso no
    autorizado. Si la restricción se justifica por la calidad o la eficacia («debes
    usarlas únicamente en tareas que controles») se mantiene la fuerza de la forma
    base (*deber* = OBL; imperativo = REC).
20. **Instrucciones de navegación y paratexto** («amplía la información en…»,
    «accede a la lista», nota de licencia Creative Commons de la propia guía) = DIR 0.
21. **Advertencia que emite la propia guía** («es importante advertir que estos
    sistemas generan errores», «es importante hacer notar que…»): el agente de
    *advertir* es el documento, no el lector = DIR 0. En cambio, «es fundamental
    tener en cuenta que…» dirige una acción cognitiva al lector = REC.

## Reglas añadidas durante la anotación (lote 05)
22. **Futuro institucional en declaraciones** («se evitarán los sesgos», «se
    implementará un sistema de auditoría», «formar a la comunidad» en una lista de
    compromisos) = COMP, DEST = INST.
23. **Destinatario doble** («profesorado y alumnado deberán…») = COM.
24. **Requisitos sobre los sistemas de IA sin agente humano recuperable** («una IA debe
    ser lícita, ética y robusta») = OBL con DEST = NE.

## Reglas añadidas durante la anotación (lote 06)
25. **Permiso general de uso sin ámbito concreto** («se permite el uso de la IA en
    todos los ámbitos») = ÁMBITO HERRAM. Si el permiso se circunscribe a los estudios
    del estudiantado, = APREND; si se circunscribe a la docencia, = DOCEN.
26. **Medidas institucionales de acompañamiento** que el documento enumera (formación,
    campañas) = COMP, DEST = INST.

## Reglas añadidas durante la anotación (lotes 07-08)
27. **Definición de niveles de una escala o de escenarios de evaluación** (p. ej., la
    AI Assessment Scale: «nivel 1: no se debe usar IA en ningún momento») = DIR 0 cuando
    se presenta como repertorio de opciones que el docente puede adoptar; si el documento
    fija el escenario como norma para el estudiantado («el alumnado no puede usar la IA
    en exámenes…»), se anota la fuerza correspondiente.
28. **Plantillas y formularios** (declaración de uso tipo) = DIR 0.
29. **Infinitivo negativo en una lista** («No compartir documentos personales…») = PROH,
    igual que el imperativo negativo.
30. **Nominalizaciones en listas de recomendaciones dirigidas a la institución**
    («Creación de campañas de concienciación», «Integración de la IA en los planes de
    estudios») = REC, DEST = INST. Las funciones que se atribuyen a un órgano que se
    propone crear (un observatorio) = DIR 0.
31. **Listas de comprobación en forma de pregunta** («¿He verificado la credibilidad de
    las fuentes…?») = REC: la pregunta funciona como pauta de autoevaluación.
32. **Indicadores de una rúbrica de evaluación** («Identifica las bases de datos
    utilizadas…») = DIR 0: describen el desempeño esperado, no dirigen la conducta del
    lector. Si el indicador incluye un modal («deben estar claramente presentes»), se
    anota.
33. **Ejercicios sugeridos** («Como ejercicio, puedes preguntar a…») = PERM; en imperativo
    («Prueba a subir un PDF…») = REC.

## Revisión del filtro y lote 25 (29-09-2026)
Al revisar la extracción se detectaron tres fuentes de falsos negativos del filtro automático:
(a) guiones blandos del maquetado (U+00AD) que partían palabras en D08 y D25; (b) imperativos en
mayúscula inicial que spaCy etiqueta como nombres propios o indicativos («Evita», «Lee», «Sé»,
«No introduzcas»); (c) listas de compromisos institucionales en infinitivo bajo epígrafes con
*compromiso*, y siglas sin artículo en el patrón de compromiso («UNIR se compromete»). Se
corrigieron `01_limpiar_segmentar.py` y `02_candidatas.py` (los identificadores de unidad no
cambian) y se anotaron las candidatas nuevas. Como D09 y D13 presentan además palabras partidas
por espacios en la extracción del PDF, en esos dos documentos se anotaron **todas** las unidades,
candidatas o no. Reglas aplicadas:
34. **Infinitivo bajo un epígrafe de compromiso institucional** («Apoyar al alumnado para que…»
    bajo «Compromiso público de Deusto») = COMP, DEST = INST.
35. **Rótulo nominal de un principio o una buena práctica** («Uso limitado de herramientas»,
    «Políticas claras y coherentes») = DIR 0; la directiva está en la oración que lo desarrolla.
    El rótulo en infinitivo («Alfabetizar al alumnado», «Impulsar la interacción») = REC, porque
    tiene forma verbal exhortativa.
(Los indicadores de evaluación en tercera persona siguen la regla 32.)

## Aclaración (29-09-2026): ÁMBITO de los permisos condicionados
36. **Permiso condicionado a otra directiva** («puedes usarla siempre que lo declares»,
    «está permitido siempre que se cite»): FUERZA = la directiva principal (PERM) y
    ÁMBITO = el de la **condición** (en esos ejemplos, TRANSP), tal como indica la
    variable 1. Se aplica cuando la condición es una acción que el destinatario debe
    cumplir (declarar, citar, no comprometer la autoría, que el profesorado revise la
    nota). Si la condición es solo una excepción o una circunstancia («salvo que se
    indique lo contrario», «si el equipo docente no se siente cómodo»), no es una
    directiva y el ÁMBITO es el de la acción principal. Si hay varias condiciones, cuenta
    la que debe cumplir el destinatario de la directiva. Se revisaron con este criterio
    los diez permisos condicionados del corpus (lote_26_correcciones).
