from fastapi import HTTPException
from io import BytesIO
from tempfile import NamedTemporaryFile
from config import settings

def get_drive_file(file_id: str):
    try:
        drive = settings.google_drive.drive

        file = drive.CreateFile({'id': file_id})
        file.FetchMetadata()

        mime_type = file['mimeType']
        file_name = file['title']
        file_size = int(file['fileSize'])  # File size in bytes

        with NamedTemporaryFile(delete=True) as temp_file:
            file.GetContentFile(temp_file.name)  # Download content to the temp file
            temp_file.seek(0)  # Go back to the start of the file

            file_content = BytesIO(temp_file.read())

        file_content.seek(0)

        return file_content, mime_type
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving file: {e}")
