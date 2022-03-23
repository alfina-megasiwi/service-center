from database import Base, engine
from models import ServiceDatabase

Base.metadata.create_all(engine)