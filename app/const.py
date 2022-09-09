TOKEN_URL = "login"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"


DATABASE_URL = "sqlite:///./app/data/db/test.db"


STORAGE_PATH = "app/data/storage"


VALIDATORS_SCHEMA_REGEX = {"name": {"min_length": 2, "max_length": 20, "regex": r"^[a-zA-Z0-9 \-_]*$"}}
