import decimal
from typing import Self, Optional

from pydantic import Field, model_validator, PositiveInt
from slugify import slugify

from .base import DTO
from .custom_types import AlphaStr


class ProductBase(DTO):
    name: str = Field(
        default=...,
        min_length=4,
        max_length=64,
        title="Product name",
        examples=["Notebook", "Ноутбук"],
    )

    brand: AlphaStr = Field(
        default=...,
        min_length=2,
        max_length=64,
        title="Product brand",
        examples=["Apple", "Xiaomi"],
    )

    price: str = Field(
        default=...,
        max_digits=6,
        decimal_places=2,
        title="Product price",
    )


class ProductCreate(ProductBase):
    id: Optional[PositiveInt] = Field(
        default=None, title="Article product", description="Uniq article product"
    )

    category_id: PositiveInt = Field(default=..., title="Category_id from category")

    slug: str = Field(
        default=None,
        min_length=4,
        max_length=64,
        title="Slug product name",
        examples=["Apple Macbook Air", "Xiaomi Mi Notebook"],
    )

    slug_brand: AlphaStr = Field(
        default=None,
        min_length=2,
        max_length=64,
        title="Slug product brand",
    )

    @model_validator(mode="after")
    def slug_create(self) -> Self:
        if self.slug is None:
            self.slug = slugify(f"{self.name}#{self.id}")
        return self

    @model_validator(mode="after")
    def slug_create(self) -> Self:
        if self.name is None:
            self.name = slugify(f"{self.name}#{self.id}")
        return self
