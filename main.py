import base64
import os
from flask import *
import mysql.connector
from werkzeug.utils import secure_filename

db = mysql.connector.connect(
    host="verissimos.ddnsfree.com",
    user="root",
    passwd="831842",
    database="website"
)

mycursor = db.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS users")


app = Flask(__name__, static_url_path="/static")
app.config['UPLOAD_FOLDER'] = "/home/ubuntu/sitewthflask/static/img"

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def home():
    return render_template("homepage.html")


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            cookie = request.cookies.get('login')
            filename = base64.b64decode(cookie).decode('utf-8') + ".png"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return ''
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <style>
        body {
            color: azure;
        }
    </style>
    <h1>Mandar foto de perfil</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Enviar>
    </form>
    '''



@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not len(password) == 0:
            sqLogin = f"SELECT login, senha FROM loginData WHERE login = '{username}' AND senha = '{password}'"
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

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


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
                mycursor.execute(f"INSERT INTO posts(title, content) VALUES ('{title}', '{content}')")
                db.commit()
            else:
                return render_template("addPost.html", len=1)
            return render_template("addPost.html")
    return render_template("addPost.html")


@app.route("/verPerfil")
def verPerfil():
    cookie = request.cookies.get('login')
    mycursor.execute(f"SELECT nomeReal from loginData WHERE login='{base64.b64decode(cookie).decode('utf-8')}'")
    for x in mycursor:
        coiso = x
	print(coiso))
    return render_template("verPerfil.html")


# remove o post
@app.route("/remove/<id>")
def removePost(id):
    mycursor.execute("DELETE FROM posts WHERE id = " + id)
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
def welcome():
    argum = request.args
    return render_template("welcome.html",id=argum)


@app.route("/uploadExcel", methods=["GET", "POST"])
def uploadExcel():
    if request.method == "GET":
        return render_template("uploadExcel.html")

@app.route("/devTest", methods=["GET", "POST"])
def devTest():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            cookie = request.cookies.get('login')
            filename = base64.b64decode(cookie).decode('utf-8') + ".png"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'foi'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
