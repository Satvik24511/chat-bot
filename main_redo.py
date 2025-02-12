import matcher as sm
hospital_name = "AIIMS"
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
Mode = 0

def inp(a,m = Mode):
    print(a)
    if(m == 0):
        return input()
    
    # voice module to be integrated here 


class Patients:
    def __init__(self):
        self.id = 1
        self.no_patients = 0
        self.patient_list = {}
    def find_record(self,phone_no,name = ""):
        flg = False
        rt = []
        for i,j in self.patient_list.items():
            if(j.phone_no == phone_no):
                flg = True
                rt.append(i)
        if(flg):
            return True,rt
        return False,[] #return the patient id and patient info if found in a dic
    def record_by_id(self,id):
        rcd = {}
        return rcd
    def add_patient(self):
        name = inp("Please input your full name:")
        num = inp("Please input your phone number:(without the +91 extension and without any space)")
        while(len(num) != 10 or num.isnumeric() == False):
            if(num == "skip"):
                break
            num = inp("Please input a valid phone or input \"skip\" to skip for now")
        flg = False
        rcd = ""
        if(num != "skip"):
            flg,rcd = self.find_record(num,name)
        if(flg):
            id = rcd[0]                                         ###########change this to match patient id
            rcdp = self.patient_list[id].rt_str()
            yn = inp(f"This record was found associated with your phone no, Is this you by chance? (y/n),\n {rcdp}")    #add a matching feature here from just y/n or yes no to be more general
            while(yn != "y" or yn != "n" or yn != "yes" or yn != "no"):                                                 # need to change how this patient id works
                yn = inp("Please input a valid input")
            if(yn == "y" or yn == "yes"):
                return 1,id
        gender = inp("Please input your gender (Male/Female):")
        gender = gender.lower()
        while(gender != "male" or gender != "female"):
            gender = inp("Please give a valid input:")
            gender = gender.lower()
        age = inp("please input your age:")
        while(age.isnumeric() == False):
            age = inp("Please give a valid input:")
        self.patient_list[self.id] = Patient(self.id,name,num,gender,age)
        self.id+=1
        self.no_patients+=1
        return 0,self.id-1
        
class Patient:
    def __init__(self,id,name,phone_no,gender,age):
        self.id = id
        self.name = name
        self.phone_no = phone_no
        self.gender = gender 
        self.age = age
        self.history = {}
        self.symptoms = []
        self.severity = {}
    
    def reset(self):
        self.symptoms = []
        self.severity = {}
    
    def rt_str(self):
        return f'''ID: {self.id}
Name: {self.name}
Phone no: {self.phone_no}
Gender: {self.gender}
Age: {self.age}'''

def Gather_info(patients_db):
    yn = inp("Is this your first time in this hospital? (y/n)").strip().lower()
    while yn not in ["y", "n", "yes", "no"]:
        yn = inp("Please input a valid response (y/n):").strip().lower()

    if yn in ["y", "yes"]:
        # New patient - Gather detailed info
        new_patient, patient_id = patients_db.add_patient()
    else:
        # Returning patient - Look up medical record
        phone_no = inp("Please enter your registered phone number (without +91 and spaces):")
        found, patient_ids = patients_db.find_record(phone_no)
        if found:
            print(f"Found records associated with this number: {patient_ids}.")
            patient_id = patient_ids[0]  # Assuming the first record for now
            print(f"Medical record pulled for Patient ID: {patient_id}")
        else:
            print("No record found. Please register as a new patient.")
            new_patient, patient_id = patients_db.add_patient()

    if patient_id not in patients_db.patient_list:
        print("Error: Patient record not found.")
        return 0
    
    patient = patients_db.patient_list[patient_id]
    
    # Ask additional medical history questions
    patient.history["major_surgery"] = inp("Have you undergone any major surgeries? (yes/no)").strip().lower()
    patient.history["family_history"] = inp("Do your parents or grandparents suffer from similar symptoms? (yes/no)").strip().lower()
    patient.history["allergies"] = inp("Do you have any known allergies? If yes, please specify. If no, type 'no':").strip()
    patient.history["smoker"] = inp("Are you a smoker? (yes/no)").strip().lower()
    patient.history["sexual_history"] = inp("Would you like to disclose any relevant sexual health information? (yes/no)").strip().lower()
    patient.reset()
    # Symptom checking
    while True:
        symptoms = inp("What symptoms are you feeling? Please list them separated by commas:").split(",")
        symptoms = [symptom.strip().lower() for symptom in symptoms if symptom.strip()]
        patient.history["symptoms"] = symptoms
        
        patient.history["severity"] = inp("On a scale of 1-10, how severe are your symptoms? (1 being mild, 10 being extreme)").strip()
        while not patient.history["severity"].isdigit() or not (1 <= int(patient.history["severity"] )<= 10):
            patient.history["severity"] = inp("Please enter a number between 1 and 10:").strip()
        
        patient.history["frequency"] = inp("How often do the symptoms occur? (e.g., daily, weekly, rarely)").strip().lower()
        
        other_symptoms = inp("Do you have any other symptoms? (yes/no)").strip().lower()
        while other_symptoms not in ["yes", "no", "y", "n"]:
            other_symptoms = inp("Please enter yes or no:").strip().lower()

        if other_symptoms in ["yes", "y"]:
            extra_symptoms = inp("Please list additional symptoms separated by commas:").split(",")
            patient.history["symptoms"].extend([symptom.strip().lower() for symptom in extra_symptoms if symptom.strip()])
        
    # If severity is very high, flag for emergency response
        if int(patient.history["severity"]) >= 8:
            print("Alert! Critical symptoms detected. Notifying doctors immediately.")
    
    print("Thank you for providing the details. Your responses have been recorded.")
    return 1



if __name__ == "__main__":
    p = Patients()
    a = input("Would you like voice or text? (v/t)")
    if(a == "v"):
        Mode = 1
    symp_mch = sm.SymptomMatcher(symptom_list)
    print(f"Hello! Welcome to {hospital_name}. I'm here to assist with your check-in. Can I start by gathering some details?")
    Gather_info(p)
        
