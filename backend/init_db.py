#!/usr/bin/env python3
"""
Script per inizializzare il database PostgreSQL
Esegui questo script prima di avviare l'applicazione
"""

from app.db.base import Base
from app.db.session import engine
from app.models import User, Food, Day

print("🔨 Inizializzazione del database...")

try:
    # Crea tutte le tabelle
    Base.metadata.create_all(bind=engine)
    print("✓ Database inizializzato con successo!")
    print("✓ Tabelle create: users, foods, days")
except Exception as e:
    print(f"✗ Errore durante l'inizializzazione: {e}")
    exit(1)
