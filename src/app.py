from operator import and_, itemgetter
from flask import Flask, jsonify, abort, render_template, request, redirect, session, url_for, flash, make_response
from sqlalchemy import ForeignKey, desc, asc
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from time import sleep
from twilio.rest import Client
from subprocess import Popen, PIPE
import pandas as pd
import csv
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import glob


app = Flask(__name__)
app.secret_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJ1c2VyLTFTTTRSUTlfLS1IVEpGM0QiLCJpYXQiOjE2NjI5ODc0Nzd9.mCvSd2o2vw5Gs7grkBLkW75dlgVcJ-aiqMzfVUvG-q4'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://kevin:123456@localhost/flask_db'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)


class User(db.Model): 
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(40))
    wa=db.Column(db.String(40))
    password=db.Column(db.String(40))
    mac=db.Column(db.String(40),unique=True)

    def __init__(self,name,wa,password,mac):
        self.name=name
        self.wa=wa
        self.password=password
        self.mac=mac
    
  
class Histori(db.Model):
    __tablename__='histori'
    id=db.Column(db.Integer,primary_key=True)
    id_user=db.Column(db.Integer, ForeignKey(User.id))
    username=db.Column(db.String(40))
    date=db.Column(db.Date)
    jam=db.Column(db.String(40))
    status=db.Column(db.Integer)
    keterangan=db.Column(db.String(120))
 
    def __init__(self,id_user,username,date,jam,status,keterangan):
        self.id_user=id_user
        self.username=username
        self.date=date
        self.jam=jam
        self.status=status
        self.keterangan=keterangan


class Harian(db.Model):
    __tablename__='harian'
    id=db.Column(db.Integer,primary_key=True)
    id_user=db.Column(db.Integer, ForeignKey(User.id))
    username=db.Column(db.String(40))
    date=db.Column(db.Date)
    jam=db.Column(db.String(40))
    status=db.Column(db.Integer)
    
    def __init__(self,id_user,username,date,jam,status):
        self.id_user=id_user
        self.username=username
        self.date=date
        self.jam=jam
        self.status=status


class Statistik(db.Model):
    __tablename__='statistik'
    id=db.Column(db.Integer,primary_key=True)
    id_user=db.Column(db.Integer, ForeignKey(User.id))
    username=db.Column(db.String(40))
    date=db.Column(db.Date)
    kehadiran=db.Column(db.Integer)
    datang=db.Column(db.String)
    pulang=db.Column(db.String)
    
 
    def __init__(self,id_user,username,date,kehadiran,datang,pulang):
        self.id_user=id_user
        self.username=username
        self.date=date
        self.kehadiran=kehadiran
        self.datang=datang
        self.pulang=pulang

##################################### LOGIN DAN REGIS #####################################

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register-submit', methods = ['POST'])
def register_submit():
    name = request.form['name']
    name = name.capitalize()
    wa = request.form['nomorwa']
    password = request.form['password']
    cpassword = request.form['cpassword']
    # mac = len(User.query.all())
    mac = request.remote_addr
    now_ = datetime.now()
    # exists = db.session.query(db.exists().where(User.mac == request.remote_addr)).scalar()
    
    if password != cpassword:
        flash('Password dan Konfirmasi Password tidak sesuai')
        return redirect(url_for('register'))
    else:
        user = User(name, wa, password, mac)
        db.session.add(user)
        db.session.commit()
        user_id = User.query.filter(User.mac == mac).first().id
        user = Histori(user_id, name, now_.strftime("%d/%m/%Y"), '08:00:00', 1, "register dan masuk")
        db.session.add(user)
        db.session.commit()
        flash('Berhasil membuat akun!')
        return redirect(url_for('login'))
        
@app.route('/regis-ulang')
def regis_ulang():
    return render_template('regis ulang.html')
       
@app.route('/regis-ulang-submit', methods = ['POST'])
def regis_ulang_submit():
    if request.method == "POST":
        try:
            name = request.form['name']
            name = name.capitalize()
            mac = request.remote_addr
            user_id = User.query.filter_by(name=name).first().id
            user_to_update = User.query.get_or_404(user_id)
            user_to_update.mac = request.remote_addr
            db.session.commit()
            
            flash('Berhasil register ulang!')
            return redirect(url_for('login'))
        except:
            flash('Akun tidak ditemukan!')
            return redirect(url_for('login'))
            
        
