import os
from google.auth.transport.requests import Request
import pathlib
from pip._vendor import cachecontrol
from flask import Flask, redirect, render_template, request, abort, session
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import requests
import models

app = Flask(__name__)
app.secret_key = "poltekpos"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "857345661580-238s2f7qfr5qiv58gt233ps1u732cc34.apps.googleusercontent.com"
client_secrets_file =  os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri = "http://127.0.0.1:5000/callback"
    )

@app.route("/login_view")
def login_view():
    return render_template('login.html')

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500) 
    
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")

    return redirect("/")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login_view')

@app.route("/", methods=['GET','POST'])
def index():
    if "google_id" not in session:
        return redirect('/login_view')


    if session["email"] != 'bosargya@gmail.com':
        error = "email invalid"
        return render_template('login.html', error=error)

    nama = session['name']
    data_tipe = [
        {'tipe' : 'sempro', 'nama' : 'SEMPRO'},
        {'tipe' : 'ta', 'nama' : 'Tugas Akhir'},
        {'tipe' : 'i2', 'nama' : 'Internship 2'},
        {'tipe' : 'i1', 'nama' : 'Internship 1'},
        {'tipe' : 'p3', 'nama' : 'Project 3'},
        {'tipe' : 'p2', 'nama' : 'Project 2'},
        {'tipe' : 'p1', 'nama' : 'Project 1'},
    ]
    data_tahun = [
        {'tahun' : '20192'},
        {'tahun' : '20202'},
        {'tahun' : '20211'},
        {'tahun' : '20212'}
    ]
    dosen = models.namaDosen()
    mahasiswa = models.namaMhs()
    pertemuan = models.jumlahPertemuan()
    tipe = request.form.get('tipe')
    tahun = request.form.get('tahun')
    tahun_id = models.data(tahun)
    hasil = models.dataJoin(tahun_id, tipe)
    return render_template('index2.html', nama=nama, data_tipe=data_tipe,hasil=hasil, activate='dashboard', dosen=dosen, mahasiswa=mahasiswa, pertemuan=pertemuan, data_tahun=data_tahun)


if (__name__) == "__main__":
    app.run(debug=True)