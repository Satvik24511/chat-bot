import asyncio
import edge_tts
import playsound
import tempfile
import os
import platform

LANGUAGE_TO_VOICE_MAP = {
    "en": "en-US-AriaNeural",      # English (US)
    "es": "es-MX-DaliaNeural",      # Spanish (Mexico) - Choose appropriate region
    "hi": "hi-IN-SwaraNeural",      # Hindi (India)
    "fr": "fr-FR-DeniseNeural",     # French (France)
    "de": "de-DE-KatjaNeural",      # German (Germany)
    "zh-CN": "zh-CN-XiaoxiaoNeural",# Chinese (Mandarin, Simplified)
    "ar": "ar-SA-HamedNeural",      # Arabic (Saudi Arabia) - Choose appropriate region
    "ru": "ru-RU-SvetlanaNeural",   # Russian (Russia)
    "pt": "pt-BR-FranciscaNeural",  # Portuguese (Brazil) - Choose appropriate region
    "ja": "ja-JP-NanamiNeural",     # Japanese (Japan)
    "mr": "mr-IN-AarohiNeural"      # Marathi (India)
}

DEFAULT_VOICE = LANGUAGE_TO_VOICE_MAP["en"] # Default to English

DEFAULT_RATE = "+0%"
DEFAULT_VOLUME = "+0%"


async def _generate_and_play(text: str, voice: str, rate: str, volume: str):
    """Internal async function to generate speech and play it."""
    tts_comm = None
    tmp_filename = None # Define outside try block for cleanup
    try:
        tts_comm = edge_tts.Communicate(text, voice, rate=rate, volume=volume)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tmp_filename = tmp_file.name

        await tts_comm.save(tmp_filename)

        playsound.playsound(tmp_filename) # playsound handles path normalization usually

    except edge_tts.exceptions.NoAudioReceived:
        print(f"(Speech Handler Warning): No audio received from TTS service for: '{text[:50]}...' (Voice: {voice})")
    except Exception as e:
        print(f"(Speech Handler Error): Could not speak text. Voice: {voice}. Error: {e}")
        print(f"(Fallback Text): {text}") # Fallback: Print the text if speaking fails
    finally:
        if tmp_filename and os.path.exists(tmp_filename):
            try:
                os.remove(tmp_filename)
            except PermissionError:
                if platform.system() == "Windows":
                    print(f"(Speech Handler Warning): Could not immediately delete temp file {tmp_filename}. It might be cleaned up later or require manual cleanup.")
                else:
                    print(f"(Speech Handler Error): PermissionError deleting temp file {tmp_filename}.")
            except Exception as e:
                 print(f"(Speech Handler Error): Error deleting temp file {tmp_filename}: {e}")


def speak(text: str, language_code: str = "en", rate: str = DEFAULT_RATE, volume: str = DEFAULT_VOLUME):
    """
    Generates speech from text using edge-tts with language-appropriate voice and plays it.
    Runs the asynchronous generation/playback function synchronously.
    """
    if not text or text.isspace():
        return # Don't try to speak empty strings

    voice_id = LANGUAGE_TO_VOICE_MAP.get(language_code, DEFAULT_VOICE)

    try:
        try:
            loop = asyncio.get_event_loop_policy().get_event_loop()
        except RuntimeError: # No running loop
             loop = asyncio.new_event_loop()
             asyncio.set_event_loop(loop)

        if loop.is_running():
             print("(Speech Handler Info): Event loop already running. Using run_coroutine_threadsafe.")
             future = asyncio.run_coroutine_threadsafe(_generate_and_play(text, voice_id, rate, volume), loop)
             future.result() # Wait for completion - This blocks the thread where speak() is called.

        else:
            loop.run_until_complete(_generate_and_play(text, voice_id, rate, volume))

    except RuntimeError as e:
        if "cannot run loop while another loop is running" in str(e) or "no running event loop" in str(e):
            print(f"(Speech Handler Warning): Asyncio loop issue prevented speech: {e}. Ensure proper async context if needed.")
            print(f"(Fallback Text): {text}")
        else:
            print(f"(Speech Handler Error): Runtime error during speech execution: {e}")
            print(f"(Fallback Text): {text}")
    except Exception as e:
        print(f"(Speech Handler Error): Unexpected error in speak function: {e}")
        print(f"(Fallback Text): {text}")

if __name__ == "__main__":
    print("Testing speech handler...")
    speak("Hello! This is a test in English.", language_code="en")
    speak("¡Hola! Esta es una prueba en español.", language_code="es")
    speak("नमस्ते! यह हिन्दी में एक परीक्षण है।", language_code="hi")
    print("Speech test complete.")
