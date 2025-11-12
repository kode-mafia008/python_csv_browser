from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.csv_file import CSVFileResponse
from app.services.csv_service import CSVService
import csv
import os

router = APIRouter(prefix="/api/csv", tags=["csv"])


@router.get("", response_model=List[CSVFileResponse])
def get_all_csv_files(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all CSV files (available to all authenticated users)
    """
    files = CSVService.get_all_csv_files(db)
    return files


@router.get("/{file_id}", response_model=dict)
def get_csv_content(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get CSV file content as JSON (available to all authenticated users)
    """
    csv_file = CSVService.get_csv_file_by_id(db, file_id)

    if not csv_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    if not os.path.exists(csv_file.filepath):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found on disk"
        )

    # Read CSV file and convert to JSON
    try:
        with open(csv_file.filepath, 'r', encoding='utf-8') as f:
            csv_reader = csv.DictReader(f)
            data = list(csv_reader)

        return {
            "filename": csv_file.filename,
            "columns": list(data[0].keys()) if data else [],
            "data": data,
            "row_count": len(data)
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to read CSV file: {str(e)}"
        )


@router.get("/{file_id}/download")
def download_csv(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Download CSV file (available to all authenticated users)
    """
    csv_file = CSVService.get_csv_file_by_id(db, file_id)

    if not csv_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    if not os.path.exists(csv_file.filepath):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found on disk"
        )

    return FileResponse(
        path=csv_file.filepath,
        filename=csv_file.filename,
        media_type="text/csv"
    )
