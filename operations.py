# operations.py
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from models import engine, Experiment, DataPoint

def main():
    with Session(engine) as session:
        # 1) Dodaj 2 wiersze do tabeli Experiments
        exp1 = Experiment(title="Test A", type=1)
        exp2 = Experiment(title="Test B", type=2)
        session.add_all([exp1, exp2])
        session.flush()  # aby mieć id bez commit
        new_experiment_ids = [exp1.id, exp2.id]
        print(f"Dodano Experiments o ID: {new_experiment_ids}")

        # 2) Dodaj 10 wierszy do tabeli DataPoints
        new_dps = []
        for i in range(10):
            dp = DataPoint(real_value=i * 0.1, target_value=1.0 - i * 0.05)
            new_dps.append(dp)
        session.add_all(new_dps)
        session.flush()
        new_dp_ids = [dp.id for dp in new_dps]
        print(f"Dodano 10 DataPoints (ID od {min(new_dp_ids)} do {max(new_dp_ids)})")

        # 3) Pobierz i wyświetl dodane przed chwilą dane
        exps = session.scalars(
            select(Experiment).where(Experiment.id.in_(new_experiment_ids)).order_by(Experiment.id)
        ).all()
        dps = session.scalars(
            select(DataPoint).where(DataPoint.id.in_(new_dp_ids)).order_by(DataPoint.id)
        ).all()

        print("\n== Świeżo dodane Experiments ==")
        for e in exps:
            print(f"- id={e.id}, title={e.title}, created_at={e.created_at}, type={e.type}, finished={e.finished}")

        print("\n== Świeżo dodane DataPoints ==")
        for dp in dps:
            print(f"- id={dp.id}, real_value={dp.real_value}, target_value={dp.target_value}")

        # Zatwierdź inserty
        session.commit()

        # 4) Aktualizacja wszystkich Experiments (finished=True)
        session.execute(update(Experiment).values(finished=True))
        session.commit()
        print("\nUstawiono finished=True dla wszystkich Experiments.")

        # Pokaż efekt aktualizacji
        updated = session.scalars(select(Experiment).order_by(Experiment.id)).all()
        print("\n== Experiments po aktualizacji ==")
        for e in updated:
            print(f"- id={e.id}, title={e.title}, finished={e.finished}")

        # zamknij transakcję po SELECTach
        session.commit()

        # 5) Usuń wszystkie wiersze z obu tabel
        # (bez session.begin, po prostu execute + commit)
        # session.execute(delete(DataPoint))
        # session.execute(delete(Experiment))
        # session.commit()
        # print("\nUsunięto wszystkie wiersze z tabel: data_points i experiments.")

if __name__ == "__main__":
    main()
