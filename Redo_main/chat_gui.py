from chat_gui import ChatApp
from imp_funcs import *
import config
from datetime import datetime

def run_my_logic(app):
    while True:
        op = app.ask_user('''Hi, This is the Medical assistant chatbot which is here to streamline the 
medical process and save your time!

Is this your first time at the hospital? (y/n)
''')

        if op.lower() == "admin!":
            pass

        elif op.lower() in ["d", "doctor"]:
            pass

        elif op.lower() in ["yes", "y", "yah"]:
            # Begin registration
            username = app.ask_user("Choose a username (for future logins):").lower()
            if users_col.find_one({"username": username}):
                app._add_bot_message("That username already exists. Please restart registration.")
                app.reset_chat()
                continue

            email = app.ask_user("Enter your email address:")
            password = app.ask_password("Set a password (input will be hidden):")
            password2 = app.ask_password("Confirm your password:")
            while password != password2:
                app._add_bot_message("Passwords do not match. Please try again.")
                password = app.ask_password("Set a password:")
                password2 = app.ask_password("Confirm your password:")

            name = app.ask_user("Full Name:")

            age = app.ask_user("What is your age? (give simple numbers like 15)")
            while not age.isdigit():
                age = app.ask_user("Please enter a valid number for age:")
            age = int(age)

            gender = "K"
            while gender.lower() not in ['m', 'f', 'o', 'r']:
                gender = app.ask_user('''Please input:
M: Male
F: Female
O: Other
R: Rather not say
''').lower()

            contact = app.ask_user("Enter your phone number:")
            enc_contact = encrypt_contact(contact)

            # Ask for medical history
            history = app.ask_user("Do you have any previous medical history we should be aware of? Please describe briefly or type 'none'.")

            # Collect symptom data
            symptoms = []
            added_symptoms = set()
            add_symptom = app.ask_user("Would you like to add a symptom? (y/n)")
            while add_symptom.lower() == "y":
                symptom = app.ask_user("Symptom:").strip().lower()
                if symptom in added_symptoms:
                    app._add_bot_message("This symptom has already been added. Please enter a new one.")
                    add_symptom = app.ask_user("Add another symptom? (y/n)")
                    continue

                frequency = app.ask_user("How frequently does this symptom occur? (e.g., daily, occasionally)")
                while frequency.strip() == "":
                    frequency = app.ask_user("Please provide a valid frequency:")

                severity = app.ask_user("On a scale of 1 to 10, how severe is this symptom?")
                while not severity.isdigit() or not (1 <= int(severity) <= 10):
                    severity = app.ask_user("Please enter a number between 1 and 10 for severity:")

                duration = app.ask_user("For how long have you been experiencing this symptom? (e.g., 2 days, 1 week)")
                while duration.strip() == "":
                    duration = app.ask_user("Please provide a valid duration:")

                notes = app.ask_user("Any additional notes you'd like to add?")
                date_str = datetime.now().strftime("%Y-%m-%d")

                symptoms.append({
                    "Symptom": symptom,
                    "Frequency": frequency,
                    "Severity": severity,
                    "Duration": duration,
                    "Additional_Notes": notes,
                    "Date": date_str
                })
                added_symptoms.add(symptom)
                add_symptom = app.ask_user("Add another symptom? (y/n)")

            # Create user and patient entries
            users_col.insert_one({
                "username": username,
                "Name": name,
                "email": email,
                "password": hash_password(password),
                "role": "patient"
            })

            patients_col.insert_one({
                "patient_id": username,
                "demographic_data": {
                    "Name": name,
                    "Age": age,
                    "Gender": gender,
                    "Contact": enc_contact
                },
                "symptoms_data": symptoms,
                "medical_history": history,
                "doctor_notes": []
            })

            app._add_bot_message(f"Thank you {name}, you have been successfully registered with ID: {username}")

        elif op.lower() in ["no", "n"]:
            app._add_bot_message("Welcome back! Let's log you in.")
            username = app.ask_user("Enter your username:").lower()
            password = app.ask_password("Enter your password:")

            user = users_col.find_one({"username": username})
            if not user or not check_password(password, user["password"]):
                app._add_bot_message("Invalid credentials. Please restart.")
                app.reset_chat()
                continue

            patient = patients_col.find_one({"patient_id": username})
            today = datetime.now().strftime("%Y-%m-%d")

            old_symptoms = patient.get("symptoms_data", [])
            to_move = [s for s in old_symptoms if s.get("Date") != today]
            keep_today = [s for s in old_symptoms if s.get("Date") == today]

            if to_move:
                history = patient.get("medical_history", "")
                if isinstance(history, str):
                    history = []
                history.extend(to_move)
                patients_col.update_one({"patient_id": username}, {
                    "$set": {
                        "symptoms_data": keep_today,
                        "medical_history": history
                    }
                })

            symptoms = keep_today[:]
            added_symptoms = set(s["Symptom"] for s in symptoms)
            add_symptom = app.ask_user("Would you like to report a new symptom? (y/n)")
            while add_symptom.lower() == "y":
                symptom = app.ask_user("Symptom:").strip().lower()
                if symptom in added_symptoms:
                    app._add_bot_message("This symptom has already been reported today.")
                    add_symptom = app.ask_user("Add another symptom? (y/n)")
                    continue

                frequency = app.ask_user("Frequency:")
                severity = app.ask_user("Severity (1-10):")
                duration = app.ask_user("Duration:")
                notes = app.ask_user("Any additional notes?")
                date_str = today

                symptoms.append({
                    "Symptom": symptom,
                    "Frequency": frequency,
                    "Severity": severity,
                    "Duration": duration,
                    "Additional_Notes": notes,
                    "Date": date_str
                })
                added_symptoms.add(symptom)
                add_symptom = app.ask_user("Add another symptom? (y/n)")

            patients_col.update_one({"patient_id": username}, {"$set": {"symptoms_data": symptoms}})
            app._add_bot_message("Your symptoms have been updated. Thank you!")

        app.reset_chat()

if __name__ == "__main__":
    app = ChatApp()
    app.after(300, lambda: run_my_logic(app))
    app.geometry("1366x768")
    app.mainloop()
