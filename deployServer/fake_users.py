import requests
import random

FAKE_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B)",
    "Mozilla/5.0 (iPad; CPU OS 13_6_1 like Mac OS X)",
    "curl/7.64.1",
    "PostmanRuntime/7.28.4",
    "Wget/1.20.3 (linux-gnu)"
]

SERVER_URL = "http://localhost/track"

def simulate_requests(n):
    for _ in range(n):
        ua = random.choice(FAKE_USER_AGENTS)
        r = requests.get(SERVER_URL, headers={"User-Agent": ua})
        print(f"Sent with User-Agent: {ua} → {r.status_code}")

if __name__ == "__main__":
    simulate_requests(100)
