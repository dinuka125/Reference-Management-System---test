import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os

doc = SimpleDocTemplate("form_letter.pdf",pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)

page = []

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

def add_image(img):
    im = Image(img, 2*inch, 2*inch)
    page.append(im)

def add_space():
    page.append(Spacer(1, 12))

def add_text(space=0):
    with open("file.txt", "r") as txt_file:
        data = txt_file.read()

    page.append(Paragraph((data.replace("\n", "<br/>")), styles["Normal"]))
    if space == 1:
        add_space()
    add_space()        

add_text()    
add_image("qr.png")
doc.build(page)
