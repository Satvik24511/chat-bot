from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
def generate_pdf_from_dict(data, filename):
    """
    Generate a PDF from the collected data dictionary.
    Translates the content to the user's preferred language before generating the PDF.
    """
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    
    # Create the PDF document
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Translate the title
    title_text = translator.translate_to_user("Patient Summary Report")
    title = Paragraph(title_text, styles["Title"])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Translate and add patient details
    subtitle_text = translator.translate_to_user("Patient Details")
    subtitle = Paragraph(subtitle_text, styles["Heading1"])
    story.append(subtitle)
    story.append(Spacer(1, 6))
    
    # Add patient information (translated)
    patient_info = [
        f"{translator.translate_to_user('Patient ID')}: {data.get('Patient ID', '')}",
        f"{translator.translate_to_user('Name')}: {data.get('Name', '')}",
        f"{translator.translate_to_user('Age')}: {data.get('Age', '')}",
        f"{translator.translate_to_user('Gender')}: {translator.translate_to_user(data.get('Gender', ''))}",
        f"{translator.translate_to_user('Phone')}: {data.get('Phone', '')}"
    ]
    
    for info in patient_info:
        p = Paragraph(info, styles["Normal"])
        story.append(p)
        story.append(Spacer(1, 6))
    
    story.append(Spacer(1, 12))
    
    # Translate and add medical history
    subtitle_text = translator.translate_to_user("Medical History")
    subtitle = Paragraph(subtitle_text, styles["Heading1"])
    story.append(subtitle)
    story.append(Spacer(1, 6))
    
    # Add medical history (translated)
    med_history = data.get("Medical History", {})
    for key, value in med_history.items():
        translated_key = translator.translate_to_user(key)
        if isinstance(value, dict):
            response = translator.translate_to_user(value.get("response", ""))
            details = translator.translate_to_user(value.get("details", ""))
            text = f"<b>{translated_key}:</b> {response}"
            if details:
                text += f" ({translator.translate_to_user('Details')}: {details})"
        else:
            text = f"<b>{translated_key}:</b> {translator.translate_to_user(value)}"
        
        p = Paragraph(text, styles["Normal"])
        story.append(p)
        story.append(Spacer(1, 6))
    
    story.append(Spacer(1, 12))
    
    # Translate and add symptoms
    subtitle_text = translator.translate_to_user("Symptoms")
    subtitle = Paragraph(subtitle_text, styles["Heading1"])
    story.append(subtitle)
    story.append(Spacer(1, 6))
    
    # Add symptoms (translated)
    symptoms = data.get("Symptoms", {})
    if not symptoms:
        p = Paragraph(translator.translate_to_user("No symptoms reported."), styles["Normal"])
        story.append(p)
    else:
        for symptom, details in symptoms.items():
            translated_symptom = translator.translate_to_user(symptom)
            p = Paragraph(f"<b>{translated_symptom}</b>", styles["Heading2"])
            story.append(p)
            
            if details and len(details) >= 3:
                frequency = translator.translate_to_user(details[0])
                severity = details[1]  # No need to translate numbers
                onset = translator.translate_to_user(details[2])
                
                freq_text = f"<b>{translator.translate_to_user('Frequency')}:</b> {frequency}"
                sev_text = f"<b>{translator.translate_to_user('Severity')}:</b> {severity}"
                onset_text = f"<b>{translator.translate_to_user('Onset')}:</b> {onset}"
                
                story.append(Paragraph(freq_text, styles["Normal"]))
                story.append(Paragraph(sev_text, styles["Normal"]))
                story.append(Paragraph(onset_text, styles["Normal"]))
            else:
                p = Paragraph(translator.translate_to_user("No details provided."), styles["Normal"])
                story.append(p)
            
            story.append(Spacer(1, 6))
    
    # Build the PDF
    doc.build(story)
    print(translator.translate_to_user(f"Report generated successfully: {filename}"))

