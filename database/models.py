from database import Base
from sqlalchemy import String, Integer, Column

class ServiceDatabase(Base):
    __tablename__ = "servicedatabase"
    case_id = Column(String(5), primary_key=True)
    unit_serial_number = Column(String, default="")
    nama_customer = Column(String, default="")
    nomor_hp = Column(String, default="")
    alamat = Column(String, default="")
    detail_kerusakan = Column(String, default="")
    status = Column(String, default="")
    foto_unit = Column(String, default="")
    cabang=Column(String, default="")
