import smtplib
from email.message import EmailMessage
import ssl
import random
import mimetypes
import os 


def gen_confirm_code():
    code = random.randint(0,9)
    return code 


def send_reference_request(cpm, type):

    msg = EmailMessage()

    msg.set_content("""


    Dear Prof. Lasith Gunawardena,

    Your have receivecd a reference request

        CPM : {cpm}
        Type : {type}
    
    In order to process the request please use following links
               To generate letter - link : http://127.0.0.1:5000/auth/{type}/web/{cpm}
               To write letter - link : http://127.0.0.1:5000/write/{type}/web/{cpm}    

    Thank you and Best Regards
    Reference management System

                            
    """.format(cpm=cpm, type=type))

    msg['Subject'] = 'Refernece Request'
    msg['From'] = "stockly125@gmail.com"
    msg['To'] = "dinugakasun125@gmail.com"
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
    server.login("stockly125@gmail.com", "bdxvxwvwbxppqaek")
    server.send_message(msg)
    server.quit()
    print("Successfully sent a reference request")


def send_email_confirmation(name,cpm,auth2,email):
    msg = EmailMessage()

    msg.set_content("""


    Dear {name}

    Thank you for using this service.
    Please click following link to confirm your email address and for further processings.

                link : http://127.0.0.1:5000/auth_dd/{cpm}/{auth2}

    Thank you and Best Regards
    Reference management System

                            
    """.format(name=name, cpm=cpm, auth2=auth2))

    msg['Subject'] = 'Confirm your email address'
    msg['From'] = "stockly125@gmail.com"
    msg['To'] = "dinugakasun125@gmail.com"#email
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
    server.login("stockly125@gmail.com", "bdxvxwvwbxppqaek")
    server.send_message(msg)
    server.quit()
    print("Successfully sent a email confirmation email")


def process_texts(text):
    if "\n" or "\r" in text:
        text = text.replace("\r", "")
        text = text.split("\n")
        text = ", ".join(text)
        return(text)
    elif "," in text:
        return (text)

def send_final_pdf_to_user(name,cpm,email,location):
    msg = EmailMessage()
    attachment_path = location
    attachment_filename = cpm+'.pdf'
    mime_type, _ = mimetypes.guess_type(attachment_path)
    mime_type, mime_subtype = mime_type.split('/', 1)
    
    

    msg.set_content("""


    Dear {name}

    Thank you for using this service.
    Please find the attach document you requested.
    Wish you all the very best for your future endeavours!             

                

    Thank you and Best Regards
    Reference management System

                            
    """.format(name=name))
    with open("static\pdf\{cpm}.pdf".format(cpm=cpm), 'rb') as ap:
        msg.add_attachment(ap.read(), maintype=mime_type, subtype=mime_subtype,
                           filename=os.path.basename(attachment_path))

    msg['Subject'] = 'Reference Mgt System - Your letter'
    msg['From'] = "stockly125@gmail.com"
    msg['To'] = "dinugakasun125@gmail.com"#email
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
    server.login("stockly125@gmail.com", "bdxvxwvwbxppqaek")
    server.send_message(msg)
    server.quit()
    print("Successfully sent the pdf email")
