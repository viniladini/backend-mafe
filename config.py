import os
from werkzeug.security import generate_password_hash

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:3006@localhost:3306/mafe_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_USER = "coordenacao"
    ADMIN_PASSWORD_HASH = generate_password_hash(os.getenv("ADMIN_PASSWORD", "123456"))