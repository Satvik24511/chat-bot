import google.generativeai as genai

class GeminiAPIHandler:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def extract_symptoms(self, user_input):
        prompt = f"Extract medical symptoms from the following text and return them as a comma-separated list: and if there are no symptoms respond with 'no' {user_input}"
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
    
    def is_exit_command(self, user_input: str) -> bool:
        """
        Uses Gemini to determine if the user's input is an exit command.
        Returns True if the input is recognized as a command to exit; otherwise, False.
        """
        prompt = (
            f"Determine if the following input from a user is meant to end the conversation. "
            f"Answer with 'yes' if it is an exit command or 'no' otherwise.\n\nUser Input: {user_input}"
        )
        response = self.model.generate_content(prompt)
        answer = response.text.strip().lower()
        # For example, if Gemini returns "yes", then we treat it as an exit command.
        return answer == "yes"


if __name__ == "__main__":
    genai.configure(api_key = "AIzaSyBkRDmEdtVhVtHHbfvpetHKANTz1EW1qYQ")
    model_list = genai.list_models()
    for model in model_list:    
        print(model.name)
