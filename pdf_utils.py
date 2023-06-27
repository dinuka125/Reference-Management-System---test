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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
import qrcode
from reportlab.lib.utils import ImageReader


def hello():
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleH = styles['Heading1']
    story = []


    doc = SimpleDocTemplate("example_flowable.pdf",pagesize=A4,
                        rightMargin=2*cm,leftMargin=2*cm,
                        topMargin=2*cm,bottomMargin=2*cm)
    
    with open("file.txt", "r") as txt_file:
        data = txt_file.read()
        qr_data = data
        img = qrcode.make(qr_data)
        img.save("qr.png")
        img = ImageReader("qr.png")

        
    # txt_file = open("file.txt", 'r')
    # while True:
    #     line = txt_file.readline()
    #     line.replace("\n", "<br />")
  
    story.append(Image("qr.png"))

    doc.build([Paragraph(data.replace("\n", "<br/>"), getSampleStyleSheet()['Normal']),])
    
        

    # P = Paragraph(text_content, styleN)
    # story.append(P)

    # doc.build(
    #     story,
    # )