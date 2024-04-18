import os
import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import numpy as np
import soundfile as sf
from PIL import Image, ImageTk




# Set the directory where the images and audio files will be stored
image_directory = "test_images"
audio_directory = "test_audios"

# Make sure the audio directory exists
if not os.path.exists(audio_directory):
    os.makedirs(audio_directory)

# Audio recording settings
sample_rate = 44100
duration = 20  # maximum duration in seconds
amplification_factor = 1.5  # Increase or adjust as needed for volume
recording = None  # To hold the recording array

def start_recording():
    global recording
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='float64', blocking=False)
    print("Recording started...")

def stop_recording(filename):
    global recording
    sd.stop()
    if recording is not None:
        # Amplify the recorded audio
        amplified_recording = recording * amplification_factor
        sf.write(filename, amplified_recording, sample_rate, format='WAV')
        print(f"Saved {filename}")
        recording = None  # Reset recording for next use
    else:
        print("Recording was not started.")

class ImageAnnotator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.index = 0
        self.files = [f for f in os.listdir(image_directory) if f.endswith('.png') or f.endswith('.jpg')]
        self.title('Image Audio Annotator')
        
        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.pack()

        self.photo = None
        self.image_on_canvas = None

        self.button_skip = tk.Button(self, text='Skip', command=self.skip_image)
        self.button_skip.pack(side=tk.BOTTOM)

        self.button_stop_rec = tk.Button(self, text='Stop Recording', command=self.stop_recording_for_image)
        self.button_stop_rec.pack(side=tk.BOTTOM)
    


        self.button_start_rec = tk.Button(self, text='Start Recording', command=self.start_recording_for_image)
        self.button_start_rec.pack(side=tk.BOTTOM)



        
        self.update_image()

    def update_image(self):
        if self.index < len(self.files):
            image_path = os.path.join(image_directory, self.files[self.index])
            img = Image.open(image_path)
            img = img.resize((500, 500), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(img)
            if self.image_on_canvas:
                self.canvas.delete(self.image_on_canvas)
            self.image_on_canvas = self.canvas.create_image(250, 250, image=self.photo)
        else:
            messagebox.showinfo("Completion", "Annotation complete for all images.")
            self.destroy()

    def start_recording_for_image(self):
        start_recording()

    def stop_recording_for_image(self):
        if self.index < len(self.files):
            filename = self.files[self.index]
            audio_path = os.path.join(audio_directory, os.path.splitext(filename)[0] + '.wav')
            stop_recording(audio_path)
            self.index += 1
            self.update_image()

    def skip_image(self):
        if self.index < len(self.files):
            self.index += 1
            self.update_image()
if __name__ == '__main__':
    app = ImageAnnotator()
    app.mainloop()
