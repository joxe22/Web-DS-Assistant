from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import declarative_base
from flask import Blueprint
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
# Definir tu Blueprint
joxedb_bp = Blueprint('joxedb', __name__)

# Inicializar la base declarativa de SQLAlchemy
Base = declarative_base()

# Crear la instancia de SQLAlchemy
db = SQLAlchemy()

# Definir tus modelos
class User(Base):
    __tablename__ = 'user_account'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    fullname = Column(String)

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user_account.id'), nullable=False)
    user = relationship("User", back_populates="addresses")

User.addresses = relationship("Address", order_by=Address.id, back_populates="user")

# Asegurarse de que las instancias se añadan correctamente
def add_users():
    jose = User(name="Jose", fullname="Jose Espinal", addresses=[
        Address(email_address="jose2espinal@gmail.com"),
        Address(email_address="jose2espinal@sgmail.com"),
    ])
    joxedb = User(name="Joxe22", fullname="Jose De La Rosa")

    db.session.add_all([jose, joxedb])
    db.session.commit()
