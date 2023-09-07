from sqlalchemy import ForeignKey, desc, asc
from flask_sqlalchemy import SQLAlchemy
from time import sleep
from re import findall
from subprocess import Popen, PIPE
# from flask import request
# from flask import Flask
from datetime import datetime
from app import User, Histori, Harian, app, db
from ping3 import ping

# app = Flask(__name__)
# app.secret_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJ1c2VyLTFTTTRSUTlfLS1IVEpGM0QiLCJpYXQiOjE2NjI5ODc0Nzd9.mCvSd2o2vw5Gs7grkBLkW75dlgVcJ-aiqMzfVUvG-q4'
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://kevin:123456@localhost/flask_db'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# db = SQLAlchemy(app)
# with app.app_context():
#     all_id = User.query.filter(User.mac.contains('.')).order_by(User.id.asc()).all()
#     nodes = [i.mac for i in all_id]

# print(nodes)

def selisih(j1, j2):
    h1, m1 = list(map(int, j1.split(':')))
    h2, m2 = list(map(int, j2.split(':')))
    return abs(((h1-h2)*60) + (m1-m2))
    
def minute5(m): return (m % 5) == 0

def minute30(m): return (m % 30) == 0

def start_scan():
    with app.app_context():
        all_id = User.query.filter(User.mac.contains('.')).order_by(User.id.asc()).all()
        emp_data = User.query.all()
        nodesall = [i.mac for i in all_id]
        nodes = nodesall[:]
        hadir = [0]*(len(nodesall))
        # pings(nodes,30)
        while True:
            if len(nodes) != len(nodesall): nodes = nodesall[:]
            print('masuk')
            now_ = datetime.now()
            jam = int(now_.strftime("%H"))
            m = int(now_.strftime("%M"))
            if jam < 9 and jam >= 7:
                if minute5(m):
                    if sum(hadir) == len(hadir):
                        pings(nodes, 30, hadir)
                    hadir = pings(nodes, 5, hadir)
                    print('masuk 5')
            elif jam >= 9 and jam < 17:
                if minute30(m):
                    if str(jam)+':'+str(m) == '12:30' or str(jam)+':'+str(m) == '12:0':
                        pass
                    else:
                        hadir = [0]*len(nodesall)
                        pings(nodes, 30, hadir)
                        print('masuk 30')
            elif (jam >= 17) and (jam <= 18):
                if minute5(m): 
                    hadir = [0]*len(nodesall)
                    pings(nodes, 5, hadir)
                    print('masuk 5')
            else : break
            sleep(58)
            print(str(jam)+':'+str(m))
        ping(nodes,5,hadir)

def pings(nodes, interval, res): 
    # res = [0]*len(nodes)
    temp = nodes[:]
    now_ = datetime.now()
    stamp = now_.strftime("%H:%M")
    # stamp = '16:00'
    m = int(now_.strftime("%M"))
    print(nodes)
    while ((m+1) % interval) != 0 and len(nodes) != 0:
        print('masuk1')
        sleep(10)
        now_ = datetime.now()
        m = int(now_.strftime("%M"))
        for ip in nodes:
            print('masuk2')
            print(ping(ip), ip, nodes)
            if ping(ip) or res[temp.index(ip)] == 1:
                print('ping masuk')
                res[temp.index(ip)] = 1
                nodes.remove(ip)
        # print(len(nodes) != 0, ((m+1)%interval) != 0)
    save(res, temp, stamp)
    return res

# def ping (host,ping_count):
#     now_ = datetime.now()
#     stamp = now_.strftime("%H:%M")
#     # stamp = '14:30'
#     res = []
#     res.append(stamp)
#     for ip in host:
#         user_id = User.query.filter(User.mac == ip).first().id
#         user_name = User.query.filter(User.mac == ip).first().name
        
#         data = ""
#         output= Popen(f"ping {ip} -n {ping_count}", stdout=PIPE, encoding="utf-8")

#         for line in output.stdout:
#             data = data + line
#             ping_test = findall("TTL", data)

#         if ping_test:
#             user = Harian(user_id, user_name, now_.strftime("%d/%m/%Y"), stamp, 1)
#         else:
#             user = Harian(user_id, user_name, now_.strftime("%d/%m/%Y"), stamp, 0)
#         db.session.add(user)
#         db.session.commit()


def save(res, nodes, stamp):
    # with app.app_context():
    now_ = datetime.now()
    # stamp = now_.strftime("%H:%M")
    # stamp = '14:30'
    for i in range(len(nodes)):
        user_id = User.query.filter(User.mac == nodes[i]).first().id
        user_name = User.query.filter(User.mac == nodes[i]).first().name
        
        # user = user_id, user_name, now_.strftime("%d/%m/%Y"), stamp, res[i]
        # print(user)
        user = Harian(user_id, user_name, now_.strftime("%d/%m/%Y"), stamp, res[i])
        db.session.add(user)
        db.session.commit()

# nodes=['192.168.1.211', '192.168.1.214', '192.168.1.117']
# nodes2=['192.168.1.211', '192.168.1.214', '192.168.1.117']
# pings(nodes, 5)
# save([0,1,1],nodes)

start_scan()
