import urllib.request
import json
import urllib.error

url = 'http://127.0.0.1:5000/tasks/extract'
data = json.dumps({"notes": "Meeting with Bob.\n- Fix the login screen."}).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

try:
    with urllib.request.urlopen(req) as response:
        print("SUCCESS:", response.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP ERROR:", e.code, e.read().decode())
except Exception as e:
    print("OTHER ERROR:", str(e))
