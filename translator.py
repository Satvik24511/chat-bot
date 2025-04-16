from deep_translator import GoogleTranslator
import json
import os

class TranslationHandler:
    def __init__(self):
        self.user_language = "en"  # Default language is English

        # Fix: Use an instance of GoogleTranslator to get supported languages
        temp_translator = GoogleTranslator(source='auto', target='en')
        self.supported_languages = list(temp_translator.get_supported_languages(as_dict=True).values())

        self.language_file = "user_language.json"
        self.load_user_language()
    
    def load_user_language(self):
        """Load saved user language preference if it exists"""
        if os.path.exists(self.language_file):
            try:
                with open(self.language_file, "r") as file:
                    data = json.load(file)
                    self.user_language = data.get("language", "en")
            except Exception as e:
                print(f"Error loading language file: {e}")
                self.user_language = "en"
    
    def save_user_language(self):
        """Save user language preference to file"""
        try:
            with open(self.language_file, "w") as file:
                json.dump({"language": self.user_language}, file)
        except Exception as e:
            print(f"Error saving language file: {e}")
    
    def detect_language(self, text):
        """
        Detect the language of the given text.
        For a production system, you might want to use a dedicated language detection library.
        """
        try:
            from langdetect import detect
            return detect(text)
        except:
            return "en"
    
    def translate_to_english(self, text):
        """Translate text from user language to English"""
        if self.user_language == "en" or not text:
            return text
        
        try:
            translator = GoogleTranslator(source=self.user_language, target='en')
            return translator.translate(text)
        except Exception as e:
            print(f"Translation error (to English): {e}")
            return text
    
    def translate_from_english(self, text):
        """Translate text from English to user language"""
        if self.user_language == "en" or not text:
            return text
        
        try:
            translator = GoogleTranslator(source='en', target=self.user_language)
            return translator.translate(text)
        except Exception as e:
            print(f"Translation error (from English): {e}")
            return text
    
    def set_language(self, language_code):
        """Set the user's preferred language"""
        if language_code in self.supported_languages:
            self.user_language = language_code
            self.save_user_language()
            return True
        return False
    
    def get_supported_languages_list(self):
        """Return list of supported languages"""
        return self.supported_languages

# Create a global translator instance
translator = TranslationHandler()

def translate_to_user(text):
    """Translate text from English to user's language"""
    return translator.translate_from_english(text)

def translate_to_english(text):
    """Translate text from user's language to English"""
    return translator.translate_to_english(text)

def set_user_language(language_code):
    """Set the user's preferred language"""
    return translator.set_language(language_code)

def get_user_language():
    """Get the user's current language"""
    return translator.user_language

def record_user_language():
    """Interactive function to let user select their preferred language"""
    languages = {
        "en": "English",
        "es": "Español (Spanish)",
        "hi": "हिन्दी (Hindi)",
        "fr": "Français (French)",
        "de": "Deutsch (German)",
        "zh-CN": "中文 (Chinese)",
        "ar": "العربية (Arabic)",
        "ru": "Русский (Russian)",
        "pt": "Português (Portuguese)",
        "ja": "日本語 (Japanese)",
        "mr": "मराठी (Marathi)"
    }
    
    print("Please select your preferred language / कृपया अपनी पसंदीदा भाषा चुनें / Por favor seleccione su idioma preferido:")
    for code, name in languages.items():
        print(f"{code}: {name}")
    
    choice = input("Enter language code: ").strip().lower()
    
    if choice in languages:
        set_user_language(choice)
        print(translate_to_user(f"Language set to {languages[choice]}"))
    else:
        print("Invalid choice. Using English as default.")
        set_user_language("en")

if __name__ == "__main__":
    print(translator.get_supported_languages_list())
