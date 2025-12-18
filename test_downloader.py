from downloader import Downloader
import logging

logging.basicConfig(level=logging.DEBUG)

try:
    dl = Downloader()
    print("Downloader initialized")
    # Test with a dummy query that should return results quickly
    result = dl.download_track("Rick Astley Never Gonna Give You Up", {})
    print("Download result:", result)
except Exception as e:
    print("Error:", e)
