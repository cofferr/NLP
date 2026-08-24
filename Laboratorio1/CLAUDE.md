# CLAUDE.md — Laboratorio I de NLP (spaCy + AWS)

Proyecto en `NLP/Laboratorio1/`. La raíz del repo es `NLP` (pueden existir otros laboratorios
como hermanos de `Laboratorio1` — no asumir que esta carpeta es la raíz).

Microservicio de NLP con spaCy (`es_core_news_sm`) desplegado en dos arquitecturas que deben
responder de forma funcionalmente equivalente ante la misma solicitud (paridad): EC2 con
Docker, y Lambda como imagen de contenedor con Function URL. El contrato completo está en
este archivo — no hay que consultar ningún PDF externo.

## Restricciones no negociables

- No usar `iam:CreateRole`, `iam:AttachRolePolicy` ni crear ningún rol de IAM — AWS Academy
  Learner Lab solo permite usar el `LabRole` precreado.
- No dejar credenciales, tokens ni archivos `.pem` en el repo, en ningún archivo.
- `core/` no debe importar nada de `deploy/ec2` ni `deploy/lambda`, ni al revés. La lógica de
  NLP es agnóstica de cómo se despliega.

## Estructura a construir

```
NLP/Laboratorio1/
├── core/
│   ├── cleaning.py
│   ├── pos_lemma.py
│   ├── ner.py
│   ├── dependencies.py
│   └── vectorize.py
├── app/
│   ├── main.py
│   └── schemas.py
├── deploy/
│   ├── ec2/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   └── lambda/
│       ├── Dockerfile
│       └── handler.py
├── tests/
│   ├── unit/
│   └── smoke/
└── requirements.txt
```

Los workflows de GitHub Actions van en `.github/workflows/` en la raíz del repo (no dentro de
`NLP/Laboratorio1/`), con `paths: ["NLP/Laboratorio1/**"]`.

## Endpoints — contrato exacto

| Capacidad    | Método/ruta                | Entrada                            | Salida                                                                    |
|--------------|------------------------------|---------------------------------------|------------------------------------------------------------------------------|
| Limpieza     | POST /api/v1/clean            | `text`: string o lista de strings      | `cleaned_text`: lista de strings (incluso si la entrada fue individual)      |
| POS          | POST /api/v1/pos              | `text`: string o lista de strings      | `results`: lista; cada item con `tokens` (`text`, `pos`, `lemma`)             |
| NER          | POST /api/v1/ner              | `text`: string o lista de strings      | `results`: lista; cada item con `entities` (`text`, `label`, `start`, `end`)  |
| Dependencias | POST /api/v1/visualize/dep     | `text`: un único string (nunca lista)  | `text/html` con SVG generado por displaCy                                    |
| Vectorización| POST /api/v1/vectorize         | `documents`: lista de ≥2 strings       | `vocabulary`, `one_hot` (lista de matrices), `bag_of_words`, `tf_idf`         |

Para `/pos` y `/ner`, la posición `i` de `results` corresponde al documento `i` de entrada;
el orden del batch debe preservarse.

## `app/schemas.py`

- `TextInput`: `text: Union[str, list[str]]`. Validador que rechaza listas vacías, elementos
  no-string, y textos vacíos o solo espacios. Usado por `/clean`, `/pos`, `/ner`.
- `DepInput`: `text: str` únicamente. Si llega una lista, debe responder 4xx.
- `VectorizeInput`: `documents: list[str]`, `min_length=2`.
- Modelos de salida (`CleanResponse`, `PosToken`, `NerEntity`, `VectorizeResponse`, etc.)
  tipados según la tabla de arriba.
- Cualquier violación de estas reglas → 4xx (422 de FastAPI/Pydantic es válido), nunca
  resultados parciales.

## Reglas de limpieza (`core/cleaning.py`)

- Minúsculas; quitar puntuación (actúa como separador, no debe concatenar los términos que
  separaba); quitar stopwords de spaCy (`Token.is_stop`).
