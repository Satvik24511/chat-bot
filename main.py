from sentence_transformers import SentenceTransformer, util
from rapidfuzz import process
import re

class SymptomMatcher:
    '''This is a class which has 1 function match_symptom, it uses the initialised symptoms when defining the class, and matches them (it can also match synonyms)'''
    def __init__(self, symptom_list):
        self.symptoms = symptom_list
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.symptom_embeddings = self.embedding_model.encode(self.symptoms, convert_to_tensor=True)

    def normalize_text(self, text):

        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return_text = ""

        for char in text.split():
            temp = self.embedding_model.encode(char,convert_to_tensor=True)
            similarities = util.cos_sim(temp,self.symptom_embeddings)
            for idx, score in enumerate(similarities[0]):
                # print(char,self.symptoms[idx],score.item())
                if score.item() > 0.5:
                    return_text+=char + " "
                    break
        # print(return_text)
        # print("The return text is above")
        return return_text

    # uses cos function with vector mapping to compare words and scentences 
    def match_symptoms(self, input_text):
        normalized_input = self.normalize_text(input_text)
        matched_symptoms = []

        for symptom in self.symptoms:
            if symptom in normalized_input:
                matched_symptoms.append(symptom)

        if not matched_symptoms:
            input_embedding = self.embedding_model.encode(normalized_input, convert_to_tensor=True)
            similarities = util.cos_sim(input_embedding, self.symptom_embeddings)
            temp = []
            # print(similarities[0])
            flg = False
            for idx, score in enumerate(similarities[0]):
                temp.append((score.item(),self.symptoms[idx]))
                if score.item() > 0.70: 
                    flg = True
            temp.sort()
            # for i in temp:
            #     print(i[0],i[1])
            a = ""
            b = ""
            if(flg):
                matched_symptoms = [temp[-1][1]]
                # print(temp[-2][1],temp[-3][1])
                a = temp[-2][1]
                b = temp[-3][1]
            # for a,b in temp:
            #     print(a,b)
        return matched_symptoms,a,b

