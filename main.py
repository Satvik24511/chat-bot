import vtt_handler as vtt
import api_handler as ga
import matcher as sm
from dic_to_pdf import generate_pdf_from_dict
import adminhandler as ah
import doctorhandler
from bson import ObjectId
import datetime
import speech_handler  
import asyncio

import translator as translator_module 

hospital_name = "AIIMS"
Mode = 0

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


def output(english_text: str):
    """Translates text to user lang, prints it, and speaks it using the correct voice."""
    user_lang_text = translator_module.translate_to_user(english_text)
    print(user_lang_text) 
    current_lang_code = translator_module.get_user_language()
    speech_handler.speak(user_lang_text, language_code=current_lang_code)

def inp(english_prompt, m=-1):
    """
    Translates prompt to user lang, speaks/prints it, gets input, translates input to English.
    """
    global Mode
    if m == -1:
        m = Mode

    output(english_prompt) 

    if m == 0:
        user_input_native_lang = input()
        return translator_module.translate_to_english(user_input_native_lang)
    else: 
        vtt.record_audio("user_audio.wav")
        recognized_text_user_lang = vtt.transcribe_audio("user_audio.wav")

        confirmation_english = "You said:" 
        output(f"{confirmation_english} {recognized_text_user_lang}")

        return translator_module.translate_to_english(recognized_text_user_lang)

def get_validated_followup(english_question, validation_type):
    """
    Repeatedly asks the translated question until a valid response (translated to English) is provided.
    """
    freq_error_en = "Please provide one of the following responses: Rarely, Occasionally, Frequently, All the time."
    sev_error_en = "Please provide a number between 1 and 10."
    num_error_en = "Please provide a valid number between 1 and 10."
    invalid_type_en = "Invalid validation type specified." 

    while True:
        response_en = inp(english_question, 0).strip() 
        if validation_type == "frequency":
            valid_en = ["rarely", "occasionally", "frequently", "all the time"]
            if response_en.lower() in valid_en:
                return response_en.capitalize()
            else:
                output(freq_error_en) 

        elif validation_type == "severity":
            try:
                severity = int(response_en)
                if 1 <= severity <= 10:
                    return severity 
                else:
                    output(sev_error_en) 
            except ValueError:
                output(num_error_en) 
        else:
             output(invalid_type_en) 
             return response_en 


def translate_label(label_en):
    """Helper to translate report labels"""
    return translator_module.translate_to_user(label_en)

def generate_markdown_report(data: dict) -> str:
    """
    Generates a markdown formatted report with translated labels.
    """
    report_lines = []
    report_lines.append(f"# {translate_label('Patient Summary Report')}")
    report_lines.append("")
    report_lines.append(f"## {translate_label('Patient Details')}")
    report_lines.append(f"- **{translate_label('Patient ID')}:** {data.get('Patient ID', '')}")
    report_lines.append(f"- **{translate_label('Name')}:** {data.get('Name', '')}")
    report_lines.append(f"- **{translate_label('Age')}:** {data.get('Age', '')}")
    gender_en = data.get('Gender', '')
    gender_translated = translate_label(gender_en.capitalize()) if gender_en else ''
    report_lines.append(f"- **{translate_label('Gender')}:** {gender_translated}")
    report_lines.append(f"- **{translate_label('Phone')}:** {data.get('Phone', '')}")
    report_lines.append("")
    report_lines.append(f"## {translate_label('Medical History')}")
    med_history = data.get("Medical History", {})
    for key_en, value in med_history.items():
        label_translated = translate_label(key_en) 
        if isinstance(value, dict):
            response_en = value.get("response", "")
            details_en = value.get("details", "")
            response_translated = translate_label(response_en.capitalize())
            line = f"- **{label_translated}:** {response_translated}"
            if details_en:
                line += f" ({translate_label('Details')}: {details_en})"
            report_lines.append(line)
        else:
            value_translated = translate_label(str(value).capitalize())
            report_lines.append(f"- **{label_translated}:** {value_translated}")

    report_lines.append("")
    report_lines.append(f"## {translate_label('Symptoms Reported (Current Session & History)')}")
    symptoms = data.get("Symptoms Reported (Current Session & History)", {}) 
    if not symptoms:
        report_lines.append(translate_label("No symptoms reported."))
    else:
        for symptom_en, details in symptoms.items():
            report_lines.append(f"- **{symptom_en.capitalize()}:**") 
            if details and len(details) >= 4: 
                frequency_en = details[0]
                severity = details[1] 
                onset_en = details[2] 
                date_reported = details[3] 

                frequency_translated = translate_label(frequency_en)

                report_lines.append(f"    - **{translate_label('Frequency')}:** {frequency_translated}")
                report_lines.append(f"    - **{translate_label('Severity')}:** {severity}")
                report_lines.append(f"    - **{translate_label('Onset')}:** {onset_en}") 
                report_lines.append(f"    - **{translate_label('Date Recorded')}:** {date_reported}")
            else:
                report_lines.append(f"    - {translate_label('Details incomplete.')}") 
    return "\n".join(report_lines)

