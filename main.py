import vtt_handler as vtt
import api_handler as ga       # Ensure this module provides extract_symptoms() and is_exit_command()
import matcher as sm
from dic_to_pdf import generate_pdf_from_dict  # Function to convert dict to PDF

hospital_name = "AIIMS"
Mode = 0  # Global mode: 0 for text input, 1 for voice input

# Define your known symptom list.
symptom_list = [
    "Shortness of breath", "Dizziness", "Nausea", "Headache", "Chest pain", "blood pressure / bp",
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

def inp(prompt, m=-1):
    """
    Get user input using text or voice depending on Mode.
    """
    global Mode
    if m == -1:
        m = Mode
    print(prompt)
    if m == 0:
        return input()
    else:
        vtt.record_audio("user_audio.wav")
        j = vtt.transcribe_audio("user_audio.wav")
        print("You said:", j)
        return j

def get_validated_followup(question, validation_type):
    """
    Repeatedly asks the question until a valid response is provided.
    For "frequency", valid responses are: Rarely, Occasionally, Frequently, All the time.
    For "severity", valid responses are integers between 1 and 10.
    """
    while True:
        response = inp(question, 0).strip()
        if validation_type == "frequency":
            valid = ["rarely", "occasionally", "frequently", "all the time"]
            if response.lower() in valid:
                return response.capitalize()
            else:
                print("Please provide one of the following responses: Rarely, Occasionally, Frequently, All the time.")
        elif validation_type == "severity":
            try:
                severity = int(response)
                if 1 <= severity <= 10:
                    return severity
                else:
                    print("Please provide a number between 1 and 10.")
            except ValueError:
                print("Please provide a valid number between 1 and 10.")
        else:
            return response

def generate_markdown_report(data: dict) -> str:
    """
    Generates a markdown formatted report from the collected data.
    This summary is strictly a record of the provided information.
    """
    report_lines = []
    report_lines.append("# Patient Summary Report")
    report_lines.append("")
    report_lines.append("## Patient Details")
    report_lines.append(f"- **Patient ID:** {data.get('Patient ID', '')}")
    report_lines.append(f"- **Name:** {data.get('Name', '')}")
    report_lines.append(f"- **Age:** {data.get('Age', '')}")
    report_lines.append(f"- **Gender:** {data.get('Gender', '')}")
    report_lines.append(f"- **Phone:** {data.get('Phone', '')}")
    report_lines.append("")
    report_lines.append("## Medical History")
    med_history = data.get("Medical History", {})
    for key, value in med_history.items():
        if isinstance(value, dict):
            response = value.get("response", "")
            details = value.get("details", "")
            line = f"- **{key}:** {response.capitalize()}"
            if details:
                line += f" (Details: {details})"
            report_lines.append(line)
        else:
            report_lines.append(f"- **{key}:** {value}")
    report_lines.append("")
    report_lines.append("## Symptoms")
    symptoms = data.get("Symptoms", {})
    if not symptoms:
        report_lines.append("No symptoms reported.")
    else:
        for symptom, details in symptoms.items():
            report_lines.append(f"- **{symptom.capitalize()}:**")
            if details and len(details) >= 3:
                frequency = details[0]
                severity = details[1]
                onset = details[2]
                report_lines.append(f"    - **Frequency:** {frequency}")
                report_lines.append(f"    - **Severity:** {severity}")
                report_lines.append(f"    - **Onset:** {onset}")
            else:
                report_lines.append("    - No details provided.")
    return "\n".join(report_lines)

class Patients:
    def __init__(self):
        self.id = 1
        self.no_patients = 0
        self.patient_list = {}
    
    def find_record(self, phone_no, name=""):
        rt = []
        for pid, patient in self.patient_list.items():
            if patient.phone_no == phone_no:
                rt.append(pid)
        if rt:
            return True, rt
        return False, []
    
    def record_by_id(self, id):
        return self.patient_list.get(id, None)
    
    def add_patient(self):
        name = inp("Please input your full name:", 0)
        num = inp("Please input your phone number (without the +91 extension and spaces):", 0)
        while len(num) != 10 or not num.isnumeric():
            if num.strip().lower() == "skip":
                break
            num = inp("Please input a valid phone number or type \"skip\" to skip:", 0)
        found, rec_ids = (False, [])
        if num.strip().lower() != "skip":
            found, rec_ids = self.find_record(num, name)
        if found:
            pid = rec_ids[0]
            rec_str = self.patient_list[pid].rt_str()
            yn = inp(f"This record was found associated with your phone number. Is this you? (y/n)\n{rec_str}", 0).strip().lower()
            while yn not in ["y", "n", "yes", "no"]:
                yn = inp("Please input a valid response (y/n):", 0).strip().lower()
            if yn in ["y", "yes"]:
                return 1, pid
        gender = inp("Please input your gender (Male/Female):", 0).strip().lower()
        while gender not in ["male", "female"]:
            gender = inp("Please provide a valid input (Male/Female):", 0).strip().lower()
        age = inp("Please input your age:", 0).strip()
        while not age.isnumeric():
            age = inp("Please provide a valid numeric age:", 0).strip()
        patient = Patient(self.id, name, num, gender, age)
        self.patient_list[self.id] = patient
        self.id += 1
        self.no_patients += 1
        return 0, self.id - 1

class Patient:
    def __init__(self, pid, name, phone_no, gender, age):
        self.id = pid
        self.name = name
        self.phone_no = phone_no
        self.gender = gender 
        self.age = age
        self.history = {}   # To store all patient data
        self.history["symptoms"] = {}  # Mapping each symptom to its follow-up responses
    
    def reset_symptoms(self):
        self.history["symptoms"] = {}
    
    def rt_str(self):
        return f'''ID: {self.id}
Name: {self.name}
Phone no: {self.phone_no}
Gender: {self.gender}
Age: {self.age}'''

def Gather_info(patients_db):
    # Instantiate the symptom matcher using your known symptom list.
    symptom_matcher = sm.SymptomMatcher(symptom_list)
    
    # Basic patient check.
    yn = inp("Is this your first time in this hospital? (y/n):", 0).strip().lower()
    while len(yn) < 1 or yn[0] not in ["y", "n", "yes", "no"]:
        yn = inp("Please input a valid response (y/n):", 0).strip().lower()
    
    if yn in ["y", "yes"]:
        new_patient, patient_id = patients_db.add_patient()
    else:
        phone_no = inp("Please enter your registered phone number (without +91 and spaces):", 0)
        found, patient_ids = patients_db.find_record(phone_no)
        if found:
            print(f"Found records associated with this number: {patient_ids}.")
            patient_id = patient_ids[0]
            print(f"Medical record pulled for Patient ID: {patient_id}")
        else:
            print("No record found. Please register as a new patient.")
            new_patient, patient_id = patients_db.add_patient()
    
    if patient_id not in patients_db.patient_list:
        print("Error: Patient record not found.")
        return 0
    
    patient = patients_db.patient_list[patient_id]
    
    # Ask about major surgeries and, if yes, request further details.
    major_surgery = inp("Have you undergone any major surgeries? (yes/no):", 0).strip().lower()
    if major_surgery in ["yes", "y"]:
        surgery_details = inp("Please provide details of your major surgeries (e.g., type, year, outcome):", 0)
        patient.history["major_surgery"] = {"response": major_surgery, "details": surgery_details}
    else:
        patient.history["major_surgery"] = {"response": major_surgery, "details": ""}
    
    patient.history["family_history"] = inp("Do your parents or grandparents suffer from similar symptoms? (yes/no):", 0).strip().lower()
    patient.history["allergies"] = inp("Do you have any known allergies? If yes, please specify. If no, type 'no':", 0).strip()
    patient.history["smoker"] = inp("Are you a smoker? (yes/no):", 0).strip().lower()
    patient.history["sexual_history"] = inp("Would you like to disclose any relevant sexual health information? (yes/no):", 0).strip().lower()
    
    # Initialize Gemini API handler (replace with your actual key)
    gemini = ga.GeminiAPIHandler("AIzaSyBkRDmEdtVhVtHHbfvpetHKANTz1EW1qYQ")
    
    print("\nNow, please describe your symptoms in plain English.")
    print("For example: 'I feel pain in my head and I'm tired all the time.'")
    print("When you are done, please provide your exit command.")
    
    # Allow multiple rounds of symptom input.
    matched_symptoms = []
    while True:
        if len(matched_symptoms) == 0:
            user_input = inp("Describe your symptoms:", 0)
            if gemini.is_exit_command(user_input):
                print("Exit command recognized. Ending symptom input.")
                break
            
            extracted_symptoms = gemini.extract_symptoms(user_input)
            # Clean up the list: strip whitespace and lowercase.
            extracted_symptoms = [sym.strip().lower() for sym in extracted_symptoms if sym.strip()]
            
            # Check if Gemini returned "no" (i.e. no symptoms found)
            if len(extracted_symptoms) == 1 and extracted_symptoms[0] == "no":
                print("No symptoms identified in your input. Please describe your symptoms in more detail.")
                continue
            
            # Use the matcher to normalize the extracted symptoms.
            matched_symptoms, a, b = symptom_matcher.match_symptoms(extracted_symptoms)
            if not matched_symptoms:
                print("None of the extracted symptoms matched our known symptoms. Please describe your symptoms in more detail.")
                continue
            
        # Use the first matched symptom.
        normalized_symptom = matched_symptoms[0]
        # print("matched symptoms are following:",matched_symptoms)
        matched_symptoms.pop(0)
        if normalized_symptom in patient.history["symptoms"]:
            print(f"The symptom '{normalized_symptom}' has already been recorded. Skipping follow-up for this symptom.")
            continue
        
        # Record the normalized symptom and ask follow-up questions with validated input.
        patient.history["symptoms"][normalized_symptom] = []
        freq_question = f"How often do you experience {normalized_symptom}? (Rarely, Occasionally, Frequently, All the time)"
        sev_question = f"On a scale of 1-10, how severe is your {normalized_symptom}?"
        start_question = f"When did the {normalized_symptom} start? (e.g., 2 days ago, 1 week ago)"
        
        frequency = get_validated_followup(freq_question, "frequency")
        severity = get_validated_followup(sev_question, "severity")
        start_time = inp(start_question, 0)
        
        patient.history["symptoms"][normalized_symptom].extend([frequency, severity, start_time])
    
    # Compile all collected data into a summary dictionary.
    collected_data = {
        "Patient ID": patient.id,
        "Name": patient.name,
        "Age": patient.age,
        "Gender": patient.gender,
        "Phone": patient.phone_no,
        "Medical History": {
            "Major Surgery": patient.history.get("major_surgery", {}),
            "Family History": patient.history.get("family_history", ""),
            "Allergies": patient.history.get("allergies", ""),
            "Smoker": patient.history.get("smoker", ""),
            "Sexual History": patient.history.get("sexual_history", "")
        },
        "Symptoms": patient.history["symptoms"]
    }
    
    # Convert the collected data into a PDF.
    generate_pdf_from_dict(collected_data, "Patient_Summary_Report.pdf")
    print("\nSummary report has been saved as 'Patient_Summary_Report.pdf'.")
    return 1

if __name__ == "__main__":
    p = Patients()
    a = inp("Would you like voice or text input? (v/t):", 0)
    if a.strip().lower() == "v":
        Mode = 1
    else:
        Mode = 0
    print(f"Hello! Welcome to {hospital_name}. I'm here to assist with your check-in. Let's start by gathering some details.")
    Gather_info(p)
