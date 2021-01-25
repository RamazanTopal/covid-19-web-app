from flask import Flask, escape, request,url_for,render_template
from covid import Covid


app = Flask(__name__)

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
    


