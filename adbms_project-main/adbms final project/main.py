#flask components
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

#db components
import psycopg2
#mail components
import smtplib
from email.message import EmailMessage
#sms components
from twilio.rest import Client
#relative components
from references import db_password
from references import admin_email,admin_password
from references import account_sid,auth_token,from_phone
#other components
import math
import random


client=Client(account_sid,auth_token)
app=Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errorpage.html'),404

@app.route('/')
def landing_page():
    return render_template('home.html')
@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/stack')
def stack_page():
    return render_template('stack_page.html')
@app.route('/loginpage',methods=["POST","GET"])
def login_page():
    global true_password
    global input_password
    global input_password

    if request.method=='POST':
        try:
            input_username=request.form['username']
            input_password=request.form['user_password']

            true_password=check_credentials(input_username,input_password)

            #if check_username(input_username)==True:


            if input_password==true_password:
                    return 'Success'
            else:

                return render_template('errormessage.html',error='Entered Username Or Password was incorrect, Please try again.')
        except:
            return render_template('errormessage.html',error='Entered Username Or Password was incorrect, Please try again.')

    return render_template('login-page.html')

@app.route('/signuppage',methods=["POST","GET"])
def signup_page():
    if request.method=='POST':
        try:

            user_name=request.form['user_name']
            user_username=request.form['user_username']
            user_email=request.form['user_email']
            user_phone=request.form['user_phone']
            user_date_of_birth=request.form['user_date_of_birth']
            user_password=request.form['user_password']
            user_re_password=request.form['user_re_password']












            if user_password==user_re_password:

                create_new_account(user_name,user_username,user_email,user_phone,user_date_of_birth)
                create_new_account_1(user_username,user_password)

                return render_template('login-page.html')#message:account created successfully


            else:
               return render_template('signup-page.html')
        except:

            return render_template('errormessage.html',error='Username/Phone number/Email are already linked to an existing account!')


    return render_template('signup-page.html')

@app.route('/emailotp',methods=["POST","GET"])
def reset_password_email():
    global username
    if request.method=="POST":
        try:
            user_email=request.form['user_email']
            username=get_username_from_email(user_email)
            send_mail(username,user_email,admin_email,admin_password)
            return redirect('/otpverification')
        except:
            return render_template('errormessage.html',error='The email id entered is not linked to any account , Please try again!')
    return render_template('email_otp.html')

@app.route('/otpverification',methods=["POST","GET"])
def check_otp():
    if request.method=='POST':
        try:
            input_otp=request.form['user_otp']
            if str(otp)==str(input_otp):
                return redirect('/resetpassword')
            else:
                return render_template('errormessage.html',error='The OTP you entered was incorrect,Please try again!')
        except:
            return render_template('errormessage.html',error='Some Error Occured While Creating A new Account , Please Try Again!')

    return render_template('check_otp.html')


@app.route('/phoneotp',methods=["POST","GET"])
def reset_password_phone():
    global username
    if request.method=='POST':
        try:
            user_phone_number=request.form['user_phone']
            username=get_username_from_phone(user_phone_number)#make case for username exist/ not exist
            if check_username(username)==True:
                send_sms(user_phone_number,from_phone)
            else:
                return render_template('errormessage.html',error='The Phone number you entered is not linked to an account!')


            return redirect('/otpverification')
        except:
            return render_template('errormessage.html',error='The Phone number you entered is not linked to an account!')

    return render_template('sms_otp.html')

@app.route('/resetpassword',methods=["POST","GET"])
def change_password():
    if request.method=="POST":
        try:
            entered_password=request.form['user_password_1']
            re_entered_password=request.form['user_password_2']

            if entered_password==re_entered_password:
                change_password(username,entered_password)      #message:password changed successfully
                return redirect('/loginpage')
            else:
                return render_template('errormessage.html',error='Passwords Didnt Match , Try Again')  #message:Some error occurred , try again.
        except:
            return render_template('errormessage.html',error='Some Error Occured,Please Try Again!')


    return render_template('reset_password.html')

