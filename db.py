from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://postgres:1@db:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)


def init_db():
    Base.metadata.create_all(engine)

    session = SessionLocal()

    try:
        if not session.query(Food).first():
            foods = [
                Food(name="Sezar salati", category="salads"),
                Food(name="Olivye salati", category="salads"),
                Food(name="Burger", category="fastfood"),
                Food(name="Hot-dog", category="fastfood"),
                Food(name="Osh", category="hot"),
                Food(name="Sho'rva", category="hot"),
            ]
            session.add_all(foods)
            session.commit()
    finally:
        session.close()


def get_foods_by_category(category):
    session = SessionLocal()
    try:
        foods = session.query(Food).filter(Food.category == category).all()
        return [f.name for f in foods]
    finally:
        session.close()