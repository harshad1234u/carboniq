# CarbonIQ

## 1. Project Overview
CarbonIQ is a comprehensive platform designed to help users track, manage, and reduce their carbon footprint. 

## 2. Problem Statement
With the increasing impact of climate change, individuals and organizations lack accessible tools to quantify and mitigate their carbon emissions. CarbonIQ solves this by providing actionable insights and easy-to-use tracking tools.

## 3. Features
- Carbon footprint tracking and analytics
- Personalized reduction recommendations
- Onboarding workflow for new users
- Weather data integration
- Cloud-native architecture with robust security

## 4. Architecture
The project follows a client-server architecture:
- **Frontend**: A React single-page application built with Vite.
- **Backend**: A scalable API service built with Python.
- **Database**: Supabase for PostgreSQL database, authentication, and secure data storage.
- **Deployment**: Google Cloud Run for serverless backend deployment.

## 5. Tech Stack
- **Frontend**: React, TypeScript, Vite, TailwindCSS (optional integration)
- **Backend**: Python, FastAPI
- **Database**: Supabase
- **Cloud/Deployment**: Google Cloud Run, Docker

## 6. Installation
1. Clone the repository: `git clone https://github.com/harshad1234u/carboniq.git`
2. Install frontend dependencies: `cd frontend && npm install`
3. Install backend dependencies: `cd backend && pip install -r requirements.txt`

## 7. Environment Variables
See `backend/.env.example` and `frontend/.env.example` for the required environment variables.
Create a `.env` file in both `backend/` and `frontend/` directories using the examples provided. **Do not commit actual keys to source control.**

## 8. Local Development
- **Backend**: `cd backend && uvicorn main:app --reload`
- **Frontend**: `cd frontend && npm run dev`

## 9. Cloud Run Deployment
The backend can be containerized using the provided `Dockerfile` and deployed to Google Cloud Run.
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/carboniq-backend
gcloud run deploy carboniq-backend --image gcr.io/PROJECT-ID/carboniq-backend --platform managed
```

## 10. Screenshots
(Placeholder for screenshots demonstrating the CarbonIQ platform)

## 11. API Documentation
When running locally, access the interactive API documentation at `http://localhost:8000/docs`.

## 12. Testing Results
The platform includes automated tests using `pytest` for the backend.
Run tests via:
```bash
cd backend && pytest
```

## 13. Security Notes
- All sensitive environment variables (API keys, Supabase secrets) are excluded from source control.
- JWT-based authentication ensures secure access.
- Make sure to review `.env.example` placeholders to avoid leaking real keys.

## 14. Future Improvements
- Deeper integration with IoT devices for real-time tracking
- Advanced analytics using Machine Learning
- Expansion of gamification features