@app.route('/login')
def login():
    # now_ = datetime.now()
    # user = Harian(6, 'Hery', now_.strftime("%d/%m/%Y"), '08:25', 1)
    # e = Harian.query.get_or_404(579)
    # e.jam = '10:30'
    # e.status = 1
    # for i in range(250, 263):
    #     Harian.query.filter(Harian.id == i).delete()
    # db.session.add(user)
    # db.session.commit()
    # print('sukses')
    # db.create_all()
    # print(socket.gethostbyaddr(request.remote_addr))
    # User.query.delete()
    # print(request.environ['REMOTE_ADDR'])
    return render_template('login.html')

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200

@app.route('/login-submit', methods = ['POST'])
def login_submit():
    # db.create_all()
    nama = request.form['nama']
    nama = nama.capitalize()
    password = request.form['password']

    user = User.query.filter(and_(User.name == nama, User.password == password)).first()
    if user:
        session['user_id'] = user.id
        session['name'] = user.name
        return redirect('/')
    else:
        flash("Gagal login\nNama atau Password salah")
        return redirect('/login')
    
@app.route("/logout")
def logout():
    try:
        p2.join()
    except:
        pass
    session.pop("user_id", None)
    return redirect(url_for("login")) 

##################################### ADMIN #####################################

@app.route('/admin')
def admin():
    history_data = Histori.query.filter_by().order_by(Histori.date.desc())
    if 'user_id' in session:
        return render_template('admin.html', histori = history_data)
    else:
        return redirect(url_for('login'))
    
##################################### SCAN #####################################

@app.route('/filter-scan')
def filter_scan():
    # if request.method == "POST":
    data_harian = Harian.query.all()
    hari = set([i.date for i in data_harian])
    return render_template('filter scan.html', hari = sorted(hari, reverse=True))

@app.route('/scan', methods = ['POST'])
def scan():
    hari_choosed = request.form['hari']
    all_id = User.query.filter(User.mac.contains('.')).order_by(User.id.asc()).all()
    nama = [i.name for i in all_id]
    nodes = [i.mac for i in all_id]
    
    data_harian = Harian.query.all()
    data_choosed = Harian.query.filter_by(date=hari_choosed).all()
    baris_jam = set([i.jam for i in data_choosed])
    baris_stat = []
    
    for i in baris_jam:
        stat = Harian.query.filter(and_(Harian.jam==i, Harian.date==hari_choosed)).order_by(Harian.id_user.asc()).all()
        baris_data = [i] + [j.status for j in stat]
        baris_stat.append(baris_data)
        
    temp = sorted(baris_stat, key=itemgetter(0), reverse=True)
    l = sum_menit(nama, temp)
    p = [['-'.join(hari_choosed.split('-')[::-1])]] + l
    with open(r"csv\time stamp\time stamp_"+ hari_choosed +".csv", "w", newline="") as f:
        writer = csv.writer(f)
        # writer.writerow(['Tanggal', 'Stamp']+nama)
        writer.writerows(p)
    
    write_csv_scan(sorted(baris_stat, key=itemgetter(0), reverse=True), hari_choosed, nama)
    c = len(temp[0])
    
    return render_template('scan.html', employee = nama, jam = temp, c = c)

def write_csv_scan(bstat, tgl, nama):
    if len(bstat)==0:
        flash(f'Belum ada data absen hari ini')
    else:
        # tgl2 = '-'.join(tgl.split('-')[::-1])
        tgl2 = tgl
        for i in bstat:
            i.insert(0, tgl2)
        
        with open(r"csv\data absen\data absen_"+tgl2+".csv", "w", newline="") as f:
            writer = csv.writer(f)
            # writer.writerow(['Tanggal', 'Stamp']+nama)
            writer.writerows(bstat)
        
        for i in bstat:
            i.remove(tgl2)
            
def sum_menit(nama, temp):
    l = []
    for k in range(len(nama)):
        tempo=[]
        counter = 0
        for j in range(len(temp)):
            if j == 0:
                if ('17:00' > temp[j][0] >= '09:00'):
                    counter += 30*(temp[j][k+1])
                elif (temp[j][0] < '09:00'):
                    counter += 5*(temp[j][k+1])
                elif (temp[j][0] >= '17:00' ):
                    counter += 5*(temp[j][k+1])
            else:
                if (temp[j][0] == '11:30'):
                    counter += 30*(temp[j][k+1])
                elif (temp[j][0] == '12:00'):
                    pass
                else:
                    counter += selisih(temp[j-1][0],temp[j][0])*temp[j][k+1]
            # counter += abs(int(temp[j][0][-2:])-int(temp[j+1][0][-2:]))*temp[j][k+1]
        # tempo.append(nama[k])
        tempo.append(counter)
        l.append(tempo)
    return l

