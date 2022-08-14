from datetime import  datetime
from xml.etree.ElementTree import fromstring
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
@app.get("/")
def Index():
    ViewData = db.query(Table_Data).all()
    return ViewData

# if we want any specific ID data we can get this from here
@app.get("/ID/{ID}")
def Show(ID:int):
    ViewData = db.query(Table_Data).filter(ID==Table_Data.ID).first()
    return ViewData

# you just have to provide start date and end date and it'll provide all the date in between of those date, as what filter does
@app.get("/Date", description= "please follow this date format Y-M-D H:M:S")
def Filter_By_Date(From_date:datetime, To_date:datetime): #it should be Year - month - day hour - min - sec
    ViewDate = db.query(Table_Data).filter(Table_Data.created_date.between(From_date,To_date)).all()
    return ViewDate

# Input New data
@app.post("/Input Data")
def Insert_Method(Data:Format_Data):
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

# Update Any existing Record
@app.put("/Update")
def Update_Method(Data_id:int, Data:Format_Data):
    db_change = db.query(Table_Data).filter(Data_id==Table_Data.ID).first()
    if db_change == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail ="This Data Id does not exists")
    
    db_change.freshWaterLevel = Data.freshWaterLevel
    db_change.batteryLevel = Data.batteryLevel
    db_change.robotLinearVelocity = Data.robotLinearVelocity
    db_change.robotAngularVelocity = Data.robotAngularVelocity
    db_change.areaName = Data.areaName

    return db_change

# Delete Any record  by the ID
@app.delete("/Remove")
def Delete_Method(Data_id : int):
    db_delete = db.query(Table_Data).filter(Data_id==Table_Data.ID).first()

    if db_delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail ="This Data Id does not exists")

    db.delete(db_delete)
    db.commit()

    return db_delete