const DEFAULT_PLATFORMS = [
  { id: 'instagram', label: 'Instagram Reels' },
  { id: 'tiktok', label: 'TikTok' },
  { id: 'youtube', label: 'YouTube Shorts' },
  { id: 'facebook', label: 'Facebook' },
  { id: 'linkedin', label: 'LinkedIn' },
];

const state = {
  submissions: [],
};

const apiBaseUrl = window.API_BASE_URL || 'http://localhost:8000';

const platformGrid = document.getElementById('platform-grid');
const timelineList = document.getElementById('timeline');
const feedbackEl = document.getElementById('feedback');
const uploadForm = document.getElementById('upload-form');

function renderPlatforms() {
  platformGrid.innerHTML = '';
  DEFAULT_PLATFORMS.forEach((platform) => {
    const label = document.createElement('label');
    label.className = 'platform-pill';
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.name = 'platforms';
    checkbox.value = platform.id;
    checkbox.checked = ['instagram', 'tiktok'].includes(platform.id);

    const span = document.createElement('span');
    span.textContent = platform.label;

    label.appendChild(checkbox);
    label.appendChild(span);
    platformGrid.appendChild(label);
  });
}

function renderTimeline() {
  timelineList.innerHTML = '';
  if (state.submissions.length === 0) {
    const empty = document.createElement('p');
    empty.className = 'empty-state';
    empty.textContent = 'No automations yet. Your activity will appear here.';
    timelineList.appendChild(empty);
    return;
  }

  state.submissions.forEach((item) => {
    const li = document.createElement('li');
    const strong = document.createElement('strong');
    strong.textContent = new Date(item.timestamp).toLocaleString();
    const msg = document.createElement('p');
    msg.textContent = item.message;
    li.appendChild(strong);
    li.appendChild(msg);
    if (item.jobId) {
      const ref = document.createElement('p');
      ref.className = 'job-ref';
      ref.textContent = `GetLate job #${item.jobId}`;
      li.appendChild(ref);
    }
    timelineList.appendChild(li);
  });
}

async function handleSubmit(event) {
  event.preventDefault();
  const fileInput = document.getElementById('video');
  if (!fileInput.files?.length) {
    showFeedback('error', 'Please attach a video file.');
    return;
  }

  const caption = document.getElementById('caption').value.trim();
  const schedule = document.getElementById('schedule').value;
  const platforms = Array.from(uploadForm.querySelectorAll('input[name="platforms"]:checked')).map(
    (input) => input.value,
  );

  if (platforms.length === 0) {
    showFeedback('error', 'Select at least one platform.');
    return;
  }

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);
  formData.append('caption', caption);
  formData.append('platforms', JSON.stringify(platforms));
  if (schedule) {
    formData.append('scheduled_time', schedule);
  }

  uploadForm.classList.add('is-submitting');
  showFeedback('info', 'Uploading…');

  try {
    const response = await fetch(`${apiBaseUrl}/api/uploads`, {
      method: 'POST',
      body: formData,
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || 'Upload failed');
    }

    state.submissions.unshift({
      timestamp: new Date().toISOString(),
      message: payload.message,
      jobId: payload.getlate_job?.id,
    });
    renderTimeline();
    uploadForm.reset();
    renderPlatforms();
    showFeedback('success', payload.message);
  } catch (error) {
    showFeedback('error', error.message);
  } finally {
    uploadForm.classList.remove('is-submitting');
  }
}

function showFeedback(type, message) {
  feedbackEl.hidden = false;
  feedbackEl.className = `feedback ${type}`;
  feedbackEl.textContent = message;
}

uploadForm.addEventListener('submit', handleSubmit);
renderPlatforms();
renderTimeline();
