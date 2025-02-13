from database import db
from lightdb.models import Model

class User(Model, table="users", db=db):
    name: str
    phone: str
    email: str 
    password: str

# user = User.create(name="Hoai Hai", phone="0923905635", email="namndh22406@st.uel.edu.vn", password="hoainam11122004")