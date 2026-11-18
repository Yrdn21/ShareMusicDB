import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException

IMAGES_DIR = Path("images")
IMAGES_URL = "/images"

ALLOWED_TYPES = {
    "image/jpeg": "jpeg",
    "image/jpg": "jpg",
    "image/png": "png",
    "image/bmp": "bmp",
    "image/webp": "webp",
    "image/heic": "heic"
}

ALLOWED_FOLDERS = {
    "artists",
    "albums",
    "tracks",
    "playlists",
    "users"}

IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def save_image(file: UploadFile, folder: str) -> str:
    if folder not in ALLOWED_FOLDERS:
        raise HTTPException(status_code=400, detail="Folder or model not allowed")

    extension = ALLOWED_TYPES.get(file.content_type)
    if not extension:
        raise HTTPException(status_code=415, detail="File extension not supported, DONKEY")

    content = file.file.read()
    folder_path = IMAGES_DIR / folder
    folder_path.mkdir(parents=True, exist_ok=True)

    file_name = f"{folder}_{uuid.uuid4().hex}.{extension}"
    file_path = folder_path / file_name
    file_path.write_bytes(content)

    return f"{IMAGES_URL}/{folder}/{file_name}"


def delete_image(image_url: str):
    if not image_url or not image_url.startswith(IMAGES_URL):
        return False


    relative_path = image_url.replace(IMAGES_URL, "").strip("/")
    file_path = IMAGES_DIR / relative_path

    if file_path.exists() and file_path.is_file():
        file_path.unlink()
        return True
    return False