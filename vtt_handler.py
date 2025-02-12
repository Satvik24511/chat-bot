import whisper
import sounddevice as sd
import numpy as np
import wave

def record_audio(filename: str, duration: int = 5, samplerate: int = 44100):
    print("Recording...")
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=2, dtype=np.int16)
    sd.wait()
    
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())
    print("Recording saved as", filename)

def transcribe_audio(audio_path: str, model_size: str = "base") -> str:

    model = whisper.load_model(model_size)
    audio = whisper.load_audio(audio_path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)

    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)


    return result.text

if __name__ == "__main__":
    filename = "user_audio.wav"
    record_audio(filename)
    text = transcribe_audio(filename)
    print("Transcription:", text)
