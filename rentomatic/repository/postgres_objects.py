from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemyには宣言型のアプローチがあるため、オブジェクトをインスタンス化し、Base
# それをテーブル/オブジェクトを宣言するための開始点として使用する必要があることに注意してください
Base = declarative_base()


class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True)

    code = Column(String(36), nullable=False)
    size = Column(Integer)
    price = Column(Integer)
    longitude = Column(Float) # 経度
    latitude = Column(Float)  # 緯度