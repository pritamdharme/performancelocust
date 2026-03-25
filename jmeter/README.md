# JMeter Performance Testing Framework

> **Alternative to Locust** — Same scenarios, different approach
>
> Choose JMeter if you prefer GUI-based test design or need to integrate with existing JMeter infrastructure.

---

## 📊 Test Plans Overview

| Test Plan | File | Users | Ramp | Duration | Purpose |
|---|---|---|---|---|---|
| **Load Test** | `BookingLoad.jmx` | 100 | 60s | 3 min | Normal peak traffic simulation |
| **Spike Test** | `SpikeTest.jmx` | 200 | 2s | 2 min | Sudden burst resilience |
| **Stress Test** | `StressTest.jmx` | 500 | 5 min | 10 min | Find system breaking point |
| **Soak Test** | `SoakTest.jmx` | 50 | 60s | 60 min | Memory leaks & degradation |

---

## 🚀 Quick Start

### Prerequisites
- JMeter 5.4+ installed
- Java 11+

### Install JMeter (Windows)

```bash
# Option 1: Chocolatey
choco install jmeter

# Option 2: Manual download
# Download from https://jmeter.apache.org/download_jmeter.cgi
# Extract and add to PATH
```

### Run a Test Plan (GUI Mode)

```bash
cd jmeter
jmeter -t test-plans/BookingLoad.jmx
```

Then in JMeter:
1. File → Open Recent
2. Select `BookingLoad.jmx`
3. Click **▶ Run** (or Ctrl+R)
4. Watch live metrics in "View Results Tree"

### Run Headless (CI/Scripted)

```bash
# Load Test - Generate HTML report
jmeter -n -t test-plans/BookingLoad.jmx \
  -l results/LoadTest_Results.jtl \
  -j jmeter.log \
  -e -o results/LoadTest_Report

# Spike Test
jmeter -n -t test-plans/SpikeTest.jmx \
  -l results/SpikeTest_Results.jtl

# Stress Test
jmeter -n -t test-plans/StressTest.jmx \
  -l results/StressTest_Results.jtl

# Soak Test (1 hour - runs in background)
jmeter -n -t test-plans/SoakTest.jmx \
  -l results/SoakTest_Results.jtl &
```

### View Reports

After headless run, open the report:
```bash
# Windows
start results/LoadTest_Report/index.html

# macOS
open results/LoadTest_Report/index.html

# Linux
xdg-open results/LoadTest_Report/index.html
```

---

## 📁 File Structure

```
jmeter/
├── test-plans/              # JMeter test plan files (.jmx)
│   ├── BookingLoad.jmx      # Load test (100 users, 3 min)
│   ├── SpikeTest.jmx        # Spike test (200 users, instant)
│   ├── StressTest.jmx       # Stress test (500 users, ramped)
│   └── SoakTest.jmx         # Soak test (50 users, 60 min)
│
├── data/                    # Test data (CSV format)
│   └── bookings.csv         # Booking payload data
│
├── config/                  # Configuration files
│   └── config.properties    # Performance thresholds & settings
│
└── results/                 # Test results (generated)
    └── *_Results.csv        # Results from each test
    └── *_Report/            # HTML reports (headless mode)
```

---

## 🎯 What Each Test Does

### 1. **Load Test** (`BookingLoad.jmx`)
- **Scenario**: Normal peak-hour traffic
- **Users**: 100 concurrent
- **Ramp**: 60 seconds (1 new user/sec)
- **Duration**: 3 minutes
- **Personas**:
  - 50% Read-Only (list & browse bookings)
  - 30% Booking Users (create & update)
  - 15% Admin (full lifecycle)
  - 5% Auth Stress (token generation)

**What to look for**:
- P95 response time < 2 seconds
- Failure rate < 1%
- Consistent throughput

---

### 2. **Spike Test** (`SpikeTest.jmx`)
- **Scenario**: Sudden traffic burst (flash sale, viral event, DDoS-lite)
- **Users**: 200 concurrent
- **Ramp**: 2 seconds (instant spike)
- **Duration**: 2 minutes
- **Key behavior**: NO ramp-up = all users hit at once

**What to look for**:
- Can system handle instant 200-user spike?
- Does it recover quickly after spike?
- Any timeouts or 500 errors?

---

### 3. **Stress Test** (`StressTest.jmx`)
- **Scenario**: Gradual load increase to find breaking point
- **Users**: Ramp from 100 → 500 users
- **Ramp**: 5 minutes
- **Duration**: 10 minutes total

**What to look for**:
- At what user count do failures appear?
- Response times increase linearly or exponentially?
- Are there memory/CPU bottlenecks?
- Where's your system's ceiling?

---

### 4. **Soak Test** (`SoakTest.jmx`)
- **Scenario**: Sustained load for extended time
- **Users**: 50 concurrent
- **Ramp**: 60 seconds
- **Duration**: 60 minutes (run overnight!)

**What to look for**:
- Memory leaks (gradual latency increase)
- Connection pool exhaustion
- Database degradation over time
- Crashes after X hours

---

## ⚙️ Configuration

Edit `config/config.properties` to customize thresholds:

