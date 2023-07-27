import smtplib
from email.message import EmailMessage
import ssl
import random

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
    
    In order to process the request please click following link or please login to the admin panel.
                link : http://127.0.0.1:5000/auth/{type}/web/{cpm}

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

