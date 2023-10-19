from datetime import datetime

from sqlalchemy import String, CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ulid import new, parse

from .base import Base


class User(Base):
    __table_args__ = (
        CheckConstraint("char_length(name) >= 2"),
        CheckConstraint("char_length(email) >= 5"),
    )

    id: Mapped[str] = mapped_column(
        String(28), default=lambda: new().str, primary_key=True
    )
    name: Mapped[str] = mapped_column(String(length=64, collation="utf8"))
    email: Mapped[str] = mapped_column(
        String(length=128, collation="utf8"), unique=True
    )
    password: Mapped[str] = mapped_column((String(128)))

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def date_of_user_create(self) -> datetime:
        return datetime.fromtimestamp(parse(self.id).timestamp())


class Category(Base):
    __table_args__ = (
        CheckConstraint("char_length(name) >= 4"),
        CheckConstraint("char_length(slug) >= 4"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)

    products: Mapped[list["Product"]] = relationship(
        back_populates="category", cascade="all"
    )

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return self.__str__()


class Brand(Base):
    __table_args__ = (
        CheckConstraint("char_length(brand) >= 2"),
        CheckConstraint("char_length(slug_brand) >= 2"),
    )
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)
    brand: Mapped[str] = mapped_column(String(24), nullable=False)
    slug_brand: Mapped[str] = mapped_column(String(24), nullable=False)

    brands: Mapped[list["Product"]] = relationship(
        back_populates="brand", cascade="all"
    )


class Product(Base):
    __table_args__ = (
        CheckConstraint("char_length(name) >= 2"),
        CheckConstraint("char_length(slug) >= 2"),
    )

    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    price: Mapped[float | None]

    category_id: Mapped[int] = mapped_column(
        ForeignKey(column="Category.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category: Mapped["Category"] = relationship(back_populates="products")

    brand_id: Mapped[int] = mapped_column(
        ForeignKey(column="Brand.id", ondelete="CASCADE"), nullable=False, index=True
    )
    brand: Mapped["Brand"] = relationship(back_populates="brands", cascade="all")

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return self.__str__()
