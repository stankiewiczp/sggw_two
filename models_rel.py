# models_rel.py
from datetime import datetime
from sqlalchemy import (
    create_engine, Integer, String, DateTime, Boolean, Float, ForeignKey, Index
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session


DATABASE_URL = "sqlite:///lab.db"   # utworzy się na nowo, bo skasowałeś stary
engine = create_engine(DATABASE_URL, echo=True, future=True)

class Base(DeclarativeBase):
    pass


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    finished: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relacja: jeden Experiment posiada wiele DataPointów
    data_points: Mapped[list["DataPoint"]] = relationship(
        back_populates="experiment",
        cascade="all, delete-orphan",   
        passive_deletes=False           
    )

    def __repr__(self) -> str:
        return f"Experiment(id={self.id!r}, title={self.title!r}, finished={self.finished!r})"


class DataPoint(Base):
    __tablename__ = "data_points"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    real_value: Mapped[float] = mapped_column(Float, nullable=False)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)

    # Klucz obcy do Experiment
    experiment_id: Mapped[int] = mapped_column(
        ForeignKey("experiments.id"),  # w SQLite nie ustawiamy ON DELETE CASCADE; kaskada jak wyżej w ORM
        nullable=False,
        index=True
    )

    # Druga strona relacji
    experiment: Mapped[Experiment] = relationship(back_populates="data_points")

    def __repr__(self) -> str:
        return f"DataPoint(id={self.id!r}, real={self.real_value!r}, target={self.target_value!r}, exp_id={self.experiment_id!r})"


# Dodatkowy indeks 
Index("ix_data_points_experiment_real", DataPoint.experiment_id, DataPoint.real_value)

# Tworzenie schematu + DEMO
if __name__ == "__main__":
    # schemat (plik lab.db)
    Base.metadata.create_all(engine)
    print("Utworzono schemat z relacją 1→N.")

    # DEMO: Dodajemy 1 Experiment z kilkoma DataPointami, by zweryfikować relację
    with Session(engine) as session:
        exp = Experiment(title="Relacyjny test", type=42)
        exp.data_points = [
            DataPoint(real_value=0.1, target_value=0.9),
            DataPoint(real_value=0.2, target_value=0.85),
            DataPoint(real_value=0.3, target_value=0.8),
        ]
        session.add(exp)
        session.commit()

        # Szybkie sprawdzenie
        from sqlalchemy import select
        got = session.scalar(select(Experiment).where(Experiment.title == "Relacyjny test"))
        print("\n== Podgląd ==")
        print(got)
        for dp in got.data_points:
            print("  ", dp)

    print("\n[DEMO] Dodano 1 eksperyment z 3 punktami. Możesz zakomentować blok __main__.")
