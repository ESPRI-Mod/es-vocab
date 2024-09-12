import sqlalchemy as sa
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.dialects.sqlite import JSON

class PkMixin:
    pk: int | None = Field(default=None, primary_key=True)


class IdMixin:
    id: str


class VersionMixin:
    version: int | None = Field(default=None, primary_key=True)


class Universe(SQLModel, PkMixin, VersionMixin, table=True):
    __tablename__ = "universes"
    data_descriptors: list["DataDescriptor"] = Relationship(back_populates="universe")


class DataDescriptor(SQLModel, PkMixin, IdMixin, table=True):
    __tablename__ = "data_descriptors"
    universe_pk: int | None = Field(default=None, foreign_key="universes.pk")
    universe: Universe = Relationship(back_populates="data_descriptors")
    terms: list["Term"] = Relationship(back_populates="data_descriptor")


class Term(SQLModel, PkMixin, IdMixin):
    json_content: dict = Field(sa_type=JSON)


class UniverseTerm(Term, table=True):
    __tablename__ = "u_terms"
    data_descriptor_pk: int | None = Field(default=None, foreign_key="data_descriptors.pk")
    data_descriptor: DataDescriptor = Relationship(back_populates="terms")


class UniverseTermPattern(Term, table=True):
    __tablename__ = "u_term_patterns"
    data_descriptor_pk: int | None = Field(default=None, foreign_key="data_descriptors.pk")
    data_descriptor: DataDescriptor = Relationship(back_populates="terms")
    regex: str


class UniverseTermComposite(Term, table=True):
    __tablename__ = "u_term_composites"
    data_descriptor_pk: int | None = Field(default=None, foreign_key="data_descriptors.pk")
    data_descriptor: DataDescriptor = Relationship(back_populates="terms")
    separator: str | None
    parts: list["UniverseCompositePart"] = Relationship(back_populates="composite")


class UniverseCompositePart(SQLModel, PkMixin, IdMixin, table=True):
    __tablename__ = "composite_parts"
    rank: int
    is_required: bool
    composite_pk: int | None = Field(default=None, foreign_key="u_term_composites.pk")
    composite: UniverseTermComposite = Relationship(back_populates="parts")


class Project(SQLModel, PkMixin, IdMixin, VersionMixin, table=True):
    __tablename__ = "projects"
    collections: list["Collection"] = Relationship(back_populates="project")


class Collection(SQLModel, PkMixin, IdMixin, table=True):
    __tablename__ = "collections"
    project_pk: int | None = Field(default=None, foreign_key="projects.pk")
    project: Project = Relationship(back_populates="collections")