@app.route('/test',methods=["POST","GET"])
def test1():
    return true_password


def check_credentials_phone_email_userame():
    pass

def create_new_account(user_name,user_username,user_email,user_phone,user_date_of_birth):
    conn=psycopg2.connect("dbname=sample1 user=postgres password={}".format(db_password))
    curr=conn.cursor()
    curr.execute("INSERT INTO sample_data_4 VALUES('{}','{}','{}','{}','{}')".format(user_name,user_username,user_email,user_phone,user_date_of_birth))
    conn.commit()
    curr.close()
    conn.close()

def create_new_account_1(user_username,user_password):
    conn=psycopg2.connect("dbname=sample1 user=postgres password={}".format(db_password))
    curr=conn.cursor()
    curr.execute("INSERT INTO sample_data_6 VALUES('{}','{}')".format(user_username,user_password))
    conn.commit()
    curr.close()
    conn.close()

def generate_otp():
    global otp
    otp=random.randint(10000,100000)
    return otp

def send_sms(user_phone_number,from_phone):
    phone_num='+91'+str(user_phone_number)
    otp=generate_otp()
    msg='Your One Time Password(OTP) for resetting your password is:'+str(otp)+' Do not share this code! Contact our team if this request was not made by you'
    message=client.messages \
             .create(
                 body=msg,
                 from_=str(from_phone),
                 status_callback='http://postb.in/1234abcd', #you can use this too maybe(?)
                 to=str(phone_num)
                 )

def send_mail(username,user_email,admin_email,admin_password):
    msg=EmailMessage()
    msg['Subject']='Reset Password'
    msg['To']=user_email
    msg['From']=admin_email
    otp=generate_otp()
    content="Dear {}, \nAs per your request , your otp is {}. Do Not Share this with anyone.\nIf this request wasn't made by you let our team know.".format(username,otp)
    msg.set_content(content)

    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(admin_email,admin_password)
        smtp.send_message(msg)

def check_username(username):
    conn=psycopg2.connect("dbname=sample1 user=postgres password={}".format(db_password))
    curr=conn.cursor()
    curr.execute("SELECT * FROM sample_data_6 WHERE username='{}'".format(username))
    true_username_1=curr.fetchone()[0]
    conn.commit()
    curr.close()
    conn.close()

    if username==true_username_1:
        return True
    else:
        return False

def get_username_from_email(user_email):
    conn=psycopg2.connect("dbname=sample1 user=postgres password={}".format(db_password))
    curr=conn.cursor()
    curr.execute("SELECT username from sample_data_4 WHERE user_email='{}'".format(user_email))
    true_username=curr.fetchone()[0]
    conn.commit()
    curr.close()
    conn.close()

    return true_username

def get_username_from_phone(user_phone):
    conn=psycopg2.connect("dbname=sample1 user=postgres password='{}'".format(db_password))
    curr=conn.cursor()
    curr.execute("SELECT username from sample_data_4 WHERE user_phone='{}'".format(user_phone))
    true_username=curr.fetchone()[0]
    conn.commit()
    curr.close()
    conn.close()

    return true_username

def change_password(username,new_password):
    conn=psycopg2.connect("dbname=sample1 user=postgres password={}".format(db_password))
    curr=conn.cursor()

    curr.execute("UPDATE sample_data_6 SET rawpass='{}' WHERE username='{}'".format(new_password,username))
    conn.commit()
    curr.close()
    conn.close()

def check_credentials(username,password):
    conn=psycopg2.connect("dbname=sample1 user=postgres password={}".format(db_password))
    curr=conn.cursor()

    curr.execute("SELECT rawpass from sample_data_6 WHERE username='{}'".format(username))
    true_password=curr.fetchone()[0]
    conn.commit()
    curr.close()
    conn.close()

    return true_password
