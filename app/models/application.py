from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Application(Base):
    __tablename__ = 'applications'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    bundle_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    templates: Mapped[list["Template"]] = relationship("Template",
                                                       secondary="application_templates", back_populates="applications")


# Вспомогательная таблица для связи many-to-many
class ApplicationTemplate(Base):
    __tablename__ = 'application_templates'

    application_id: Mapped[int] = mapped_column(Integer, ForeignKey('applications.id'), primary_key=True)
    template_id: Mapped[int] = mapped_column(Integer, ForeignKey('templates.id'), primary_key=True)
