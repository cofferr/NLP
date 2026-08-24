"""Esquemas de entrada/salida de la API, con validación estricta según el contrato."""

from typing import Union

from pydantic import BaseModel, field_validator


class TextInput(BaseModel):
    text: Union[str, list[str]]

    @field_validator("text")
    @classmethod
    def validate_text(cls, value):
        if isinstance(value, list):
            if len(value) == 0:
                raise ValueError("La lista de textos no puede estar vacía.")
            for item in value:
                if not isinstance(item, str):
                    raise ValueError("Todos los elementos deben ser strings.")
                if item.strip() == "":
                    raise ValueError("Los textos no pueden estar vacíos o contener solo espacios.")
        else:
            if value.strip() == "":
                raise ValueError("El texto no puede estar vacío o contener solo espacios.")
        return value

    def as_list(self) -> list[str]:
        return self.text if isinstance(self.text, list) else [self.text]

    def is_batch(self) -> bool:
        return isinstance(self.text, list)


class DepInput(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        if value.strip() == "":
            raise ValueError("El texto no puede estar vacío o contener solo espacios.")
        return value


class VectorizeInput(BaseModel):
    documents: list[str]

    @field_validator("documents")
    @classmethod
    def validate_documents(cls, value: list[str]) -> list[str]:
        if len(value) < 2:
            raise ValueError("Se requieren al menos 2 documentos.")
        for item in value:
            if not isinstance(item, str):
                raise ValueError("Todos los elementos deben ser strings.")
            if item.strip() == "":
                raise ValueError("Los documentos no pueden estar vacíos o contener solo espacios.")
        return value


class CleanResponse(BaseModel):
    cleaned_text: list[str]


class PosToken(BaseModel):
    text: str
    pos: str
    lemma: str


class PosResult(BaseModel):
    tokens: list[PosToken]


class PosResponse(BaseModel):
    results: list[PosResult]


class NerEntity(BaseModel):
    text: str
    label: str
    start: int
    end: int


class NerResult(BaseModel):
    entities: list[NerEntity]


class NerResponse(BaseModel):
    results: list[NerResult]


class VectorizeResponse(BaseModel):
    vocabulary: list[str]
    one_hot: list[list[list[int]]]
    bag_of_words: list[list[int]]
    tf_idf: list[list[float]]
