# Criterios de elegibilidad del corpus

> Redactados el 29-9-2026 a partir de las decisiones que constan en `candidatos_log.md` y en
> `inventario.csv`. Durante la búsqueda (septiembre de 2026) se aplicaron caso por caso, pero no se
> habían puesto por escrito. Revisados por BHP el 1-10-2026: se amplían los criterios 1 (biblioteca)
> y 3 (repositorio institucional) para recoger D22 y D12. El 23-10-2026 se revisaron todos los candidatos
> que el registro dejaba sin decisión; entraron cinco documentos (D33-D37) y, por decisión de BHP, se
> precisaron los criterios 1 (entidad titular) y 2 (biblioguías).

Periodo: documentos publicados y accesibles hasta el 30 de septiembre de 2026.

Marco muestral: las 99 universidades del RUCT (`ruct_universidades.csv`). Para cada una se buscó en
la web con el patrón «<universidad> guía/recomendaciones inteligencia artificial generativa
(docencia)» y, cuando hizo falta, dentro del dominio institucional. Como verificación cruzada se usó
el directorio de guías del Observatorio de IA de REBIUN.

Se incluye un documento si cumple los cinco criterios siguientes.

1. **Autoría institucional.** Lo emite la universidad en cuanto institución: el Consejo de Gobierno,
   un vicerrectorado, una delegación del rector o un servicio central, incluida la biblioteca cuando
   da pautas de uso (no solo una lista de recursos), sea cual sea el destinatario (caso D22, UFV). Se excluyen los documentos de centro, de
   departamento, de un título o de autoría individual (p. ej., la guía de la Escola de Enxeñaría de
   Telecomunicación de Vigo o la guía del MUPES de Salamanca). En una universidad privada cuenta también la
   entidad titular cuando dicta pautas para la universidad (D37: la guía de Proeduca, que se cita como de UNIR).
2. **Contenido orientador.** Contiene pautas sobre el uso de la IA generativa en la docencia, el
   aprendizaje o la investigación dirigidas a miembros de la comunidad universitaria. Se excluyen los
   directorios de recursos, las noticias, los anuncios de cursos, los catálogos de herramientas y los
   documentos de estrategia que no contienen orientaciones. Las biblioguías (portales de recursos de la
   biblioteca) se excluyen como género; sí entra un documento de pautas autónomo publicado por la
   biblioteca (D22). Las normas generales (de evaluación, de TFG) con algún artículo sobre IA no se
   consideran guías de IA.
3. **Versión definitiva y pública.** Es de acceso abierto en un dominio oficial, o en un repositorio
   con autoría institucional declarada (caso D12, Universidad Europea, en Zenodo), y está aprobado o
   publicado como definitivo, y es la versión vigente: cuando un documento posterior de la misma universidad
   lo actualiza o lo sustituye, se toma solo el posterior (UNIA v2, Extremadura v2; el informe de la UCM de
   julio de 2023, actualizado por los principios rectores de 2025, D26). Se excluyen los borradores (p. ej.,
   el borrador de normativa de la UDC).
4. **Versión en castellano.** El esquema de anotación se diseñó para la modalidad del español. Se
   excluyen los documentos que solo están disponibles en catalán, gallego, euskera o valenciano.
5. **Sin duplicados.** Una guía común a varias universidades se cuenta una sola vez. Cuando una
   universidad publica varios documentos de género o destinatario distintos (p. ej., Cádiz: PDI y
   alumnado; ULPGC: recomendaciones y declaración), se incluyen todos.

Resultado: 37 documentos de 29 universidades (17 públicas y 12 privadas), repartidas en 9
comunidades autónomas. La decisión sobre cada candidato consta en `candidatos_log.md`.
