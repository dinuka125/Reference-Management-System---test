from flask import Flask,render_template,request,flash
from email_validator import check
from utils import send_email_confirmation, send_reference_request 
from db import * #initiate_db, fetch_data, fetch_data_requests, insert_data_L_to_whome, fetch_auto,insert_data_L_higher_studies, insert_ref_emp,insert_data_L_visa,insert_data_L_other
from gpt_utils import generate_letter
from pdf_utils import hello
from utils import gen_confirm_code, process_texts
from utils import send_email_confirmation
from db import send_to_db_auth1,send_to_db_auth2,fetch_auth_data,fetch_data_2
import re
from flask_ckeditor import CKEditor


app = Flask(__name__)
ckeditor = CKEditor(app)

app.secret_key = "abc"  

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/get', methods=['POST'])
def get_data():
    if request.method == "POST":
     

        cpm = request.form.get("cpm")
        mc = request.form.get("mc")
        nic = request.form.get("nic")
        

        initiate_db()
        out = fetch_data(cpm, mc, nic)
        if not out:
            flash("Your data doesn't match")
            return render_template('index.html')
        else:
            return render_template("next.html",cpm=cpm)

    return render_template('index.html')



@app.route('/email/<cpm>', methods = ['POST'])
def contact_info(cpm):
    if request.method == "POST":

        email = request.form.get('email')
        phone_no = request.form.get('phone_no')

        email_valid_status = check(email)

        if not email_valid_status:
            flash("Invalid Email Address")
            return render_template("next.html")
        
        else:
            code = gen_confirm_code()
            out = fetch_data_2(cpm)
            if out:
                name = out[0][3]
                send_to_db_auth1(cpm, code)
                send_email_confirmation(name,cpm,code,email) 
                return render_template("confirmation_msg.html")

        
    



@app.route('/type_of_letter/<cpm>', methods = ["POST"])
def type_of_letter(cpm):

    if request.method == "POST":
        type_of_letter = request.form.get("radio")

        if type_of_letter == "to_whome_it":
            return render_template("to_whome.html",cpm=cpm)
        
        if type_of_letter == "higher":
            return render_template("reference.html",cpm=cpm)

        if type_of_letter == "reference":
            return render_template("reference_emp.html",cpm=cpm)    
        
        if type_of_letter == "visa":
            return render_template("ref_visa.html",cpm=cpm)

        if type_of_letter == "other":
            return render_template("other.html",cpm=cpm)
        
      


@app.route('/letter_to_whome_it/<cpm>', methods = ["POST"])
def letter_to_whome_it_func(cpm):
    
    if request.method == "POST":
        positions = request.form.get("positions")
        contributions = request.form.get("contributions")
        summary_by_user = request.form.get("summary")

        send_reference_request(cpm, "to_whome_it")
        insert_data_L_to_whome(positions, contributions, summary_by_user, cpm)

    return render_template("letter_to_whome_success.html")


@app.route('/higher_studies/<cpm>', methods = ["GET", "POST"])
def higher_studies(cpm):
    if request.method == "POST":
        university = request.form.get("uni")
        degree = request.form.get("degree")
        year = request.form.get("year")
        other_details = request.form.get("text")

        send_reference_request(cpm,"Reference_for_higher_studies")
        insert_data_L_higher_studies(university, degree, year, other_details, cpm)


    return render_template("letter_to_whome_success.html")


@app.route('/ref_emp/<cpm>', methods = ["GET", "POST"])
def ref_emp(cpm):
    if request.method == "POST":
        company = request.form.get("company")
        job = request.form.get("job")
        activities_at_uni = request.form.get("activities_at_uni")

        send_reference_request(cpm,"Reference_for_employement")
        insert_ref_emp(company, job, activities_at_uni,cpm)


    return render_template("letter_to_whome_success.html")
    

@app.route('/ref_visa/<cpm>', methods = ["GET", "POST"])
def ref_visa(cpm):
    if request.method == "POST":
        country = request.form.get("country")
        reason = request.form.get("reason")
        activities_at_uni = request.form.get("activities_at_uni")
    
        send_reference_request(cpm,"A_letter_of_support_for_Visa_Purposes")
        insert_data_L_visa(country, reason, activities_at_uni, cpm)
    return render_template("letter_to_whome_success.html")        


@app.route('/letter_to_other/<cpm>', methods = ["GET", "POST"])
def letter_other(cpm):
    if request.method == "POST":
        reason = request.form.get("reason")
        summary = request.form.get("text")
        
        send_reference_request(cpm,"other")
        insert_data_L_other(reason, summary, cpm)
        
    return render_template("letter_to_other_success.html")


@app.route("/type_of_letter/<cpm>")
def type_of_letter_show(cpm):
    print("here at show",cpm)
    return render_template("type_of_letter.html", cpm=cpm)

@app.route('/auth_dd/<cpm>/<auth2>')
def auth_dd(cpm,auth2):
    send_to_db_auth2(cpm,auth2)
    
    out = fetch_auth_data(cpm)
    if out:
        if (out[0][1]) == (out[0][1]):
            return render_template("email_verified.html", cpm=cpm)
        return "Error with confirmation, Please Try again later"

 
    