class Patients:
    def __init__(self):
        self.id = 1
        try:
            self.db = ah.encrypted_client[ah.encrypted_database_name]
            self.patients_collection = self.db[ah.encrypted_collection_name]
        except AttributeError:
             print("FATAL: Admin handler (ah) not configured correctly for database.")
             exit() 
        except Exception as e:
            output(f"{translator_module.translate_to_user('Database connection error')}: {e}")
            exit() 

    def find_record(self, Phone, name=""):
        try:
            patients = list(self.patients_collection.find({"Phone": Phone}))
            if patients:
                patient_ids = [str(patient["_id"]) for patient in patients]
                return True, patient_ids
            return False, []
        except Exception as e:
             output(f"{translator_module.translate_to_user('Error finding record by phone')}: {e}")
             return False, []

    def record_by_id(self, id_str):
        try:
            if not ObjectId.is_valid(id_str):
                 return None
            obj_id = ObjectId(id_str)
            patient_data = self.patients_collection.find_one({"_id": obj_id})
            if patient_data:
                return Patient.from_dict(patient_data) 
            return None        
        except Exception as e:
             output(f"{translator_module.translate_to_user('Error fetching record by ID')}: {e}")
             return None

    def add_patient(self):
        name = inp("Please input your full name:", 0)
        num = inp("Please input your phone number (e.g., 10 digits, no country code or spaces):", 0)
        while not (num.isdigit() and len(num) == 10):
            if num.strip().lower() == "skip":
                break
            num = inp("Please input a valid 10-digit phone number or type 'skip' to skip:", 0)

        found, rec_ids = (False, [])
        if num.strip().lower() != "skip":
            found, rec_ids = self.find_record(num, name) 

        if found:
            pid = rec_ids[0] 
            patient = self.record_by_id(pid)
            if patient is None:
                output("Error: Failed to fetch the record details after finding the ID.")
                return 0, None 
            rec_str = patient.rt_str() 
            prompt_text_en = f"This record was found associated with your phone number. Is this you? (y/n)\n{rec_str}"
            yn = inp(prompt_text_en, 0).strip().lower() 

            while yn not in ["y", "n", "yes", "no"]:
                yn = inp("Please input a valid response (y/n):", 0).strip().lower()
            if yn in ["y", "yes"]:
                output("Proceeding with existing record.") 
                return 1, pid 

        output("Registering as a new patient or confirming details.") 
        gender_prompt = "Please input your gender (Male/Female/Other):"
        gender = inp(gender_prompt, 0).strip().lower()
        while gender not in ["male", "female", "other"]: 
             gender_prompt_retry = "Please provide a valid input (e.g., Male, Female, Other):"
             gender = inp(gender_prompt_retry, 0).strip().lower()

        age = inp("Please input your age:", 0).strip()
        while not age.isdigit() or not (0 < int(age) < 120): 
            age = inp("Please provide a valid numeric age:", 0).strip()

        password_prompt = translator_module.translate_to_user("Please input your new password:")
        print(password_prompt) 
        password = input().strip()
        confirm_prompt = translator_module.translate_to_user("Please confirm your new password:")
        print(confirm_prompt) 
        confirm_password = input().strip()

        while not password or password != confirm_password:
            output("Passwords do not match or are empty. Please try again.") 
            print(password_prompt)
            password = input().strip()
            print(confirm_prompt) 
            confirm_password = input().strip()


        patient_data = {
            "name": name,
            "Phone": num if num.strip().lower() != "skip" else "",
            "gender": gender.capitalize(), 
            "age": int(age),
            "password" : password, 
            "history": { "symptoms": {} }
        }
        try:
            result = self.patients_collection.insert_one(patient_data)
            pid = str(result.inserted_id)
            output(f"New patient record created successfully. Your Patient ID is {pid}") 
            return 0, pid 
        except Exception as e:
             output(f"{translator_module.translate_to_user('Error adding new patient to database')}: {e}")
             return 0, None 


