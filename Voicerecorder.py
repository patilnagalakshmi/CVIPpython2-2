import tkinter as tk
import sounddevice as sd
import numpy as np
import wavio

class VoiceRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Recorder")

        self.record_button = tk.Button(root, text="Record", command=self.start_recording)
        self.record_button.pack()

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack()

        self.save_button = tk.Button(root, text="Save", command=self.save_recording, state=tk.DISABLED)
        self.save_button.pack()

        self.recording = False
        self.frames = []

    def start_recording(self):
        self.recording = True
        self.frames = []

        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)

        def callback(indata, frames, time, status):
            if status:
                print(status, file=sys.stderr)
            if self.recording:
                self.frames.append(indata.copy())

        self.stream = sd.InputStream(callback=callback)
        self.stream.start()

    def stop_recording(self):
        self.recording = False
        self.stream.stop()

        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.NORMAL)

    def save_recording(self):
        if self.frames:
            filename = "recording.wav"
            wavio.write(filename, np.concatenate(self.frames, axis=0), 44100, sampwidth=2)
            print(f"Recording saved as {filename}")
            self.frames = []

if __name__ == '__main__':
    root = tk.Tk()
    app = VoiceRecorderApp(root)
    root.mainloop()