##################################### MESSAGE #####################################
        
@app.route('/message')
def message():
    emp_data = User.query.all()
    return render_template('message.html', employee = emp_data)
    
@app.route('/send-notification')
def send_notification():
    emp_data = User.query.all()
    numbers = ['whatsapp:'+(i.wa) for i in emp_data if len(i.wa) > 9]
    account_sid = 'AC411d9b870b3da291d51c153da36e5788'
    auth_token = '30a8719b4123874991f3613aa0684668'
    client = Client(account_sid, auth_token)

    for number in numbers:
        message = client.messages.create(
        from_='whatsapp:+14155238886',
        body='Jangan lupa absen pagi',
        to=number
        )
    flash(f'Pesan berhasil dikirim')
    return redirect('/admin')

@app.route('/broadcast', methods = ['POST', 'GET'])
def broadcast():
    if request.method == "POST":
        emp_data = User.query.all()
        pesan = request.form['pesan']
        numbers = ['whatsapp:'+(i.wa) for i in emp_data if len(i.wa) > 9]
        account_sid = 'AC411d9b870b3da291d51c153da36e5788'
        auth_token = '30a8719b4123874991f3613aa0684668'
        client = Client(account_sid, auth_token)

        for number in numbers:
            message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=pesan,
            to=number
            )
        flash(f'Pesan berhasil dikirim')
        return redirect('/admin')

@app.route('/private', methods = ['POST', 'GET'])
def private():
    if request.method == "POST":
        pesan = request.form['pesan']
        nama = request.form['nama']
        number = User.query.filter(User.name == nama).first().wa
        account_sid = 'AC411d9b870b3da291d51c153da36e5788'
        auth_token = '30a8719b4123874991f3613aa0684668'
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=pesan,
        to='whatsapp:'+number
        )
        flash(f'Pesan berhasil dikirim kepada {nama}')
        return redirect('/admin')

##################################### EMPLOYEE #####################################

@app.route('/employee')
def employee():
    emp_data = User.query.all()
    if 'user_id' in session:
        return render_template('employee.html', employee = emp_data)
    else:
        return redirect(url_for('login'))

@app.route('/delete-employee')
def delete_employee():
    id_user = request.args.get('id')
    User.query.filter(User.id == id_user).delete()
    db.session.commit()
    return redirect('/employee')

@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update(id):
    # id_file = request.args.get('id')
    user_to_update = User.query.get_or_404(id)
    return render_template('update.html', user_to_update=user_to_update)
      
@app.route('/edit-user/<int:id>', methods = ['POST', 'GET'])
def edit_employe(id):
    user_to_update = User.query.get_or_404(id)
    if request.method == "POST":
      user_to_update.name = request.form['name']
      user_to_update.password = request.form['pw']
      user_to_update.wa = request.form['wa']
      user_to_update.mac = request.form['mac']
      
      try:
        db.session.commit()
        return redirect('/employee')
      except:
        return "There was problem"
    else:
        return render_template('update.html', user_to_update=user_to_update)
    
@app.route('/statistik/<int:id>', methods = ['POST', 'GET'])
def statistik(id):
    plot = get_plot(id)
    plot.savefig(os.path.join('static', 'img', 'plot.png'))
    user_to_update = User.query.get_or_404(id)
    return render_template('statistik.html', user_to_update=user_to_update)

def get_plot(id):
    data1 = []
    data2 = []    
    
    all_id = User.query.filter(User.mac.contains('.')).order_by(User.id.asc()).all()
    ids = [i.id for i in all_id]
    indx = ids.index(id)
    for i in import_csv():
        data1.append(i[0])
        temp = int((int(i[indx+1])/480)*100)
        if temp > 100: temp = 100
        data2.append(temp)
        
    
    tanggal = data1
    values = data2
    fig = plt.figure(figsize = (10, 5))
    
    plt.bar(tanggal, values, color ='maroon', width = 0.4)
    p1 = plt.bar(np.arange(len(data2)), data2)
    
    for rect1 in p1:
        height = rect1.get_height()
        plt.annotate( "{}%".format(height), (rect1.get_x() + rect1.get_width()/2, height/2),ha="center",va="bottom",fontsize=15)
    
    plt.xlabel("Tanggal")
    plt.ylabel("Kehadiran")
    plt.title("Persentase Kehadiran")
    return plt

