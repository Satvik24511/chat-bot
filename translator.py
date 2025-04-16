from deep_translator import GoogleTranslator
# Available language options
def record_user_language():
    user_choice = int(input("Please press 1 for English\nकृपया हिंदी के लिए 2 दबाएँ \nVeuillez appuyer sur 3 pour le français \nPor favor presione 4 para español \n"))
    if(user_choice == 1):
        return "en"
    elif(user_choice == 2):
        return "hi"
    elif(user_choice == 3):
        return "fr"
    elif(user_choice == 4):
        return "es"
    else:
        return "en"

def chatbot_input(user_input, user_lang):
    translated_text = GoogleTranslator(source=user_lang, target='en').translate(user_input).lower()
    return translated_text


def chatbot_response(chatbot_output, user_lang):
    translated_text = GoogleTranslator(source='en', target=user_lang).translate(chatbot_output).lower()
    return translated_text

if __name__ == "__main__":
    user_input = input("Enter your input: ")
    user_lang = input("Enter your language: ")
    chatbot_output = chatbot_input(user_input, user_lang)
    translated_text = chatbot_response(chatbot_output, user_lang)
    print(chatbot_output)
    print(translated_text)
