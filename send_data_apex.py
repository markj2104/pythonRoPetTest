import requests
import certifi
import urllib3

# Optional: suppress InsecureRequestWarning if you ever disable SSL (not recommended)
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://apex.oracle.com/pls/apex/test_development_ropet/ropetdata/interactions/"
headers = {
    "Content-Type": "application/json",
    "User-Agent": "PythonClient/1.0"
}
payload = {
    "pet_id": 20,
    "head_move": 20,
    "tail_move": 20,
    "sound": 20
}

try:
    print("Sending POST request to Oracle APEX...")
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=10,
        verify=certifi.where()  # Use certifi's CA bundle for SSL verification
    )
    print(f"Status Code: {response.status_code}")
    if response.text:
        print(f"Response Body:\n{response.text}")
    else:
        print("No response body returned.")

except requests.exceptions.Timeout:
    print("Error: Request timed out.")

except requests.exceptions.SSLError as ssl_err:
    print(f"SSL Error: {ssl_err}")
    print("Try upgrading certifi package or disabling SSL verification (not recommended).")

except requests.exceptions.RequestException as err:
    print(f"Request failed: {err}")
