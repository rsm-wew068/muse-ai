#!/bin/bash
set -e

# Load environment variables
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "🚀 Muse.AI Deployment Script"
echo "Make sure you are logged in via 'gcloud auth login'"

if [ -z "$PROJECT_ID" ]; then
    read -p "Enter your Google Cloud Project ID: " PROJECT_ID
fi

gcloud config set project $PROJECT_ID

echo "Step 1: Enabling APIs..."
gcloud services enable cloudbuild.googleapis.com run.googleapis.com artifactregistry.googleapis.com

echo "Step 2: Deploying Backend..."
cd backend
gcloud builds submit --tag gcr.io/$PROJECT_ID/muse-backend
gcloud run deploy muse-backend \
  --image gcr.io/$PROJECT_ID/muse-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --set-env-vars GEMINI_API_KEY=$GEMINI_API_KEY,SPOTIFY_CLIENT_ID=$SPOTIFY_CLIENT_ID,SPOTIFY_CLIENT_SECRET=$SPOTIFY_CLIENT_SECRET,LANGSMITH_TRACING=$LANGSMITH_TRACING,LANGSMITH_ENDPOINT=$LANGSMITH_ENDPOINT,LANGSMITH_API_KEY=$LANGSMITH_API_KEY,LANGSMITH_PROJECT=$LANGSMITH_PROJECT

BACKEND_URL=$(gcloud run services describe muse-backend --platform managed --region us-central1 --format 'value(status.url)')
echo "✅ Backend deployed at: $BACKEND_URL"

echo "Step 3: Deploying Frontend..."
cd ../frontend

# Create a temporary .env.production for the build
echo "NEXT_PUBLIC_API_URL=$BACKEND_URL" > .env.production

gcloud builds submit --tag gcr.io/$PROJECT_ID/muse-frontend
gcloud run deploy muse-frontend \
  --image gcr.io/$PROJECT_ID/muse-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

FRONTEND_URL=$(gcloud run services describe muse-frontend --platform managed --region us-central1 --format 'value(status.url)')
echo "🎉 Deployment Complete!"
echo "🌎 Live App: $FRONTEND_URL"
