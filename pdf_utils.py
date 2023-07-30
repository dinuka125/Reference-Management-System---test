# # from fpdf import FPDF
# # from io import StringIO
  
# # pdf = FPDF()  
  
# # pdf.add_page()
  
# # def pdf_create(text):
# #     pdf.set_font("Arial", size = 10)

    
# #     s = StringIO(text)
# #     for line in s:
# #         print(len(line))
# #         pdf.cell(200, 8, txt =line+"\n", ln = 1, align = 'l')

        
    
# #     pdf.output("mygfg.pdf")  

# # platypus_multipage.py

# # hello_platypus.py

# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph
# from reportlab.lib.styles import getSampleStyleSheet

# def hello(text):
#     doc = SimpleDocTemplate(
#             "hello_platypus.pdf",
#             pagesize=letter,
#             rightMargin=72, leftMargin=72,
#             topMargin=72, bottomMargin=18,
#             )
#     styles = getSampleStyleSheet()

#     flowables = []

    
#     para = Paragraph(text, style=styles["Normal"])
#     flowables.append(para)

#     doc.build(flowables)

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageTemplate, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.styles import (ParagraphStyle, getSampleStyleSheet)
import qrcode
from reportlab.lib.utils import ImageReader
from reportlab.platypus.frames import Frame
from functools import partial
from reportlab.lib.units import inch


def header(canvas, doc, content):
    canvas.saveState()
    w, h = content.wrap(doc.width, doc.topMargin)
    content.drawOn(canvas, doc.leftMargin, doc.height + doc.bottomMargin + doc.topMargin - h)
    canvas.restoreState()

def footer(canvas, doc, content):
    canvas.saveState()
    w, h = content.wrap(doc.width, doc.bottomMargin)
    content.drawOn(canvas, doc.leftMargin, h)
    canvas.restoreState()

def header_and_footer(canvas, doc, header_content, footer_content):
    header(canvas, doc, header_content)
    footer(canvas, doc, footer_content)


def make_letter(text):
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleH = styles['Heading1']
    story = []

    header_img = 'HEADER.png'
    footer_img = 'FOOTER.png'

    yourStyle = ParagraphStyle('yourtitle',
                           fontName="Times-Roman",
                           fontSize=12,
                           parent=styles['Normal'],
                           alignment=4,
                           spaceAfter=14)
    
    doc = SimpleDocTemplate("example_flowable.pdf",pagesize=A4,
                        rightMargin=2*cm,leftMargin=2*cm,
                        topMargin=2*cm,bottomMargin=2*cm,
                        alignment='RIGHT')
    
    
    # header_content = Image(header_img, 500 , 80)
    header_content = Image(footer_img)
    footer_content = Image(footer_img)

   



    # with open("file.txt", "r") as txt_file:
    #     data = txt_file.read()
    #     qr_data = data
    #     img = qrcode.make(qr_data)
    #     img.save("qr.png")
    #     img = ImageReader("qr.png")

        
    # txt_file = open("file.txt", 'r')
    # while True:
    #     line = txt_file.readline()
    #     line.replace("\n", "<br />")
  
    # story.append(Image("qr.png"))

    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')

    template = PageTemplate(id='test', frames=frame, onPage=partial(header_and_footer, header_content=header_content, footer_content=footer_content))

    
    doc.addPageTemplates([template])
 
    
    doc.build([Paragraph(text.replace("\n", "<br/>"), yourStyle),])
    
        

    # P = Paragraph(text_content, styleN)
    # story.append(P)

    # doc.build(
    #     story,
    # )