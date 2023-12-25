from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from setting import get_app_settings
from pymongo import MongoClient, ASCENDING, DESCENDING

settings = get_app_settings()
# Create the engine
print(settings)
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, connect_args={"connect_timeout": 15})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)

client = MongoClient('mongodb://localhost:27017/')
db = client['logingestor']
collection = db['log_data']
# Index on 'level' field in ascending order
collection.create_index([('level', ASCENDING)])

# Index on 'message' field in descending order
collection.create_index([('message', DESCENDING)])

# Index on 'resourceId' field in ascending order
collection.create_index([('resourceId', ASCENDING)])

# Index on 'metadata_parentResourceId' field in ascending order
collection.create_index([('metadata_parentResourceId', ASCENDING)])


def get_db():
    db = SessionLocal()
    print(db)
    try:
        yield db
    finally:
        db.close()