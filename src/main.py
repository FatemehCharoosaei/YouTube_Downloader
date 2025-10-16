import argparse
from pathlib import Path
from yt_dlp import YoutubeDL
import os
class YouTubeDownloader:
   """
   A class to download YouTube videos using yt-dlp with optimized settings for speed.
   """
   def __init__(self, url, output_path=None, quality=None):
       self.url = url
       self.output_path = output_path or str(Path.cwd())
       
       # Create output directory if it doesn't exist
       os.makedirs(self.output_path, exist_ok=True)
       
       # Optimized format selection for speed
       self.quality = quality or "best[height<=720][ext=mp4]/best[height<=720]"
       
       self.ydl_opts = {
           'format': self.quality,
           'outtmpl': f'{self.output_path}/%(title)s.%(ext)s',
           'progress_hooks': [self._hook],
           'quiet': False,
           'no_warnings': False,
           # Optimizations for speed
           'http_chunk_size': 10485760,  # 10MB chunks
           'continuedl': True,
           'noprogress': False,
           'retries': 10,
           'fragment_retries': 10,
           'skip_unavailable_fragments': True,
           'keep_fragments': False,
           # No postprocessing for speed
           'postprocessors': [],
       }
   
   def download(self):
       try:
           with YoutubeDL(self.ydl_opts) as ydl:
               ydl.download([self.url])
           return True
       except Exception as e:
           print(f"❌ Download failed: {e}")
           return False
   
   def _hook(self, d):
       if d['status'] == 'downloading':
           percent = d.get('_percent_str', 'N/A')
           total_size = d.get('_total_bytes_str', 'N/A')
           speed = d.get('_speed_str', 'N/A')
           print(f"⬇️ Downloading: {percent} at {speed} - ETA: {d.get('_eta_str', 'N/A')}")
       elif d['status'] == 'finished':
           print(f"✅ Download completed: {d['filename']}")
if __name__ == "__main__":
   parser = argparse.ArgumentParser(description="Fast YouTube Downloader using yt-dlp")
   parser.add_argument("url", help="YouTube video URL")
   parser.add_argument("-q", "--quality", help="Video quality (e.g. best, 720p)", default=None)
   parser.add_argument("-o", "--output_path", help="Output directory", default=None)
   args = parser.parse_args()
   
   downloader = YouTubeDownloader(
       url=args.url,
       quality=args.quality,
       output_path=args.output_path,
   )
   downloader.download()