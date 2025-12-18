import logging
import os
from dotenv import load_dotenv
from spotify_service import SpotifyService
from downloader import Downloader

# Configure logging to console for this script
logging.basicConfig(level=logging.DEBUG)

load_dotenv()

def test_download():
    print("Initializing services...")
    try:
        spotify = SpotifyService()
        downloader = Downloader()
    except Exception as e:
        print(f"Failed to init services: {e}")
        return

    # Test Album URL
    test_url = "https://open.spotify.com/album/1kCHru7uhxBUdzkm4gzRQc" # Hamilton (Original Broadway Cast Recording) - just checking fetch, not download all
    
    print(f"Testing album fetch for: {test_url}")
    
    try:
        album_name = spotify.get_album_name(test_url)
        print(f"Album Name: {album_name}")
        
        tracks = spotify.get_album_tracks(test_url)
        if not tracks:
            print("Failed to get album tracks")
            return
            
        print(f"Found {len(tracks)} tracks in album.")
        print(f"First track: {tracks[0]['name']} - {tracks[0]['artist']}")
        
        # We won't download all of them in debug to save time/bandwidth
        # Just verify we got the list
        
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    test_download()
