from flask import Flask, render_template, request, Response, stream_with_context, jsonify, send_from_directory
import json
import os
import io
from dotenv import load_dotenv
from spotify_service import SpotifyService
from downloader import Downloader
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3

import logging

load_dotenv()

# Configure logging for Render (stdout)
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s %(levelname)s %(name)s : %(message)s')

# Validate credentials early
if not os.getenv("SPOTIPY_CLIENT_ID") or not os.getenv("SPOTIPY_CLIENT_SECRET"):
    logging.error("Missing Spotify credentials in environment variables")
    raise RuntimeError("Faltan credenciales de Spotify en variables de entorno (SPOTIPY_CLIENT_ID/SECRET)")

app = Flask(__name__)

# Ensure downloads directory exists
os.makedirs("downloads", exist_ok=True)

# Initialize services
try:
    spotify = SpotifyService()
    downloader = Downloader()
except Exception as e:
    logging.error(f"Error initializing services: {e}")
    spotify = None
    downloader = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/play/<path:filename>')
def play_file(filename):
    response = send_from_directory('downloads', filename)
    response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response

@app.route('/download/<path:filename>')
def download_file(filename):
    """Universal download route - works on Android, iOS, and PC"""
    file_path = os.path.join('downloads', filename)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    return send_from_directory(
        'downloads',
        filename,
        as_attachment=True,
        download_name=os.path.basename(filename),
        mimetype='audio/mpeg'
    )

@app.route('/cover/<path:filename>')
def cover_art(filename):
    try:
        path = os.path.join('downloads', filename)
        # logging.debug(f"Requested cover for: {path}")
        
        if not os.path.exists(path):
            # logging.warning(f"File not found: {path}")
            response = send_from_directory('static', 'default_cover.png')
            response.headers['Cache-Control'] = 'public, max-age=31536000'
            return response

        audio = ID3(path)
        for tag in audio.values():
            if isinstance(tag, APIC):
                response = Response(io.BytesIO(tag.data), mimetype=tag.mime)
                response.headers['Cache-Control'] = 'public, max-age=31536000'
                return response
    except Exception as e:
        # logging.error(f"Error extracting cover for {filename}: {e}")
        pass 
    
    response = send_from_directory('static', 'default_cover.png')
    response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response

