from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from src.settings.settings import engine


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True)

    async def get_session(self):
        async_session = async_sessionmaker(engine, expire_on_commit=False)
        async with async_session as session:
            yield session
            await session.close()

    @declared_attr
    def __tablename__(cls) -> str:
        return "".join(
            f"_{i.lower()}" if i.isupper() else i for i in cls.__tablename__
        ).strip("_")
