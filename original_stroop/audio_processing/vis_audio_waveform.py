import os
import pandas as pd
import librosa
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks

def analyze_word_end_time(audio_path, plot=True):
    """Analyze audio file to detect word end time."""
    try:
        y, sr = librosa.load(audio_path, sr=None)
        duration = librosa.get_duration(y=y, sr=sr)
        
        # Compute RMS energy
        frame_length = int(sr * 0.02)
        hop_length = frame_length // 2
        rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
        rms_db = librosa.amplitude_to_db(rms, ref=np.max)
        
        # Smooth the signal
        window_size = min(51, len(rms_db) // 4 * 2 + 1)
        if window_size > 2:
            smoothed_db = savgol_filter(rms_db, window_length=window_size, polyorder=3)
        else:
            smoothed_db = rms_db
        
        # Time axis for plotting
        times = librosa.times_like(rms, sr=sr, hop_length=hop_length)
        
        # Find global maximum (peak)
        global_max_idx = np.argmax(smoothed_db)
        global_max_time = times[global_max_idx]
        
        # Find all local minima (valleys)
        valleys, _ = find_peaks(-smoothed_db)
        
        # Find first valley after global max
        post_max_valleys = valleys[valleys > global_max_idx]
        
        if len(post_max_valleys) > 0:
            first_valley_idx = post_max_valleys[0]
            first_valley_time = times[first_valley_idx]
            end_time = min((global_max_time + first_valley_time) / 2, 1.0)
        else:
            end_time = min(duration, 1.0)
        
        if plot:
            plt.figure(figsize=(12, 6))
            plt.plot(times, rms_db, label="Original dB Level", color='b', alpha=0.3)
            plt.plot(times, smoothed_db, label="Smoothed dB Level", color='b')
            plt.scatter(global_max_time, smoothed_db[global_max_idx], 
                       color='orange', label="Global Max")
            if len(post_max_valleys) > 0:
                plt.scatter(first_valley_time, smoothed_db[first_valley_idx],
                           color='purple', label="First Valley After Max")
            plt.axvline(x=end_time, color='g', linestyle='--', 
                       label=f"End Time (Avg: {end_time:.2f}s)")
            plt.xlabel("Time (s)")
            plt.ylabel("dB Level")
            plt.title(f"Word End Detection\n{os.path.basename(audio_path)}")
            plt.legend()
            plt.grid()
            plt.show()
        
        return end_time
    
    except Exception as e:
        print(f"Audio analysis failed for {audio_path}: {str(e)}")
        return None

def process_single_audio_from_csv(csv_path, line_number):
    """Process a single audio file from CSV with proper path handling."""
    try:
        # Get absolute path of CSV
        csv_path = os.path.abspath(csv_path)
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        df = pd.read_csv(csv_path)
        
        if line_number < 0 or line_number >= len(df):
            raise IndexError(f"Line number must be between 0 and {len(df)-1}")
        
        row = df.iloc[line_number]
        audio_path_in_csv = row['audio_path']
        
        # Get the script's directory and project root
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)  # Goes up one level from audio_processing
        
        # Construct the correct audio path
        # Remove any leading "pilot_study_data" from the CSV path if present
        audio_rel_path = audio_path_in_csv.replace("pilot_study_data/", "", 1)
        final_audio_path = os.path.join(project_root, "pilot_study_data", audio_rel_path)
        
        if not os.path.exists(final_audio_path):
            raise FileNotFoundError(
                f"Audio file not found at:\n"
                f"- Expected path: {final_audio_path}\n"
                f"- CSV path: {audio_path_in_csv}\n"
                f"- Script dir: {script_dir}\n"
                f"- Project root: {project_root}"
            )
        
        print(f"\nProcessing line {line_number}:")
        print(f"CSV location: {csv_path}")
        print(f"Found audio at: {final_audio_path}")
        print(f"Current data: Polarity={row['polarity']}, Word={row['todotask']}, Correct={row['correct']}")
        
        end_time = analyze_word_end_time(final_audio_path)
        
        if end_time is not None:
            print(f"\nDetected word end time: {end_time:.3f} seconds")
            return end_time
        return None
        
    except Exception as e:
        print(f"\nError processing CSV: {str(e)}")
        return None

if __name__ == "__main__":

    csv_path = "../pilot_study_data/2/data.csv"  
    line_number = 5  # 0-based index (ignoring header)
    
    process_single_audio_from_csv(csv_path, line_number)