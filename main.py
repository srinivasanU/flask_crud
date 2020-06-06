from flask import Flask, render_template, request , redirect , url_for
from db import dbconnection
from conversion import get_dict_resultset
import pandas as pd

conn = dbconnection()
cur = conn.cursor()
 
app = Flask(__name__)
 
@app.route('/contacts', methods=['GET','POST'])
@app.route('/contacts/<method>/<contact_id>', methods=['GET'])
def contacts(contact_id=None,method=None):
    contact_id = contact_id or ''
    method = method or ''
    if (contact_id == ''):
        if (request.method == 'GET'):
            sql = "select * from contacts";
            contacts = get_dict_resultset(sql)
            return render_template('contacts.html',contacts=contacts)
        elif (request.method == 'POST'):
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            phone_no = request.form['phone_no']
            cur.execute("insert into contacts (firstname,lastname,phone_no) values(%s,%s,%s)",(firstname,lastname,phone_no));
            conn.commit()
            return redirect(url_for('contacts'))
        else:
            return redirect(url_for('contacts'))        
    else:
        if (method == 'edit'):
            sql = "select * from contacts";
            contacts = get_dict_resultset(sql)
            for i in contacts:
                if int(contact_id) == int(i['contact_id']):
                    contact = i
            return render_template('contacts.html',contacts=contacts,contact=contact)
        elif (method == 'delete'):
            cur.execute("DELETE FROM contacts WHERE contact_id = " + contact_id);
            conn.commit();
            return redirect(url_for('contacts'))
        else:
            return redirect(url_for('contacts'))
        return redirect(url_for('contacts'))

@app.route('/contacts/update', methods=['POST'])
def update_contacts():
    firstname = request.form['updatefirstname']
    lastname = request.form['updatelastname']
    phone_no = request.form['updatephone_no']
    contact_id = request.form['contact_id']
    cur.execute("update contacts SET firstname = %s , lastname = %s , phone_no = %s  WHERE contact_id = %s" , (firstname,lastname,phone_no,contact_id));
    conn.commit();
    return redirect(url_for('contacts'))  

@app.route('/contacts/export', methods=['GET','POST'])
def export_data():
    sql = "select firstname,lastname,phone_no from contacts";
    contacts = get_dict_resultset(sql)
    df = pd.DataFrame(contacts)
    df.to_excel (r'exportdbdata.xlsx', index = False, header=True) 
    return redirect(url_for('contacts'))

@app.route('/contacts/import', methods=['GET','POST'])
def import_data():
    filedata = request.form['importexcel']
    re = pd.read_excel(str(filedata), sheet_name='Sheet1')
    final_res = re.to_dict('records')
    for row in final_res:
        cur.execute("insert into contacts (lastname,phone_no,firstname) values(%s,%s,%s)",(str(row['lastname']),str(row['phone_no']),str(row['firstname'])));
    conn.commit()
    return redirect(url_for('contacts'))

        
if __name__ == '__main__':
    app.run()