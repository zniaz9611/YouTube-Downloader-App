import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from pytubefix import YouTube
from pytubefix.exceptions import VideoUnavailable
import threading
import os
from moviepy.editor import VideoFileClip, AudioFileClip


# System Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


# App
class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("YouTube Video Downloader")
        self.geometry("720x550")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Title Label
        self.title_label = ctk.CTkLabel(self.main_frame, text="YouTube Video Downloader", font=("Roboto", 24))
        self.title_label.pack(padx=10, pady=20)

        # Link Input
        self.link_label = ctk.CTkLabel(self.main_frame, text="Insert a YouTube link")
        self.link_label.pack(padx=10, pady=(10, 0))

        self.url_var = tk.StringVar()
        self.link_entry = ctk.CTkEntry(self.main_frame, width=400, height=35, textvariable=self.url_var,
                                       placeholder_text="e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        self.link_entry.pack(padx=10, pady=10)
        self.link_entry.bind("<KeyRelease>", self.fetch_video_info)

        # Video Title Preview
        self.video_title_label = ctk.CTkLabel(self.main_frame, text="", wraplength=400, font=("Roboto", 16))
        self.video_title_label.pack(padx=10, pady=5)

        # Quality Selection and Audio-Only
        self.options_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.options_frame.pack(padx=10, pady=10)
        self.options_frame.grid_columnconfigure((0, 1), weight=1)

        self.quality_label = ctk.CTkLabel(self.options_frame, text="Select Quality:")
        self.quality_label.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="e")

        self.quality_var = ctk.StringVar(value="Loading...")
        self.quality_menu = ctk.CTkOptionMenu(self.options_frame, values=["Loading..."], variable=self.quality_var,
                                              state="disabled")
        self.quality_menu.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="w")

        self.audio_only_var = ctk.StringVar(value="off")
        self.audio_only_checkbox = ctk.CTkCheckBox(self.options_frame, text="Download Audio Only",
                                                   variable=self.audio_only_var, onvalue="on", offvalue="off")
        self.audio_only_checkbox.grid(row=1, column=0, columnspan=2, pady=5)
        self.audio_only_checkbox.configure(state="disabled")

        # Download Path
        self.path_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.path_frame.pack(padx=10, pady=10)
        self.path_frame.grid_columnconfigure(0, weight=1)

        self.path_entry = ctk.CTkEntry(self.path_frame, placeholder_text="Select download path...", width=300)
        self.path_entry.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.browse_button = ctk.CTkButton(self.path_frame, text="Browse", command=self.browse_path)
        self.browse_button.grid(row=0, column=1, padx=(5, 0))

        # Set the default download path
        self.path_entry.insert(0, os.path.join(os.path.expanduser("~"), "Downloads"))

        # Progress elements
        self.status_label = ctk.CTkLabel(self.main_frame, text="")
        self.status_label.pack(padx=10, pady=(10, 0))

        self.progress_bar = ctk.CTkProgressBar(self.main_frame, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(padx=10, pady=10)

        # Download Button
        self.download_button = ctk.CTkButton(self.main_frame, text="Download", command=self.start_download_thread,
                                             state="disabled")
        self.download_button.pack(padx=10, pady=20)

        # Instance variables for download
        self.yt_object = None
        self.download_thread = None

    def on_progress(self, stream, chunk, bytes_remaining):
        # Schedule the GUI update on the main thread
        self.after(0, self.update_progress_gui, stream, bytes_remaining)

    def update_progress_gui(self, stream, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = bytes_downloaded / total_size * 100

        self.progress_bar.set(percentage / 100)
        self.status_label.configure(text=f"Downloading: {int(percentage)}%")
        self.update_idletasks()

    def fetch_video_info(self, event=None):
        try:
            link = self.url_var.get()
            if not link:
                self.title_label.configure(text="YouTube Video Downloader")
                self.video_title_label.configure(text="")
                self.quality_menu.configure(values=["Loading..."], state="disabled")
                self.audio_only_checkbox.configure(state="disabled")
                self.download_button.configure(state="disabled")
                return

            self.status_label.configure(text="Fetching video information...", text_color="white")
            self.update_idletasks()

            self.yt_object = YouTube(link, on_progress_callback=self.on_progress)

            # Update title
            self.title_label.configure(text=self.yt_object.title)
            self.video_title_label.configure(text=self.yt_object.title, text_color="green")

            # Populate a quality menu with both progressive and non-progressive resolutions
            progressive_resolutions = [stream.resolution for stream in
                                       self.yt_object.streams.filter(progressive=True, file_extension='mp4')]
            non_progressive_resolutions = [stream.resolution for stream in
                                           self.yt_object.streams.filter(only_video=True, file_extension='mp4')]

            # Combine and remove duplicates
            all_resolutions = list(dict.fromkeys(progressive_resolutions + non_progressive_resolutions))

            if all_resolutions:
                self.quality_menu.configure(values=all_resolutions, state="normal")
                self.quality_var.set(all_resolutions[-1])  # Set default to highest

            # Enable widgets
            self.audio_only_checkbox.configure(state="normal")
            self.download_button.configure(state="normal")
            self.status_label.configure(text="", text_color="white")

        except VideoUnavailable:
            self.status_label.configure(text="Video is unavailable or the link is invalid.", text_color="red")
            self.video_title_label.configure(text="Video Not Found", text_color="red")
            self.quality_menu.configure(values=["N/A"], state="disabled")
            self.download_button.configure(state="disabled")
        except Exception as e:
            self.status_label.configure(text=f"An error occurred: {e}", text_color="red")
            self.video_title_label.configure(text="Error", text_color="red")
            self.quality_menu.configure(values=["N/A"], state="disabled")
            self.download_button.configure(state="disabled")

    def browse_path(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_path)

    def start_download_thread(self):
        self.download_thread = threading.Thread(target=self.download_video)
        self.download_thread.start()

    def download_video(self):
        # Reset UI
        self.progress_bar.set(0)
        self.status_label.configure(text="Starting download...")

        # Disable buttons during download
        self.download_button.configure(state="disabled")
        self.link_entry.configure(state="disabled")

        try:
            download_path = self.path_entry.get()

            if not self.yt_object:
                self.status_label.configure(text="Please fetch video info first.", text_color="red")
                return
            if not download_path:
                self.status_label.configure(text="Please select a download path.", text_color="red")
                return

            self.status_label.configure(text=f"Downloading '{self.yt_object.title}'...", text_color="white")

            quality = self.quality_var.get()

            # Check if the selected stream is progressive (contains both audio and video)
            progressive_stream = self.yt_object.streams.filter(progressive=True, resolution=quality).first()

            if self.audio_only_var.get() == "on":
                stream = self.yt_object.streams.get_audio_only()
                if stream:
                    stream.download(output_path=download_path)
                    self.progress_bar.set(1)
                    self.status_label.configure(text="Audio Download Complete!", text_color="green")
                else:
                    self.status_label.configure(text="Audio stream not available.", text_color="red")
            elif progressive_stream:
                progressive_stream.download(output_path=download_path)
                self.progress_bar.set(1)
                self.status_label.configure(text="Download Complete!", text_color="green")
            else:
                # If non-progressive, download video and audio separately and merge
                video_stream = self.yt_object.streams.filter(only_video=True, resolution=quality).first()
                audio_stream = self.yt_object.streams.get_audio_only()

                if video_stream and audio_stream:
                    # Download video and audio files to a temp directory
                    temp_dir = os.path.join(download_path, "temp_downloads")
                    os.makedirs(temp_dir, exist_ok=True)

                    self.status_label.configure(text="Downloading video stream...", text_color="white")
                    video_file = video_stream.download(output_path=temp_dir, filename="video")
                    self.status_label.configure(text="Downloading audio stream...", text_color="white")
                    audio_file = audio_stream.download(output_path=temp_dir, filename="audio")

                    self.status_label.configure(text="Merging video and audio...", text_color="white")

                    # Merge using moviepy
                    final_filename = video_stream.default_filename
                    video_clip = VideoFileClip(video_file)
                    audio_clip = AudioFileClip(audio_file)
                    final_clip = video_clip.set_audio(audio_clip)
                    final_clip.write_videofile(os.path.join(download_path, final_filename))

                    # Clean up temp files
                    video_clip.close()
                    audio_clip.close()
                    os.remove(video_file)
                    os.remove(audio_file)
                    os.rmdir(temp_dir)

                    self.progress_bar.set(1)
                    self.status_label.configure(text="Download and Merge Complete!", text_color="green")
                else:
                    self.status_label.configure(text="Selected quality or audio stream not available.",
                                                text_color="red")

        except Exception as e:
            self.status_label.configure(text=f"An error occurred: {e}", text_color="red")
            print(f"An error occurred: {e}")

        finally:
            # Re-enable buttons after download
            self.download_button.configure(state="normal")
            self.link_entry.configure(state="normal")


# Run App
if __name__ == "__main__":
    app = MyApp()
    app.mainloop()