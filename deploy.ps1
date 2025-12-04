# PowerShell deployment script for ADK to Cloud Run
# This avoids bash/Windows path issues

# Activate virtual environment
& .\venv\Scripts\Activate.ps1

# Set environment variables
$env:GOOGLE_CLOUD_PROJECT = "mundomotrizdev"
$env:GOOGLE_CLOUD_LOCATION = "us-central1"
$env:GOOGLE_GENAI_USE_VERTEXAI = "True"

# Deploy to Cloud Run
adk deploy cloud_run `
  --project=mundomotrizdev `
  --region=us-central1 `
  --service_name=bigquery-agent-service `
  --app_name=bigquery_agent_app `
  --with_ui `
  ./bigquery_agent
