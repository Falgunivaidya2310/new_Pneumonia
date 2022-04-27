from flask import Flask, render_template, request, flash, redirect, url_for, session
import sqlite3


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "123"

con = sqlite3.connect("database1.db")
con.execute("create table if not exists doctors(pid integer primary key, name text, address text, contact integer, mail text)")
con.close()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/login')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name=request.form['name']
        password=request.form['password']
        con = sqlite3.connect("database.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from doctors where name=? and mail=?", (name,password))
        data = cur.fetchone()

        if data:
            session["name"] = data["name"]
            session["mail"] = data["mail"]
            return redirect("patient")

        else:
            flash("Username and password mismatched", "danger")
    return redirect(url_for("index"))

@app.route('/patient', methods=['GET', 'POST'])
def patient():
    return render_template("patient.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            name=request.form['name']
            address=request.form['address']
            contact = request.form['contact']
            mail = request.form['mail']
            con = sqlite3.connect("database1.db")
            cur = con.cursor()
            cur.execute("insert into doctors(name,address,contact,mail) values(?,?,?,?)", (name,address,contact,mail))
            con.commit()
            flash("Record Added Successfully", "success")

        except:
            flash("Something went wrong, please check your credentials again!!", "danger")

        finally:
            return redirect(url_for("index"))
            con.close()

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("main"))

if __name__ == '__main__':
    app.run(debug=True)