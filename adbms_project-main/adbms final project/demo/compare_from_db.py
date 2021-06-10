import psycopg2


def take_input_username():

    username=input("Enter Your Username:")
    password=input("Enter Your Password:")

    return username,password

def check_password_for_username():
    conn=psycopg2.connect("dbname=sample1 user=postgres password=qw3rtyui0p")
    curr=conn.cursor()

    username,password=take_input_username()

    curr.execute("SELECT rawpass FROM sample_data_2 WHERE username='{}'".format(username))
    true_password=curr.fetchone()[0]
    conn.commit()
    curr.close()
    conn.close()

    if password==true_password:
        print('Correct Password')
    else:
        print('Incorrect Password')



check_password_for_username()
