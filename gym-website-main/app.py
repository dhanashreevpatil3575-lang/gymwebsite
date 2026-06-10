from flask import Flask, render_template, request
from pymongo import MongoClient
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# ================= MONGODB =================
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["gym_database"]
    collection = db["members"]
except:
    collection = None


# ================= ROUTES =================

# HOME
@app.route('/')
def home():
    return render_template('index.html')


# GALLERY
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


# FORM
@app.route('/form')
def form():
    return render_template('form.html')


# ================= SUBMIT =================
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    user_email = request.form['email']
    phone = request.form['phone']
    plan = request.form['plan']

    # ✅ SAVE TO MONGODB (FIXED)
    if collection is not None:
        try:
            collection.insert_one({
                "name": name,
                "email": user_email,
                "phone": phone,
                "plan": plan
            })
        except:
            pass

    # ================= EMAIL SENDING =================
    try:
        sender_email = "dhanashreevpatil3575@gmail.com"      # 🔴 CHANGE THIS
        app_password = "qvurmsrshflynhes"        # 🔴 CHANGE THIS

        subject = "Welcome to PowerFit Gym 💪"

        body = f"""
Dear {name},

Congratulations and welcome to PowerFit Gym!

We are absolutely thrilled to have you join our fitness community. 
Your decision to begin this journey shows commitment, strength, and determination.

Your Selected Plan: {plan}

At PowerFit Gym, we are dedicated to helping you achieve your goals 
with the best equipment, guidance, and motivation.

Remember:
"Success starts with self-discipline."

We look forward to seeing your transformation!

Best Regards,  
PowerFit Gym Team
"""

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = user_email

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()

    except Exception as e:
        print("Email error:", e)

    return render_template('success.html', name=name)


# ================= RUN =================
if __name__ == '__main__':
    app.run(debug=True)