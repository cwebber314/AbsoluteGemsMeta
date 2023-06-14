from flask import Flask, request, jsonify
import boto3
import os
# ... [Your other imports go here] ...
#os.environ['TK_SILENCE_DEPRECATION'] = '1'
import uuid
import secrets
import string
import subprocess
import glob
import re
import tkinter as tk
from tkinter import filedialog, messagebox

app = Flask(__name__)

s3 = boto3.client('s3', aws_access_key_id='YOUR_ACCESS_KEY', aws_secret_access_key='YOUR_SECRET_KEY')

@app.route('/process-video', methods=['POST'])
def process_video():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'Video URL is missing.'}), 400

    output_dir = "your_output_dir"  # Set your output directory here

    try:
        # Add your video processing logic here, using the 'url' variable for the video URL
        # and the 'output_dir' variable for the output directory
    
            # ... [Your code goes here] ...

    #def browse_output_directory():   
        output_dir = filedialog.askdirectory()
        if output_dir:
            selected_output_dir.set(output_dir)
        else:
            return filedialog.askdirectory()
    
    #def detect_scenes(input_file, threshold=0.1):    
        scene_detection_cmd = ["ffmpeg", "-i", input_file, "-filter_complex", f"select='gt(scene,{threshold})',metadata=print:file=-", "-f", "null", "-"]
        scene_detection_proc = subprocess.Popen(scene_detection_cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        scene_detection_output = scene_detection_proc.communicate()[0].decode("utf-8")
        scene_timestamps = re.findall(r"pts_time:(\d+\.\d+)", scene_detection_output)
        return scene_timestamps

        #overwrite
        overwrite = overwrite_var.get()

        if overwrite:
            os.makedirs(output_dir, exist_ok=True)
        else:
            os.makedirs(output_dir)

    #def generate_output_video():
        input_video = glob.glob(f"{output_dir}/input_video.*")[0]
        cmd = [
            "ffmpeg",
            "-i",
            input_video,
            "-c:v",
            "libx264",
            "-crf",
            "23",
            "-vf",
            "scale=-1:1920",
            "-map",
            "0:v",
            "-f",
            "mp4",
            f"{output_dir}/output.mp4",
        ]
        subprocess.run(cmd, check=True)


    #def download_and_convert():
        url = url_entry.get()

        if not url:
            messagebox.showerror("Error", "Please enter a Video URL")
            return

        output_dir = selected_output_dir.get()

        if not output_dir:
            messagebox.showerror("Error", "Please select an output directory")
            return

        #overwrite
        overwrite = overwrite_var.get()

        if overwrite:
            os.makedirs(output_dir, exist_ok=True)
        else:
            os.makedirs(output_dir)

        # Create a folder named after the link to put everything in it
        dl_info_cmd = ["yt-dlp", "--get-title", url]
        dl_info_proc = subprocess.run(dl_info_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        folder_name = dl_info_proc.stdout.strip().replace('/', '-')
        output_dir = os.path.join(output_dir, folder_name)
        os.makedirs(output_dir, exist_ok=True)

        segments_dir = os.path.join(output_dir, "segments")
        os.makedirs(segments_dir, exist_ok=True)

        gifs_dir = os.path.join(output_dir, "gifs")
        os.makedirs(gifs_dir, exist_ok=True)

        images_dir = os.path.join(output_dir, "images")
        os.makedirs(images_dir, exist_ok=True)

        try:
            # Download the video
            subprocess.run(["yt-dlp", "-f", "best[ext=mp4]", "-o", f"{output_dir}/input_video.mp4", url])


            # Detect and remove letterboxing
            cropdetect_cmd = ["ffmpeg", "-i", f"{output_dir}/input_video.mp4", "-vf", "cropdetect=80:16:0", "-f", "null", "-"]
            cropdetect_proc = subprocess.Popen(cropdetect_cmd, stderr=subprocess.PIPE)
            cropdetect_output = cropdetect_proc.communicate()[1].decode("utf-8")
            cropdetect_matches = re.findall(r"crop=\d+:\d+:\d+:\d+", cropdetect_output)
            if cropdetect_matches:
                crop_params = cropdetect_matches[-1]
                crop_cmd = ["ffmpeg", "-i", f"{output_dir}/input_video.mp4", "-vf", crop_params, "-c:a", "copy", f"{output_dir}/output.mp4"]
            else:
                crop_cmd = ["cp", f"{output_dir}/input_video.mp4", f"{output_dir}/output.mp4"]
            subprocess.run(crop_cmd)

            # Detect scenes
            scene_timestamps = detect_scenes(f"{output_dir}/output.mp4", threshold=0.2)

            # Calculate segment durations using scene timestamps
            segment_durations = [float(scene_timestamps[i + 1]) - float(scene_timestamps[i]) for i in range(len(scene_timestamps) - 1)]

            # Segment the video based on scene changes
            prev_timestamp = 0
            for i, duration in enumerate(segment_durations):
                subprocess.run(["ffmpeg", "-ss", str(prev_timestamp), "-t", str(duration), "-i", f"{output_dir}/output.mp4", "-c", "copy", f"{segments_dir}/segment_{i:04d}.mp4"])
                prev_timestamp += duration


            # Get a list of segment files
            segments = [f for f in os.listdir(segments_dir) if f.startswith("segment_") and f.endswith(".mp4")]

            for segment in segments:
                random_name = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))

                # Extract keyframe from the segment and save it in the "images" folder
                subprocess.run(["ffmpeg", "-i", f"{segments_dir}/{segment}", "-vf", "select='eq(pict_type,I)',scale=3840:-1:flags=lanczos", "-vsync", "vfr", "-qscale:v", "2", f"{images_dir}/{random_name}_keyframe_original.jpg"])

                # Convert the segment to an animated GIF
                subprocess.run(["ffmpeg", "-i", f"{segments_dir}/{segment}", "-vf", "scale=1920:-1:flags=lanczos", "-f", "gif", f"{gifs_dir}/{random_name}.gif"])

            # Remove segment files after the loop
            for segment in segments:
                os.remove(f"{segments_dir}/{segment}")

            # Remove the input video file
            os.remove(f"{output_dir}/input_video.mp4")

            # Remove the output video file
            os.remove(f"{output_dir}/output.mp4")

            messagebox.showinfo("Success", "Keyframes & GIFs have been generated!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


        # Assuming 'image_files' and 'gif_files' are lists of paths to the created images and gifs
        image_urls = []
        for image_file in image_files:
            image_key = 'your_s3_folder/' + os.path.basename(image_file)
            s3.upload_file(image_file, 'your_bucket_name', image_key)
            image_url = f'https://your_bucket_name.s3.amazonaws.com/{image_key}'
            image_urls.append(image_url)

        gif_urls = []
        for gif_file in gif_files:
            gif_key = 'your_s3_folder/' + os.path.basename(gif_file)
            s3.upload_file(gif_file, 'your_bucket_name', gif_key)
            gif_url = f'https://your_bucket_name.s3.amazonaws.com/{gif_key}'
            gif_urls.append(gif_url)

        return jsonify({'image_urls': image_urls, 'gif_urls': gif_urls})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)


