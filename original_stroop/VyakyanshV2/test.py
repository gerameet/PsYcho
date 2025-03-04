import torch
import torchaudio

"""

# Load the model
model_path = "enm_700.pt"  # Update with the actual path
model = torch.load(model_path, map_location=torch.device("cpu"))
model.eval()

# Load and preprocess the OGG audio
def load_audio(audio_path):
    waveform, sample_rate = torchaudio.load(audio_path, format="ogg")
    return waveform, sample_rate

# Perform inference
def transcribe(audio_path):
    waveform, sample_rate = load_audio(audio_path)
    
    # Convert stereo to mono if necessary
    if waveform.dim() == 2:  
        waveform = waveform.mean(dim=0, keepdim=True)

    with torch.no_grad():
        output = model(waveform)  # Modify if preprocessing is needed

    # Decode the output (Assuming output is indices mapping to text)
    if isinstance(output, torch.Tensor):
        predicted_text = decode_output(output)  # Implement based on your model's output format
        return predicted_text

    return output  # Adjust based on actual model output

# Example usage
# audio_file = "soham_test.ogg"  # Provide the actual OGG file
# result = transcribe(audio_file)
# print("Transcription:", result)

"""