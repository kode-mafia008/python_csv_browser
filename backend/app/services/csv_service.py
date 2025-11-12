from sqlalchemy.orm import Session
from app.models.csv_file import CSVFile
from typing import Optional, List
import os


class CSVService:
    @staticmethod
    def create_csv_file(
        db: Session,
        filename: str,
        filepath: str,
        size: int,
        uploader_id: int
    ) -> CSVFile:
        """Create a new CSV file record"""
        db_csv = CSVFile(
            filename=filename,
            filepath=filepath,
            size=size,
            uploader_id=uploader_id
        )
        db.add(db_csv)
        db.commit()
        db.refresh(db_csv)
        return db_csv

    @staticmethod
    def get_all_csv_files(db: Session) -> List[CSVFile]:
        """Get all CSV files"""
        return db.query(CSVFile).order_by(CSVFile.upload_date.desc()).all()

    @staticmethod
    def get_csv_file_by_id(db: Session, file_id: int) -> Optional[CSVFile]:
        """Get CSV file by ID"""
        return db.query(CSVFile).filter(CSVFile.id == file_id).first()

    @staticmethod
    def delete_csv_file(db: Session, file_id: int) -> bool:
        """Delete a CSV file record and physical file"""
        csv_file = db.query(CSVFile).filter(CSVFile.id == file_id).first()
        if csv_file:
            # Delete physical file
            if os.path.exists(csv_file.filepath):
                os.remove(csv_file.filepath)

            # Delete database record
            db.delete(csv_file)
            db.commit()
            return True
        return False
