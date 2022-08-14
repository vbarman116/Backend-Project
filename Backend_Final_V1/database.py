from sqlalchemy import DateTime, create_engine,Column, String, Float, Integer, func
from sqlalchemy.orm import declarative_base,sessionmaker

Base = declarative_base()

# in this case we are using Postgres
# To make this project run in your machine / enviorment, just make sure to change the URL as per the next Comment
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/Databas_name"
# in this case i manually create a database in postgres sql and using the same database here!!!!

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost/DataStore"

engine = create_engine(SQLALCHEMY_DATABASE_URL,echo = False) 

SessionLocal = sessionmaker(bind=engine)
print("Creating Table.....")

class Table_Data(Base):
    __tablename__ = "LiveData"

    ID = Column(Integer, primary_key=True)
    freshWaterLevel = Column(Float)
    batteryLevel  = Column(Float)
    robotLinearVelocity = Column(Float)
    robotAngularVelocity = Column(Float)
    areaName = Column(String)
    created_date = Column(DateTime, server_default=func.now())   #"created_date":"2022-08-14T19:56:01.072714" 

print("****Table has been created added to your database****")

Base.metadata.create_all(engine)
