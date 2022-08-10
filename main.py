import base64
from flask import *
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Pv831842@",
    database="users"
)

mycursor = db.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS users")


app = Flask(__name__)


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
            sqLogin = "SELECT * FROM loginData WHERE login = '" + username + "' AND senha = '" + password + "'"
            mycursor.execute(sqLogin)
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
        mycursor.execute("SELECT * FROM loginData WHERE login = '" + username + "'")
        if mycursor.fetchone():
            return render_template("register.html", existe=True)

        sql = """INSERT INTO loginInfo(
        login, senha)
        VALUES ('%s', '%s')""" % (username, password)
        mycursor.execute(sql)
        db.commit()
        res = make_response(render_template("register.html", login=True))
        res.set_cookie("login", base64.b64encode(username.encode('ascii')))
        return res
    return render_template('register.html')


@app.route("/calc")
def calc():
    return render_template("calc.html")


@app.route("/edit", methods=["GET", "POST"])
def editdiario():
    mycursor.execute("SELECT * FROM posts")
    posts = mycursor.fetchall()
    print(posts)
    return render_template("editdiario.html", aaaa=posts)


@app.route("/addPost", methods=["POST", "GET"])
def addPost():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        mycursor.execute("INSERT INTO posts(title, content) VALUES ('" + title + "', '" + content + "')")
        db.commit()
        return render_template("editdiario.html")
    return render_template("addPost.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
    app.run()