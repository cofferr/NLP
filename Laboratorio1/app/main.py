"""API FastAPI del microservicio de NLP. Agnóstica de la plataforma de despliegue."""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.schemas import (
    CleanResponse,
    DepInput,
    NerResponse,
    PosResponse,
    TextInput,
    VectorizeInput,
    VectorizeResponse,
)
from core.cleaning import clean_texts
from core.dependencies import render_dependencies
from core.ner import extract_entities_batch
from core.pos_lemma import pos_lemma_batch
from core.vectorize import vectorize

app = FastAPI(title="NLP Laboratorio 1")


@app.post("/api/v1/clean", response_model=CleanResponse)
def clean(payload: TextInput) -> CleanResponse:
    cleaned = clean_texts(payload.as_list())
    return CleanResponse(cleaned_text=cleaned)


@app.post("/api/v1/pos", response_model=PosResponse)
def pos(payload: TextInput) -> PosResponse:
    results = pos_lemma_batch(payload.as_list())
    return PosResponse(results=[{"tokens": tokens} for tokens in results])


@app.post("/api/v1/ner", response_model=NerResponse)
def ner(payload: TextInput) -> NerResponse:
    results = extract_entities_batch(payload.as_list())
    return NerResponse(results=[{"entities": entities} for entities in results])


@app.post("/api/v1/visualize/dep", response_class=HTMLResponse)
def visualize_dep(payload: DepInput) -> HTMLResponse:
    svg_html = render_dependencies(payload.text)
    return HTMLResponse(content=svg_html, media_type="text/html")


@app.post("/api/v1/vectorize", response_model=VectorizeResponse)
def vectorize_documents(payload: VectorizeInput) -> VectorizeResponse:
    result = vectorize(payload.documents)
    return VectorizeResponse(**result)
