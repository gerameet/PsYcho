import pandas as pd
import whisper
import librosa
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

# Your functions
def transcribe_audio_files(files: list):
    # files is a list of file paths
    model = whisper.load_model("base")
    results = []
    for file in tqdm(files):
        result = model.transcribe(file, language="english")
        results.append(result["text"])
    return results

def get_word_time(audio_path, silence_threshold=-25, min_silence_duration=0.2, plot=False):
    """
    Plot the dB level over time for an audio file and mark the detected word end time.
    
    Args:
        audio_path (str): Path to the audio file (.m4a).
        silence_threshold (float): Silence threshold in dB (default: -25).
        min_silence_duration (float): Minimum silence duration to consider (default: 0.1s).
        plot (bool): Whether to plot the dB level (default: True).
    """
    # Load audio
    y, sr = librosa.load(audio_path, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)
    # print("Duration of the audio: ", duration)
    
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
    if plot:
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
    
    return end_time

# Main processing
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
    i = 0
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
        i += 1
    
    # Save the updated dataframe
    df.to_csv(output_csv_path, index=False)
    print(f"Processing complete. Results saved to {output_csv_path}")

# Example usage
if __name__ == "__main__":
    input_csv = "data.csv"
    process_csv(input_csv)