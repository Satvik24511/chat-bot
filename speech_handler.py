# speech_handler.py

import asyncio
import edge_tts
import playsound
import tempfile
import os
import platform

# --- Language to Voice Mapping ---
# Add more mappings as needed. Find voices with: edge-tts --list-voices
# Use language codes consistent with translator.py (e.g., 'en', 'es', 'hi')
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
    # Add other languages your users might select
}

DEFAULT_VOICE = LANGUAGE_TO_VOICE_MAP["en"] # Default to English

# --- Configuration --- (Rate and Volume remain the same)
DEFAULT_RATE = "+0%"
DEFAULT_VOLUME = "+0%"

# --- Core Functionality ---

async def _generate_and_play(text: str, voice: str, rate: str, volume: str):
    """Internal async function to generate speech and play it."""
    tts_comm = None
    tmp_filename = None # Define outside try block for cleanup
    try:
        tts_comm = edge_tts.Communicate(text, voice, rate=rate, volume=volume)

        # Use a temporary file to store the audio
        # Making delete=False is crucial as playsound needs the file path after the 'with' block closes it
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tmp_filename = tmp_file.name

        # Stream the audio to the temporary file
        await tts_comm.save(tmp_filename)

        # Play the temporary audio file
        playsound.playsound(tmp_filename) # playsound handles path normalization usually

    except edge_tts.exceptions.NoAudioReceived:
        print(f"(Speech Handler Warning): No audio received from TTS service for: '{text[:50]}...' (Voice: {voice})")
    except Exception as e:
        print(f"(Speech Handler Error): Could not speak text. Voice: {voice}. Error: {e}")
        print(f"(Fallback Text): {text}") # Fallback: Print the text if speaking fails
    finally:
        # Clean up the temporary file if it exists
        if tmp_filename and os.path.exists(tmp_filename):
            try:
                os.remove(tmp_filename)
            except PermissionError:
                # On Windows, playsound might still hold the file briefly
                if platform.system() == "Windows":
                    print(f"(Speech Handler Warning): Could not immediately delete temp file {tmp_filename}. It might be cleaned up later or require manual cleanup.")
                else:
                    print(f"(Speech Handler Error): PermissionError deleting temp file {tmp_filename}.")
            except Exception as e:
                 print(f"(Speech Handler Error): Error deleting temp file {tmp_filename}: {e}")


# Modified speak function to accept language code
def speak(text: str, language_code: str = "en", rate: str = DEFAULT_RATE, volume: str = DEFAULT_VOLUME):
    """
    Generates speech from text using edge-tts with language-appropriate voice and plays it.
    Runs the asynchronous generation/playback function synchronously.
    """
    if not text or text.isspace():
        return # Don't try to speak empty strings

    # Select voice based on language code, fall back to default English
    voice_id = LANGUAGE_TO_VOICE_MAP.get(language_code, DEFAULT_VOICE)
    # print(f"[Debug] Speaking in language: {language_code}, using voice: {voice_id}") # Optional debug

    try:
        # Handle asyncio loop management
        try:
            loop = asyncio.get_event_loop_policy().get_event_loop()
            # loop = asyncio.get_running_loop() # Use get_running_loop if available and appropriate
        except RuntimeError: # No running loop
             loop = asyncio.new_event_loop()
             asyncio.set_event_loop(loop)

        if loop.is_running():
            # If called from within an already running async function/framework
            # Creating a future and running in thread might be safer than run_coroutine_threadsafe sometimes
            # For simple scripts, this might be overly complex. Let's stick to run_coroutine_threadsafe
            # but be aware of potential issues in complex async environments.
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

# --- Optional utility functions remain unchanged ---
# ... set_default_rate, set_default_volume etc. (though default voice is now less relevant)

# Example usage (if run directly)
if __name__ == "__main__":
    print("Testing speech handler...")
    speak("Hello! This is a test in English.", language_code="en")
    speak("¡Hola! Esta es una prueba en español.", language_code="es")
    speak("नमस्ते! यह हिन्दी में एक परीक्षण है।", language_code="hi")
    # speak("你好！这是一个中文测试。", language_code="zh-CN") # Uncomment to test Chinese
    print("Speech test complete.")
