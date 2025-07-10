from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Voice(Base):
    __tablename__ = 'voices'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    speaker: Mapped[str] = mapped_column(nullable=False)
    avatar_url: Mapped[str] = mapped_column(nullable=True)
    avatar_url_webp: Mapped[str] = mapped_column(nullable=True)
