from flask import Flask, escape, request,url_for,render_template,abort,session,redirect,request
from covid import Covid
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import sqlalchemy#404 hatalarını karşılaması için
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1346795432120@localhost/covid19'
app.config['SECRET_KEY'] = 'ramazansecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
admin=Admin(app)



class Makale(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    baslik=db.Column(db.String(255))
    makale=db.Column(db.String(1000))
    yazar=db.Column(db.String(255))
    slug=db.Column(db.String(255))
    tarih=db.Column(db.DateTime)
#db.create_all() 
class ModelViewKıyasla(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)
admin.add_view(ModelViewKıyasla(Makale,db.session))

@app.route('/')
def index():
    covid = Covid()
    toplam = covid.get_total_confirmed_cases()
    toplam1 = "{sayi:,}".format(sayi=toplam)
    iyilesen = covid.get_total_recovered()
    iyilesen1 = "{iyilesenler:,}".format(iyilesenler=iyilesen)
    olu = covid.get_total_deaths()
    olu1 = "{olenler:,}".format(olenler=olu)
    turkey_cases = covid.get_status_by_country_name("turkey")
    return render_template('index.html',toplam=toplam1,iyilesen=iyilesen1,olu=olu1,turkey_cases=turkey_cases)


@app.route('/ulkevakasayisi')
def toplamvaka():
    covid = Covid()
    sayi=covid.get_data()
    return render_template('ulkevakasayisi.html',sayi=sayi)
@app.route('/makaleler')
def makale():
    posts=Makale.query.all()
    return render_template('makale.html',posts=posts)

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form.get("username") == "ramazan" and request.form.get("password") == "1346795":
            session['logged_in']=True
            return redirect("/admin")
        else:
            return render_template('login.html',hata=True)
    return render_template('login.html')
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route("/post/<string:slug>")
def post(slug):
    try:
        post = Makale.query.filter_by(slug=slug).one()
        return render_template("post.html", post=post)
    except sqlalchemy.orm.exc.NoResultFound:
        abort(404)
if __name__ == '__main__':
    app.debug = True
    app.run()