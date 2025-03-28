import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os
import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")


def record_audio(filename="user_audio.wav", duration=5, samplerate=44100):
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()  # Wait until recording is finished
    wav.write(filename, samplerate, audio_data)

def transcribe_audio_files(files: list):
    # files is a list of file paths
    print("Loading model...")
    # model can be "base", "tiny", "medium", "large", "turbo"
    model = whisper.load_model("base")
    results = []
    print("Transcribing audio files...")
    for file in files:
        result = model.transcribe(file, language="english")
        results.append(result["text"])
    return results


### Example usage
# if __name__ == "__main__":
#     path_to_files = "enter_path"
#     files = os.listdir(path_to_files)
#     files = [os.path.join(path_to_files, file) for file in files]
#     files = sorted(files)
#     results = transcribe_audio_files(files)
#     for i, result in enumerate(results):
#         print(f"File {files[i]}: {result}")
