import sys
import webbrowser

import customtkinter
from yt_dlp import YoutubeDL
import tkinter.filedialog as filedialog
import os
import threading

download_folder = os.getcwd()

FORMATS = {
    "360p": 'bestvideo[height<=360]+bestaudio/best[height<=360]',
    "720p": 'bestvideo[height<=720]+bestaudio/best[height<=720]',
    "1080p": 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
}

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def run_main_app():
    global download_type, quality_var, quality_dropdown, folder_label, status_label, downloadBtn, progress_bar, url


    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    app = customtkinter.CTk()
    icon_path = resource_path("icon.ico")
    app.iconbitmap(icon_path)
    app.title("YouTube Downloader")
    app.geometry("800x500")

    download_type = customtkinter.StringVar(value="Video")

    title_label = customtkinter.CTkLabel(app, text="YouTube Video/Audio Downloader", font=("Macan", 20, "bold"))
    title_label.pack(padx=10, pady=10)

    url = customtkinter.StringVar()
    url_entry = customtkinter.CTkEntry(app, placeholder_text="Paste YouTube link here", height=30, width=500 ,textvariable=url)
    url_entry.pack(pady=20)

    folder_frame = customtkinter.CTkFrame(app, corner_radius=10, fg_color="#303030")
    folder_frame.pack(padx=10, pady=10, anchor="center", fill=None)

    folder_label = customtkinter.CTkLabel(folder_frame, text=f"📁 {download_folder}", font=("Macan", 12, "bold"))
    folder_label.pack(side="left" ,padx=8, pady=4)

    folder_btn = customtkinter.CTkButton(folder_frame, text="Choose Folder", command=choose_folder, font=("Macan", 12, "bold"))
    folder_btn.pack(side="left" ,padx=4, pady=4)

    current_folder_btn = customtkinter.CTkButton(folder_frame, text="Open download Directory", command=open_directory, font=("Macan", 12, "bold"))
    current_folder_btn.pack(side="left" ,padx=4, pady=4)

    radio_frame = customtkinter.CTkFrame(app, corner_radius=10, fg_color="transparent")
    radio_frame.pack(padx=10, pady=10, anchor="center", fill=None)

    video_radio = customtkinter.CTkRadioButton(radio_frame, text="Video", variable=download_type, value="Video", command=update_quality_options)
    video_radio.pack(side="left" ,padx=4, pady=4)

    audio_radio = customtkinter.CTkRadioButton(radio_frame, text="Audio", variable=download_type, value="Audio", command=update_quality_options)
    audio_radio.pack(side="left" ,padx=4, pady=4)

    action_frame = customtkinter.CTkFrame(app, fg_color="transparent")
    action_frame.pack(padx=10, pady=(10,0))

    quality_var = customtkinter.StringVar(value="360p")
    quality_dropdown = customtkinter.CTkOptionMenu(action_frame, variable=quality_var, values=list(FORMATS.keys()), font=("Macan", 12, "bold"))
    quality_dropdown.pack(side="left" ,padx=5)

    downloadBtn = customtkinter.CTkButton(action_frame, text="Download", command=lambda: threading.Thread(target=download_video).start(), font=("Macan", 12, "bold"))
    downloadBtn.pack(side="left" ,padx=5)

    progress_bar = customtkinter.CTkProgressBar(app, width=400)
    progress_bar.set(0)
    progress_bar.pack(pady=10)

    status_label = customtkinter.CTkLabel(app, text="", font=("Macan", 14, "bold"))
    status_label.pack(pady=10)

    developer_frame = customtkinter.CTkFrame(app, fg_color="transparent")
    developer_frame.pack(padx=10, pady=10, anchor="center", fill=None, side="bottom")

    github_frame = customtkinter.CTkFrame(developer_frame, corner_radius=10, fg_color="#ffffff", cursor="hand2")
    github_frame.pack(side="left", pady=10, padx=10, anchor="center")
    github_label = customtkinter.CTkLabel(
        github_frame,
        text="Github",
        text_color="black",
        font=("Macan", 10, "bold"),
        cursor="hand2"
    )
    github_label.pack(padx=8, pady=2)
    github_frame.bind("<Button-1>", open_github)
    github_label.bind("<Button-1>", open_github)

    developer_name = customtkinter.CTkLabel(developer_frame, text="Developed by itsNaleeka", font=("Macan", 10, "bold"))
    developer_name.pack(side="left",padx=(2,10), pady=2)

    update_quality_options()


    app.mainloop()

