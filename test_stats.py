import requests
import os

# Create a dummy file in downloads if it doesn't exist
if not os.path.exists('downloads'):
    os.makedirs('downloads')
with open('downloads/test_file.mp3', 'w') as f:
    f.write('dummy content')

try:
    response = requests.get('http://127.0.0.1:5000/stats')
    if response.status_code == 200:
        data = response.json()
        print("Stats Endpoint Test Passed")
        print(f"Count: {data['count']}")
        print(f"Size: {data['size']}")
        print(f"History: {data['history']}")
    else:
        print(f"Stats Endpoint Failed: {response.status_code}")
except Exception as e:
    print(f"Error testing stats: {e}")
