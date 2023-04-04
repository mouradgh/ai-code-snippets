import subprocess
import whisper
import ssl
import logging

# To bypass the SSL: CERTIFICATE_VERIFY_FAILED error
logging.info("Creating the context")
ssl._create_default_https_context = ssl._create_unverified_context

# Load the desired OpenAI model
# The available models are : tiny / base / small / medium / large
# The required Ram goes from 1Gb for tiny to 10Gb for large
logging.info("Loading the desired model")
model = whisper.load_model("base")  # You can also use "base.en" for English-only applications

# Put the names of the input video file and the output audio file
video_in = 'video.mp4'
audio_out = 'audio.mp3'

# Read the video file and convert it to an audio file
logging.info("Converting the video to audio")
ffmpeg_cmd = f"ffmpeg -i {video_in} -vn -c:a libmp3lame -b:a 192k {audio_out}"
subprocess.run(["ffmpeg", "-i", video_in, "-vn", "-c:a", "libmp3lame", "-b:a", "192k", audio_out])

# Transcribe
logging.info("Transcribing")
result = model.transcribe(audio_out)

# Show the result
logging.info("Transcript")
print(result["text"])