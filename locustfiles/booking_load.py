"""
Restful Booker — Locust Performance Framework
=============================================
User Personas:
  - ReadOnlyUser    : Simulates guests browsing bookings (high volume, read-only)
  - BookingUser     : Simulates customers creating & managing bookings (CRUD flows)
  - AdminUser       : Simulates admin staff doing full lifecycle operations
  - AuthStressUser  : Hammers the auth endpoint to test token generation under load

Run modes:
  locust -f locustfiles/booking_load.py                        # Interactive UI
  locust -f locustfiles/booking_load.py --headless ...         # CI/headless
"""

import random
from locust import HttpUser, TaskSet, task, between, events
from locust.exception import RescheduleTask

from utils.auth import get_auth_token
from test_data.payloads import random_booking, PARTIAL_UPDATES
from config import BASE_URL, THRESHOLDS


# ── Shared headers ─────────────────────────────────────────────────────────────

JSON_HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


def authed_headers(token: str) -> dict:
    return {**JSON_HEADERS, "Cookie": f"token={token}"}


# ── Task Sets ──────────────────────────────────────────────────────────────────

class ReadOnlyTasks(TaskSet):
    """
    Read-only browsing behaviour.
    Weighted towards listing bookings (most common real-world pattern).
    """

    @task(5)
    def get_all_bookings(self):
        with self.client.get("/booking", headers=JSON_HEADERS, name="GET /booking", catch_response=True) as r:
            if r.status_code == 200:
                r.success()
            else:
                r.failure(f"Expected 200, got {r.status_code}")

    @task(3)
    def get_booking_by_name(self):
        first = random.choice(["Pritam", "Raj", "Amit", "Sneha"])
        with self.client.get(
            f"/booking?firstname={first}",
            headers=JSON_HEADERS,
            name="GET /booking?firstname=",
            catch_response=True
        ) as r:
            if r.status_code == 200:
                r.success()
            else:
                r.failure(f"Filter failed: {r.status_code}")

    @task(2)
    def get_single_booking(self):
        # Get a random booking ID from the list first
        ids_resp = self.client.get("/booking", headers=JSON_HEADERS, name="GET /booking (for ID)")
        if ids_resp.status_code != 200:
            raise RescheduleTask()
        ids = ids_resp.json()
        if not ids:
            raise RescheduleTask()
        booking_id = random.choice(ids)["bookingid"]
        with self.client.get(
            f"/booking/{booking_id}",
            headers=JSON_HEADERS,
            name="GET /booking/{id}",
            catch_response=True
        ) as r:
            if r.status_code == 200:
                r.success()
            elif r.status_code == 404:
                r.failure("Booking not found")
            else:
                r.failure(f"Unexpected {r.status_code}")

    @task(1)
    def health_check(self):
        with self.client.get("/ping", name="GET /ping", catch_response=True) as r:
            if r.status_code == 201:
                r.success()
            else:
                r.failure(f"Health check failed: {r.status_code}")


class BookingCRUDTasks(TaskSet):
    """
    Full CRUD lifecycle — create → read → partial update → delete.
    Simulates a customer managing their own booking.
    """

    def on_start(self):
        """Authenticate once per simulated user session."""
        self.token = get_auth_token()
        self.created_ids = []

    @task(4)
    def create_booking(self):
        payload = random_booking()
        with self.client.post(
            "/booking",
            json=payload,
            headers=JSON_HEADERS,
            name="POST /booking",
            catch_response=True
        ) as r:
            if r.status_code == 200:
                booking_id = r.json().get("bookingid")
                if booking_id:
                    self.created_ids.append(booking_id)
                r.success()
            else:
                r.failure(f"Create failed: {r.status_code} — {r.text}")

    @task(3)
    def read_own_booking(self):
        if not self.created_ids:
            raise RescheduleTask()
        booking_id = random.choice(self.created_ids)
        with self.client.get(
            f"/booking/{booking_id}",
            headers=JSON_HEADERS,
            name="GET /booking/{id} (own)",
            catch_response=True
        ) as r:
            if r.status_code == 200:
                r.success()
            else:
                r.failure(f"Read failed: {r.status_code}")

    @task(2)
    def partial_update_booking(self):
        if not self.created_ids:
            raise RescheduleTask()
        booking_id = random.choice(self.created_ids)
        payload = random.choice(PARTIAL_UPDATES)
        with self.client.patch(
            f"/booking/{booking_id}",
            json=payload,
            headers=authed_headers(self.token),
            name="PATCH /booking/{id}",
            catch_response=True
        ) as r:
            if r.status_code == 200:
                r.success()
            else:
                r.failure(f"Partial update failed: {r.status_code}")

    @task(1)
    def delete_booking(self):
        if not self.created_ids:
            raise RescheduleTask()
        booking_id = self.created_ids.pop()
        with self.client.delete(
            f"/booking/{booking_id}",
            headers=authed_headers(self.token),
            name="DELETE /booking/{id}",
            catch_response=True
        ) as r:
            if r.status_code == 201:
                r.success()
            else:
                r.failure(f"Delete failed: {r.status_code}")


