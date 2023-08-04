from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate,Image,Spacer,PageTemplate
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.platypus.frames import Frame
from functools import partial
from reportlab.lib.styles import (ParagraphStyle, getSampleStyleSheet)
from reportlab.lib.units import cm



def header(canvas, doc, content):
    w1, h1 = A4
    canvas.saveState()
    header_img = 'resized-head.png'
    header_content = ImageReader(header_img)
    img_w, img_h = header_content.getSize()
    w, h = content.wrap(img_w, img_h)
    content.drawOn(canvas, 0, h1 - img_h)
    canvas.restoreState()

def footer(canvas, doc, content):
    w1, h1 = A4
    canvas.saveState()
    footer_img = 'resized-foo.png'
    footer_content = ImageReader(footer_img)
    img_w, img_h = footer_content.getSize()
    w, h = content.wrap(img_w, img_h)
    content.drawOn(canvas, 0, h1 - 840)
    canvas.restoreState()

def header_and_footer(canvas, doc, header_content, footer_content):
    header(canvas, doc, header_content)
    footer(canvas, doc, footer_content)   

def make_pdf(text,cpm):
    styles = getSampleStyleSheet()
    style_2 = ParagraphStyle("style_2", fontName="Times-Roman",
                            fontSize=11.5,
                            parent=styles['Normal'],
                            alignment=4)
    
    yourStyle = ParagraphStyle('yourtitle',
                            fontName="Times-Roman",
                            fontSize=12,
                            parent=styles['Normal'],
                            alignment=4)
                            #spaceAfter=100)       
                            # 

    doc = SimpleDocTemplate("static\pdf\{cpm}.pdf".format(cpm=cpm),pagesize=A4,
                            rightMargin=2*cm,leftMargin=2*cm,
                            topMargin=2*cm,bottomMargin=2*cm,
                            )                        
                    
    h,w = A4
    story = []    

    
    header_img = 'resized-head.png'
    footer_img = 'resized-foo.png'

    header_content = Image(header_img)
    footer_content = Image(footer_img)
    sign_img = Image('sign.png',hAlign='LEFT')

    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')

    template = PageTemplate(id='test', frames=frame, onPage=partial(header_and_footer, header_content=header_content, footer_content=footer_content))

    doc.addPageTemplates([template])

    story.append(Spacer(10,100))

    story.append(Paragraph(text.replace("\n", "<br/>"), yourStyle))

    story.append(Spacer(10,3))

    story.append(sign_img)

    story.append(Paragraph("""Prof. K.S. Lasith Gunawardena <br></br>
                              D. Eng., M.Sc., B.Sc., SMIEEE, FBCS, MCS <br></br>
                              Professor and Head, Department of Information Technology, <br></br>
                              University of Sri Jayewardenepura.
                    """,style_2))

    doc.build(story)