class Patient:
    def __init__(self, pid, name, Phone, gender, age, password):
        self.id = pid
        self.name = name
        self.Phone = Phone
        self.gender = gender
        self.age = age
        self.password = password 
        self.history = {}
        if "symptoms" not in self.history:
             self.history["symptoms"] = {}


    @classmethod
    def from_dict(cls, data):
        """Creates a Patient object from a dictionary fetched from DB."""
        pid = str(data.get("_id", ""))
        name = data.get("name", "N/A")
        Phone = data.get("Phone", "N/A")
        gender = data.get("gender", "N/A")
        age = data.get("age", "N/A")
        password = data.get("password", "") 
        patient = cls(pid, name, Phone, gender, age, password)
        patient.history = data.get("history", {"symptoms": {}}) 
        if "symptoms" not in patient.history: 
            patient.history["symptoms"] = {}
        return patient

    def to_dict(self):
        """Converts the Patient object to a dictionary for DB storage."""
        return {
           "name": self.name,
           "Phone": self.Phone,
           "gender": self.gender,
           "age": self.age,
           "password" : self.password, 
           "history": self.history
        }

    def save(self, patients_db): 
        """Saves the Patient object to the database."""
        update_data = self.to_dict()

        if not self.id or not ObjectId.is_valid(self.id):
             output(f"{translator_module.translate_to_user('Error: Invalid Patient ID for saving')}: {self.id}")
             return False

        doc_id_obj = ObjectId(self.id)

        try:
            result = patients_db.patients_collection.update_one(
                {"_id": doc_id_obj},
                {"$set": update_data} 
            )
            if result.matched_count == 0:
                output(f"{translator_module.translate_to_user('Warning: No patient record found with ID {self.id} to update.')}")
                return False
            return True 
        except Exception as e:
            output(f"{translator_module.translate_to_user('Error saving patient data')}: {e}")
            return False

    def reset_symptoms(self):
        self.history["symptoms"] = {}

    def rt_str(self):
        return f'''{translate_label('ID')}: {self.id}
{translate_label('Name')}: {self.name}
{translate_label('Phone no')}: {self.Phone}
{translate_label('Gender')}: {translate_label(self.gender.capitalize())}
{translate_label('Age')}: {self.age}'''


