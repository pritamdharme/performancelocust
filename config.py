import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL       = os.getenv("BASE_URL", "https://restful-booker.herokuapp.com")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "password123")

# ── Load profile thresholds ────────────────────────────────────────────────
THRESHOLDS = {
    "response_time_p95_ms": 2000,   # 95th percentile must be under 2s
    "response_time_p99_ms": 5000,   # 99th percentile must be under 5s
    "failure_rate_pct":     1.0,    # Less than 1% failures allowed
}
