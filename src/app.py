import streamlit as st
from main import YouTubeDownloader
from pathlib import Path
import tempfile
import sys
import time
import os
st.set_page_config(page_title="Sara YouTube Downloader", page_icon="⚡", layout="centered")
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Logo_of_YouTube_%282015-2017%29.svg/2560px-Logo_of_YouTube_%282015-2017%29.svg.png", width=400)
st.title("Sara YouTube Downloader")
st.markdown("Download YouTube videos quickly with optimized settings")
url = st.text_input("Enter YouTube URL", placeholder="https://youtu.be/...")
output_path = st.text_input("Output Folder", value=str(Path.home() / "Downloads"))
download_type = st.radio("Download Type", ["Video + Audio", "Audio Only", "Video Only"])
quality_map = {
   "Fastest (480p)": "best[height<=480][ext=mp4]/best[height<=480]",
   "Medium (720p)": "best[height<=720][ext=mp4]/best[height<=720]",
   "High Quality (1080p)": "best[height<=1080][ext=mp4]/best[height<=1080]",
   "Best Available": "best[ext=mp4]/best",
   "Audio Only (m4a)": "bestaudio[ext=m4a]",
   "Video Only (mp4)": "bestvideo[ext=mp4]"
}
if download_type == "Audio Only":
   selected_quality = "Audio Only (m4a)"
elif download_type == "Video Only":
   selected_quality = "Video Only (mp4)"
else:
   selected_quality = st.selectbox("Select Quality", list(quality_map.keys())[:4])
if 'downloaded_file' not in st.session_state:
   st.session_state.downloaded_file = None
if 'download_success' not in st.session_state:
   st.session_state.download_success = False
if st.button("Start Fast Download", type="primary"):
   if not url.strip():
       st.warning("Please enter a valid YouTube URL.")
   else:
       st.info("Preparing download...")
       
       if download_type == "Audio Only":
           format_code = quality_map["Audio Only (m4a)"]
       elif download_type == "Video Only":
           format_code = quality_map["Video Only (mp4)"]
       else:
           format_code = quality_map[selected_quality]
       
       progress_bar = st.progress(0)
       status_text = st.empty()
       
       with tempfile.TemporaryDirectory() as temp_dir:
           temp_output = temp_dir
           
           try:
               downloader = YouTubeDownloader(
                   url=url,
                   output_path=temp_output,
                   quality=format_code
               )
               
               start_time = time.time()
               
               def run_download():
                   return downloader.download()
               
               success = run_download()
               
               if success:
                   downloaded_files = list(Path(temp_output).glob("*"))
                   if downloaded_files:
                       downloaded_file_path = str(downloaded_files[0])
                       st.session_state.downloaded_file = downloaded_file_path
                       st.session_state.download_success = True
                       
                       st.success("Download completed successfully!")
                       
                       file_extension = os.path.splitext(downloaded_file_path)[1].lower()
                       file_size = os.path.getsize(downloaded_file_path) / (1024 * 1024)
                       
                       st.subheader("Downloaded File")
                       st.info(f"File size: {file_size:.2f} MB")
                       
                       if file_extension in ['.mp4', '.webm', '.mkv', '.avi', '.mov']:
                           if file_size > 50:
                               st.warning("Large video file - preview may take time")
                               video_file = open(downloaded_file_path, 'rb')
                               video_bytes = video_file.read()
                               st.download_button(
                                   label="Download Video",
                                   data=video_bytes,
                                   file_name=os.path.basename(downloaded_file_path),
                                   mime="video/mp4"
                               )
                           else:
                               video_file = open(downloaded_file_path, 'rb')
                               video_bytes = video_file.read()
                               st.video(video_bytes)
                               st.download_button(
                                   label="Download Video",
                                   data=video_bytes,
                                   file_name=os.path.basename(downloaded_file_path),
                                   mime="video/mp4"
                               )
                       elif file_extension in ['.m4a', '.mp3', '.wav', '.ogg']:
                           audio_file = open(downloaded_file_path, 'rb')
                           audio_bytes = audio_file.read()
                           st.audio(audio_bytes, format=f"audio/{file_extension[1:]}")
                           st.download_button(
                               label="Download Audio",
                               data=audio_bytes,
                               file_name=os.path.basename(downloaded_file_path),
                               mime=f"audio/{file_extension[1:]}"
                           )
                       else:
                           st.download_button(
                               label="Download File",
                               data=open(downloaded_file_path, 'rb').read(),
                               file_name=os.path.basename(downloaded_file_path)
                           )
                   else:
                       st.error("Downloaded file not found")
               else:
                   st.error("Download failed")
                   
           except Exception as e:
               st.error(f"Download error: {e}")
if st.session_state.downloaded_file and os.path.exists(st.session_state.downloaded_file):
   st.subheader("Last Downloaded File")
   
   file_extension = os.path.splitext(st.session_state.downloaded_file)[1].lower()
   
   try:
       if file_extension in ['.mp4', '.webm', '.mkv', '.avi', '.mov']:
           video_file = open(st.session_state.downloaded_file, 'rb')
           video_bytes = video_file.read()
           st.video(video_bytes)
           st.download_button(
               label="Download Video Again",
               data=video_bytes,
               file_name=os.path.basename(st.session_state.downloaded_file),
               mime="video/mp4"
           )
       elif file_extension in ['.m4a', '.mp3', '.wav', '.ogg']:
           audio_file = open(st.session_state.downloaded_file, 'rb')
           audio_bytes = audio_file.read()
           st.audio(audio_bytes, format=f"audio/{file_extension[1:]}")
           st.download_button(
               label="Download Audio Again",
               data=audio_bytes,
               file_name=os.path.basename(st.session_state.downloaded_file),
               mime=f"audio/{file_extension[1:]}"
           )
   except Exception as e:
       st.error(f"File display error: {e}")
st.markdown("---")
st.markdown("Built with Python + yt-dlp + Streamlit")