from fastapi import FastAPI,Depends,HTTPException,Query
from sqlalchemy.orm import Session
from typing import Annotated
from database import get_db
from models import DimDate,DimAgeGroup,DimDeviceType,DimGender,DimPlacement,DimPlatform,DimRegion,FactAdMetricsDaily
from Data import metadata,ad_metrics_data
from datetime import datetime,date
import schemas  
from typing import List, Optional
from scheduler import scheduler
from contextlib import asynccontextmanager
from sqlalchemy.exc import SQLAlchemyError
from alembic.config import Config
from alembic import command


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()
db_dependency=Annotated[Session,Depends(get_db)]

    
app = FastAPI(lifespan=lifespan)

@app.post("/insert-metrics-and-metadata/",description="Run this first to add dummy data")
async def insert_metadata_and_metrics(
    db: Session = Depends(get_db),
):
    try:
        # Insert metadata
        data_count = db.query(FactAdMetricsDaily).count()
        if data_count==0:
            db.bulk_save_objects(
                [DimDate(date_value=datetime.strptime(date, "%Y-%m-%d")) for date in metadata["dates"]]
            )
            db.bulk_save_objects([DimRegion(region_name=region) for region in metadata["regions"]])
            db.bulk_save_objects([DimAgeGroup(age_range=age) for age in metadata["age_groups"]])
            db.bulk_save_objects([DimGender(gender_name=gender) for gender in metadata["genders"]])
            db.bulk_save_objects([DimPlatform(platform_name=platform) for platform in metadata["platforms"]])
            db.bulk_save_objects([DimPlacement(placement_name=placement) for placement in metadata["placements"]])
            db.bulk_save_objects([DimDeviceType(device_type_name=device) for device in metadata["device_types"]])
            db.commit()

            # Insert ad metrics data
            for data in ad_metrics_data:
                    ad_metric = FactAdMetricsDaily(**data)
                    db.add(ad_metric)
            db.commit()
        else:
            return{"message":"already Dummy Data Exists"} 

        return {"message":"inserted Dummy Data"} 

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error inserting data: {e}")
    
    finally:
        db.close()


@app.get("/ad-metrics/", response_model=List[schemas.AdMetricsResponse])
def get_ad_metrics(
    start_date: date = Query(..., description="Start date for filtering",example="2021-01-01"),
    end_date: date = Query(..., description="End date for filtering",example="2025-01-01"),
    region: Optional[str] = Query(None, description="Region Name",example="Asia"),
    platform: Optional[str] = Query(None, description="Platform Name",example="Google"),
    db: Session = Depends(get_db)):
    try:
        if start_date >end_date:
            raise HTTPException(status_code=400, detail="Start date cannot be after end date")

        query = (
            db.query(
                FactAdMetricsDaily,
                DimDate.date_value,
                DimRegion.region_name,
                DimAgeGroup.age_range,
                DimGender.gender_name,
                DimPlatform.platform_name,
                DimPlacement.placement_name,
                DimDeviceType.device_type_name
            )
            .join(DimDate, FactAdMetricsDaily.date_id == DimDate.date_id)
            .join(DimRegion, FactAdMetricsDaily.region_id == DimRegion.region_id)
            .join(DimAgeGroup, FactAdMetricsDaily.age_id == DimAgeGroup.age_id)
            .join(DimGender, FactAdMetricsDaily.gender_id == DimGender.gender_id)
            .join(DimPlatform, FactAdMetricsDaily.platform_id == DimPlatform.platform_id)
            .join(DimPlacement, FactAdMetricsDaily.placement_id == DimPlacement.placement_id)
            .join(DimDeviceType, FactAdMetricsDaily.device_type_id == DimDeviceType.device_type_id)
            .filter(DimDate.date_value.between(start_date, end_date))
        )
        
        if region:
            query = query.filter(DimRegion.region_name == region)
        if platform:
            query = query.filter(DimPlatform.platform_name == platform)

        result = query.all()

        if not result:
            raise HTTPException(status_code=404, detail="No data found for the given filters")

        return [
            schemas.AdMetricsResponse(
                date=row.date_value,
                region_name=row.region_name,
                age_range=row.age_range,
                gender_name=row.gender_name,
                platform_name=row.platform_name,
                placement_name=row.placement_name,
                device_type_name=row.device_type_name,
                impressions=row.FactAdMetricsDaily.impressions,
                clicks=row.FactAdMetricsDaily.clicks,
                cost=float(row.FactAdMetricsDaily.cost),
                conversions=row.FactAdMetricsDaily.conversions,
                likes=row.FactAdMetricsDaily.likes,
            )
            for row in result
        ]

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/")
def home():
    return {"message": "FastAPI with APScheduler is running!","url":"http://127.0.0.1:8000/docs"}