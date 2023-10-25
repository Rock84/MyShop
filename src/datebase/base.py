from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr,
    sessionmaker,
)


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True)

    engine = create_engine(url='postgresql://admin:admin@0.0.0.0:5433/admin')
    session = sessionmaker(bind=engine)

    @declared_attr
    def __tablename__(cls) -> str:
        return "".join(
            f"_{i.lower()}" if i.isupper() else i for i in cls.__name__
        ).strip("_")
