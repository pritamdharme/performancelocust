# Locust Performance Testing Framework

![Locust](https://img.shields.io/badge/Locust-2.24-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![CI](https://github.com/pritamdharme/locust-performance/actions/workflows/locust.yml/badge.svg)
![License](https://img.shields.io/badge/License-MIT-yellow)

A production-style performance testing framework built with **Python + Locust**, covering load, spike, stress, and soak testing with multiple user personas and CI/CD integration via GitHub Actions.

Built by **Pritam Dharme** — SDET with 10+ years of experience.

---

## ⭐ Key Features

- **Multi-persona testing** — 4 realistic user personas (guest, customer, admin, stress-user)
- **4 test scenarios** — Load, Spike, Stress, and Soak tests for comprehensive coverage
- **Automated thresholds** — CI build automatically fails if P95/P99/failure-rate breach targets
- **Token caching** — Auth once per session, not per request (realistic + efficient)
- **Randomised payloads** — Realistic test data that simulates actual user variance
- **CI/CD ready** — GitHub Actions pipeline with automated smoke → load → spike progression
- **Headless + UI modes** — Run interactively for exploration or headless for CI
- **HTML reports** — Download artifacts from every CI run with full metrics

---

## 💡 Real-World Use Cases

| Scenario | What You'll Discover |
|---|---|
| **Load Test** | System handles normal peak traffic (100 concurrent users) |
| **Spike Test** | Sudden DDoS/flash-sale burst (200 users in 2 seconds) — can it recover? |
| **Stress Test** | System breaking point — find your max capacity (500+ users) |
| **Soak Test** | Memory leaks, connection pool degradation over 1 hour |

---

## What this framework covers

| Scenario | File | Users | Purpose |
|---|---|---|---|
| Load test | `booking_load.py` | Mixed personas | Normal traffic simulation |
| Spike test | `spike_stress.py SpikeUser` | 150–200 | Sudden burst resilience |
| Stress test | `spike_stress.py StressUser` | 500+ | Find system ceiling |
| Soak test | `spike_stress.py SoakUser` | 50 / 60min | Memory leak & degradation |

---

## User Personas

| Persona | Weight | Behaviour |
|---|---|---|
| `ReadOnlyUser` | 50% | Guest browsing — list & read bookings |
| `BookingUser` | 30% | Customer CRUD — create, read, patch, delete |
| `AdminUser` | 15% | Staff operations — full lifecycle + bulk delete |
| `AuthStressUser` | 5% | Auth endpoint throughput testing |

---

## Project Structure

```
locust-performance/
│
├── locustfiles/
│   ├── booking_load.py       # Main load test — 4 user personas
│   └── spike_stress.py       # Spike, stress & soak scenarios
│
├── utils/
│   └── auth.py               # Token helper — auth once per user session
│
├── test_data/
│   └── payloads.py           # Randomised booking payloads
│
├── config.py                 # ENV config + performance thresholds
│
├── .github/
│   └── workflows/
│       └── locust.yml        # CI — smoke → load → spike (nightly)
│
└── reports/                  # HTML + CSV output (gitignored)
```

---

## Performance Thresholds

Defined in `config.py` — the CI run **fails automatically** if these are breached:

| Metric | Threshold |
|---|---|
| P95 response time | < 2,000ms |
| P99 response time | < 5,000ms |
| Failure rate | < 1% |

---

## 🔧 Challenges Solved

### 1. **Authentication Under Load** 
Problem: Calling `/auth` on every request floods the auth endpoint.  
Solution: `get_auth_token()` fetches once per user session and reuses the token — 95% fewer auth calls.

### 2. **Realistic vs. Artificial Load**
Problem: Hammer testing doesn't reveal real bottlenecks.  
Solution: 4 personas with weighted task distributions (50% read, 30% create, 15% admin, 5% stress) mirrors production traffic.

### 3. **Finding System Limits**
Problem: Load tests pass but spike tests fail — when do you scale infrastructure?  
Solution: Separate scenarios isolate behavior: normal load vs. sudden spike vs. sustained stress.

### 4. **Threshold Validation**
Problem: Manual review of reports = slow feedback loop.  
Solution: Automatic CI gate — build fails if P95 > 2s or failure rate > 1%.

---

## 📊 Performance Metrics Captured

Each run generates:
- **Response time percentiles** — P50, P75, P95, P99
- **Failure rate & errors** — Catch 4xx/5xx/timeouts
- **Throughput** — Requests/sec under load
- **User ramp-up curves** — See where latency degrades
- **HTML reports** — Beautiful visuals for stakeholders

---

## 🚀 Choose Your Testing Framework

This repository includes **two approaches** to the same performance testing scenarios:

### 🐍 **Locust** (Python-driven)
```bash
cd locust/
locust -f locustfiles/booking_load.py --host https://restful-booker.herokuapp.com
```
✅ **Best for**: Python developers, custom logic, distributed testing, beautiful UI  
📍 **Location**: Root directory — `locustfiles/`, `utils/`, `test_data/`

### 🎯 **JMeter** (GUI-based)
```bash
cd jmeter/
jmeter -t test-plans/BookingLoad.jmx
```
✅ **Best for**: Teams with JMeter expertise, existing JMeter infrastructure  
📍 **Location**: `/jmeter` directory — `test-plans/`, `data/`, `config/`  
📖 **Docs**: See [jmeter/README.md](jmeter/README.md) for full guide

**Same scenarios, different tools** — pick what works for your team!

---

## Getting Started

### Prerequisites
- Python >= 3.11

### ⚡ 5-Minute Quick Start

```bash
# Clone & install
git clone https://github.com/pritamdharme/locust-performance.git
cd locust-performance
pip install -r requirements.txt
cp .env.example .env

# Run interactive test (opens http://localhost:8089)
locust -f locustfiles/booking_load.py --host https://restful-booker.herokuapp.com
```

Then in the browser:
1. Enter **100 users** and **10 spawn-rate**
2. Click **"Start swarming"**
3. Watch live metrics: requests/sec, response times, failures
4. Stop after 2-3 min and download the HTML report

---

### Prerequisites

```bash
git clone https://github.com/pritamdharme/locust-performance.git
cd locust-performance
pip install -r requirements.txt
cp .env.example .env
```

### Run — Interactive UI (recommended for first run)

```bash
locust -f locustfiles/booking_load.py --host https://restful-booker.herokuapp.com
# Open http://localhost:8089 → set users & spawn rate → Start
```

### Run — Headless (CI / scripted)

```bash
# Load test — 100 users, ramp 10/sec, run 3 minutes
locust -f locustfiles/booking_load.py \
  --headless -u 100 -r 10 --run-time 3m \
  --host https://restful-booker.herokuapp.com \
  --html reports/report.html

# Spike test — instant burst of 200 users
locust -f locustfiles/spike_stress.py SpikeUser \
  --headless -u 200 -r 200 --run-time 2m \
  --host https://restful-booker.herokuapp.com

# Stress test — ramp to 500, find the ceiling
locust -f locustfiles/spike_stress.py StressUser \
  --headless -u 500 -r 10 --run-time 10m \
  --host https://restful-booker.herokuapp.com

# Soak test — 50 users for 1 hour
locust -f locustfiles/spike_stress.py SoakUser \
  --headless -u 50 -r 5 --run-time 60m \
  --host https://restful-booker.herokuapp.com
```

### View Report
Open `reports/report.html` in your browser.

---

## CI/CD Pipeline

```
Push / PR
    └── Smoke Load Test (20 users, 1m) ──── fast feedback

Push to main / Nightly
    ├── Full Load Test (100 users, 3m)
    └── Spike Test (150 users, instant ramp, 2m)
```

HTML reports and CSV stats uploaded as artifacts on every run (7–14 day retention).

---

## Tech Stack

- **Locust** — distributed load testing engine
- **Python** — test logic and personas
- **GitHub Actions** — CI/CD pipeline with threshold gates
- **python-dotenv** — environment variable management

---

## 🏆 Best Practices Demonstrated

- ✅ **DRY principle** — Shared headers, reusable auth, randomised payloads
- ✅ **Task weighting** — Realistic traffic distribution instead of uniform load
- ✅ **Error handling** — `catch_response=True` to track failures, not crash
- ✅ **Performance thresholds** — CI gates based on business SLAs, not arbitrary numbers
- ✅ **Modular code** — Utils separated from test logic for reusability
- ✅ **CI/CD integration** — Automated runs on push/PR with artifact storage
- ✅ **Env management** — `.env.example` for easy setup, no hardcoded secrets

---

## 📚 Suggested Enhancements (Future)

- [x] **JMeter alternative** — Same 4 scenarios in GUI-based format (✅ DONE!)
- [ ] Database performance profiling (slow query logs during load)
- [ ] Custom metrics (e.g., "booking success rate" vs. HTTP errors)
- [ ] Distributed testing across multiple machines
- [ ] Integration with monitoring (Datadog/New Relic alerts)
- [ ] Load test against staging with production data (anonymized)
- [ ] GraphQL performance testing
- [ ] WebSocket load testing

---

## 💬 Contributing

Found an issue? Want to add another scenario or persona?  
1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Add tests/scenarios in `locustfiles/` with docstrings
4. Update `test_data/payloads.py` if needed
5. Submit a PR with a clear description

---

## 📖 Resources

- [Locust Documentation](https://docs.locust.io/)
- [RESTful Booker API](https://restful-booker.herokuapp.com/)
- [Performance Testing Guide](https://en.wikipedia.org/wiki/Software_performance_testing)

---

## 👨‍💼 About the Author

**Pritam Dharme** — Senior SDET | Performance Testing Expert | 10+ years in QA Automation

This framework represents real-world performance testing patterns learned from:
- Building load tests for 100M+ user platforms
- Optimizing CI/CD pipelines to catch regressions early
- Training QA teams on production-grade test automation

📱 **Connect & Follow:**
- 🔗 LinkedIn: [linkedin.com/in/pritamdharme](https://linkedin.com/in/pritamdharme)
- 📧 Email: pritamdharme@gmail.com
- ⭐ Star this repo if it helped you!

---

## 📄 License

This project is licensed under the MIT License — See LICENSE file for details.

---

**Happy Performance Testing! 🚀**
