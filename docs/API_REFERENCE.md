# CarbonIQ – API Reference

Base URL: `http://localhost:8000/api`

All endpoints except auth require `Authorization: Bearer <jwt_token>` header.

---

## Authentication & Profile (`/api`)

### POST /api/auth/signup
Create a new user account.
```json
Request: { "email": "user@example.com", "password": "securePass123", "name": "John" }
Response: { "user_id": "uuid", "email": "user@example.com", "access_token": "jwt" }
```

### POST /api/auth/login
Login with email/password.
```json
Request: { "email": "user@example.com", "password": "securePass123" }
Response: { "user_id": "uuid", "access_token": "jwt", "profile_complete": true }
```

### GET /api/profile
Get current user's profile. **Auth required.**
```json
Response: { "id": "uuid", "name": "John", "email": "...", "city": "Mumbai", "transport_type": "car_petrol", "avg_travel_distance": 25, "diet_type": "average", "household_size": 3, "eco_points": 50 }
```

### PUT /api/profile
Update/complete profile. **Auth required.**
```json
Request: { "city": "Mumbai", "transport_type": "car_petrol", "avg_travel_distance": 25, "diet_type": "average", "household_size": 3 }
Response: { "id": "uuid", ...profile_fields }
```

---

## Carbon Calculator & AI (`/api/carbon`)

### POST /api/carbon/calculate
Calculate carbon footprint. **Auth required.**
```json
Request: { "vehicle_type": "car_petrol", "daily_travel_km": 25, "electricity_kwh": 200, "ac_hours": 4, "diet_type": "average", "flights_short": 2, "flights_long": 1 }
Response: { "transport_emissions": 157.5, "electricity_emissions": 164.0, "food_emissions": 75.0, "flight_emissions": 134.2, "total_emissions": 530.7, "carbon_score": { "score": 80, "level": "High Impact", "color": "orange" }, "impact_equivalents": { "driving_km": 2494, "smartphone_charges": 53070, "trees_to_offset": 24 } }
```

### POST /api/carbon/ai-coach
Get AI recommendations. **Auth required.**
```json
Request: { "entry_id": "uuid" }
Response: { "recommendations": [...], "total_co2_savings": 85.5, "total_cost_savings": 1200, "weather_context": {...} }
```

### POST /api/carbon/eco-twin
Get Eco Twin prediction. **Auth required.**
```json
Request: { "entry_id": "uuid", "recommendation_id": "uuid" }
Response: { "current_footprint": 530.7, "predicted_footprint": 365.2, "reduction_percentage": 31.2, "impact_equivalents": {...}, "recommendation_impacts": [...] }
```

### GET /api/carbon/weather/{city}
Get weather data for a city. **Auth required.**
```json
Response: { "city": "Mumbai", "temperature": 32, "description": "Humid", "humidity": 78 }
```

---

## Dashboard (`/api/dashboard`)

### GET /api/dashboard/summary
Get dashboard summary for current user. **Auth required.**
```json
Response: { "latest_score": {...}, "monthly_footprint": 530.7, "impact_equivalents": {...}, "active_challenge": {...}, "trend": [...] }
```

### GET /api/dashboard/history
Get carbon entry history. **Auth required.**
```json
Response: [{ "recorded_date": "2026-06-19", "total_emissions": 530.7, "carbon_score": 80 }, ...]
```

### GET /api/challenges
Get current weekly challenges. **Auth required.**
```json
Response: [{ "id": "uuid", "title": "Walk twice this week", "description": "...", "eco_points": 15, "is_completed": false }, ...]
```

### POST /api/challenges/{id}/complete
Mark a challenge as completed. **Auth required.**
```json
Response: { "id": "uuid", "is_completed": true, "eco_points_earned": 15 }
```

### GET /api/badges
Get earned badges. **Auth required.**
```json
Response: [{ "badge_name": "First Step", "badge_description": "Completed first calculation", "earned_at": "..." }, ...]
```
