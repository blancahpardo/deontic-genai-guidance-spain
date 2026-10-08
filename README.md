# Deontic modality in generative AI guidance from Spanish universities

[![DOI](https://zenodo.org/badge/1410427162.svg)](https://doi.org/10.5281/zenodo.23242833)

Data and code for a corpus study of how Spanish universities regulate the use of generative artificial
intelligence (GenAI) through the language of their institutional guidance. The study analyses 32 documents
issued by 26 universities (120,225 words; 5,317 sentences and list items) and annotates every unit for
directive status, deontic force, addressee and domain. It identifies 1,793 directives.

Author: Blanca Hernández Pardo, Universidad Pontificia Comillas
([ORCID 0000-0001-9005-7577](https://orcid.org/0000-0001-9005-7577)) · bhpardo@comillas.edu

## What the repository contains

| Folder / file | Content |
|---|---|
| `corpus/inventario.csv` | The 32 documents: university, ownership, region, title, issuing body, date, addressee, genre, format and URL |
| `corpus/criterios_elegibilidad.md` | Sampling frame and the five eligibility criteria (in Spanish) |
| `corpus/candidatos_log.md` | Search log: every candidate document found, with its URL and the decision taken (in Spanish) |
| `corpus/ruct_universidades.csv` | Sampling frame: the 99 universities in the Spanish Register of Universities, Centres and Degrees (RUCT) |
| `corpus/checksums_raw.csv` | SHA-256 checksum of each source file as downloaded, to check that a new download is the same version |
| `corpus/extraer*.py` | Text extraction from the downloaded PDF and HTML files |
| `analisis/libro_de_codigos.md` | Annotation codebook: variables, categories and the 36 decision rules (in Spanish) |
| `analisis/01_…07_*.py` | Cleaning and segmentation, candidate filter, analysis, figures, validation samples, Cohen's κ, robustness checks |
| `analisis/anot/` | Annotation of every unit, in batches (see below) |
| `analisis/resultados/` | Results tables; `directivas.csv` lists the 1,793 directives with their text and all variables |
| `validacion/` | Blind expert validation: annotation instructions, samples with the expert labels, and sample keys |
| `figuras/` | Figures 1 and 2 |

### Annotation files

Each line of `analisis/anot/lote_*.csv` is `unit;DIR;FUERZA;DEST;AMBITO`, where `unit` is the identifier
of a sentence or list item (`D01-0009` = document D01, unit 9). DIR is 1 for a directive and 0 otherwise.
FUERZA is the deontic force: OBL obligation, PROH prohibition, PERM permission, REC recommendation, COMP
institutional self-commitment. DEST is the addressee: EST students, DOC teaching staff, INV researchers,
COM whole community, INST the institution, NE unspecified. ÁMBITO is the domain: INTEG integrity, TRANSP
transparency/disclosure, DATOS data and privacy, VERIF verification of outputs, DOCEN teaching and assessment
design, APREND learning, HERRAM tool use, ETICA general ethics, OTRO other. When a unit appears in more than
one batch, the later batch prevails.

- `lote_01`–`lote_24`: units selected by the rule-based candidate filter.
- `lote_25`: exhaustive annotation of two documents whose PDF extraction split words, and units added by the revised filter.
- `lote_26_correcciones`: corrections after the codebook was revised.
- `lote_27`–`lote_52`: every unit rejected by the filter (exhaustive annotation).
- `lote_53_muestra_nc_BHP`: the expert labels adopted for the 100 rejected units of the first validation sample.

### Validation

| Sample | Units | Agreement (Cohen's κ) |
|---|---|---|
| Training round (`validacion/ronda1_entrenamiento/`) | 388 | used to calibrate the codebook; not reported |
| Validation sample (`muestra_validacion_ronda2_BHP.xlsx`) | 306 candidates + 100 rejected units | DIR .81 · FUERZA .96 · DEST .91 · ÁMBITO .74 |
| Check of the exhaustive annotation (`comprobacion_no_candidatas_BHP.xlsx`) | 150 rejected units | DIR .87 · FUERZA .76 · DEST .90 · ÁMBITO .74 |

The expert annotated blind, without access to the model's labels. The column of the expert's free-text comments
has been left empty in the published spreadsheets; the labels are complete. `analisis/06_kappa.py` recomputes the
figures from the spreadsheets and the keys.

## Use of a large language model

The annotation was carried out with the assistance of a large language model (Claude Opus 5.5, Anthropic,
through Claude Code, September–October 2026). The model received the codebook and batches of about one
hundred units and returned one line per unit; the author validated the annotation against the blind samples
above. The model also assisted in writing the scripts.

## The texts of the documents are not included

The guidance documents belong to the universities that issued them and are not redistributed here. Each one
can be downloaded from the URL in `corpus/inventario.csv`; three of them were retrieved from the Internet
Archive, as the column `via_descarga` indicates. The guide of the University of Málaga (D23) was compiled from six
chapter pages, and the four documents of Loyola University (D29–D32) come from a single web portal. Web documents
may change: compare a new download with `corpus/checksums_raw.csv` before relying on the unit identifiers.

## How to reproduce the analysis

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
# 1. download each document to corpus/raw/<archivo>.pdf or .html (file names in corpus/inventario.csv)
cd corpus && mkdir -p txt && ../.venv/bin/python extraer.py && ../.venv/bin/python extraer_pdf_bloques.py && cd ..
# 2. segment, filter, analyse
.venv/bin/python analisis/01_limpiar_segmentar.py
.venv/bin/python analisis/02_candidatas.py
.venv/bin/python analisis/03_analisis.py
.venv/bin/python analisis/04_figuras.py
.venv/bin/python analisis/07_robustez.py
# 3. agreement
.venv/bin/python analisis/06_kappa.py
.venv/bin/python analisis/06_kappa.py validacion/comprobacion_no_candidatas_BHP.xlsx validacion/clave_comprobacion.csv
```

Steps 2 and 3 read the annotation batches in `analisis/anot/`; the model is not called again.

## Licence

Data and documentation: CC BY 4.0. Scripts: MIT. Excerpts from the universities' documents are not covered
by either licence; see `LICENSE-DATA.md`.

## How to cite

Hernández Pardo, B. (2026). *Deontic modality in generative AI guidance from Spanish universities: Corpus inventory,
annotations, validation data and analysis scripts* (Version 1.0.0) [Data set]. Zenodo.
https://doi.org/10.5281/zenodo.23242834

The DOI [10.5281/zenodo.23242833](https://doi.org/10.5281/zenodo.23242833) always points to the latest version.
