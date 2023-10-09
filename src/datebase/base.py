from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from src.settings.settings import engine, get_session


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True)
    engine_base: Mapped[str] = mapped_column(engine)
    session_base: Mapped[str] =mapped_column(get_session())

    @declared_attr
    def __tablename__(cls) -> str:
        return "".join(
            f"_{i.lower()}" if i.isupper() else i for i in cls.__tablename__
        ).strip("_")
