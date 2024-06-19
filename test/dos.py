import requests

from config import HOST


for i in range(20):
    requests.post(
        f"http://{HOST}/DVWA/login.php",
        params={
            "login": "login",
            "password": "password"
        }
    )