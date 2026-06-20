# CarbonIQ – Architectural Decisions

## Decision Log

### 1. Use Supabase Auth instead of custom authentication
- **Date**: 2026-06-19
- **Reason**: Provides production-grade security (JWT, session management, RLS integration) without custom implementation. Supports Email/Password + Google Sign-In. Reduces attack surface.

### 2. Consolidate API routes into 3 files
- **Date**: 2026-06-19
- **Reason**: Avoids excessive file fragmentation. `profile.py` (auth+profile), `carbon.py` (calculator+AI+eco-twin+weather), `dashboard.py` (dashboard+challenges+badges) provides logical grouping while keeping each file manageable.

### 3. Use configurable emission factors from EPA/DEFRA/IPCC
- **Date**: 2026-06-19
- **Reason**: Scientifically recognized sources provide credibility. Storing factors in a separate config file makes them easy to update without changing business logic.

### 4. Use India CEA grid factor (0.82 kg CO₂/kWh) as default
- **Date**: 2026-06-19
- **Reason**: Target user base includes Indian users. Factor is configurable for other regions.

### 5. Implement fallback recommendations for Gemini failures
- **Date**: 2026-06-19
- **Reason**: AI services are unreliable (rate limits, timeouts, quota). Predefined recommendations ensure the app continues working without Gemini.

### 6. Use TailwindCSS v4 with CSS-first configuration
- **Date**: 2026-06-19
- **Reason**: Latest standard, no PostCSS config needed, simplified Vite plugin setup, ShadCN compatible.

### 7. No Framer Motion – CSS transitions only
- **Date**: 2026-06-19
- **Reason**: Keeps bundle size small. CSS transitions + Recharts animations provide sufficient visual polish without adding a large dependency.

### 8. Dark mode with emerald/green theme
- **Date**: 2026-06-19
- **Reason**: Sustainability branding (green = eco). Dark mode is modern, reduces eye strain, and looks premium.

### 9. Cost savings in INR (₹) as default
- **Date**: 2026-06-19
- **Reason**: Aligns with Indian user base. Currency is configurable in savings_calculator_service.py.

### 10. Row Level Security on all tables
- **Date**: 2026-06-19
- **Reason**: Defense in depth. Even if backend is compromised, users cannot access other users' data at the database level.

### 11. Global React Context for Authentication State
- **Date**: 2026-06-20
- **Reason**: Using `useAuth` as a standalone hook caused massive redundancy, generating multiple parallel `GET /profile` requests per active component and leading to infinite 404 loading loops. Migrating to an `AuthContext` ensures the session and profile completeness flag are fetched precisely once, making state management predictable and improving performance.