@app.route('/auth/<type>/<sender>/<cpm>', methods=["GET"])
def auth(type,sender,cpm):
    if type == "to_whome_it":
        out = fetch_data_requests_to_whome_it(cpm)
        
        if len(out) >1:
            valid_out = out[-1]
        else:
            valid_out = out[0]
        
        cpm = valid_out[-1]

        positions = process_texts(valid_out[1])
        contributions = process_texts(valid_out[2])
        summary = valid_out[3]

        user_data =  get_user_data(cpm)
        if user_data:
            name = user_data[0][3]


            #prompt 
            prompt = """Can you write a brief 'to whome it may concern type of 
            letter' using followig information ? The information = "'I'm {name}, and I was a student of Department of information technology,
            Faculty of management of commerce, University of Sri Jayewardenepura. 
            During my undergrads I held these positions : {positions}, and i contributed to the department using 
            following ways : {contributions}. {remarks} " """.format(name=name, positions=positions, contributions=contributions, remarks=summary)

            out = generate_letter(prompt)
            print(out)

        if sender == "web":
            return render_template("edit_letter.html", letter = out)
        
        if sender == "admin":
            return True

    if type == "Reference_for_higher_studies":
        out = fetch_data_requests_higher_studies(cpm)

        if len(out) >1:
            valid_out = out[-1]
        else:
            valid_out = out[0]

        cpm = valid_out[-1]
        university = valid_out[1]
        degree = valid_out[2]
        year = valid_out[3]
        other_details = valid_out[4]
        
        user_data =  get_user_data(cpm)
        if user_data:
            name = user_data[0][3]

            prompt = """Can you write a brief reference for higher studies email for me
            using following infomration ? 'I'm {name}, and I'm hoping to apply for higher studies in{university} for {year} for {degree}, ' and using following 
            information {other_details}""".format(name=name, university=university, year=year, degree=degree, other_details=other_details)

            out = generate_letter(prompt)
            print(out)

        if sender == "web":
            return render_template("edit_letter.html", letter = out)
        
        if sender == "admin":
            return True

    if type == "Reference_for_employement":        
        out = fetch_data_requests_ref_emp(cpm)

        if len(out) >1:
            valid_out = out[-1]
        else:
            valid_out = out[0]

        cpm = valid_out[-1]
        company = valid_out[1]
        job_title = valid_out[2]
        activities_at_uni = process_texts(valid_out[3])

        user_data = get_user_data(cpm)
        if user_data:
            name = user_data[0][3]

            prompt = """Can you write a professional 'Reference for employement' type of letter using following information ? 
            "I'm {name}, I graduated from Department of information technology, University of Sri Jayewardenepura. I hope to apply for {company} for 
            {job_title} position, Here are some of my activities that i have done during my undergrad {activities_at_uni}    """.format(name = name, company=company, job_title = job_title,
            activities_at_uni = activities_at_uni)


            out = generate_letter(prompt)
            print(out) 

        if sender == "web":
            return render_template("edit_letter.html", letter = out)
        
        if sender == "admin":
            return True

    if type == "A_letter_of_support_for_Visa_Purposes":
        out = fetch_data_requests_L_visa(cpm)

        if len(out) >1:
            valid_out = out[-1]
        else:
            valid_out = out[0]


        cpm = valid_out[-1]
        country = valid_out[1]
        reason = valid_out[2]
        activities = process_texts(valid_out[3])

        user_data = get_user_data(cpm)
   
        if user_data:
            name = user_data[0][3]

            prompt = """  Can you write a letter of support for visa purposes using following information ?
            'I'm {name}, I graduated from Department of information technology, University of Sri Jayewardenepura. I hope to apply for visa for purpose of {reason}. 
            During my undergrad, here are my activities {activities}
            """.format(name=name, reason=reason, activities=activities)

            out = generate_letter(prompt)
            print(out)

        else:
            return "Unexpected error occured please try again later"    

        if sender == "web":
            return render_template("edit_letter.html", letter = out)
        
        if sender == "admin":
            return True


        
    if type == "other":
        out = fetch_data_requests_other(cpm)

        if len(out) >1:
            valid_out = out[-1]
        else:
            valid_out = out[0]

        cpm = valid_out[-1]
        reason = valid_out[1]
        summary = valid_out[2]

        prompt =""" Can you write a professional brief letter regarding the matter of {reason} using these information ? '{summary}'""".format(reason=reason,summary=summary)

        out = generate_letter(prompt)
        print(out)

        if sender == "web":
            return render_template("edit_letter.html", letter = out)    
        
        if sender == "admin":
            return True


@app.route('/create_pdf', methods=["POST"])
def create_pdf():
    if request.method == "POST":
        text = request.form.get("content")
        print("This is the text output from textarea and taken from api :\n",text)

        if text:
            text = text.replace("<pre>", "")
            text = text.replace("</pre>", "")

            with open("file.txt", "w") as file:
                file.writelines(text)
                file.close()

        hello() 

    return render_template("sent_pdf_file.html")




    
    
    



if __name__ == "__main__":
    app.run()