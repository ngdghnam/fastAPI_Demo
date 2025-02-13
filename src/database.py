import os
from lightdb import LightDB

db_path = os.path.join(os.path.dirname(__file__), "db.json")
db = LightDB(db_path)
