# RNA Lab Navigator - Railway Deployment Guide

## Project Structure and Deployment Information

This document serves as a reference for the deployment setup of the RNA Lab Navigator project on Railway.

### Repository Information

- **Original Project Directory:** `/Users/vishalbharti/Downloads/rna-lab-navigator`
- **Deployment Repository Directory:** `/Users/vishalbharti/Downloads/rna-lab-deploy`
- **GitHub Repository:** https://github.com/visvikbharti/rna-lab-deploy

### Services on Railway

1. **Backend (Django + DRF)**
   - Service Name: rna-lab-deploy
   - Root Directory: `backend`
   - Building with Dockerfile
   - Start Command: `/app/docker-entrypoint.sh`
   - Health Check Path: `/api/health/`

2. **PostgreSQL**
   - Connected to the backend service
   - Provided by Railway's managed PostgreSQL service

3. **Redis**
   - Connected to the backend service
   - Provided by Railway's managed Redis service

### Key Environment Variables

Backend service requires the following environment variables:

```
PORT=8000
OPENAI_API_KEY=[Your OpenAI API Key]
OPENAI_MODEL=gpt-4o
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
OPENAI_TIMEOUT=30
SECRET_KEY=[Generated Secret Key]
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,*.railway.app
CELERY_TIMEZONE=Asia/Kolkata
POSTGRES_DB=[From Railway PostgreSQL service]
POSTGRES_USER=[From Railway PostgreSQL service]
POSTGRES_PASSWORD=[From Railway PostgreSQL service]
POSTGRES_HOST=[From Railway PostgreSQL service]
POSTGRES_PORT=[From Railway PostgreSQL service]
REDIS_URL=[From Railway Redis service]
```

### Key Files

1. **docker-entrypoint.sh**
   - Located at: `/Users/vishalbharti/Downloads/rna-lab-deploy/backend/docker-entrypoint.sh`
   - Purpose: Initializes the application, waits for PostgreSQL, runs migrations, and starts the Gunicorn server
   - Added PostgreSQL connection check for deployment reliability

2. **railway.json**
   - Located at: `/Users/vishalbharti/Downloads/rna-lab-deploy/backend/railway.json`
   - Purpose: Configures Railway build and deployment settings
   - Contains healthcheck configuration and deployment policies

3. **Dockerfile**
   - Located at: `/Users/vishalbharti/Downloads/rna-lab-deploy/backend/Dockerfile`
   - Purpose: Defines the container image for the backend service

### Deployment Workflow

1. Make changes to the local repository at `/Users/vishalbharti/Downloads/rna-lab-deploy`
2. Commit and push changes to GitHub
3. Railway automatically detects changes and rebuilds/redeploys the service

### Troubleshooting

Common deployment issues:
- PostgreSQL connection failures: Ensure database credentials are correct and database is accessible
- Missing environment variables: Check all required environment variables are set correctly
- Dockerfile build errors: Check build logs for dependency issues
- Healthcheck failures: Verify the health endpoint is working correctly

To debug deployment issues:
1. Check Railway deployment logs
2. Verify environment variable connections between services
3. Use the health check endpoint to confirm application status

### Next Steps for Complete Deployment

To complete the deployment:

1. Deploy the frontend service to Railway
2. Configure the frontend to connect to the backend API
3. Set up Weaviate for vector storage (if using Railway)
4. Configure Celery workers for background tasks

### Frontend Deployment Instructions

Once the backend is successfully deployed, follow these steps to deploy the frontend:

1. Create a new service in Railway
2. Link it to the GitHub repository
3. Set the Root Directory to `frontend`
4. Configure environment variables:
   - VITE_API_URL=[Backend URL]
   - VITE_RAILWAY_STATIC_URL=[Static files URL]

### Connecting Frontend to Backend

Update the frontend API configuration to point to the backend service URL.

File: `/Users/vishalbharti/Downloads/rna-lab-deploy/frontend/src/api/config.js`