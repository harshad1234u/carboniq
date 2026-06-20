# CarbonIQ – Architecture

## System Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────────┐
│   Frontend   │────▶│   Backend    │────▶│  Supabase DB     │
│  React+Vite  │     │   FastAPI    │     │  PostgreSQL+RLS  │
└──────┬───────┘     └──────┬───────┘     └──────────────────┘
       │                    │
       │                    ├────▶ Gemini API (AI Coach)
       │                    ├────▶ OpenWeather API
       │                    │
       └────────────────────┘
              Supabase Auth
```

## Data Flow

1. User authenticates via Supabase Auth (frontend direct)
2. Frontend sends JWT token to backend with API requests
3. Backend validates JWT, processes business logic via service layer
4. Backend stores/retrieves data from Supabase PostgreSQL
5. Backend calls Gemini/OpenWeather when needed (with fallbacks)
6. Frontend renders results with loading/error/empty states

## Backend Structure

```
backend/
├── main.py                    # FastAPI app entry point
├── api/
│   ├── profile.py             # Auth + profile endpoints
│   ├── carbon.py              # Calculator + AI Coach + Eco Twin + Weather
│   └── dashboard.py           # Dashboard + challenges + badges
├── services/                  # Business logic (never in routes)
│   ├── carbon_calculator.py
│   ├── weather_service.py
│   ├── ai_coach_service.py
│   ├── eco_twin_service.py
│   ├── impact_equivalent_service.py
│   ├── savings_calculator_service.py
│   ├── challenge_service.py
│   └── profile_service.py
├── models/                    # Pydantic schemas
├── database/                  # Supabase client + repositories
├── utils/                     # Config, validators, emission factors
└── tests/                     # Unit + integration tests
```

## Frontend Structure

```
frontend/src/
├── App.tsx                    # Router with lazy-loaded routes
├── lib/supabase.ts            # Supabase client
├── components/
│   ├── ui/                    # ShadCN components
│   ├── Layout.tsx             # App shell
│   ├── ProtectedRoute.tsx     # Auth guard
│   └── ...                    # Feature components
├── pages/                     # Route pages
├── hooks/                     # Custom React hooks
├── services/api.ts            # Backend API client
└── utils/                     # Constants, formatters
```

## Database Schema

### Tables
- **profiles** – User profile linked to auth.users(id)
- **carbon_entries** – Historical footprint calculations
- **recommendations** – AI coach responses with savings
- **eco_predictions** – Eco Twin before/after data
- **challenges** – Weekly sustainability tasks
- **badges** – Earned achievements

### Security
- Row Level Security (RLS) on ALL tables
- Users can only access their own data via `auth.uid() = profile_id`
- Service role key used only on backend, never exposed to frontend

## API Structure

### profile.py
- `POST /api/auth/signup`
- `POST /api/auth/login`
- `GET /api/profile`
- `PUT /api/profile`

### carbon.py
- `POST /api/carbon/calculate`
- `POST /api/carbon/ai-coach`
- `POST /api/carbon/eco-twin`
- `GET /api/carbon/weather/{city}`

### dashboard.py
- `GET /api/dashboard/summary`
- `GET /api/dashboard/history`
- `GET /api/challenges`
- `POST /api/challenges/{id}/complete`
- `GET /api/badges`