- Conservar tildes, ñ y dígitos. Normalizar espacios en blanco.

## Reglas de vectorización (`core/vectorize.py`) — la parte de mayor peso, verificar con tests a mano

- Vocabulario: términos resultantes de la limpieza, orden lexicográfico ascendente.
- Bag of Words: frecuencia absoluta por término y documento; filas en orden de entrada.
- One-Hot: cada ocurrencia retenida de un término → vector binario de tamaño `|V|` con un
  único 1 en la posición del término.
- TF-IDF: `tf(t,d)` = frecuencia absoluta de `t` en `d`;
  `idf(t) = ln((|D|+1)/(n_t+1)) + 1` (`|D|` = número de documentos, `n_t` = documentos que
  contienen `t`); valor = `tf(t,d) * idf(t)`, sin normalización posterior, redondeado a 4
  decimales.

## Entradas inválidas → 4xx sin resultados parciales

Campos obligatorios ausentes, valores `null`, tipos distintos a los declarados, listas
vacías, elementos no-string, textos vacíos o solo espacios, batch (lista) en
`/visualize/dep`, menos de 2 documentos en `/vectorize`.

## Requisitos no funcionales a cubrir con tests

- Paridad funcional entre EC2 y Lambda ante la misma request.
- Batch conserva orden y correspondencia entrada↔salida.
- Requests equivalentes no dependen de solicitudes previas (sin estado compartido entre
  requests).
- Al menos 5 requests concurrentes manejadas correctamente.
- Limpieza/POS/NER: soportar ≥25 documentos de hasta 1000 caracteres cada uno.
- Vectorización: soportar ≥10 documentos de hasta 1000 caracteres cada uno.
- Cada request válida responde en ≤10s.

## `deploy/ec2/`

- `Dockerfile`: instala `core/` + `app/`, `CMD` arranca
  `uvicorn app.main:app --host 0.0.0.0 --port 8000`.
- `docker-compose.yml`: expone el puerto, `restart: unless-stopped`.

## `deploy/lambda/`

- `Dockerfile`: parte de `public.ecr.aws/lambda/python:3.11` (obligatorio para el runtime de
  contenedor de Lambda), instala `core/` + `app/` + `mangum`, `CMD` = `handler.handler`.
- `handler.py`:
  ```python
  from mangum import Mangum
  from app.main import app

  handler = Mangum(app)
  ```
- No reimplementar lógica aquí — solo empaquetado/arranque sobre `app.main:app`.

## CI/CD — workflows a generar en `.github/workflows/`

- `nlp-lab1-ci.yml`: en push que toque `NLP/Laboratorio1/**` → instalar dependencias, correr
  `pytest tests/unit`. Runner hosted, sin credenciales AWS.
- `nlp-lab1-deploy.yml`: en push a `main` (mismo path filter) o `workflow_dispatch` →
  1) build + push de imagen a ECR, `aws lambda update-function-code` usando
  `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` / `AWS_SESSION_TOKEN` (secrets);
  2) deploy a EC2 por SSH usando el secret `EC2_SSH_KEY` contra el host en la variable
  `EC2_HOST`, ejecutando `docker compose pull && docker compose up -d --build` en la
  instancia; 3) correr `pytest tests/smoke` contra `EC2_HOST` y la URL de Lambda (variable)
  para verificar paridad.

GitHub Secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`,
`EC2_SSH_KEY`. GitHub Variables: `EC2_HOST`, URL de Lambda Function URL, nombre del
repositorio ECR.

## Qué no hacer

- No dupliques lógica de NLP entre `deploy/ec2` y `deploy/lambda`.
- No agregues autenticación ni infraestructura nueva (buckets, roles, colas) sin que se pida.
- No asumas credenciales AWS válidas en tests unitarios — solo `tests/smoke` puede depender
  de servicios desplegados.
