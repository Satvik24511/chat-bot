from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf_from_dict(data: dict, filename: str):
    """
    Converts the provided dictionary into a PDF and saves it to the specified filename.
    The dictionary is flattened into text lines which are then written into the PDF.
    """
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y = height - 40  # Starting from a top margin

    def flatten_dict(d, indent=0):
        lines = []
        for key, value in d.items():
            prefix = " " * indent
            if isinstance(value, dict):
                lines.append(f"{prefix}{key}:")
                lines.extend(flatten_dict(value, indent=indent + 4))
            elif isinstance(value, list):
                lines.append(f"{prefix}{key}:")
                for item in value:
                    lines.append(f"{' ' * (indent + 4)}- {item}")
            else:
                lines.append(f"{prefix}{key}: {value}")
        return lines

    # Flatten the dictionary into a list of text lines.
    lines = flatten_dict(data)

    for line in lines:
        c.drawString(40, y, line)
        y -= 15  # Move down for the next line
        if y < 40:
            c.showPage()  # Create a new page if needed
            y = height - 40

    c.save()