def main1(patients_db):
    doctororpatient = inp("Are you a doctor or a patient? (Enter 'doctor' or 'patient'):", 0).strip().lower()
    while doctororpatient not in ["d", "p", "doctor", "patient"]:
        doctororpatient = inp("Please input a valid role ('doctor' or 'patient'):", 0).strip().lower()

    if doctororpatient in ["d", "doctor"]:
        output("Doctor access selected. Authentication required.")
        doc_user = inp("Enter doctor username:", 0) # Use inp for potential voice input
        doc_pass_prompt = translator_module.translate_to_user("Enter doctor password:")
        print(doc_pass_prompt)
        doc_pass = input().strip()

        if doc_user == "admin" and doc_pass == "password123": 
            output("Authentication successful.")
            printallrecords = inp("Do you want to print all patient records? (y/n):", 0).strip().lower()
            while printallrecords not in ["y", "n", "yes", "no"]:
                printallrecords = inp("Please input a valid response (y/n):", 0).strip().lower()

            if printallrecords in ["y", "yes"]:
                output("Fetching all patient records...")
                try:
                    doctorhandler.print_patient_records(patients_db.patients_collection)
                    output("Record printing process initiated.") 
                except AttributeError:
                     output("Error: Doctor handler function 'print_patient_records' not found or misconfigured.")
                except Exception as e:
                     output(f"{translator_module.translate_to_user('Error fetching records')}: {e}")
            else:
                output("No records requested. Exiting doctor module.")
            return None 
        else:
            output("Authentication failed.")
            return None 

    yn_first_time = inp("Is this your first time using our system here? (y/n):", 0).strip().lower()
    while yn_first_time not in ["y", "n", "yes", "no"]:
        yn_first_time = inp("Please input a valid response (y/n):", 0).strip().lower()

    patient = None 

    if yn_first_time in ["y", "yes"]:
        new_or_existing, patient_id = patients_db.add_patient()
        if patient_id:
            patient = patients_db.record_by_id(patient_id)
            if not patient:
                 output("Error: Could not retrieve the newly created patient record.")
                 return None
        else:
            output("Failed to create a new patient record.")
            return None
    else: 
        phone_no = inp("Please enter your registered 10-digit phone number:", 0)
        password_prompt = translator_module.translate_to_user("Please enter your password:")
        print(password_prompt)
        password = input().strip()

        found, patient_ids = patients_db.find_record(phone_no)

        selected_patient = None
        if found:
            patient_id = patient_ids[0] 
            potential_patient = patients_db.record_by_id(patient_id)

            if potential_patient:
                attempts = 0
                max_attempts = 3
                while attempts < max_attempts and potential_patient.password != password: 
                    attempts += 1
                    remaining = max_attempts - attempts
                    output(f"Incorrect password. {remaining} attempts remaining.")
                    if remaining > 0:
                        print(password_prompt)
                        password = input().strip()
                    else:
                         output("Maximum login attempts reached.")
                         return None 

                if potential_patient.password == password: 
                    selected_patient = potential_patient
                    output(f"Login successful. Welcome back, {selected_patient.name}.")

            else: 
                output(f"Error retrieving record details for ID {patient_id}.")
                return None

        if not selected_patient:
            output("Login failed or no record found with that phone number.")
            yn_register = inp("Would you like to register as a new patient? (y/n):", 0).strip().lower()
            if yn_register in ['y', 'yes']:
                new_or_existing, patient_id = patients_db.add_patient()
                if patient_id:
                    patient = patients_db.record_by_id(patient_id)
                    if not patient:
                         output("Error retrieving newly created patient record after failed login.")
                         return None
                else:
                    output("Failed to create a new patient record after failed login.")
                    return None
            else:
                output("Exiting session.")
                return None 
        else:
             patient = selected_patient 

    return patient


