TOKEN_URL = "login"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"


DATABASE_URL = "sqlite:///./data/db/test.db"


STORAGE_PATH = "data/storage"


VALIDATORS_SCHEMA_REGEX = {
    # Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character
    "password": {"regex": r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"}
}
