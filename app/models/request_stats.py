from sqlalchemy import Integer, String, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.database import Base


class RequestStats(Base):
    __tablename__ = 'request_stats'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    app_id: Mapped[str] = mapped_column(String(255),
                                        nullable=False)
    user_id: Mapped[str] = mapped_column(String(255),
                                         nullable=False)
    __table_args__ = {'extend_existing': True}


