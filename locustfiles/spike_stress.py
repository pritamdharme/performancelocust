"""
Spike & Stress Test Scenarios
==============================
Run these to identify system breaking points and recovery behaviour.

Spike test  : Sudden burst of traffic — tests system resilience
Stress test : Gradually increasing load beyond normal capacity — finds the ceiling
Soak test   : Sustained load over time — catches memory leaks and degradation
"""

from locust import HttpUser, task, between, constant_pacing, events
from locust.exception import RescheduleTask
import random

from utils.auth import get_auth_token
from test_data.payloads import random_booking
from config import THRESHOLDS

JSON_HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


class SpikeUser(HttpUser):
    """
    Spike test persona — no wait time between requests.
    Simulates a sudden traffic burst (flash sale, viral event, DDoS-lite).

    Run with:
      locust -f locustfiles/spike_stress.py SpikeUser \
        --headless -u 200 -r 200 --run-time 2m \
        --host https://restful-booker.herokuapp.com
    """
    wait_time = constant_pacing(1)   # 1 request/sec per user — pure spike pressure

    def on_start(self):
        self.token = get_auth_token()

    @task(6)
    def spike_read(self):
        with self.client.get("/booking", headers=JSON_HEADERS, name="SPIKE — GET /booking", catch_response=True) as r:
            if r.status_code == 200:
                r.success()
            else:
                r.failure(f"{r.status_code}")

    @task(3)
    def spike_create(self):
        with self.client.post(
            "/booking",
            json=random_booking(),
            headers=JSON_HEADERS,
            name="SPIKE — POST /booking",
            catch_response=True
        ) as r:
            if r.status_code == 200:
                r.success()
            else:
                r.failure(f"{r.status_code}")

    @task(1)
    def spike_auth(self):
        with self.client.post(
            "/auth",
            json={"username": "admin", "password": "password123"},
            headers=JSON_HEADERS,
            name="SPIKE — POST /auth",
            catch_response=True
        ) as r:
            if r.status_code == 200:
                r.success()
            else:
                r.failure(f"{r.status_code}")


class StressUser(HttpUser):
    """
    Stress test persona — very short wait times.
    Used with --spawn-rate to gradually ramp until the system buckles.

    Run with:
      locust -f locustfiles/spike_stress.py StressUser \
        --headless -u 500 -r 10 --run-time 10m \
        --host https://restful-booker.herokuapp.com

    Increase -u until P95 > 2s or failure rate > 1% to find the ceiling.
    """
    wait_time = between(0.5, 1.5)

    def on_start(self):
        self.token = get_auth_token()
        self.booking_ids = []

    @task(4)
    def stress_list(self):
        with self.client.get("/booking", headers=JSON_HEADERS, name="STRESS — GET /booking", catch_response=True) as r:
            if r.status_code == 200:
                r.success()
            else:
                r.failure(f"{r.status_code}")

    @task(3)
    def stress_create(self):
        with self.client.post(
            "/booking",
            json=random_booking(),
            headers=JSON_HEADERS,
            name="STRESS — POST /booking",
            catch_response=True
        ) as r:
            if r.status_code == 200:
                bid = r.json().get("bookingid")
                if bid:
                    self.booking_ids.append(bid)
                r.success()
            else:
                r.failure(f"{r.status_code}")

    @task(2)
    def stress_read_single(self):
        if not self.booking_ids:
            raise RescheduleTask()
        bid = random.choice(self.booking_ids)
        with self.client.get(
            f"/booking/{bid}",
            headers=JSON_HEADERS,
            name="STRESS — GET /booking/{id}",
            catch_response=True
        ) as r:
            if r.status_code == 200:
                r.success()
            else:
                r.failure(f"{r.status_code}")

    @task(1)
    def stress_delete(self):
        if not self.booking_ids:
            raise RescheduleTask()
        bid = self.booking_ids.pop()
        with self.client.delete(
            f"/booking/{bid}",
            headers={**JSON_HEADERS, "Cookie": f"token={self.token}"},
            name="STRESS — DELETE /booking/{id}",
            catch_response=True
        ) as r:
            if r.status_code == 201:
                r.success()
            else:
                r.failure(f"{r.status_code}")


class SoakUser(HttpUser):
    """
    Soak test persona — moderate load sustained over a long period.
    Catches memory leaks, connection pool exhaustion, and gradual degradation.

    Run with:
      locust -f locustfiles/spike_stress.py SoakUser \
        --headless -u 50 -r 5 --run-time 60m \
        --host https://restful-booker.herokuapp.com
    """
    wait_time = between(3, 8)   # Realistic pacing — sustained over hours

    def on_start(self):
        self.token = get_auth_token()

    @task(5)
    def soak_read(self):
        with self.client.get("/booking", headers=JSON_HEADERS, name="SOAK — GET /booking", catch_response=True) as r:
            r.success() if r.status_code == 200 else r.failure(f"{r.status_code}")

    @task(3)
    def soak_create_delete(self):
        """Create and immediately delete — tests connection recycling over time."""
        resp = self.client.post(
            "/booking", json=random_booking(),
            headers=JSON_HEADERS, name="SOAK — POST /booking"
        )
        if resp.status_code == 200:
            bid = resp.json().get("bookingid")
            if bid:
                self.client.delete(
                    f"/booking/{bid}",
                    headers={**JSON_HEADERS, "Cookie": f"token={self.token}"},
                    name="SOAK — DELETE /booking/{id}"
                )

    @task(2)
    def soak_health(self):
        with self.client.get("/ping", name="SOAK — GET /ping", catch_response=True) as r:
            r.success() if r.status_code == 201 else r.failure(f"{r.status_code}")


# ── Threshold check ────────────────────────────────────────────────────────────

@events.quitting.add_listener
def check_thresholds(environment, **kwargs):
    stats       = environment.runner.stats.total
    p95         = stats.get_response_time_percentile(0.95)
    p99         = stats.get_response_time_percentile(0.99)
    failure_pct = (stats.num_failures / stats.num_requests * 100) if stats.num_requests else 0
    failures    = 0

    print("\n── Spike/Stress Threshold Check ─────────────────────────")
    print(f"  P95 : {p95:.0f}ms | P99 : {p99:.0f}ms | Failures : {failure_pct:.2f}%")

    if p95 > THRESHOLDS["response_time_p95_ms"]:
        print(f"  ❌ P95 exceeded")
        failures += 1
    if failure_pct > THRESHOLDS["failure_rate_pct"]:
        print(f"  ❌ Failure rate exceeded")
        failures += 1

    print("  ✅ Passed" if failures == 0 else f"  {failures} breach(es) — FAILED")
    print("─────────────────────────────────────────────────────────\n")

    if failures:
        environment.process_exit_code = 1