def import_csv():
    path = r'C:\D_Drive\Kantor\test\src\csv\time stamp' # use your path
    all_files = glob.glob(os.path.join(path , "*.csv"))
    # print(all_files)
    li = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=None)
        dfl = df.values.tolist()
        res = [i[0] for i in dfl]
        print(res)
        li.append(res)
        
    return li

##################################### HOME #####################################

@app.route('/')
def home():
    try:
        user_data = User.query.filter_by(id=session['user_id']).first().name
    except:
        return redirect(url_for('login'))
    if user_data == "Admin":
        return redirect('/admin')
    # if isConnected():
    if 'user_id' in session:
        now = datetime.now()
        user_to_update = User.query.get_or_404(session['user_id'])
        # exist = db.session.query(db.exists().where(and_(Histori.id_user==session['user_id'], Histori.date == now.strftime("%d/%m/%Y")))).scalar()
        # print(exist)
        # if not exist and '.' in (User.query.filter_by(id=session['user_id']).first().mac):
        # while True:
        #     i = 0
        #     try:
        #         user_to_update.mac = i
        #         db.session.commit()
        #         print('oke')
        #         break
        #     except:
        #         i+=1
        #         print(i)
        
        # mac_address = get_mac_address()
        # if User.query.filter_by(id=session['user_id']).first().mac == request.remote_addr:    
        # timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
        timestamp = now.strftime("%H:%M:%S")
        return render_template('home.html', user = user_data)
        # else:
        #     return render_template('gagal.html', pesan = "Gunakan device yang digunakan saat register!")
    else:
        return redirect(url_for('login'))
    # else:
    #     return render_template('gagal.html', pesan = "Anda tidak berada di lingkungan kantor!")

    
@app.route('/absen-datang')
def absen_datang():
    now = datetime.now()
    exists = db.session.query(db.exists().where(and_(and_(Histori.id_user==session['user_id'], Histori.date == now.strftime("%d/%m/%Y")),and_(Histori.status==1, Histori.date == now.strftime("%d/%m/%Y"))))).scalar()
    if not exists:
        user = Histori(session['user_id'], session['name'], now.strftime("%d/%m/%Y"), now.strftime("%H:%M:%S"), 1, "masuk")
        user_to_update = User.query.get_or_404(session['user_id'])
        try:
            user_to_update.mac = request.remote_addr
            db.session.add(user)
            db.session.commit()
            flash("Berhasil Absen Datang")
        except:
            flash("Device ini sudah digunakan untuk absen")
    else:
        flash("Anda sudah absen datang hari ini")
    return redirect('/')

@app.route('/izin-keluar', methods = ['POST', 'GET'])
def izin_keluar(): 
    if request.method == "POST":
        now = datetime.now()
        ket = request.form['ket']
        user = Histori(session['user_id'], session['name'], now.strftime("%d/%m/%Y"), now.strftime("%H:%M:%S"), 2, ket)
        db.session.add(user)
        db.session.commit()
        flash("Berhasil Izin")
        return redirect('/')

@app.route('/absen-pulang')
def absen_pulang():
    now = datetime.now()
    hour = int(now.strftime("%H"))
    if hour >= 16:
        exists = db.session.query(db.exists().where(and_(and_(Histori.id_user==session['user_id'], Histori.date == now.strftime("%d/%m/%Y")),and_(Histori.status==3, Histori.date == now.strftime("%d/%m/%Y"))))).scalar()
        if not exists:
            if User.query.filter_by(id=session['user_id']).first().mac == request.remote_addr :
                user = Histori(session['user_id'], session['name'], now.strftime("%d/%m/%Y"), now.strftime("%H:%M:%S"), 3, "pulang")
                db.session.add(user)
                db.session.commit()
                flash("Berhasil Absen Pulang")
                user_to_update = User.query.get_or_404(session['user_id'])
                while True:
                    i = 0
                    try:
                        user_to_update.mac = i
                        break
                        print('oke')
                    except:
                        i+=1
                        print(i)
            else:
                flash("Sistem mendeteksi perbedaan device!")
        else:
            flash("Anda sudah absen pulang hari ini")
    else:
        flash("Absen pulang baru bisa dilakukan diatas jam 4!")
    
    return redirect('/')

