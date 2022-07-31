
from database import Table_Data,SessionLocal
from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel



app = FastAPI()
db = SessionLocal()

class Format_Data(BaseModel):
    ID : int
    freshWaterLevel : float
    batteryLevel : float
    robotLinearVelocity :   float
    robotAngularVelocity : float
    areaName : str


# Default Page / HomePage where all the table data will be visible
@app.get("/" , tags = ["Root"])
def Show():
    ViewData = db.query(Table_Data).all()
    return ViewData

# Input method
@app.post("/Input Data" , tags = ["Endpoint1"])
def Create(Data:Format_Data):
    NewItem = Table_Data(
        ID = Data.ID,
        freshWaterLevel = Data.freshWaterLevel,
        batteryLevel  = Data.batteryLevel,
        robotLinearVelocity  = Data.robotLinearVelocity,
        robotAngularVelocity  = Data.robotAngularVelocity,
        areaName = Data.areaName) 

    db_exists = db.query(Table_Data).filter(Table_Data.ID==NewItem.ID).first()
    if db_exists is not None:
        raise HTTPException(status_code=400, detail ="ID number already exists")

    db.add(NewItem)
    db.commit()
    return NewItem 

# Update Method
@app.put("/Update")
def alter(Data_id:int, Data:Format_Data):
    db_change = db.query(Table_Data).filter(Data_id==Table_Data.ID).first()
    if db_change == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail ="This Data Id does not exists")
    
    db_change.freshWaterLevel = Data.freshWaterLevel
    db_change.batteryLevel = Data.batteryLevel
    db_change.robotLinearVelocity = Data.robotLinearVelocity
    db_change.robotAngularVelocity = Data.robotAngularVelocity
    db_change.areaName = Data.areaName

    return db_change

# Delete Method
@app.delete("/Remove", tags=["DESTROY"])
def Delete(Data_id : int):
    db_delete = db.query(Table_Data).filter(Data_id==Table_Data.ID).first()

    if db_delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail ="This Data Id does not exists")

    db.delete(db_delete)
    db.commit()

    return db_delete