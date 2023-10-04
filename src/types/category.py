from typing import Self

from pydantic import Field, model_validator, PositiveInt
from slugify import slugify

from .base import DTO
from .custom_types import AlphaStr

class CategoryBase(DTO):
    name: AlphaStr = Field(
        default=...,
        min_length=4,
        max_length=64,
        title='Category name',
        description='Main category catalog'
    )

class CategoryCreate(CategoryBase):

    id: PositiveInt = Field(
        default=None,
        title='Category ID',
        description='Main category ID'
    )

    slug: str = Field(
        default=None,
        min_length=4,
        max_length=64,
        title='Slug category',
        description='Slug main category'
    )

    @model_validator(mode='after')
    def slug_create(self) -> Self:
        if self.slug is None:
            self.slug = slugify(self.name)
        return self
