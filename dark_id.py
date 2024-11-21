from tinydb import TinyDB,Query
from flask import Flask,request,render_template,jsonify

dark_db = TinyDB('dark_db.json')
dark_table = dark_db.table('Ids')
User = Query()

db = TinyDB('messages.json')  # TinyDB database
m_table = db.table('Messages')
qmessage =Query()

# Function to send message
def send_message(sender_name, phone_email, message, m_id, uid):
    m_table.insert({'m_id':m_id, 'sender_name': sender_name, 'phone_email': phone_email, 'message': message,'uid':uid})


def add_user(user_name,user_pass,full_name,user_dob,user_gender,fathers_name,user_address,pin_code,user_unique_id,user_email,user_phone,user_adhar,user_pan):
    dark_table.insert({'user_unique_id': user_unique_id,'user_name':user_name,'user_pass':user_pass,'full_name':full_name,'user_dob':user_dob,'user_gender':user_gender,'fathers_name':fathers_name,'user_address':user_address,'pin_code':pin_code,'user_email':user_email,'user_phone':user_phone,'user_adhar':user_adhar,'user_pan':user_pan})


def unique_id_fetch(user_name,user_pass):
    if dark_table.search((User.user_name == user_name) & (User.user_pass == user_pass)):
        t_user = dark_table.get((User.user_name == user_name) & (User.user_pass == user_pass))
        uid = t_user['user_unique_id']
        return uid
    else:
        return False
    
def m_id():
    all = m_table.all()
    m_id = 100 + len(all)  # Initial m_id set kar rahe hain

    # Jab tak m_id duplicate hai, 1000 add karte rahenge
    while m_table.get(qmessage.m_id == m_id):
        m_id += 1000

    return m_id

def unique_id_gen():
    c_users = len(dark_table.all())
    return int(c_users)+10000000

def email_gen(user_name):
    return user_name+'@dmail.com'
def ph_gen():
    c_users = len(dark_table.all())
    return int(c_users)+7479549608
def adhar_gen():
    c_users = len(dark_table.all())
    return int(c_users)+438789302384
def pan_gen():
    c_users = len(dark_table.all())
    pre = str(int(c_users)+1000)
    mid = 'DARKP'
    pos = 'S'
    return mid+pre+pos

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/submit_signup',methods = ['POST'])
def submit_singup():
    if request.method=='POST':
        user_name = request.form['username']
        user_pass = request.form['password']
        full_name = request.form['full_name']
        user_dob = request.form['dob']
        user_gender = request.form['gender']
        fathers_name = request.form['fathers_name']
        user_address = request.form['address']
        pin_code = request.form['pin_code']
        user_unique_id = unique_id_gen()
        if dark_table.search(User.user_name == user_name):
            return render_template('/submit_signup_fail.html')
        else:
            add_user(user_name,user_pass,full_name,user_dob,user_gender,fathers_name,user_address,pin_code,user_unique_id,email_gen(user_name),ph_gen(),adhar_gen(),pan_gen())
            send_message('DARK WORLD','PHONE+MAIL','Hey '+user_name+' Welcome TO The World Of DARK IDS \n\n\n\n\n'+'Have a Nice Day...       Greeting From Dark Ranjan,Thank You',m_id(),user_unique_id)
            return render_template('/submit_signup.html')
    return render_template('signup.html')

        

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/submit_login',methods = ['POST'])
def submit_login():
    if request.method == 'POST':
        user_name = request.form['username']
        user_pass = request.form['password']
        uid = unique_id_fetch(user_name,user_pass)
        if uid:
            return render_template('login_pass.html',uid = uid)
        else:
            return render_template('login_fail.html')
        

@app.route('/user_profile',methods = ['POST'])
def user_profile():
    if request.method == 'POST':
        try :
            uid = request.form['uid']
            user = dark_table.get(User.user_unique_id == int(uid))
            return render_template('user_profile.html',user = user)
        except :
            return render_template('login.html')
    

@app.route('/message_inbox',methods = ['POST'])
def message_inbox():
    if request.method == 'POST':
        uid = request.form['uid']
        print(uid)
        user = dark_table.all()
        messages = m_table.search(qmessage.uid == int(uid))
        print(messages)
        return render_template('message_inbox.html', messages=messages,users =user,uid = uid)

@app.route('/message_delete',methods = ['POST'])
def message_delete():
    if request.method=='POST':
        m_id = request.form['m_id']
        confirm = request.form['del_btn']
        uid = request.form['uid']
        messages = m_table.search(qmessage.uid == int(uid))
        if confirm == 'yes':
            # mess = m_table.get(message.m_id == str(m_id()))
            print(m_id)
            m_table.remove(qmessage.m_id == int(m_id))
            return render_template('message_delete.html',uid = uid)
        return render_template('message_inbox.html',messages = messages)

    return render_template('message_delete.html')




@app.route('/sender', methods = ['GET','POST'])
def sender():
    if request.method == 'POST':
        sender_name = request.form['sender_name']
        phone_email = request.form['phone_email']
        message = request.form['message']
        send_message(sender_name, phone_email, message, m_id(),unique_id_gen()-1)
    return render_template('sender.html')


@app.route('/sent_message', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        reciever_phone = request.form['phone']
        sender_id = request.form['s_uid']
        Message = request.form['sent_text']
        print(reciever_phone)
        print(type(reciever_phone))
        # Process the data or save it
        user = dark_table.get(User.user_phone == int(reciever_phone))
        s_user = dark_table.get(User.user_unique_id == int(sender_id))
        uid = user['user_unique_id']
        send_message(s_user['full_name'], 'phone+email', Message, m_id(), uid)
        return jsonify({"message": "Form submitted successfully!", "username": reciever_phone ,'Message':Message,'sender': sender_id})



#API-OTP CONNECTION 
@app.route('/data', methods=['GET'])
def handle_data():
    try:
        # Query parameters ko get karte hain
        param1 = int(request.args.get('ph'))  # Pehla data
        param2 = int(request.args.get('auth'))  # Dusra data

        # Response return karte hain
        print(param2)
        print(type(param2))
        return f"Received Param1: {param1}, Param2: {param2}"
    except:
        return f"Something went Wrong....Please Go Back And Try Again Later...."


if __name__=='__main__':
    app.run(debug=True,port=5200)