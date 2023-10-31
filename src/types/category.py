from typing import Optional
from typing_extensions import Self

from sqlalchemy import select
from pydantic import Field, model_validator, PositiveInt, field_validator
from slugify import slugify

from .base import DTO
from .custom_types import AlphaStr
from src.datebase import Category


class CategoryCreateForm(DTO):
    name: AlphaStr = Field(
        default=...,
        min_length=4,
        max_length=64,
        title="Category name",
        description="Main category catalog",
    )

    @field_validator("name", mode="after")
    def category_name_validator(cls, name: str) -> str:
        with Category.session as session:
            category = session.scalar(select(Category).filter_by(name=name))
            if category is not None:
                raise ValueError("category name is not unique")
            return name


class CategoryDetail(CategoryCreateForm):
    id: Optional[PositiveInt] = Field(
        default=None, title="Category ID", description="Main category ID"
    )

    slug: str = Field(
        default=None,
        min_length=4,
        max_length=64,
        title="Slug category",
        description="Slug main category",
    )

    @model_validator(mode="after")
    def slug_create(self) -> Self:
        if self.slug is None:
            self.slug = slugify(self.name)
        return self
