import base64
import os
from flask import *
import mysql.connector
from OpenSSL import SSL


# context = SSL.Context(SSL.TLSv1_2_METHOD)
# context.use_certificate_file('/home/opc/acme.sh/_certs_/verissimos.ddnsfree.com/verissimos.ddnsfree.com.cer')
# context.use_privatekey_file('/home/opc/acme.sh/_certs_/verissimos.ddnsfree.com/verissimos.ddnsfree.com.key')



db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Pv831842",
    database="users",
    auth_plugin='mysql_native_password'
)

mycursor = db.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS users")


app = Flask(__name__, static_url_path="/static")
@app.route('/', methods=['GET'])
def home():
    return render_template("homepage.html")


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not len(password) == 0:
            sqLogin = f"SELECT * FROM loginData WHERE login = '{username}' AND senha = '{password}'"
            mycursor.execute(sqLogin)
            print(mycursor)
            a = mycursor.fetchall()
            if a:
                res = make_response(redirect(url_for("home")))
                res.set_cookie("login", base64.b64encode(username.encode('ascii')))
                
                return res

        else:
            return render_template("login.html", len=False)

        return render_template('login.html', no=True)

    return render_template('login.html')


@app.route("/logado")
def logado():
    return render_template("logado.html")

@app.route('/register', methods=["GET", 'POST'])
def register():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form['password']
        mycursor.execute(f"SELECT * FROM loginData WHERE login = '{username}'")
        if mycursor.fetchone():
            return render_template("register.html", existe=True)

        sql = f"INSERT INTO loginData(login, senha) VALUES ('{username}', '{password}')"
        mycursor.execute(sql)
        db.commit()
        res = make_response(render_template("register.html", login=True))
        res.set_cookie("login", base64.b64encode(username.encode('ascii')))
        return res
    return render_template('register.html')


# calculadora
@app.route("/calc")
def calc():
    return render_template("calc.html")


@app.route("/edit", methods=["GET", "POST"])
def editdiario():
    mycursor.execute("SELECT * FROM posts")
    posts = mycursor.fetchall()
    print(posts)
    return render_template("editdiario.html", posts=posts)

@app.route("/verDiario")
def verDiario():
    mycursor.execute("SELECT * FROM posts")
    posts = mycursor.fetchall()
    print(posts)
    return render_template("verDiario.html", posts=posts)


@app.route("/addPost", methods=["POST", "GET"])
def addPost():
    if request.method == "GET":
        return render_template("addPost.html")
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        if len(title) == 0 or len(content) == 0:
            return render_template("addPost.html", len=0)
        else:
            if len(content) < 65.535:
                mycursor.execute("INSERT INTO posts(title, content) VALUES ('" + title + "', '" + content + "')")
                db.commit()
            else:
                return render_template("addPost.html", len=1)
            return render_template("addPost.html")
    return render_template("addPost.html")


@app.route("/verPerfil")
def verPerfil():
    return render_template("verPerfil.html")
    
# remove o post
@app.route("/remove/<id>")
def removePost(id):
    mycursor.execute("DELETE FROM posts WHERE postId = " + id)
    db.commit()
    return redirect(url_for("editdiario"))


@app.route("/editarPerfil", methods=["GET", "POST"])
def editarPerfil():
    if request.method == "GET":
        return render_template("editarPerfil.html", edit=None)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if len(password) == 0:
            return render_template("editarPerfil.html", len=0)
        else:
            mycursor.execute("UPDATE loginData SET senha = '" + password + "' WHERE login = '" + username + "'")
            db.commit()
            return render_template("editarPerfil.html")
    return render_template("editarPerfil.html")


@app.route("/welcome", methods=["GET"])
def welcome(id):
    argum = request.args
    return render_template("welcome.html",id=argum)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
