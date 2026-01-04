
#Gcloud list projects
gcloud projects list

#set gcloud project
gcloud config set project mundomotrizdev


#create a virtual environment for python in windows
python -m venv venv
#activate the virtual environment in windows
source venv/Scripts/activate

#upgrade pip
pip install --upgrade pip
#install required packages
pip install -r requirements.txt
#deactivate the virtual environment
deactivate

# adk run bigquery_agent
adk run bigquery_agent


#deploy to google cloud run
export GOOGLE_CLOUD_PROJECT=mundomotrizdev
export GOOGLE_CLOUD_LOCATION=us-central1 # Or your preferred location
export GOOGLE_GENAI_USE_VERTEXAI=True

export AGENT_PATH="bigquery_agent" # Assuming capital_agent is in the current directory

export SERVICE_NAME="bigquery-agent-service"

export APP_NAME="bigquery_agent_app"

adk deploy cloud_run \
--project=$GOOGLE_CLOUD_PROJECT \
--region=$GOOGLE_CLOUD_LOCATION \
--service_name=$SERVICE_NAME \
--app_name=$APP_NAME \
--with_ui $AGENT_PATH


echo "<secret_here>" | gcloud secrets create GOOGLE_API_KEY --project=mundomotrizdev --data-file=-



#service account 
# 137982761941-compute@developer.gserviceaccount.com

gcloud secrets add-iam-policy-binding GOOGLE_API_KEY --member="serviceAccount:137982761941-compute@developer.gserviceaccount.com" --role="roles/secretmanager.secretAccessor" --project=mundomotrizdev
