import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "Joxe@220620") # Clave para sesiones
    DEBUG = True  # Activa modo debug
    SQLALCHEMY_DATABASE_URI = "sqlite:///joxe.db"  # Base de datos SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False