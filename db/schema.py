from pydantic import BaseModel

class ServiceDatabase(BaseModel):
    case_id: str
    unit_serial_number: str
    nama_customer: str
    nomor_hp: str
    alamat: str
    detail_kerusakan: str
    status: str
    foto_unit: str
    cabang: str
    
    class Config:
        orm_mode=True

class ServiceDatabaseCreate(BaseModel):
    unit_serial_number: str
    nama_customer: str
    nomor_hp: str
    alamat: str
    detail_kerusakan: str
    status: str
    cabang: str
    
    class Config:
        orm_mode=True

class ServiceDatabaseUpdate(BaseModel):
    detail_kerusakan: str
    status: str
    
    class Config:
        orm_mode=True

class ServiceDatabaseImageUpdate(BaseModel):
    foto_unit: str
    
    class Config:
        orm_mode=True
