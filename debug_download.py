import requests
import json

def test_download():
    url = 'http://localhost:5000/download'
    # Song: "Never Gonna Give You Up" by Rick Astley (Classic test)
    spotify_url = 'https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT'
    
    print(f"Testing download for: {spotify_url}")
    
    try:
        response = requests.post(url, json={'url': spotify_url}, stream=True)
        
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("Response Stream:")
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    print(f"Received: {decoded_line}")
                    try:
                        data = json.loads(decoded_line)
                        if data.get('status') == 'error':
                            print(f"❌ Error reported by server: {data.get('message')}")
                        elif data.get('status') == 'completed':
                            print("✅ Download completed successfully!")
                    except json.JSONDecodeError:
                        print("Could not parse JSON")
        else:
            print(f"❌ Request failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    test_download()