class AdminTasks(TaskSet):
    """
    Full lifecycle admin operations — heavier write load.
    Simulates staff doing bulk updates and cleanup.
    """

    def on_start(self):
        self.token = get_auth_token()
        self.managed_ids = []

    @task(3)
    def create_and_track(self):
        with self.client.post(
            "/booking",
            json=random_booking(),
            headers=JSON_HEADERS,
            name="POST /booking (admin)",
            catch_response=True
        ) as r:
            if r.status_code == 200:
                self.managed_ids.append(r.json()["bookingid"])
                r.success()
            else:
                r.failure(f"{r.status_code}")

    @task(3)
    def full_update(self):
        if not self.managed_ids:
            raise RescheduleTask()
        booking_id = random.choice(self.managed_ids)
        with self.client.put(
            f"/booking/{booking_id}",
            json=random_booking(),
            headers=authed_headers(self.token),
            name="PUT /booking/{id}",
            catch_response=True
        ) as r:
            if r.status_code == 200:
                r.success()
            else:
                r.failure(f"Full update failed: {r.status_code}")

    @task(2)
    def list_all_bookings(self):
        with self.client.get("/booking", headers=JSON_HEADERS, name="GET /booking (admin)", catch_response=True) as r:
            if r.status_code == 200:
                r.success()
            else:
                r.failure(f"{r.status_code}")

    @task(1)
    def bulk_delete(self):
        """Delete up to 3 managed bookings in one task execution."""
        to_delete = self.managed_ids[:3]
        for booking_id in to_delete:
            with self.client.delete(
                f"/booking/{booking_id}",
                headers=authed_headers(self.token),
                name="DELETE /booking/{id} (bulk)",
                catch_response=True
            ) as r:
                if r.status_code == 201:
                    self.managed_ids.remove(booking_id)
                    r.success()
                else:
                    r.failure(f"{r.status_code}")


class AuthStressTasks(TaskSet):
    """
    Stress test the auth endpoint specifically.
    Tests token generation throughput and failure handling.
    """

    @task(7)
    def valid_auth(self):
        with self.client.post(
            "/auth",
            json={"username": "admin", "password": "password123"},
            headers=JSON_HEADERS,
            name="POST /auth (valid)",
            catch_response=True
        ) as r:
            if r.status_code == 200 and "token" in r.json():
                r.success()
            else:
                r.failure(f"Auth failed: {r.text}")

    @task(3)
    def invalid_auth(self):
        with self.client.post(
            "/auth",
            json={"username": "wrong", "password": "wrong"},
            headers=JSON_HEADERS,
            name="POST /auth (invalid)",
            catch_response=True
        ) as r:
            # Expect 200 with "Bad credentials" — this is valid API behaviour
            if r.status_code == 200:
                r.success()
            else:
                r.failure(f"Unexpected status: {r.status_code}")


# ── User Personas ──────────────────────────────────────────────────────────────

class ReadOnlyUser(HttpUser):
    """
    Guest / anonymous user — browse-only behaviour.
    High volume, no writes. Represents the majority of traffic.
    """
    tasks       = [ReadOnlyTasks]
    wait_time   = between(1, 3)
    weight      = 50   # 50% of simulated users


class BookingUser(HttpUser):
    """
    Authenticated customer — full booking lifecycle.
    Moderate volume with CRUD operations.
    """
    tasks       = [BookingCRUDTasks]
    wait_time   = between(2, 5)
    weight      = 30   # 30% of simulated users


class AdminUser(HttpUser):
    """
    Admin persona — heavier write operations and bulk actions.
    Low volume but high write pressure.
    """
    tasks       = [AdminTasks]
    wait_time   = between(1, 2)
    weight      = 15   # 15% of simulated users


class AuthStressUser(HttpUser):
    """
    Auth-only stress persona — hammers the token endpoint.
    Used for auth service throughput testing.
    """
    tasks       = [AuthStressTasks]
    wait_time   = between(0.5, 1.5)
    weight      = 5    # 5% of simulated users


# ── Pass/Fail threshold check (used in CI) ────────────────────────────────────

@events.quitting.add_listener
def check_thresholds(environment, **kwargs):
    """
    Fail the CI run if performance thresholds are breached.
    Mirrors the kind of quality gate used in production pipelines.
    """
    stats = environment.runner.stats.total

    failures = 0

    p95 = stats.get_response_time_percentile(0.95)
    p99 = stats.get_response_time_percentile(0.99)
    failure_pct = (stats.num_failures / stats.num_requests * 100) if stats.num_requests else 0

    print("\n── Performance Threshold Check ──────────────────────────")
    print(f"  P95 response time : {p95:.0f}ms  (threshold: {THRESHOLDS['response_time_p95_ms']}ms)")
    print(f"  P99 response time : {p99:.0f}ms  (threshold: {THRESHOLDS['response_time_p99_ms']}ms)")
    print(f"  Failure rate      : {failure_pct:.2f}%  (threshold: {THRESHOLDS['failure_rate_pct']}%)")

    if p95 > THRESHOLDS["response_time_p95_ms"]:
        print(f"  ❌ FAIL — P95 {p95:.0f}ms exceeds {THRESHOLDS['response_time_p95_ms']}ms")
        failures += 1

    if p99 > THRESHOLDS["response_time_p99_ms"]:
        print(f"  ❌ FAIL — P99 {p99:.0f}ms exceeds {THRESHOLDS['response_time_p99_ms']}ms")
        failures += 1

    if failure_pct > THRESHOLDS["failure_rate_pct"]:
        print(f"  ❌ FAIL — Failure rate {failure_pct:.2f}% exceeds {THRESHOLDS['failure_rate_pct']}%")
        failures += 1

    if failures == 0:
        print("  ✅ All thresholds passed")
    else:
        print(f"\n  {failures} threshold(s) breached — marking run as FAILED")
        environment.process_exit_code = 1

    print("─────────────────────────────────────────────────────────\n")