class CardiologyChatbot:
    
    def __init__(self):
        self.symptom_list = [
    "Shortness of breath", "Dizziness", "Nausea", "Headache", "Chest pain",
    "Fatigue", "Swelling in the legs or feet", "Stomach cramps", "Back pain",
    "Sore throat", "Rash", "Itchy skin", "Blurry vision", "Ringing in the ears",
    "Sweating", "Chills", "Fainting", "Difficulty swallowing", "Weight loss",
    "Weight gain", "Heart palpitations", "Dry mouth", "Frequent urination",
    "Painful urination", "Blood in urine", "Constipation", "Diarrhea", "Cough",
    "Coughing up blood", "Joint pain", "Numbness", "Tingling sensation",
    "Muscle weakness", "Loss of appetite", "Trouble sleeping",
    "Sleepiness during the day", "Hot flashes", "Feeling cold", "Bruising",
    "Difficulty concentrating", "Memory problems", "Tremors",
    "Cold hands or feet", "Sudden pain in one part of the body",
    "Sensitivity to light", "Sensitivity to sound", "Hoarseness", "Thirst",
    "Dry skin", "Vomiting", "Abdominal pain", "Heartburn", "Gas or bloating",
    "Painful menstruation", "Irregular menstrual cycle", "Weakness",
    "Increased hunger", "Shaking", "Difficulty breathing (general)",
    "Dizziness when standing", "Blackouts", "Feeling faint", "Dry eyes",
    "Difficulty moving limbs", "Skin color changes", "Lump or swelling",
    "Pain when touched", "Anxiety", "Hearing loss", "Bad breath",
    "Excessive saliva", "Changes in bowel habits", "Chest pressure",
    "Gurgling from the stomach", "Throbbing head", "Mental fog",
    "Night sweating", "Coughing up mucus", "Blood in stool", "Leg cramps",
    "Brittle nails", "Swelling around the eyes", "Wound discharge",
    "Uncontrolled movements", "Loss of taste", "Fullness after eating",
    "Red or inflamed skin", "Mouth ulcers", "Heavy periods",
    "Discomfort after eating", "Sensitivity to cold or heat", "Muscle cramps",
    "Choking feeling", "Skin sensitivity to pressure", "Sore eyes",
    "Sudden urge to urinate", "Fever", "Persistent hiccups",
    "Difficulty speaking", "Loss of balance", "Feeling unsteady", "Confusion",
    "Mood swings", "Restlessness", "Irritability", "Changes in vision (general)",
    "Double vision", "Eye pain", "Nosebleeds", "Excessive tearing",
    "Ear pain", "Ear discharge", "Nasal congestion", "Sneezing",
    "Swollen lymph nodes", "Chest tightness", "Rapid heartbeat",
    "Slow heartbeat", "Irregular heartbeat", "Paleness",
    "Yellowing of skin or eyes", "Excessive thirst",
    "Excessive urination (general)", "Joint stiffness", "Muscle stiffness",
    "Muscle spasms", "Paralysis", "Seizures", "Delusions", "Hallucinations",
    "Suicidal thoughts", "Itchy scalp", "Hair loss", "Bleeding gums",
    "Tooth pain", "Difficulty chewing", "Soreness in mouth or tongue",
    "Metallic taste", "Chest burning", "Chest heaviness", "Frequent belching",
    "Passing gas", "Anal itching", "Rectal pain", "Pain during bowel movements",
    "Changes in stool color", "Fecal incontinence", "Difficulty controlling urination",
    "Abnormal vaginal bleeding", "Vaginal discharge", "Pain during intercourse",
    "Erectile dysfunction", "Skin lumps", "Skin lesions", "Excessive dryness (skin)",
    "Oily skin", "Acne", "Skin peeling", "Skin thickening", "Skin scarring",
    "Night blindness", "Sensitivity to glare", "Chronic tearing (eyes)",
    "Eye redness", "Eye discharge", "Vision loss", "Water retention",
    "Decreased urine output", "Swollen hands", "Muscle aches", "Joint swelling",
    "Neck stiffness", "Neck pain", "Throat swelling", "Sore mouth corners",
    "Difficulty opening mouth", "Jaw pain", "Jaw locking", "Tooth sensitivity",
    "Hot flushes", "Excessive hair growth (body or face)", "Body odor (unusual or excessive)",
    "Nipple discharge", "Lump in breast", "Unusual body odor", "Skin cracking",
    "Excessive dandruff", "Brittle hair", "Sensitivity in scalp",
    "Feeling of pressure in the head", "Rapid weight changes",
    "Loose skin (after weight change)", "Stretch marks",
    "Bulging veins in legs or feet", "Pain behind the eyes", "Eye swelling",
    "Burning sensation on skin", "Crawling sensation on skin",
    "Restlessness in legs (general)"
]

        self.matcher = SymptomMatcher(self.symptom_list)
        self.pending_symptoms = []
        self.current_symptom = None
        self.current_followup_index = 0
        self.collected_data = {}
        self.a = ""
        self.b = ""
        self.detected_symptoms = []


    def ask_followup(self, symptom):
        followup_questions = [
            f"How often do you experience {symptom}? (Rarely, Occasionally, Frequently, All the time)",
            f"On a scale of 1-10, how severe is your {symptom}?",
            f"When did the {symptom} start? (e.g., 2 days ago, 1 week ago)"   
        ]
        return followup_questions

    def validate_followup_response(self, question_type, user_input):
        if question_type == "frequency":
            valid_responses = ["rarely", "occasionally", "frequently", "all the time"]
            if user_input.lower() in valid_responses:
                return True, user_input.capitalize()
            else:
                return False, "Please provide one of the following responses: Rarely, Occasionally, Frequently, All the time."
        elif question_type == "severity":
            try:
                severity = int(user_input)
                if 1 <= severity <= 10:
                    return True, severity
                else:
                    return False, "Please provide a number between 1 and 10 for severity."
            except ValueError:
                return False, "Please provide a valid number between 1 and 10 for severity."
        return True, user_input

    def handle_input(self, user_input):
        exit_commands = exit_commands = [
    "exit", "quit", "stop", "end", "close", "bye", "goodbye", 
    "thank you", "thanks", "that's all", "that's it", "done", 
    "no, thank you", "nothing else", "I'm done", "all set", 
    "no", "nope", "nah", "not really", "not now", "leave me alone", 
    "thx", "bye bye", "cya", "see ya", "gtg", "im done", 
    "nothin else", "nope im good", "I have no more symptoms", 
    "I don't need help anymore", "Nothing more to add", 
    "I'm fine now", "That's all I needed", "leave", "go away", 
    "stop talking", "I don't want to talk anymore", "stop bothering me", 
    "ttyl", "brb", "afaik"
]

        if user_input.lower() in exit_commands:
            if self.collected_data:
                summary = "\nSummary of Collected Data:\n" + "\n".join(
                    [f"- {symptom.capitalize()}: {', '.join(map(str, details))}" for symptom, details in self.collected_data.items()]
                )
                return f"Thank you for using the Cardiology Assistant Chatbot. Take care!\n\n------------------------------------------------------------------------\n{summary}\n\n"
            return "Thank you for using the Cardiology Assistant Chatbot. Take care!"

        if self.current_symptom and self.current_followup_index < len(self.ask_followup(self.current_symptom)):
            current_question = self.ask_followup(self.current_symptom)[self.current_followup_index]
            if "How often do you experience" in current_question:
                is_valid, response = self.validate_followup_response("frequency", user_input)
            elif "On a scale of 1-10, how severe is" in current_question:
                is_valid, response = self.validate_followup_response("severity", user_input)
            else:
                is_valid, response = True, user_input

            if not is_valid:
                return response

            self.collected_data[self.current_symptom].append(response)
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
                    return f"Thank you for providing details about your symptoms. Can you describe any other symptoms you are experiencing such as {self.a} or {self.b}?"

        if not self.current_symptom:
            symptoms,self.a,self.b= self.matcher.match_symptoms(user_input)
            if symptoms:
                if(symptoms[0] in self.detected_symptoms):
                    return "I've already detected this symptom. Please describe another symptom."
                self.pending_symptoms.extend(symptoms)
                self.current_symptom = self.pending_symptoms.pop(0)
                #if(self.current_symptom in self.detected_symptoms):
                self.detected_symptoms.append(symptoms[0])
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