def Gather_info(patients_db, patient):

    if patient is None:
        output("Cannot gather information: No patient data available.")
        return 0

    symptom_matcher = sm.SymptomMatcher(symptom_list) 

    major_surgery_q = "Have you undergone any major surgeries? (yes/no):"
    major_surgery_en = inp(major_surgery_q, 0).strip().lower()
    surgery_details_en = ""
    if major_surgery_en in ["yes", "y"]:
        surgery_details_q = "Please provide details of your major surgeries (e.g., type, year):"
        surgery_details_en = inp(surgery_details_q, 0)
        patient.history["Major Surgery"] = {"response": "yes", "details": surgery_details_en}
    else:
        patient.history["Major Surgery"] = {"response": "no", "details": ""} 

    allergies_q = "Do you have any known allergies (medications, food, etc.)? If yes, please specify. If no, type 'no':"
    allergies_resp_en = inp(allergies_q, 0).strip()
    if allergies_resp_en.lower() == 'no':
         patient.history["Allergies"] = {"response": "no", "details": ""}
    else:
         patient.history["Allergies"] = {"response": "yes", "details": allergies_resp_en} 

    smoker_q = "Do you currently smoke or use tobacco? (yes/no):"
    smoker_resp_en = inp(smoker_q, 0).strip().lower()
    smoker_details_en = ""
    if smoker_resp_en in ["yes", "y"]:
         smoker_details_q = "How much and for how long? (e.g., 1 pack/day for 10 years)"
         smoker_details_en = inp(smoker_details_q, 0)
         patient.history["Smoking Status"] = {"response": "yes", "details": smoker_details_en}
    else:
         past_smoker_q = "Have you ever smoked in the past? (yes/no):"
         past_smoker_en = inp(past_smoker_q, 0).strip().lower()
         if past_smoker_en in ["yes", "y"]:
              past_smoker_details_q = "When did you quit and what did you smoke?"
              past_smoker_details_en = inp(past_smoker_details_q, 0)
              patient.history["Smoking Status"] = {"response": "past", "details": past_smoker_details_en}
         else:
              patient.history["Smoking Status"] = {"response": "no", "details": ""}

    gemini = ga.GeminiAPIHandler("AIzaSyBkRDmEdtVhVtHHbfvpetHKANTz1EW1qYQ")
    output("\nNow, please describe your main health concern or symptoms.")
    output("For example: 'I have had a headache and felt dizzy for three days.'")
    output("You can say 'done' or 'finished' when you have described your symptoms.")



    session_symptoms = {} 
    processed_symptoms_in_session = set() 

    while True:
        user_input_en = inp("Describe your symptoms (or say 'done'):", Mode)

        if user_input_en.lower().strip() in ["done", "finished", "stop", "exit", "no more", ""]:
             output("Okay, finishing symptom input.")
             break

        extracted_symptoms_en = []
        extracted_symptoms_en = [user_input_en]
        output(f"Processing: '{user_input_en}'")

        extracted_symptoms_en = [sym.strip().lower() for sym in extracted_symptoms_en if sym.strip()]

        if not extracted_symptoms_en or (len(extracted_symptoms_en) == 1 and extracted_symptoms_en[0] in ["no", "none"]):
            output("I didn't quite catch any specific symptoms there. Could you please describe them again?")
            continue

        matched_symptoms_en, _, suggestions_en = symptom_matcher.match_symptoms(extracted_symptoms_en)

        if not matched_symptoms_en and suggestions_en:
             output(f"I didn't find an exact match. Did you mean one of these: {', '.join(suggestions_en)}? Or please describe it differently.")
             continue
        elif not matched_symptoms_en:
             output("I couldn't identify a known symptom from that description. Could you please try phrasing it differently?")
             continue

        newly_matched_count = 0
        for normalized_symptom_en in matched_symptoms_en:
            normalized_symptom_en = normalized_symptom_en.capitalize() 

            if normalized_symptom_en in processed_symptoms_in_session:
                continue 

            output(f"Okay, let's talk about: {normalized_symptom_en}.") 
            newly_matched_count += 1

            freq_question_en = f"How often do you experience {normalized_symptom_en}? (Rarely, Occasionally, Frequently, All the time)"
            sev_question_en = f"On a scale of 1 to 10, how severe is your {normalized_symptom_en} (1 mild, 10 severe)?"
            start_question_en = f"When did the {normalized_symptom_en} start? (e.g., 3 days ago, 2 weeks ago)"

            frequency_en = get_validated_followup(freq_question_en, "frequency")
            severity = get_validated_followup(sev_question_en, "severity") # Returns number
            start_time_en = inp(start_question_en, 0) # Gets English translation of user's answer
            current_date = datetime.datetime.now().strftime("%Y-%m-%d") # Standard format

            session_symptoms[normalized_symptom_en] = [frequency_en, severity, start_time_en, current_date]
            processed_symptoms_in_session.add(normalized_symptom_en)

        if newly_matched_count > 0:
             output("Okay, got it. Any other symptoms? (or say 'done')")
        elif not processed_symptoms_in_session:
            pass 
        else:  
             output("It seems we've covered the symptoms mentioned. Anything else? (or say 'done')")


    if session_symptoms:
        output("Updating your symptom history...")
        for symptom_en, details_en in session_symptoms.items():
            patient.history["symptoms"][symptom_en] = details_en # Overwrite/add

        if patient.save(patients_db):
             output("Your information has been updated.")
        else:
             output("There was an issue saving your information. Please notify staff.")
             return 0 # Indicate failure
    else:
        output("No new symptoms were recorded in this session.")

    output("Preparing your summary report...")
    collected_data = {
        "Patient ID": patient.id,
        "Name": patient.name,
        "Age": patient.age,
        "Gender": patient.gender, 
        "Phone": patient.Phone,
        "Report Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Medical History": patient.history.get("Medical History", {}), # Fetch potentially updated history
        "Symptoms Reported (Current Session & History)": patient.history.get("symptoms", {})
    }

    markdown_report = generate_markdown_report(collected_data) # For internal use/logging maybe
    pdf_filename = f"Patient_Summary_{patient.id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    try:
        pdf_data_english = {}
        pdf_data_english["Patient Summary Report"] = {}

        pdf_data_english["Patient Summary Report"]["Patient Details"] = {
            "Patient ID": patient.id,
            "Name": patient.name,
            "Age": patient.age,
            "Gender": patient.gender.capitalize(), 
            "Phone": patient.Phone,
            "Report Date": collected_data_for_report["Report Date"]
        }

        pdf_data_english["Patient Summary Report"]["Medical History"] = {}
        history_en = collected_data_for_report.get("Medical History", {})
        for key_en, value_dict in history_en.items():
            response_en = value_dict.get("response", "").capitalize() 
            details_en = value_dict.get("details", "") 
            pdf_data_english["Patient Summary Report"]["Medical History"][key_en] = f"{response_en} (Details: {details_en})" if details_en else response_en

        pdf_data_english["Patient Summary Report"]["Symptoms Reported"] = {} 
        symptoms_en = collected_data_for_report.get("Symptoms Reported (Current Session & History)", {})
        if not symptoms_en:
             pdf_data_english["Patient Summary Report"]["Symptoms Reported"]["Status"] = "No symptoms reported." 
        else:
             for symptom_en, details_en in symptoms_en.items():
                  if details_en and len(details_en) >= 4:
                       freq_en = details_en[0] 
                       sev = details_en[1]
                       onset_en = details_en[2] 
                       date = details_en[3]
                       pdf_data_english["Patient Summary Report"]["Symptoms Reported"][symptom_en.capitalize()] = (
                           f"Frequency: {freq_en}, "
                           f"Severity: {sev}, "
                           f"Onset: {onset_en}, "
                           f"Date Recorded: {date}"
                       )
                  else:
                       pdf_data_english["Patient Summary Report"]["Symptoms Reported"][symptom_en.capitalize()] = "Details incomplete." # English status

        pdf_generated = generate_pdf_from_dict(pdf_data_english["Patient Summary Report"], pdf_filename)

        if pdf_generated:
            output(f"Summary report (in English) has been saved as '{pdf_filename}'.")
            return 1 
        else:
            output("Failed to generate the PDF report.") 
            return 0 

    except ModuleNotFoundError:
         output("Error: PDF generation module ('dic_to_pdf') not found. Report not created.")
         return 0 
    except Exception as e:
        output(f"Error preparing data or generating PDF report: {e}") 
        return 0    


