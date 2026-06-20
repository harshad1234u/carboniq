# CarbonIQ – Project Context

## Status: 🟢 Testing & Verification Phase

## Project Goals
Build an AI-powered Carbon Footprint Awareness Platform that acts as a personal sustainability coach. The platform helps users understand, track, reduce, and predict their carbon footprint through personalized recommendations, future simulations, and measurable progress tracking.

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | React + Vite + TypeScript + TailwindCSS v4 + ShadCN UI + Recharts |
| Backend | FastAPI (Python) |
| Database | Supabase PostgreSQL |
| Auth | Supabase Auth (Email/Password + Google Sign-In) |
| AI | Google Gemini API |
| Weather | OpenWeather API |

## Features In Scope
1. **Authentication** – Supabase Auth (Email/Password + Google)
2. **Profile Completion** – City, transport, diet, household size
3. **Carbon Calculator** – EPA/DEFRA/IPCC emission factors
4. **Carbon Score** – 0-100 scoring with 4 levels
5. **Impact Equivalents** – Real-world emission comparisons
6. **AI Carbon Coach** – Gemini-powered recommendations with cost savings
7. **Eco Twin Prediction** – Future footprint simulation
8. **Progress Dashboard** – Charts, trends, score display
9. **Weekly Challenges** – Gamified sustainability tasks
10. **Project Memory System** – docs/ directory for persistent context

## Features Excluded
- Blockchain / NFTs / Carbon trading
- Social media feeds
- Real-time GPS tracking
- Complex ML models
- Unnecessary third-party APIs

## Evaluation Priorities
1. Code Quality
2. Security (AuthContext ensures predictable and secure session state)
3. Testing
4. Accessibility
5. Real-world usability
6. Problem alignment