@app.route('/stats')
def stats():
    download_path = 'downloads'
    if not os.path.exists(download_path):
        return jsonify({'count': 0, 'size': '0 MB', 'library': {}})

    library = {}
    total_count = 0
    total_size_bytes = 0

    # Walk through downloads directory
    for root, dirs, files in os.walk(download_path):
        folder = os.path.relpath(root, download_path)
        if folder == '.':
            folder = 'Uncategorized'
        
        if folder not in library:
            library[folder] = []

        for f in files:
            if f.endswith('.mp3'):
                path = os.path.join(root, f)
                size = os.path.getsize(path)
                total_count += 1
                total_size_bytes += size
                
                # Read metadata
                try:
                    from mutagen.easyid3 import EasyID3
                    from mutagen.mp3 import MP3
                    
                    audio_file = MP3(path)
                    length = audio_file.info.length
                    minutes = int(length // 60)
                    seconds = int(length % 60)
                    duration_str = f"{minutes}:{seconds:02d}"

                    audio = EasyID3(path)
                    title = audio.get('title', [f])[0]
                    artist = audio.get('artist', ['Unknown Artist'])[0]
                    album = audio.get('album', ['Unknown Album'])[0]
                except Exception as e:
                    logging.warning(f"Error reading metadata for {f}: {e}")
                    title = f
                    artist = "Unknown Artist"
                    album = "Unknown Album"
                    duration_str = "0:00"

                # Relative path for playback
                rel_path = os.path.join(folder, f) if folder != 'Uncategorized' else f
                # Normalize path separators for web
                rel_path = rel_path.replace('\\', '/')

                library[folder].append({
                    'filename': f,
                    'path': rel_path,
                    'title': title,
                    'artist': artist,
                    'album': album,
                    'duration': duration_str,
                    'size': size,
                    'timestamp': os.path.getmtime(path)
                })

    total_size_mb = f"{total_size_bytes / (1024 * 1024):.2f} MB"

    # Flatten library to a single list for the frontend
    all_tracks = []
    for folder, tracks in library.items():
        all_tracks.extend(tracks)
    
    # Sort by modification time (newest first) if possible, or just reverse
    # We need to get modification time. Let's add it to the track object above or just sort by name for now.
    # Better: let's sort by file modification time.
    # We need to re-iterate or store mtime in the loop above.
    
    # Let's just sort by name for now, or add a timestamp field in the loop above.
    # Actually, let's update the loop above to include timestamp.
    
    return jsonify({
        'count': total_count,
        'size': total_size_mb,
        'library': library,
        'tracks': sorted(all_tracks, key=lambda x: x.get('timestamp', 0), reverse=True)
    })

@app.route('/download', methods=['POST'])
def download():
    if not spotify:
        return jsonify({'status': 'error', 'message': 'Server configuration error (Spotify credentials missing)'}), 500

    data = request.json
    url = data.get('url')
    
    def generate():
        try:
            if 'track' in url:
                yield json.dumps({'status': 'processing', 'message': 'Fetching track info...'}) + '\n'
                track = spotify.get_track_info(url)
                if track:
                    folder_name = track['artist']  # Use Artist name for single tracks
                    yield json.dumps({'status': 'processing', 'message': f"Found: {track['name']} - {track['artist']}"}) + '\n'
                    
                    # Create search query for YouTube
                    search_query = f"{track['name']} {track['artist']}"
                    
                    yield json.dumps({'status': 'processing', 'message': f"Searching YouTube for: {search_query}"}) + '\n'
                    # Pass folder_name to organize by artist
                    result = downloader.download_track(search_query, track, folder_name=folder_name)
                    
                    if result.get('status') == 'success':
                        yield json.dumps({'status': 'completed', 'message': f"Downloaded: {track['name']}"}) + '\n'
                    else:
                        yield json.dumps({'status': 'error', 'message': result.get('message', 'Download failed')}) + '\n'
                else:
                    yield json.dumps({'status': 'error', 'message': 'Could not fetch track info'}) + '\n'
            
            elif 'playlist' in url:
                yield json.dumps({'status': 'processing', 'message': 'Fetching playlist info...'}) + '\n'
                # Get playlist name for folder organization
                playlist_name = spotify.get_playlist_name(url)
                tracks = spotify.get_playlist_tracks(url)
                if tracks:
                    yield json.dumps({'status': 'processing', 'message': f"Found playlist '{playlist_name}' with {len(tracks)} tracks"}) + '\n'
                    
                    for i, track in enumerate(tracks):
                        search_query = f"{track['name']} {track['artist']}"
                        yield json.dumps({'status': 'processing', 'message': f"Downloading {i+1}/{len(tracks)}: {track['name']}"}) + '\n'
                        
                        # Pass playlist_name as folder_name to organize tracks
                        result = downloader.download_track(search_query, track, folder_name=playlist_name)
                        
                        if result.get('status') == 'success':
                            yield json.dumps({'status': 'completed', 'message': f"Downloaded: {track['name']}"}) + '\n'
                        else:
                            yield json.dumps({'status': 'error', 'message': f"Failed: {track['name']} - {result.get('message', 'Unknown error')}"}) + '\n'
                else:
                    yield json.dumps({'status': 'error', 'message': 'Could not fetch playlist info'}) + '\n'

            elif 'album' in url:
                yield json.dumps({'status': 'processing', 'message': 'Fetching album info...'}) + '\n'
                album_name = spotify.get_album_name(url)
                tracks = spotify.get_album_tracks(url)
                if tracks:
                    yield json.dumps({'status': 'processing', 'message': f"Found album '{album_name}' with {len(tracks)} tracks"}) + '\n'
                    
                    for i, track in enumerate(tracks):
                        search_query = f"{track['name']} {track['artist']}"
                        yield json.dumps({'status': 'processing', 'message': f"Downloading {i+1}/{len(tracks)}: {track['name']}"}) + '\n'
                        
                        result = downloader.download_track(search_query, track, folder_name=album_name)
                        
                        if result.get('status') == 'success':
                            yield json.dumps({'status': 'completed', 'message': f"Downloaded: {track['name']}"}) + '\n'
                        else:
                            yield json.dumps({'status': 'error', 'message': f"Failed: {track['name']} - {result.get('message', 'Unknown error')}"}) + '\n'
                else:
                    yield json.dumps({'status': 'error', 'message': 'Could not fetch album info'}) + '\n'
            
            else:
                 yield json.dumps({'status': 'error', 'message': 'Invalid Spotify URL'}) + '\n'

        except Exception as e:
            logging.error(f"Error in download stream: {e}", exc_info=True)
            yield json.dumps({'status': 'error', 'message': str(e)}) + '\n'

    return Response(stream_with_context(generate()), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
