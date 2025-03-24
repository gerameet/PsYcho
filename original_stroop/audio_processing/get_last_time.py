import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

def plot_db_level(audio_path, silence_threshold=-25, min_silence_duration=0.1):
    """
    Plot the dB level over time for an audio file and mark the detected word end time.
    
    Args:
        audio_path (str): Path to the audio file (.m4a).
        silence_threshold (float): Silence threshold in dB (default: -25).
        min_silence_duration (float): Minimum silence duration to consider (default: 0.1s).
    """
    # Load audio
    y, sr = librosa.load(audio_path, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)
    
    # Compute RMS energy
    frame_length = int(sr * 0.02)  # 20ms frame
    hop_length = frame_length // 2
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    
    # Convert RMS to dB
    rms_db = librosa.amplitude_to_db(rms, ref=np.max)
    
    # Time axis for plotting (convert frames to seconds)
    times = librosa.times_like(rms, sr=sr, hop_length=hop_length)
    
    # Find word end time (same logic as before)
    silent_frames = np.where(rms_db < silence_threshold)[0]
    end_time = duration  # Default: word continues till end
    
    if len(silent_frames) > 0:
        min_silence_frames = int(min_silence_duration * sr / hop_length)
        silent_regions = np.split(silent_frames, np.where(np.diff(silent_frames) != 1)[0] + 1)
        
        for region in silent_regions:
            if len(region) >= min_silence_frames:
                end_frame = region[0]
                end_time = end_frame * hop_length / sr
                break
    
    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(times, rms_db, label="dB Level", color='b')
    plt.axhline(y=silence_threshold, color='r', linestyle='--', label="Silence Threshold")
    plt.axvline(x=end_time, color='g', linestyle='--', label="Detected Word End")
    plt.xlabel("Time (s)")
    plt.ylabel("dB Level")
    plt.title("dB Level Over Time")
    plt.legend()
    plt.grid()
    plt.show()

audio_path = "blue.m4a"
plot_db_level(audio_path)