from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.deps import get_admin_user
from app.models.user import User
from app.schemas.user import UserResponse
from app.schemas.csv_file import CSVFileResponse, CSVFileWithUploader
from app.services.user_service import UserService
from app.services.csv_service import CSVService
from app.services.websocket_manager import ws_manager
from app.core.config import settings
import os
import uuid

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/csv/upload", response_model=CSVFileResponse)
async def upload_csv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Upload a new CSV file (Admin only)
    """
    # Validate file extension
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files are allowed"
        )

    # Create upload directory if it doesn't exist
    upload_dir = settings.UPLOAD_DIR
    os.makedirs(upload_dir, exist_ok=True)

    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(upload_dir, unique_filename)

    # Save file
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        file_size = len(contents)

        # Create database record
        csv_file = CSVService.create_csv_file(
            db=db,
            filename=file.filename,
            filepath=file_path,
            size=file_size,
            uploader_id=current_user.id
        )

        # Broadcast update to all connected clients
        await ws_manager.broadcast({
            "type": "csv_list_updated",
            "action": "upload",
            "file": {
                "id": csv_file.id,
                "filename": csv_file.filename,
                "size": csv_file.size,
                "upload_date": csv_file.upload_date.isoformat()
            }
        })

        return csv_file

    except Exception as e:
        # Clean up file if database operation fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )


@router.delete("/csv/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_csv(
    file_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Delete a CSV file (Admin only)
    """
    success = CSVService.delete_csv_file(db, file_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    # Broadcast update to all connected clients
    await ws_manager.broadcast({
        "type": "csv_list_updated",
        "action": "delete",
        "file_id": file_id
    })

    return None


@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get all users (Admin only)
    """
    users = UserService.get_all_users(db)
    return users


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Delete a user (Admin only)
    """
    # Prevent admin from deleting themselves
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )

    success = UserService.delete_user(db, user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return None


@router.get("/csv", response_model=List[CSVFileResponse])
def get_all_csv_files_admin(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get all CSV files (Admin only)
    """
    files = CSVService.get_all_csv_files(db)
    return files
