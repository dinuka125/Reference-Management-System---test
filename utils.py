import smtplib
from email.message import EmailMessage
import ssl
import random
import mimetypes
import os 
from db import *


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
               click here to see user info - http://127.0.0.1:5000/user/{type}/web/{cpm}     

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




def show_user_data(type,cpm):
    user_details = {}

    out = get_user_data(cpm)
    cpm = out[0][0]
    mc = out[0][1]
    nic = out[0][2]
    name = out[0][3]
    dob = out[0][4]
    email = out[0][5]
    phone = out[0][6]

    if type == "to_whome_it":
        out2 = fetch_data_requests_to_whome_it(cpm)
        
        if len(out2) >1:
            valid_out = out2[-1]
        else:
            valid_out = out2[0]

        positions = process_texts(valid_out[1])
        contributions = process_texts(valid_out[2])
        summary = valid_out[3]

        user_details.update({"CPM":cpm, "MC":mc, "NIC":nic, "Name":name, "DOB" : dob, "Email":email, "Phone":phone, "Requested Letter type":type, "S@it Positions":positions, "Contributions":contributions,"Other details":summary})

        return user_details
    
    elif type == "Reference_for_higher_studies":
        out2 = fetch_data_requests_higher_studies(cpm)

        if len(out2) >1:
            valid_out = out2[-1]
        else:
            valid_out = out2[0]


        university = valid_out[1]
        degree = valid_out[2]
        year = valid_out[3]
        other_details = valid_out[4]

        user_details.update({"CPM":cpm, "MC":mc, "NIC":nic, "Name":name, "DOB" : dob, "Email":email, "Phone":phone,"Requested Letter type":type, "University Applying For":university, "Degree Applying For":degree, "Year":year, "Other Details":other_details})

        return user_details
    
    elif type == "Reference_for_employement":
        out2 = fetch_data_requests_ref_emp(cpm)

        if len(out2) >1:
            valid_out = out2[-1]
        else:
            valid_out = out2[0]

        company = valid_out[1]
        job_title = valid_out[2]
        activities_at_uni = process_texts(valid_out[3])

        user_details.update({"CPM":cpm, "MC":mc, "NIC":nic, "Name":name, "DOB" : dob, "Email":email, "Phone":phone,"Requested Letter type":type, "Company Applying For":company,"Job Title":job_title,"Activities at Uni":activities_at_uni})

        return user_details
    
    elif type == "A_letter_of_support_for_Visa_Purposes":
        out2 = fetch_data_requests_L_visa(cpm)

        if len(out2) >1:
            valid_out = out2[-1]
        else:
            valid_out = out2[0]

        country = valid_out[1]
        reason = valid_out[2]
        activities = process_texts(valid_out[3])

        user_details.update({"CPM":cpm, "MC":mc, "NIC":nic, "Name":name, "DOB" : dob, "Email":email, "Phone":phone,"Requested Letter type":type, "Country":country, "Reason":reason, "Other Details":activities})

        return user_details
    
    elif type == "other":
        out2 = fetch_data_requests_other(cpm)

        if len(out2) >1:
            valid_out = out2[-1]
        else:
            valid_out = out2[0]

        reason = valid_out[1]
        summary = valid_out[2]

        user_details.extend({"CPM":cpm, "MC":mc, "NIC":nic, "Name":name, "DOB" : dob, "Email":email, "Phone":phone,"Requested Letter type":type,"Reason":reason, "Other-details":summary})

        return user_details




        

