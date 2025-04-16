import google.generativeai as genai

class GeminiAPIHandler:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def extract_symptoms(self, user_text):
        # Always translate user input to English for consistent symptom extraction
        english_text = translator.translate_to_english(user_text)
        
        prompt = f"""
        Extract medical symptoms from the following patient description:
        
        "{english_text}"
        
        Return ONLY a comma-separated list of the symptoms mentioned. 
        If no symptoms are detected, return "no".
        """
        
        try:
            response = self.model.generate_content(prompt)
            symptom_text = response.text.strip()
            
            # Split by commas and clean up whitespace
            symptoms = [s.strip() for s in symptom_text.split(',')]
            return symptoms
        except Exception as e:
            print(f"Error in symptom extraction: {e}")
            return ["no"]
    def normalize_symptom(self, symptom):
        prompt = f"Normalize the following medical symptom to a standard term: {symptom}"
        response = self.model.generate_content(prompt)
        return response.text.strip()

    def generate_followup_questions(self, symptom):
        prompt = f"Generate follow-up questions for the symptom: {symptom}"
        response = self.model.generate_content(prompt)
        return response.text.split('\n')

    def generate_pdf_report(self, collected_data):
        prompt = f"Generate a detailed medical report in markdown format based on the following data: {collected_data}"
        response = self.model.generate_content(prompt)
        return response.text
     
    def is_exit_command(self, user_text):
        # Translate to English for consistent command detection
        english_text = translator.translate_to_english(user_text).lower()
        
        exit_commands = [
            "done", "exit", "quit", "finish", "end", "complete", 
            "that's all", "no more symptoms", "nothing else", "stop"
        ]
        
        return any(cmd in english_text for cmd in exit_commands)
    
if __name__ == "__main__":
    genai.configure(api_key = "AIzaSyBkRDmEdtVhVtHHbfvpetHKANTz1EW1qYQ")
    model_list = genai.list_models()
    for model in model_list:    
        print(model.name)
