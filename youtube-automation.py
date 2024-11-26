import os
from moviepy.editor import *
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random
import json
import numpy
from datetime import datetime


class ShortsCreator:
    def __init__(self):
        # Create required directories if they don't exist
        self.output_dir = "output_shorts"
        self.background_dir = "backgrounds"
        self.temp_dir = "temp"

        for directory in [self.output_dir, self.background_dir, self.temp_dir]:
            os.makedirs(directory, exist_ok=True)

    def get_random_background(self):
        """Get a random background video from the backgrounds directory"""
        try:
            background_videos = [f for f in os.listdir(self.background_dir)
                                 if f.endswith(('.mp4', '.MP4', '.mov', '.MOV'))]

            if not background_videos:
                raise Exception("No background videos found in backgrounds directory!")

            return os.path.join(self.background_dir, random.choice(background_videos))
        except Exception as e:
            print(f"Error getting background video: {e}")
            return None

    def create_text_overlay(self, text, size=(720, 1280)):
        """Create text overlay for the video"""
        try:
            # Create blank image
            img = Image.new('RGBA', size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # Try to use Arial font, fallback to default if not available
            try:
                font = ImageFont.truetype("arial.ttf", 70)
            except OSError:
                # Fallback to default font
                font = ImageFont.load_default()
                print("Warning: Arial font not found, using default font")

            # Wrap text
            wrapper = textwrap.TextWrapper(width=20)
            word_list = wrapper.wrap(text)

            # Calculate text position
            font_size = 300
            text_height = len(word_list) * font_size
            y = (size[1] - text_height) // 2

            # Draw text
            for line in word_list:
                line_width = draw.textlength(line, font=font)
                x = (size[0] - line_width) // 2

                # Draw outline
                outline_color = "black"
                outline_width = 3
                for adj in range(-outline_width, outline_width + 1):
                    for adj2 in range(-outline_width, outline_width + 1):
                        draw.text((x + adj, y + adj2), line, font=font, fill=outline_color)

                # Draw main text
                draw.text((x, y), line, font=font, fill="white")
                y += font_size + 10

            return img
        except Exception as e:
            print(f"Error creating text overlay: {e}")
            return None

    def create_voice_over(self, text, filename):
        """Create voice over using gTTS"""
        try:
            tts = gTTS(text=text, lang='en')
            tts.save(filename)
            return AudioFileClip(filename)
        except Exception as e:
            print(f"Error creating voice over: {e}")
            return None

    def create_short(self, text, background_video_path=None, output_filename=None):
        """Create a complete short video"""
        try:
            # If no background video specified, get random one
            if not background_video_path:
                background_video_path = self.get_random_background()
                if not background_video_path:
                    raise Exception("No background video available!")

            # If no output filename specified, generate one
            if not output_filename:
                output_filename = f"short_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"

            print(f"Creating short with background: {background_video_path}")

            # Load and prepare background video
            video = VideoFileClip(background_video_path).resize(height=1280)
            video = video.crop(x_center=video.w / 2, y_center=video.h / 2,
                               width=720, height=1280)

            # Create text overlay
            text_img = self.create_text_overlay(text)
            text_clip = ImageClip(numpy.array(text_img))

            # Create voice over
            temp_audio = os.path.join(self.temp_dir, "temp_voice.mp3")
            voice_clip = self.create_voice_over(text, temp_audio)

            # Adjust durations
            video = video.set_duration(voice_clip.duration)
            text_clip = text_clip.set_duration(voice_clip.duration)

            # Combine video, text, and audio
            final_video = CompositeVideoClip([video, text_clip])
            final_video = final_video.set_audio(voice_clip)

            # Write output file
            output_path = os.path.join(self.output_dir, output_filename)
            final_video.write_videofile(
                output_path,
                fps=30,
                codec='libx264',
                audio_codec='aac'
            )

            # Cleanup
            os.remove(temp_audio)
            print(f"Successfully created short: {output_path}")

        except Exception as e:
            print(f"Error creating short: {e}")


# Example usage
if __name__ == "__main__":
    # Example content
    sample_facts = [
        "Did you know? Honey never spoils. Archaeologists found 3000-year-old honey in Egyptian tombs!",
        "The average person spends 6 months of their lifetime waiting for red lights to turn green.",
        "A day on Venus is longer than its year! It takes 243 Earth days to rotate on its axis.",
    ]

    creator = ShortsCreator()

    # Create a short for each fact
    for i, fact in enumerate(sample_facts):
        print(f"\nCreating short {i + 1} of {len(sample_facts)}")
        creator.create_short(fact)