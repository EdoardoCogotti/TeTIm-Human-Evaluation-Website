import os


class Config:
    DOCKER_FLAG = True

    # SECRET_KEY to protect against modifying cookies and cross-site request forgery attacks
    if DOCKER_FLAG:
        SQLALCHEMY_DATABASE_URI ="postgresql+psycopg2://postgres:postgres@db:5432/tetim"
        SECRET_KEY = os.getenv("SECRET_KEY")
    else:
        SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:postgres@localhost:5432/tetim"
        SECRET_KEY = os.environ.get("SECRET_KEY")
    SESSION_TYPE = "filesystem"
