# models.py
from datetime import datetime
from sqlalchemy import create_engine, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# tworzy bazkę 'lab.db' w bieżącym katalogu
DATABASE_URL = "sqlite:///lab.db"
engine = create_engine(DATABASE_URL, echo=True, future=True)


class Base(DeclarativeBase):
    pass


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    finished: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f"Experiment(id={self.id!r}, title={self.title!r})"


class DataPoint(Base):
    __tablename__ = "data_points"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    real_value: Mapped[float] = mapped_column(Float, nullable=False)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"DataPoint(id={self.id!r}, real={self.real_value!r}, target={self.target_value!r})"


# schemat bazy
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Utworzono plik bazy i tabele: experiments, data_points")
