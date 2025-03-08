from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
# from database import Base
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class FactAdMetricsDaily(Base):
    __tablename__ = "fact_ad_metrics_daily"

    id = Column(Integer, primary_key=True,autoincrement=True)
    date_id = Column(Integer, ForeignKey("dim_date.date_id"), nullable=False)
    region_id = Column(Integer, ForeignKey("dim_region.region_id"), nullable=False)
    age_id=Column(Integer,ForeignKey('dim_age_group.age_id'), nullable=False)
    gender_id=Column(Integer,ForeignKey('dim_gender.gender_id'), nullable=False)
    platform_id = Column(Integer, ForeignKey("dim_platform.platform_id"), nullable=False)
    placement_id=Column(Integer, ForeignKey("dim_placement.placement_id"), nullable=False)
    device_type_id=Column(Integer,ForeignKey("dim_device_type.device_type_id"), nullable=False)
    
    impressions = Column(Integer,nullable=False)
    clicks = Column(Integer, nullable=False)
    cost = Column(Numeric(10, 2), nullable=False)
    conversions = Column(Integer, nullable=False)
    likes = Column(Integer, nullable=False)
    
    
    date = relationship("DimDate", back_populates="ad_metrics")
    region = relationship("DimRegion", back_populates="ad_metrics")
    age_group = relationship("DimAgeGroup", back_populates="ad_metrics")
    gender = relationship("DimGender", back_populates="ad_metrics")
    platform = relationship("DimPlatform", back_populates="ad_metrics")
    placement = relationship("DimPlacement", back_populates="ad_metrics")
    device_type = relationship("DimDeviceType", back_populates="ad_metrics")

class DimDate(Base):
    __tablename__ = "dim_date"
    date_id = Column(Integer, primary_key=True,autoincrement=True)
    date_value = Column(Date)
    
    ad_metrics=relationship("FactAdMetricsDaily",back_populates='date')
    
class DimRegion(Base):
    __tablename__ = "dim_region"

    region_id = Column(Integer, primary_key=True, autoincrement=True)
    region_name = Column(String(255), nullable=False, unique=True)

    ad_metrics = relationship("FactAdMetricsDaily", back_populates="region")

class DimAgeGroup(Base):
    __tablename__ = "dim_age_group"

    age_id = Column(Integer, primary_key=True, autoincrement=True)
    age_range = Column(String(50), nullable=False, unique=True)

    ad_metrics = relationship("FactAdMetricsDaily", back_populates="age_group")

class DimGender(Base):
    __tablename__ = "dim_gender"

    gender_id = Column(Integer, primary_key=True, autoincrement=True)
    gender_name = Column(String(50), nullable=False, unique=True)

    ad_metrics = relationship("FactAdMetricsDaily", back_populates="gender")

class DimPlatform(Base):
    __tablename__ = "dim_platform"

    platform_id = Column(Integer, primary_key=True, autoincrement=True)
    platform_name = Column(String(255), nullable=False, unique=True)

    ad_metrics = relationship("FactAdMetricsDaily", back_populates="platform")

class DimPlacement(Base):
    __tablename__ = "dim_placement"

    placement_id = Column(Integer, primary_key=True, autoincrement=True)
    placement_name = Column(String(255), nullable=False, unique=True)

    ad_metrics = relationship("FactAdMetricsDaily", back_populates="placement")

class DimDeviceType(Base):
    __tablename__ = "dim_device_type"

    device_type_id = Column(Integer, primary_key=True, autoincrement=True)
    device_type_name = Column(String(255), nullable=False, unique=True)

    ad_metrics = relationship("FactAdMetricsDaily", back_populates="device_type")
