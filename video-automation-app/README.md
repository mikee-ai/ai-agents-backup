# Video Automation App

This application enables marketers to upload short-form videos into a Google Drive folder and automatically schedule distribution across social networks through the [GetLate](https://getlate.dev/docs) automation API.

The project is split into two parts:

1. **FastAPI backend** – receives uploads, stores them in Google Drive, then triggers a GetLate post workflow.
2. **Vanilla JS frontend** – lightweight interface for uploading, selecting platforms, and scheduling.

## Backend Setup

```bash
cd video-automation-app/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Required environment variables

| Variable | Description |
| --- | --- |
| `GOOGLE_DRIVE_FOLDER_ID` | Target folder to store uploaded videos. |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | JSON string for a Google service account with Drive access. Alternatively set `GOOGLE_APPLICATION_CREDENTIALS`. |
| `GETLATE_API_KEY` | API key for GetLate. |
| `GETLATE_API_BASE` | Optional override for the GetLate endpoint (defaults to `https://api.getlate.dev/v1/posts`). |

## Frontend Setup

```bash
cd video-automation-app/frontend
python -m http.server 4173
# or serve via any static host of your choice
```

If your backend is not on `http://localhost:8000`, expose it globally by setting `API_BASE_URL` before loading the page:

```html
<script>
  window.API_BASE_URL = 'https://your-domain.com';
</script>
```

## Workflow

1. Users upload an MP4 video, caption, target platforms, and an optional schedule.
2. Backend uploads the file to Google Drive using service account credentials.
3. A share link is sent to the GetLate API so it can publish to all configured social accounts.
4. The UI surfaces confirmations from both Drive and GetLate.

