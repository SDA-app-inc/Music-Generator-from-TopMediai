from sqlalchemy import Integer, String, Text, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum

from app.database import Base


class TemplateStatus(PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class TemplateCategory(PyEnum):
    TRENDING = "Trending"
    GENERAL = "General"
    CLASSIC = "Classic"


class Template(Base):
    __tablename__ = 'templates'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(Enum(TemplateStatus), nullable=True, default=TemplateStatus.INACTIVE)
    category: Mapped[str] = mapped_column(Enum(TemplateCategory), nullable=True, default=TemplateCategory.CLASSIC)

    applications: Mapped[list["Application"]] = relationship("Application", secondary="application_templates",
                                                             back_populates="templates")