@app.route('/keluar')
def keluar():
    return render_template('keluar.html')

@app.route("/gagal")
def gagal():
    return render_template('gagal.html') 

@app.route('/delete-history')
def delete_history():
    id_histori = request.args.get('id')
    Histori.query.filter(Histori.id == id_histori).delete()
    db.session.commit()
    return redirect('/admin')

##################################### CSV #####################################

@app.route('/write-csv')
def writecsv():
    records = Histori.query.all()
    a = [[i.id, i.id_user, i.username, i.date.strftime('%d/%m/%Y'), i.jam, i.status, i.keterangan] for i in records]
    
    if len(a)==0:
        flash(f'Belum ada data absen')
        return redirect("/admin")
    
    with open("data absen.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(['ID histori', 'ID User', 'Nama User', 'Tanggal', 'Jam', 'Status', 'Keterangan'])
        writer.writerows(a)
    
        
    df = pd.read_csv(r"data absen.csv")
    writer = pd.ExcelWriter(r'file.xlsx', engine='xlsxwriter') 
    df.to_excel(writer, sheet_name='Sheet1', index = None, header=True)
    # read_file.to_excel (r'data.xlsx', index = None, header=True)
    
    for column in df:
        column_length = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_length+8)
    writer.close()
    flash(f'File.xksx dan data absen.csv berhasil dibuat')
    return redirect("/admin")

@app.route('/write-csv-today')
def writecsvtoday():
    tgl = datetime.now().strftime("%d-%m-%Y")
    records = Histori.query.all()
    res = []
    for i in records:
        if i.date.strftime('%d-%m-%Y')==tgl:
            a = [i.id, i.id_user, i.username, i.date.strftime('%d/%m/%Y'), i.jam, i.status, i.keterangan] 
            res.append(a)
        
    if len(res)==0:
        flash(f'Belum ada data absen hari ini')
    
    else:
        with open("data absen_"+tgl+".csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(res)
        flash(f'data absen_{tgl}.csv berhasil dibuat!')
    return redirect("/admin")

##################################### FILTER #####################################

@app.route('/filter-name', methods = ['POST'])
def filter_name():
    name = request.form['fil-name']
    if request.method == "POST":
        his_data = Histori.query.filter_by(username=name).order_by(Histori.date.desc())
        return render_template('admin.html', histori = his_data)

@app.route('/filter-name-fm', methods = ['POST'])
def filter_name_fm():
    name = request.form['fil-name']
    if request.method == "POST":
        his_data = Histori.query.filter_by(username=name).order_by(Histori.date.desc())
        return render_template('admin fm.html', histori = his_data)
    
@app.route('/filter-name-fi', methods = ['POST'])
def filter_name_fi():
    name = request.form['fil-name']
    if request.method == "POST":
        his_data = Histori.query.filter_by(username=name).order_by(Histori.date.desc())
        return render_template('admin fi.html', histori = his_data)  
    
@app.route('/filter-name-fp', methods = ['POST'])
def filter_name_fp():
    name = request.form['fil-name']
    if request.method == "POST":
        his_data = Histori.query.filter_by(username=name).order_by(Histori.date.desc())
        return render_template('admin fp.html', histori = his_data)  

@app.route('/filter-masuk')
def filter_masuk():
    his_data = Histori.query.all()
    return render_template('admin fm.html', histori = his_data)

@app.route('/filter-keluar')
def filter_keluar():
    his_data = Histori.query.all()
    return render_template('admin fi.html', histori = his_data)

@app.route('/filter-pulang')
def filter_pulang():
    his_data = Histori.query.all()
    return render_template('admin fp.html', histori = his_data)

##################################### OTHER #####################################

def selisih(j1, j2):
    h1, m1 = list(map(int, j1.split(':')))
    h2, m2 = list(map(int, j2.split(':')))
    return abs(((h1-h2)*60) + (m1-m2))

if __name__ == '__main__':    
    app.run(host='0.0.0.0', debug=True, port=os.environ.get('PORT', 80))
    
