from typing import Any

from pydantic import BaseModel, Field, ConfigDict


class CalculatorParameters(BaseModel):
    expression: str = Field(
        ...,
        description="Mathematical expression to evaluate"
    )


class FilesystemParameters(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str = Field(
        ...,
        description="Path of the file or directory."
    )


class GitParameters(BaseModel):
    """
    Parameters for Git status.
    """

    model_config = ConfigDict(extra="forbid")


class PostgreSQLParameters(BaseModel):
    """
    Parameters for PostgreSQL operations.
    """

    model_config = ConfigDict(extra="forbid")

    sql: str = Field(
        ...,
        description="SQL query to execute."
    )


class RAGParameters(BaseModel):
    """
    Parameters for RAG operations.
    Currently no additional parameters are required.
    """

    model_config = ConfigDict(extra="forbid")