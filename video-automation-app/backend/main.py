import json
import os
import tempfile
import uuid
from typing import List, Optional

import requests
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


API_DESCRIPTION = """Backend service for uploading videos to Google Drive and posting them via GetLate."""


def _load_service_account_info() -> dict:
    """Load Google service account credentials from environment variables."""
    json_blob = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if json_blob:
        try:
            return json.loads(json_blob)
        except json.JSONDecodeError as exc:  # pragma: no cover - defensive
            raise RuntimeError("Invalid GOOGLE_SERVICE_ACCOUNT_JSON value") from exc

    if credentials_path and os.path.exists(credentials_path):
        with open(credentials_path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    raise RuntimeError(
        "Google service account credentials not provided. Set GOOGLE_SERVICE_ACCOUNT_JSON "
        "or GOOGLE_APPLICATION_CREDENTIALS."
    )


def _build_drive_service():
    credentials_info = _load_service_account_info()
    scopes = ["https://www.googleapis.com/auth/drive.file"]
    credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=scopes)
    return build("drive", "v3", credentials=credentials)


def upload_video_to_drive(file_path: str, filename: str) -> dict:
    folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
    if not folder_id:
        raise RuntimeError("GOOGLE_DRIVE_FOLDER_ID is not configured")

    drive_service = _build_drive_service()
    file_metadata = {
        "name": filename,
        "parents": [folder_id],
        "mimeType": "video/mp4",
    }

    media = MediaFileUpload(file_path, mimetype="video/mp4")
    uploaded = (
        drive_service.files()
        .create(body=file_metadata, media_body=media, fields="id, webViewLink, webContentLink")
        .execute()
    )

    return uploaded


def trigger_getlate_automation(
    *,
    media_url: str,
    caption: str,
    platforms: List[str],
    scheduled_time: Optional[str],
) -> dict:
    api_key = os.getenv("GETLATE_API_KEY")
    if not api_key:
        raise RuntimeError("GETLATE_API_KEY is not configured")

    endpoint = os.getenv("GETLATE_API_BASE", "https://api.getlate.dev/v1/posts")
    payload = {
        "caption": caption,
        "media_url": media_url,
        "platforms": platforms,
    }
    if scheduled_time:
        payload["scheduled_time"] = scheduled_time

    response = requests.post(endpoint, json=payload, headers={"Authorization": f"Bearer {api_key}"}, timeout=30)

    if response.status_code >= 400:
        raise RuntimeError(f"GetLate API error: {response.status_code} - {response.text}")

    return response.json()


app = FastAPI(title="Video Automation API", description=API_DESCRIPTION, version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _normalize_platforms(value: str) -> List[str]:
    try:
        data = json.loads(value)
        if isinstance(data, list):
            return [str(item) for item in data if item]
    except json.JSONDecodeError:
        pass
    return [platform.strip() for platform in value.split(",") if platform.strip()]


@app.get("/api/health")
def healthcheck():
    return {"status": "ok"}


@app.post("/api/uploads")
def upload_video(
    file: UploadFile = File(...),
    caption: str = Form(""),
    platforms: str = Form("[]"),
    scheduled_time: Optional[str] = Form(None),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="File name missing")

    platforms_list = _normalize_platforms(platforms)
    if not platforms_list:
        raise HTTPException(status_code=400, detail="Select at least one platform")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            contents = file.file.read()
            tmp_file.write(contents)
            tmp_path = tmp_file.name

        upload_name = f"{uuid.uuid4().hex}_{file.filename}"
        drive_metadata = upload_video_to_drive(tmp_path, upload_name)

        media_url = drive_metadata.get("webContentLink") or drive_metadata.get("webViewLink")
        getlate_response = trigger_getlate_automation(
            media_url=media_url,
            caption=caption,
            platforms=platforms_list,
            scheduled_time=scheduled_time,
        )

        return {
            "message": "Video uploaded and social campaign scheduled",
            "drive_file": drive_metadata,
            "getlate_job": getlate_response,
        }
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        file.file.close()
        if "tmp_path" in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
