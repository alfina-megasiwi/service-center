from fastapi import FastAPI, File, UploadFile, status, HTTPException, Depends
from fastapi.responses import FileResponse
from typing import List
from database import SessionLocal
from schema import *
import models as models
import random, string, shutil, os
from sqlalchemy.orm import Session

app = FastAPI()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def caseid_generator():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

@app.post('/service/add', response_model=ServiceDatabase, status_code=status.HTTP_201_CREATED)
def create_new_service_data(data: ServiceDatabaseCreate, db: Session = Depends(get_db)):
    try:
        new_case = models.ServiceDatabase(
            case_id = caseid_generator(),
            unit_serial_number = data.unit_serial_number.upper(),
            nama_customer = data.nama_customer,
            nomor_hp = data.nomor_hp,
            alamat = data.alamat,
            detail_kerusakan = data.detail_kerusakan,
            status = data.status,
            foto_unit = "",
            cabang = data.cabang
        )

        db.add(new_case)
        db.flush()
        db.commit()
        db.refresh(new_case)
        db.close()
        return new_case
    except:
        raise HTTPException(status_code=400, detail="Request yang dimasukkan salah")


@app.get('/service/database/', response_model=List[ServiceDatabase], status_code=status.HTTP_200_OK)
def get_all_service_data(db: Session = Depends(get_db)):
    try:
        data = db.query(models.ServiceDatabase).all()
        db.close()
        return data    
    except:
        raise HTTPException(status_code=400, detail="Data service tidak ada")


@app.get('/service/database/{case_id}', response_model=ServiceDatabase, status_code=status.HTTP_200_OK)
def get_service_data_by_case_id(case_id:str, db: Session = Depends(get_db)):
    try:
        data = db.query(models.ServiceDatabase).filter(models.ServiceDatabase.case_id==case_id).first()
        db.close()
        return data
    except:
        raise HTTPException(status_code=400, detail="Request yang dimasukkan salah")


@app.put('/service/database/{case_id}', response_model=ServiceDatabase, status_code=status.HTTP_200_OK)
def update_unit_status_by_case_id(case_id:str, data:ServiceDatabaseUpdate, db: Session = Depends(get_db)):
    try:
        data_to_update = db.query(models.ServiceDatabase).filter(models.ServiceDatabase.case_id==case_id).first()
        data_to_update.status = data.status
        data_to_update.detail_kerusakan = data.detail_kerusakan
        db.commit()
        db.refresh(data_to_update)
        db.close()
        return data_to_update
    except:
        raise HTTPException(status_code=400, detail="Request yang dimasukkan salah")


@app.put('/service/image/{case_id}', response_model=ServiceDatabase, status_code=status.HTTP_200_OK)
async def update_image_by_case_id(
        case_id:str, 
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
    ):
    try:
        data_to_update = db.query(models.ServiceDatabase).filter(models.ServiceDatabase.case_id==case_id).first()
        
        if(data_to_update.foto_unit != ""):
            os.remove(f"pic/{data_to_update.foto_unit}")

        file_name = f"{data_to_update.case_id}-{file.filename}"
        with open(f"pic/{file_name}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        data_to_update.foto_unit = file_name
        db.flush()
        db.commit()
        db.refresh(data_to_update)
        db.close()
        return data_to_update
    except:
        raise HTTPException(status_code=400, detail="Request yang dimasukkan salah")


@app.get('/service/image/{case_id}', status_code=status.HTTP_200_OK)
def get_image_by_case_id(case_id:str, db: Session = Depends(get_db)):
    data = db.query(models.ServiceDatabase).filter(models.ServiceDatabase.case_id==case_id).first()
    db.close()
    if(data.foto_unit != ""):
        return FileResponse(f"pic/{data.foto_unit}")
    else:
        raise HTTPException(status_code=400, detail="Gambar yang dicari tidak ada")

@app.delete('/service/database/{case_id}')
def delete_service_data_by_case_id(case_id:str, db: Session = Depends(get_db)):
    try:
        data_to_delete = db.query(models.ServiceDatabase).filter(models.ServiceDatabase.case_id==case_id).first()
        if(data_to_delete.foto_unit != ""):
            os.remove(f"pic/{data_to_delete.foto_unit}")

        db.delete(data_to_delete)
        db.commit()
        db.close()
        return f"Service dengan case id {data_to_delete.case_id} telah dihapus"
    except:
        raise HTTPException(status_code=400, detail="Data service yang dicari tidak ada")