if __name__ == "__main__":
    db_connection_successful = False
    patients_db_instance = None
    try:
        translator_module.record_user_language()
        current_lang = translator_module.get_user_language()
        print(f"Current language code: {current_lang}") # Debug confirmation

        patients_db_instance = Patients()
        if hasattr(patients_db_instance, 'patients_collection') and patients_db_instance.patients_collection is not None:
             db_connection_successful = True
             print("Database connection appears successful.") # Debug
        else:
             print("Exiting due to database connection failure.")
             exit()

        mode_choice = inp("Would you like voice or text input? (Enter 'v' for voice, 't' for text):", 0).strip().lower()
        if mode_choice == "v":
            Mode = 1
            output("Voice input mode selected.")
        else:
            Mode = 0
            output("Text input mode selected.")

        welcome_message_en = f"Hello! Welcome to {hospital_name}. I'm here to assist. Let's start."
        output(welcome_message_en)

        current_patient = main1(patients_db_instance)

        if current_patient:
            greeting_en = f"Thank you, {current_patient.name}. Now let's gather some health information."
            output(greeting_en)
            gather_result = Gather_info(patients_db_instance, current_patient)
            if gather_result == 1:
                 output("Check-in process complete. Please proceed as directed by staff.")
            else:
                 output("Check-in process could not be fully completed due to errors. Please seek assistance.")
        else:
            output("Could not identify or register patient. Exiting.")

    except Exception as main_e:
        print(f"FATAL ERROR in main execution: {main_e}") # Log detailed error
        try:
             output(f"An unexpected error occurred. Please report this issue. Error: {main_e}")
        except:
             print("System error prevented final message.") # Absolute fallback

    finally:
        print("\nPerforming cleanup...")
        try:
            output("Closing application. Goodbye.")
        except:
            print("Goodbye.") # Fallback print

        if db_connection_successful and patients_db_instance and hasattr(ah, "encrypted_client") and ah.encrypted_client:
            try:
                ah.encrypted_client.close()
                print("Database connection closed.")
            except Exception as close_e:
                print(f"Error closing database connection: {close_e}")
        else:
             print("Database connection was not established or already closed.")

        try:
            loop = asyncio.get_event_loop_policy().get_event_loop()
            if loop.is_running():
                loop.stop()
        except Exception as loop_close_e:
            pass
        print("Cleanup finished.")
