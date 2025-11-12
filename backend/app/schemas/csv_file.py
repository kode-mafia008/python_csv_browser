from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CSVFileBase(BaseModel):
    filename: str


class CSVFileCreate(CSVFileBase):
    filepath: str
    size: int
    uploader_id: int


class CSVFileResponse(CSVFileBase):
    id: int
    filepath: str
    size: int
    uploader_id: int
    upload_date: datetime

    class Config:
        from_attributes = True


class CSVFileWithUploader(CSVFileResponse):
    uploader_username: Optional[str] = None
