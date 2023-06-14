import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'
import uuid
import secrets
import string
import subprocess
import glob
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def browse_output_directory():
    output_dir = filedialog.askdirectory()
    if output_dir:
        selected_output_dir.set(output_dir)
    else:
        return filedialog.askdirectory()

def detect_scenes(input_file, threshold=0.1):
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
def generate_output_video():
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


def download_and_convert():
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

# Create the GUI
root = tk.Tk()
root.title("Video to Keyframes & GIFs")

url_label = tk.Label(root, text="Video URL:")
url_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)

overwrite_var = tk.IntVar()
overwrite_check = tk.Checkbutton(root, text="Overwrite files", variable=overwrite_var)
overwrite_check.grid(row=1, column=0, padx=5, pady=5, sticky="w")

default_output_dir_label = tk.Label(root, text="Default output directory:")
default_output_dir_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

selected_output_dir = tk.StringVar()

default_output_dir_entry = tk.Entry(root, width=50, textvariable=selected_output_dir)
default_output_dir_entry.grid(row=2, column=1, padx=5, pady=5)

browse_output_dir_button = tk.Button(root, text="Browse", command=browse_output_directory)
browse_output_dir_button.grid(row=2, column=2, padx=5, pady=5)

download_button = tk.Button(root, text="Download & Convert", command=download_and_convert)
download_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()


