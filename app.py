from flask import Flask,render_template,request,flash
from email_validator import check
from utils import send_email_confirmation, send_reference_request 
from db import initiate_db, fetch_data, insert_data_requests, fetch_data_requests
from gpt_utils import generate_letter
from pdf_utils import hello
from utils import gen_confirm_code
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
        global cpm
        global mc
        global nic

        cpm = request.form.get("cpm")
        mc = request.form.get("mc")
        nic = request.form.get("nic")
        

        initiate_db()
        out = fetch_data(cpm, mc, nic)
        if not out:
            flash("Your data doesn't match")
            return render_template('index.html')
        else:
            return render_template("next.html")

    return render_template('index.html')



@app.route('/email', methods = ['POST'])
def contact_info():
    if request.method == "POST":
        global email
        global phone_no

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

        
    



@app.route('/type_of_letter', methods = ["POST"])
def type_of_letter():
    if request.method == "POST":
        type_of_letter = request.form.get("radio")

        if type_of_letter == "to_whome_it":
            return render_template("to_whome.html")
        
        if type_of_letter == "reference":
            return render_template("reference.html")
        
        if type_of_letter == "other":
            return render_template("other.html")
        
      


@app.route('/letter_to_whome_it', methods = ["GET", "POST"])
def letter_to_whome_it():
    if request.method == "POST":
        summary_by_user = request.form.get("text")

        send_reference_request(cpm, mc, "to_whome_it")
        out = fetch_data_2(cpm)
        
        if out:
            print(out[0][3])
            insert_data_requests(cpm = cpm, mc= mc, nic = nic, name = out[0][3], dob = out[0][4], email = email, phone = phone_no, type= "to_whome_it", remarks = summary_by_user)

    return render_template("letter_to_whome_success.html")


@app.route('/reference', methods = ["GET", "POST"])
def reference():
    if request.method == "POST":
        university = request.form.get("uni")
        degree = request.form.get("degree")
        year = request.form.get("year")
        other_details = request.form.get("text")

        send_reference_request(cpm, mc, "reference")
        out = fetch_data_2(cpm)
        
        if out:
            print(out[0][3])
            insert_data_requests(cpm = cpm, mc= mc, nic = nic, name = out[0][3],
                                  dob = out[0][4], email = email, phone = phone_no,
                                    type= "reference", university= university, degree = degree, year = year, other_details = other_details)

    return render_template("letter_to_whome_success.html")


@app.route('/letter_to_other', methods = ["GET", "POST"])
def letter_other():
    if request.method == "POST":
        reason = request.form.get("reason")
        summary = request.form.get("text")
        

        send_reference_request(cpm, mc, "other")
        out = fetch_data_2(cpm)
        
        if out:
            print(out[0][3])
            insert_data_requests(cpm = cpm, mc= mc, nic = nic, name = out[0][3],
                                  dob = out[0][4], email = email, phone = phone_no,
                                    type= "other", reason=reason, summary=summary)

    return render_template("letter_to_other_success.html")

@app.route("/type_of_letter")
def type_of_letter_show():
    return render_template("type_of_letter.html")

@app.route('/auth_dd/<cpm>/<auth2>')
def auth_dd(cpm,auth2):
    send_to_db_auth2(cpm,auth2)
    
    out = fetch_auth_data(cpm)
    if out:
        if (out[0][1]) == (out[0][1]):
            return render_template("email_verified.html")
        return "Error with confirmation, Please Try again later"

 
    


@app.route('/auth/<type>/<sender>/<cpm>', methods=["GET"])
def auth(type,sender,cpm):
    if type == "to_whome_it":
        out = fetch_data_requests(cpm)
        print("this is the out of to whom it may concern", out)
        if out:
            cpm = out[0][0]
            mc = out[0][1]
            name = out[0][3]
            remarks = out[0][8]

        #processing core functions should goes here
            prompt = """Can you write a brief to whome it may concern type of 
            letter using followig information ? 'I'm {name}, {remarks} '""".format(name=name, remarks=remarks)

            out = generate_letter(prompt)
            print(out)

        if sender == "web":
            return render_template("edit_letter.html", letter = out)
        
        if sender == "admin":
            return True

    if type == "reference":
        out = fetch_data_requests(cpm)

        if out:
            cpm = out[0][0]
            name = out[0][3]
            university = out[0][9]
            year = out[0][11]

            prompt = """Can you write a brief reference for higher studies email for me
            using following infomration ? 'I'm {name}, and I'm hoping to apply for higher studies in{university} for {year} '""".format(name=name, university=university, year=year)

            out = generate_letter(prompt)
            print(out)

        if sender == "web":
            return render_template("edit_letter.html", letter = out)
        
        if sender == "admin":
            return True
        
    if type == "other":
        out = fetch_data_requests(cpm)
        if out :
            name = out[0][3]
            reason = out[0][13]

            prompt =""" Can you write a brief letter regarding the matter of {reason} and please generate only the letter body""".format(reason=reason)

            out = generate_letter(prompt)
            print(out)
        #processing core functions should goes here
                    #return render_template("edit_letter.html", letter = out)
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