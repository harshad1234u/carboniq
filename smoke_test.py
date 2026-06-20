import httpx
import sys

BASE_URL = "https://carboniq-backend-722791638231.asia-south1.run.app"
API_URL = f"{BASE_URL}/api"

def run_tests():
    print("Running Smoke Tests...")
    
    # 1. Health Check
    try:
        r = httpx.get(f"{BASE_URL}/health/readiness", timeout=10)
        assert r.status_code == 200
        print("[PASS] Backend Readiness Check")
    except Exception as e:
        print(f"[FAIL] Backend Readiness Check: {e}")
        sys.exit(1)

    print("All basic smoke tests passed.")

if __name__ == "__main__":
    run_tests()
