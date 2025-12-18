import yt_dlp
import os

import logging

class Downloader:
    def __init__(self, download_path='downloads'):
        self.download_path = download_path
        if not os.path.exists(download_path):
            os.makedirs(download_path)

    def download_track(self, query, metadata, folder_name=None):
        """Download track with optional subfolder organization"""
        # Determine download path
        if folder_name:
            # Sanitize folder name
            import re
            sanitized_folder = re.sub(r'[<>:"/\\|?*]', '', folder_name)
            target_path = os.path.join(self.download_path, sanitized_folder)
            # Create folder if it doesn't exist
            if not os.path.exists(target_path):
                os.makedirs(target_path)
        else:
            target_path = self.download_path
            
        search_query = f"ytsearch1:{query}"
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                },
                {
                    'key': 'FFmpegMetadata',
                    'add_metadata': True,
                },
                {
                    'key': 'EmbedThumbnail',
                },
            ],
            'writethumbnail': True,
            'outtmpl': os.path.join(target_path, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search_query, download=True)
                if 'entries' in info:
                    video_info = info['entries'][0]
                else:
                    video_info = info
                
                filename = ydl.prepare_filename(video_info)
                final_filename = os.path.splitext(filename)[0] + '.mp3'
                
                return {
                    'status': 'success',
                    'filename': os.path.basename(final_filename),
                    'title': video_info.get('title', 'Unknown'),
                    'original_query': query
                }
        except Exception as e:
            logging.error(f"Error downloading {query}: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'query': query
            }
