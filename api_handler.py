import google.generativeai as genai

class GeminiAPIHandler:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def extract_symptoms(self, user_input):
        prompt = f"Extract medical symptoms from the following text and return them as a comma-separated list: {user_input}"
        response = self.model.generate_content(prompt)
        return response.text.split(',')

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