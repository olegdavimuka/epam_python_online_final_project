import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "my-secret-key"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + "dev.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST_DATABASE_URL") or "sqlite:///" + "test.db"
    )
    TESTING = True
    DEBUG = False
