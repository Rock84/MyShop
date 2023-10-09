from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, declared_attr

from src.settings.settings import get_session, engine

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

    engine = engine
    session = get_session()

    @declared_attr
    def __tablename__(cls) -> str:
        return ''.join(f'_{i.lower()}' if i.issupper() else i for i in cls.__name__).strip('_')


