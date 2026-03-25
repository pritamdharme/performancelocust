import random

FIRST_NAMES = ["Pritam", "Raj", "Amit", "Sneha", "Priya", "Vikram", "Neha", "Sanjay"]
LAST_NAMES  = ["Dharme", "Sharma", "Patel", "Kumar", "Singh", "Joshi", "Mehta", "Gupta"]
NEEDS       = ["Breakfast", "Lunch", "Dinner", "Late checkout", "Airport transfer", None]


def random_booking() -> dict:
    """Generate a randomised booking payload to simulate real user variance."""
    checkin_day  = random.randint(1, 20)
    checkout_day = checkin_day + random.randint(1, 10)
    needs        = random.choice(NEEDS)

    payload = {
        "firstname":   random.choice(FIRST_NAMES),
        "lastname":    random.choice(LAST_NAMES),
        "totalprice":  random.randint(50, 500),
        "depositpaid": random.choice([True, False]),
        "bookingdates": {
            "checkin":  f"2024-{random.randint(6, 11):02d}-{checkin_day:02d}",
            "checkout": f"2024-{random.randint(6, 11):02d}-{checkout_day:02d}",
        }
    }
    if needs:
        payload["additionalneeds"] = needs
    return payload


PARTIAL_UPDATES = [
    {"firstname": "Updated", "totalprice": 999},
    {"depositpaid": True},
    {"additionalneeds": "Extra pillow"},
    {"totalprice": random.randint(100, 800)},
]
