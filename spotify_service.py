import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

import logging

class SpotifyService:
    def __init__(self):
        self.client_id = os.getenv('SPOTIPY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        
        if not self.client_id or not self.client_secret:
            raise ValueError("Spotify credentials not found in environment variables")
            
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=self.client_id,
            client_secret=self.client_secret
        ))

    def _clean_url(self, url):
        import re
        # Extract ID and type using regex
        # Matches: .../track/ID, .../playlist/ID, .../album/ID
        match = re.search(r'(track|playlist|album)/([a-zA-Z0-9]+)', url)
        if match:
            type_ = match.group(1)
            id_ = match.group(2)
            return f"https://open.spotify.com/{type_}/{id_}"
        
        # Fallback to simple cleaning if no match (though regex should cover valid cases)
        url = url.strip()
        if '?' in url:
            url = url.split('?')[0]
        return url

    def get_track_info(self, url):
        try:
            url = self._clean_url(url)
            track = self.sp.track(url)
            return {
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'image': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'url': track['external_urls']['spotify']
            }
        except Exception as e:
            logging.error(f"Error fetching track for URL '{url}': {e}")
            return None

    def get_playlist_tracks(self, url):
        try:
            url = self._clean_url(url)
            results = self.sp.playlist_tracks(url)
            tracks = results['items']
            while results['next']:
                results = self.sp.next(results)
                tracks.extend(results['items'])
            
            cleaned_tracks = []
            for item in tracks:
                track = item['track']
                if track:
                    cleaned_tracks.append({
                        'name': track['name'],
                        'artist': track['artists'][0]['name'],
                        'album': track['album']['name'],
                        'image': track['album']['images'][0]['url'] if track['album']['images'] else None,
                        'url': track['external_urls']['spotify']
                    })
            return cleaned_tracks
        except Exception as e:
            logging.error(f"Error fetching playlist: {e}")
            return None
    
    def get_playlist_name(self, url):
        """Get playlist name and return sanitized folder name"""
        try:
            url = self._clean_url(url)
            playlist = self.sp.playlist(url)
            # Sanitize playlist name for folder
            import re
            name = playlist['name']
            # Remove invalid characters for Windows/Unix file systems
            sanitized = re.sub(r'[<>:"/\\|?*]', '', name)
            return sanitized.strip()
        except Exception as e:
            logging.error(f"Error getting playlist name: {e}")
            return "Unknown Playlist"

    def get_album_tracks(self, url):
        try:
            url = self._clean_url(url)
            results = self.sp.album_tracks(url)
            tracks = results['items']
            while results['next']:
                results = self.sp.next(results)
                tracks.extend(results['items'])
            
            cleaned_tracks = []
            for track in tracks:
                # Album tracks object is slightly different, doesn't have 'track' key wrapper
                if track:
                    cleaned_tracks.append({
                        'name': track['name'],
                        'artist': track['artists'][0]['name'],
                        'album': "Unknown Album", # Album tracks don't always have album info in the list item
                        'image': None, # Images are usually on the album object, not individual tracks here
                        'url': track['external_urls']['spotify']
                    })
            return cleaned_tracks
        except Exception as e:
            logging.error(f"Error fetching album: {e}")
            return None

    def get_album_name(self, url):
        """Get album name and return sanitized folder name"""
        try:
            url = self._clean_url(url)
            album = self.sp.album(url)
            import re
            name = album['name']
            sanitized = re.sub(r'[<>:"/\\|?*]', '', name)
            return sanitized.strip()
        except Exception as e:
            logging.error(f"Error getting album name: {e}")
            return "Unknown Album"
