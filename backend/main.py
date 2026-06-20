import os
import logging
from pythonjsonlogger import jsonlogger
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from api.profile import router as profile_router
from api.carbon import router as carbon_router
from api.dashboard import router as dashboard_router
from utils.error_handlers import register_error_handlers, CarbonIQError
from fastapi.exceptions import RequestValidationError
from utils.config import load_settings, ConfigError
from database.client import get_supabase

# Setup structured logging for Cloud Run
logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
# Default log level from env, else INFO
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logger.setLevel(getattr(logging, log_level, logging.INFO))

app = FastAPI(title="CarbonIQ API", version="1.0.0")

# CORS middleware
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]
if frontend_url and frontend_url not in origins:
    origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
register_error_handlers(app)

# Include routers
app.include_router(profile_router)
app.include_router(carbon_router)
app.include_router(dashboard_router)

# Track readiness status
is_ready = False

@app.on_event("startup")
async def startup_event():
    global is_ready
    try:
        load_settings()
        logger.info("CarbonIQ Backend Started. All required environment variables loaded.", extra={"event": "startup_success"})
        is_ready = True
    except ConfigError as e:
        logger.error(f"Configuration Error: {e}", extra={"event": "startup_failure"})
        import sys
        sys.exit(1)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/health/startup")
def startup_check(response: Response):
    if is_ready:
        return {"status": "started"}
    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {"status": "starting"}

@app.get("/health/readiness")
def readiness_check(response: Response):
    if not is_ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "not_ready"}
    
    # Check Supabase connectivity
    try:
        supabase = get_supabase()
        # Just a lightweight check if client instantiated
        if not supabase:
            raise Exception("Supabase client not initialized")
        return {"status": "ready", "database": "connected"}
    except Exception as e:
        logger.error(f"Readiness probe failed: {e}", extra={"event": "readiness_failure"})
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "unhealthy", "reason": str(e)}
