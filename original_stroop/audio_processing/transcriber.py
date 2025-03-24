import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

def record_audio(filename="user_audio.wav", duration=5, samplerate=44100):
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()  # Wait until recording is finished
    wav.write(filename, samplerate, audio_data)

def transcribe_audio_files(files: list):
    # files is a list of file paths
    model = whisper.load_model("base")
    results = []
    for file in files:
        result = model.transcribe(file)
        results.append(result["text"])
    return results

# if __name__ == "__main__":
#     record_audio(duration=5)
#     transcription = transcribe_audio()
#     print("\nTranscribed Text:", transcription)
