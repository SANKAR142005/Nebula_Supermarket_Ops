from app.storage.connection import Base, engine
from app.storage import entities  # noqa: F401
from app.storage.seed_data import load_demo_products
from app.storage.seed_clients import load_demo_clients

Base.metadata.create_all(engine)
load_demo_products()
load_demo_clients()
print("SmartStore AI database is ready.")
