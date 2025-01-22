from sentence_transformers import SentenceTransformer, util
from rapidfuzz import process
import re

class SymptomMatcher:
    def __init__(self, symptom_list):
        self.symptoms = symptom_list

        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.symptom_embeddings = self.embedding_model.encode(self.symptoms, convert_to_tensor=True)

    def normalize_text(self, text):
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def match_symptoms(self, input_text):
        normalized_input = self.normalize_text(input_text)
        matched_symptoms = []

        for symptom in self.symptoms:
            if symptom in normalized_input:
                matched_symptoms.append(symptom)

        if not matched_symptoms:
            input_embedding = self.embedding_model.encode(normalized_input, convert_to_tensor=True)
            similarities = util.cos_sim(input_embedding, self.symptom_embeddings)
            for idx, score in enumerate(similarities[0]):
                if score.item() > 0.5:
                    matched_symptoms.append(self.symptoms[idx])

        return matched_symptoms

class CardiologyChatbot:
    def __init__(self):
        self.symptom_list = [
            "stomach ache",
            "chest pain",
            "shortness of breath",
            "irregular heartbeat",
            "dizziness",
            "fatigue",
            "swelling in legs",
            "palpitations",
            "fainting"
        ]
        self.matcher = SymptomMatcher(self.symptom_list)
        self.pending_symptoms = []
        self.current_symptom = None
        self.current_followup_index = 0
        self.collected_data = {}

    def ask_followup(self, symptom):
        followup_questions = {
            "chest pain": [
                "How often do you experience chest pain? (Rarely, Occasionally, Frequently, All the time)",
                "On a scale of 1-10, how severe is your chest pain?",
                "When did the chest pain start? (e.g., 2 days ago, 1 week ago)",
                "Does the pain radiate to other areas like the arms, back, or jaw?"
            ],
            "shortness of breath": [
                "How often do you experience shortness of breath?",
                "On a scale of 1-10, how severe is your shortness of breath?",
                "When did the shortness of breath start?",
                "Is it triggered by physical activity or occurs even at rest?"
            ],
            "irregular heartbeat": [
                "How often do you feel your heartbeat is irregular?",
                "On a scale of 1-10, how severe is the irregular heartbeat?",
                "When did the irregular heartbeat start?",
                "Do you feel any accompanying symptoms like dizziness or chest discomfort?"
            ]
        }
        return followup_questions.get(symptom, ["Can you tell me more about your symptoms?"])

    def handle_input(self, user_input):
        exit_commands = ["exit", "quit", "stop", "no", "thank you", "that's all", "done"]
        if user_input.lower() in exit_commands:
            if self.collected_data:
                summary = "\nSummary of Collected Data:\n" + "\n".join(
                    [f"- {symptom.capitalize()}: {', '.join(details)}" for symptom, details in self.collected_data.items()]
                )
                return f"Thank you for using the Cardiology Assistant Chatbot. Take care!\n \n------------------------------------------------------------------------ \n{summary}\n \n"
            return "Thank you for using the Cardiology Assistant Chatbot. Take care!"

        if self.current_symptom and self.current_followup_index < len(self.ask_followup(self.current_symptom)):
            question = self.ask_followup(self.current_symptom)[self.current_followup_index]
            self.collected_data[self.current_symptom].append(user_input)
            self.current_followup_index += 1

            if self.current_followup_index < len(self.ask_followup(self.current_symptom)):
                return self.ask_followup(self.current_symptom)[self.current_followup_index]
            else:
                self.current_followup_index = 0
                if self.pending_symptoms:
                    self.current_symptom = self.pending_symptoms.pop(0)
                    self.collected_data[self.current_symptom] = []
                    return f"I detected the symptom: {self.current_symptom}. {self.ask_followup(self.current_symptom)[self.current_followup_index]}"
                else:
                    self.current_symptom = None
                    return "Thank you for providing details about your symptoms. Can you describe any other symptoms you are experiencing?"

        if not self.current_symptom:
            symptoms = self.matcher.match_symptoms(user_input)
            if symptoms:
                self.pending_symptoms.extend(symptoms)
                self.current_symptom = self.pending_symptoms.pop(0)
                self.collected_data[self.current_symptom] = []
                self.current_followup_index = 0
                return f"I detected the symptom: {self.current_symptom}. {self.ask_followup(self.current_symptom)[self.current_followup_index]}"
            else:
                return "I'm sorry, I couldn't identify any symptoms in your input. Can you describe your symptoms in more detail?"

if __name__ == "__main__":
    chatbot = CardiologyChatbot()

    print("Welcome to the Cardiology Assistant Chatbot. Please describe your symptoms.")

    while True:
        user_input = input("You: ")
        response = chatbot.handle_input(user_input)
        print(f"Chatbot: {response}")
        if "Thank you for using the Cardiology Assistant Chatbot" in response:
            break
