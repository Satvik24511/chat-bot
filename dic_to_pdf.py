from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER 
import os 

SECTION_KEYS_EN = {
    "details": "Patient Details",
    "history": "Medical History",
    "symptoms": "Symptoms Reported (Current Session & History)"
}

def generate_pdf_from_dict(data, filename):
    """
    Generates a PDF document from a dictionary containing pre-translated data.

    Args:
        data (dict): A dictionary where keys (section titles, labels) and relevant
                     string values are already translated into the target language.
                     The structure should correspond to how 'pdf_ready_data' is
                     built in the main script.
        filename (str): The desired output filename for the PDF.
    """
    try:
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        for section_title, section_content in data.items():

            story.append(Paragraph(str(section_title), styles['h1']))
            story.append(Spacer(1, 6))

            if not isinstance(section_content, dict):
                story.append(Paragraph(str(section_content), styles['Normal']))
                story.append(Spacer(1, 12))
                continue 

            for key, value in section_content.items():
                is_symptoms_section = "Symptom" in section_title 
                if is_symptoms_section and key != translate_label("Status"): 
                    story.append(Paragraph(f"<b>{key}</b>", styles['h2'])) 
                    story.append(Paragraph(str(value), styles['Normal'])) 
                else:
                    story.append(Paragraph(f"<b>{key}:</b> {value}", styles['Normal'])) 

                story.append(Spacer(1, 4)) 

            story.append(Spacer(1, 12)) 

        doc.build(story)
        print(f"PDF generated successfully: {filename}")
        return True 

    except ImportError:
         print("Error: ReportLab library not found. Cannot generate PDF.")
         print("Please install it: pip install reportlab")
         return False
    except Exception as e:
        print(f"Error occurred during PDF generation for {filename}: {e}")
        return False

def translate_label(label_en):
     """Placeholder - Requires importing translator module"""
     pass
