import whisper
import sounddevice as sd
import numpy as np
import wave

def record_audio(filename: str, duration: int = 5, samplerate: int = 44100):
    """
    Records audio from the user's microphone and saves it to a file.

    :param filename: Name of the output WAV file.
    :param duration: Duration of recording in seconds (default: 5 seconds).
    :param samplerate: Sample rate of the recording (default: 44100 Hz).
    """
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
    """
    Transcribes an audio file to text using OpenAI's Whisper model.

    :param audio_path: Path to the audio file.
    :param model_size: Size of the Whisper model to use (e.g., "tiny", "base", "small", "medium", "large").
    :return: Transcribed text.
    """
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    return result["text"]

if __name__ == "__main__":
    filename = "user_audio.wav"
    record_audio(filename)
    text = transcribe_audio(filename)
    print("Transcription:", text)
