"""Seed Railway with all questions"""
import requests
import time

URL = "https://ai-interview-trainer-backend-production.up.railway.app"

print("Waiting for Railway...")
for i in range(20):
    try:
        r = requests.get(f"{URL}/api/health", timeout=5)
        if r.status_code == 200:
            print("Railway is back!\n")

            r1 = requests.post(f"{URL}/api/setup/seed")
            d1 = r1.json()
            print(f"General: {r1.status_code} - {d1.get('message', d1.get('detail', ''))}")

            r2 = requests.post(f"{URL}/api/setup/seed-companies")
            d2 = r2.json()
            print(f"Companies: {r2.status_code} - {d2.get('message', d2.get('detail', ''))}")

            # Login and verify
            r3 = requests.post(f"{URL}/api/auth/login", json={
                "email": "admin@interview-trainer.app",
                "password": "admin123",
            })
            if r3.status_code == 200:
                token = r3.json()["access_token"]
                headers = {"Authorization": f"Bearer {token}"}
                r4 = requests.get(f"{URL}/api/user/admin/stats", headers=headers)
                if r4.status_code == 200:
                    s = r4.json()
                    print(f"\nFinal stats:")
                    print(f"  Users: {s['total_users']}")
                    print(f"  Questions: {s['total_questions']}")
            break
    except Exception:
        pass
    print(f"  waiting... {i+1}/20")
    time.sleep(10)
