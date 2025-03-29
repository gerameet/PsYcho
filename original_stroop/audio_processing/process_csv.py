import pandas as pd
import os
import whisper
import librosa
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import warnings
from scipy.signal import savgol_filter
from scipy.signal import find_peaks
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
import json

with open("../config.json", "r") as f:
    config = json.load(f)

def transcribe_audio_files(files: list):
    # files is a list of file paths
    model = whisper.load_model("tiny")
    results = []
    for file in tqdm(files):
        result = model.transcribe(file, language="english")
        results.append(result["text"])
    return results

def get_word_time(audio_path, plot=True):
    """
    Plot the dB level over time for an audio file and mark the detected word end time.
    Uses smoothed signal and finds the average of global max and first minima after it.
    End time is clipped to max 1 second.
    
    Args:
        audio_path (str): Path to the audio file (.m4a).
        plot (bool): Whether to plot the dB level (default: True).
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
    
    # Smooth the signal
    window_size = min(51, len(rms_db) // 4 * 2 + 1)  # Ensure window size is odd and smaller than signal length
    if window_size > 2:
        smoothed_db = savgol_filter(rms_db, window_length=window_size, polyorder=3)
    else:
        smoothed_db = rms_db
    
    # Time axis for plotting (convert frames to seconds)
    times = librosa.times_like(rms, sr=sr, hop_length=hop_length)
    
    # Find global maximum (peak)
    global_max_idx = np.argmax(smoothed_db)
    global_max_time = times[global_max_idx]
    
    # Find all local minima (valleys)
    valleys, _ = find_peaks(-smoothed_db)
    
    # Find first valley after global max
    post_max_valleys = valleys[valleys > global_max_idx]

    stimulus_duration = config["stimulus_duration"]
    
    if len(post_max_valleys) > 0:
        first_valley_idx = post_max_valleys[0]
        first_valley_time = times[first_valley_idx]
        
        # End time is average of global max and first valley times, clipped to max 1s
        end_time = min((global_max_time + first_valley_time) / 2, stimulus_duration)
    else:
        # Fallback: clip to max 1s if no valley found
        end_time = min(duration, stimulus_duration)
    
    # Plotting
    if plot:
        plt.figure(figsize=(12, 6))
        plt.plot(times, rms_db, label="Original dB Level", color='b', alpha=0.3)
        plt.plot(times, smoothed_db, label="Smoothed dB Level", color='b')
        
        # Mark global max and first valley
        plt.scatter(global_max_time, smoothed_db[global_max_idx], 
                   color='orange', label="Global Max")
        if len(post_max_valleys) > 0:
            plt.scatter(first_valley_time, smoothed_db[first_valley_idx],
                       color='purple', label="First Valley After Max")
        
        # Mark end time
        plt.axvline(x=end_time, color='g', linestyle='--', 
                   label=f"End Time (Avg: {end_time:.2f}s)")
        
        plt.xlabel("Time (s)")
        plt.ylabel("dB Level")
        plt.title("Smoothed dB Level with Word End Detection")
        plt.legend()
        plt.grid()
        plt.show()
    
    return end_time

def process_csv(input_csv_path, output_csv_path=None):
    # Read the CSV file
    df = pd.read_csv(input_csv_path)
    
    # If output path not provided, overwrite the input file
    if output_csv_path is None:
        output_csv_path = input_csv_path
    
    # Initialize new columns if they don't exist
    if 'response' not in df.columns:
        df['response'] = None
    if 'time_taken' not in df.columns:
        df['time_taken'] = None 
    
    # Transcribe audio files
    audio_files = df['audio_path'].tolist()
    audio_files = ["../" + file for file in audio_files]
    transcription = transcribe_audio_files(audio_files)

    # Process each audio file
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing audio files"):
        audio_file = row['audio_path']
        audio_file = "../" + audio_file
        
        try:
            # Get word time
            word_time = get_word_time(audio_file, plot=False)
            
            # Update the dataframe
            df.at[idx, 'response'] = transcription[idx]
            df.at[idx, 'time_taken'] = word_time
            
        except Exception as e:
            print(f"Error processing {audio_file}: {str(e)}")
            df.at[idx, 'response'] = f"Error: {str(e)}"
            df.at[idx, 'time_taken'] = None
    
    # Save the updated dataframe
    df.to_csv(output_csv_path, index=False)
    print(f"Processing complete. Results saved to {output_csv_path}")

# Example usage
def process_audios():
    data_dir = "../pilot_study_data"
    for folder in os.listdir(data_dir):
        folder_path = os.path.join(data_dir, folder)
        print(f"Processing folder: {folder_path}")
        if os.path.isdir(folder_path):
            csv_file = os.path.join(folder_path, "data.csv")
            if os.path.exists(csv_file):
                process_csv(csv_file)

if __name__ == "__main__":
    process_audios()