def open_github(event=None):
    webbrowser.open_new("https://github.com/itsNaleeka")

def update_quality_options():
    if download_type.get() == "Video":
        quality_dropdown.configure(values=["360p", "720p", "1080p"])
        quality_dropdown.set("360p")
    else:
        quality_dropdown.configure(values=["128kbps", "192kbps", "256kbps", "312kbps"])
        quality_dropdown.set("128kbps")

def choose_folder():
    global download_folder
    folder = filedialog.askdirectory()
    if folder:
        download_folder = folder
        folder_label.configure(text=f"📂 {download_folder}")

def open_directory():
    try:
        os.startfile(download_folder)
    except Exception as e:
        status_label.configure(text=f"Can't open folder: {str(e)}", text_color="red")

def download_video():
    link = url.get().strip()
    quality = quality_var.get()
    downloadBtn.configure(state="disabled")

    if not link.startswith("http"):
        status_label.configure(text="❌ Invalid YouTube URL", text_color="red")
        return

    ydl_opts = {
        'format': FORMATS.get(quality, "best"),
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'quiet': True,
        'verbose': True,
    }

    if download_type.get() == "Audio":
        bitrate = quality_var.get().replace("kbps", "")
        ydl_opts.update({
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': bitrate,
                },
                {'key': 'EmbedThumbnail'},
                {'key': 'FFmpegMetadata'},
            ],
            'format': 'bestaudio',
            'writethumbnail': True,
            'embedthumbnail': True,
            'addmetadata': True,
            'prefer_ffmpeg': True,
            'merge_output_format': None,
            'postprocessor_args': ['-id3v2_version', '3'],
        })
    else:
        ydl_opts['merge_output_format'] = 'mp4'

    try:
        status_label.configure(text="⬇️ Downloading...", text_color="orange")
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        status_label.configure(text="✅ Download Completed", text_color="green")
    except Exception as e:
        status_label.configure(text="❌ Error: " + str(e), text_color="red")
    finally:
        downloadBtn.configure(state="normal")

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0.00%').strip().replace('%', '')
        try:
            progress_bar.set(float(percent)/100)
        except:
            pass

        total_bytes = d.get('total_bytes') or d.get("total_bytes_estimate")
        downloaded_bytes = d.get("downloaded_bytes", 0)
        speed = d.get('speed', 0)
        eta = d.get('eta', 0)

        if total_bytes:
            size_mb = total_bytes / 1024 / 1024
            speed_mb = speed / 1024 if speed else 0
            downloaded_mb = downloaded_bytes / 1024 / 1024

            status_label.configure(
                text=f"⬇️ Downloading: {downloaded_mb: .2f}/{size_mb:.2f} MB at {speed_mb:.1f} kB/s | ETA: {eta:.2f}s",
                text_color="orange"
            )

    elif d['status'] == 'finished':
        progress_bar.set(1.0)
        status_label.configure(text="✅ Download Completed", text_color="green")
        downloadBtn.configure(state="normal")


def show_splash():
    splash = customtkinter.CTk()
    splash.geometry("400x200")
    splash.overrideredirect(True)

    splash.update_idletasks()
    w = 400
    h = 200
    x = (splash.winfo_screenwidth() // 2) - (w // 2)
    y = (splash.winfo_screenheight() // 2) - (h // 2)
    splash.geometry(f"{w}x{h}+{x}+{y}")

    label = customtkinter.CTkLabel(splash, text="🚀 Launching YouTube Downloader...", font=("Macan", 18, "bold"))
    label.pack(expand=True)

    splash.after(2500, lambda: [splash.destroy(), run_main_app()])
    splash.mainloop()

show_splash()