```properties
# Base URL
BASE_URL=https://restful-booker.herokuapp.com

# Performance Thresholds
P95_THRESHOLD_MS=2000       # 95th percentile must be under 2 seconds
P99_THRESHOLD_MS=5000       # 99th percentile must be under 5 seconds
FAILURE_RATE_THRESHOLD_PCT=1.0  # Less than 1% failures

# Load Test
LOAD_TEST_USERS=100
LOAD_TEST_RAMP_UP_SECS=60
LOAD_TEST_DURATION_MINS=3

# Spike Test
SPIKE_TEST_USERS=200
SPIKE_TEST_RAMP_UP_SECS=2
SPIKE_TEST_DURATION_MINS=2

# And so on...
```

---

## 📊 Understanding JMeter Test Plans

### Core Elements

| Element | Purpose |
|---|---|
| **Thread Group** | Defines # of users, ramp-up time, duration |
| **HTTP Request** | Single API call (GET, POST, etc.) |
| **CSV Data Set** | Load test data from `bookings.csv` |
| **Assertions** | Validate response (must be 200, etc.) |
| **Listeners** | Collect & display results |
| **Controllers** | Logic (if/else, loops, etc.) |

### Example: Adding a New API Call

1. Open JMeter → Load test plan
2. Right-click **Thread Group** → Add → Sampler → HTTP Request
3. Fill in:
   - **Name**: `PUT /booking/{id}` 
   - **Method**: PUT
   - **Path**: `/booking/1`
   - **Body Data**: `{"firstname":"Updated"}`
4. Right-click → Add → Assertions → Response Assertion
5. Set response code = 200

---

## 📈 Analyzing Results

### CSV Results Format

Each results file contains:
```
timeStamp,elapsed,label,responseCode,responseMessage,threadName,dataType,success,failureMessage,bytes,sentBytes,grpThreads,allThreads,Latency
```

**Key columns**:
- `elapsed` — Response time in milliseconds
- `responseCode` — HTTP status (200, 500, etc.)
- `success` — true/false
- `Latency` — Time to first byte

### HTML Report (Headless Mode)

After running with `-e -o results/Report/`:
- **Summary Report** — Overview of all metrics
- **Aggregate Report** — Percentiles (P50, P90, P95, P99)
- **Response Times Over Time** — Graph of latency trends
- **Transactions Per Second** — Throughput graph
- **Errors** — Failed requests breakdown

---

## 🔧 Tips & Best Practices

### 1. **Use CSV Data Sets**
- Leverage `bookings.csv` for realistic payloads
- Add more data rows for longer tests
- Use "Random" line selection for variety

### 2. **Correlate Responses**
- Extract ID from POST response
- Use in subsequent requests (e.g., GET /booking/{id})
- Add **Regular Expression Extractor** or **JSON Extractor**

### 3. **Monitor Resources**
- Watch CPU, memory, disk during tests
- Use **Windows Performance Monitor** or **top` command
- Look for resource exhaustion

### 4. **Ramp-Up Gradually**
- Don't start with 1000 users instantly
- Gradual ramp reveals bottleneck thresholds
- Helps identify whether problem is @ startup or under load

### 5. **Think Time**
- Add realistic delays between requests
- Use **Constant Timer** (fixed delay) or **Random Timer** (variable)
- Simulate real user behavior

---

## 🐛 Troubleshooting

### "Connection refused"
```
→ Check BASE_URL in config or test plan
→ Verify API server is running
→ Check firewall/proxy settings
```

### "Response Code = 500"
```
→ Recent changes to API?
→ Check request payload format
→ Look at API server logs
```

### "Test runs very slow"
```
→ Reduce # of threads
→ Check think-time (delays between requests)
→ Verify CSV data set line count
```

### "Out of memory"
```
→ Increase JMeter heap: HEAP=-Xmx4096m jmeter
→ Reduce # of threads
→ Use "Results File Writer" instead of UI listeners
```

---

## 📚 Locust vs. JMeter

| Aspect | Locust | JMeter |
|---|---|---|
| **Language** | Python code | XML config |
| **Learning curve** | Gradual (write code) | Steep (complex UI) |
| **Flexibility** | Very high | Medium |
| **Distributed** | Easy (Python distributed) | Hard (requires plugins) |
| **Realism** | Excellent (custom logic) | Good (standard flows) |
| **UI** | Beautiful web dashboard | Dense Swing UI |
| **Scripting** | Full Python power | Limited |

**Choose Locust if**: You love Python, need custom logic, want easy distributed testing  
**Choose JMeter if**: Your team knows JMeter, you prefer GUI, you need to integrate with existing JMeter infra

---

## 📖 Resources

- [JMeter User Manual](https://jmeter.apache.org/usermanual/index.html)
- [JMeter Best Practices](https://jmeter.apache.org/usermanual/best-practices.html)
- [Regular Expressions in JMeter](https://jmeter.apache.org/usermanual/functions.html)
- [JSON Extraction Guide](https://jmeter.apache.org/usermanual/component_reference.html#JSON_Extractor)

---

## 💡 Next Steps

1. ✅ Run **Load Test** first (3 min, no risk)
2. ✅ Analyze results — check P95, P99, failures
3. ✅ Run **Spike Test** — test resilience
4. ✅ Run **Stress Test** — find your ceiling
5. ✅ Schedule **Soak Test** overnight
6. ✅ Share results with team/stakeholders

---

**Happy Load Testing! 🚀**
