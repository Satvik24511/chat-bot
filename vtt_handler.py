import speech_recognition as sr
import pyaudio
import wave
import os
import translator

def record_audio(filename, duration=5, sample_rate=44100):
    """Record audio from microphone and save to file"""
    chunk = 1024
    audio_format = pyaudio.paInt16
    channels = 1
    
    p = pyaudio.PyAudio()
    
    print(translator.translate_to_user("Recording... Please speak now."))
    
    stream = p.open(format=audio_format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk)
    
    frames = []
    
    for i in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    
    print(translator.translate_to_user("Recording finished."))
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(audio_format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe_audio(filename):
    """Transcribe audio file to text using Google Speech Recognition"""
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
        
    user_lang = translator.get_user_language()
    
    try:
        # Use the user's preferred language for recognition
        text = recognizer.recognize_google(audio_data, language=user_lang)
        return text
    except sr.UnknownValueError:
        return translator.translate_to_user("Sorry, I could not understand the audio.")
    except sr.RequestError:
        return translator.translate_to_user("Could not request results from speech recognition service.")
