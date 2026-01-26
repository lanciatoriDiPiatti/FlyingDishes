#!/usr/bin/env python3
"""
Script per inizializzare il database PostgreSQL
Esegui questo script prima di avviare l'applicazione
"""
import logging
from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.models import User, Food, Day

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db():
    logger.info("🔨 Inizializzazione del database...")
    try:
        # Crea tutte le tabelle
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Tabelle create: users, foods, days")

        db = SessionLocal()

        # Popola solo se il DB è vuoto
        if db.query(Day).first() is None:
            logger.info("Popolamento tabella 'days'...")
            days_to_create = [Day(nome=f"Giorno {i+1}") for i in range(8)]
            db.add_all(days_to_create)
            db.commit()
            logger.info("✓ Tabella 'days' popolata.")
        else:
            logger.info("Tabella 'days' già popolata.")

        if db.query(Food).first() is None:
            logger.info("Popolamento tabella 'foods'...")
            foods_to_create = [
                Food(nome="pizzeria"),
                Food(nome="sushi"),
                Food(nome="trattoria"),
                Food(nome="mcdonald"),
                Food(nome="kebabbaro"),
            ]
            db.add_all(foods_to_create)
            db.commit()
            logger.info("✓ Tabella 'foods' popolata.")
        else:
            logger.info("Tabella 'foods' già popolata.")

        db.close()
        logger.info("✓ Database inizializzato con successo!")

    except Exception as e:
        logger.error(f"✗ Errore durante l'inizializzazione: {e}")
        raise

if __name__ == "__main__":
    init_db()
