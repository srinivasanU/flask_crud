import psycopg2
from db import dbconnection
from conversion import get_dict_resultset
import sys 

conn = dbconnection()
cur = conn.cursor()

Option_list = ['Option 1 . Add', 'Option 2 . Update', 'Option 3 . List','Option 4 . Delete', 'Option 5 . Exit']

def looper():
    for i in Option_list:
        print i
    print '#######################################';
    input_option = input ("Enter a Option Number: ");
    options(int(input_option))

def create_option():
    firstname = raw_input("Enter the Firstname : ")
    lastname = raw_input("Enter the Lastname : ")
    phone_no = raw_input("Enter the Phone Number : ")
    cur.execute("insert into contacts (firstname,lastname,phone_no) values(%s,%s,%s)",(firstname,lastname,phone_no));
    conn.commit()
    print '#######################################';
    print 'Contact Created succesfully'
    print '#######################################';
    calling_loop = looper()

def update_option():
    contact_id = raw_input("Enter the Contact ID : ")
    firstname = raw_input("Enter the Firstname : ")
    lastname = raw_input("Enter the Lastname : ")
    phone_no = raw_input("Enter the Phone Number : ")
    cur.execute("update contacts SET firstname = %s , lastname = %s , phone_no = %s  WHERE contact_id = %s" , (firstname,lastname,phone_no,contact_id));
    conn.commit();
    print '#######################################';
    print 'Contact Updated succesfully'
    print '#######################################';
    calling_loop = looper()

def list_option():
    sql = "select * from contacts";
    ans = get_dict_resultset(sql)
    print '#######################################';
    print 'Contacts Retrieved succesfully'
    print '#######################################';
    print ans;
    print '#######################################';
    calling_loop = looper()

def delete_option():
    contact_id = raw_input("Enter the Contact ID : ")
    cur.execute("DELETE FROM contacts WHERE contact_id = %s" , (contact_id));
    conn.commit();
    print '#######################################';
    print 'Contact Deleted succesfully'
    print '#######################################';
    calling_loop = looper()

def exit_option():
    print 'Thanks for using this CRUD'
    sys.exit()

def options(option):
    if option == 1:
        print 'Create'
        create = create_option()
    elif option == 2:
        print 'Update'
        update = update_option()
    elif option == 3:
        print 'List'
        list = list_option()
    elif option == 4:
        print 'Delete'
        delete = delete_option()
    elif option == 5:
        print 'Exit'
        exiting_script1 = exit_option()
    else:
        print 'Exit'
        exiting_script2 = exit_option()

call_loop = looper()