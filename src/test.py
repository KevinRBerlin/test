# # # # # from requests import get

# # # # # ip = get('https://api.ipify.org').content.decode('utf8')
# # # # # print('My public IP address is: {}'.format(ip))

# # # # # from getmac import get_mac_address as gmac
# # # # # eth_mac = gmac(interface="eth0")
# # # # # ip_mac = gmac(ip="192.168.1.21")
# # # # # host_mac = gmac(hostname="localhost")

# # # # # print(ip_mac, eth_mac)
# # # from re import findall
# # # from subprocess import Popen, PIPE

# # # def pingt (host,ping_count):
# # #     for ip in host:
# # #         # user_id = User.query.filter(User.mac == ip).first().id
# # #         # user_name = User.query.filter(User.mac == ip).first().name
        
# # #         data = ""
# # #         output= Popen(f"ping {ip} -n {ping_count}", stdout=PIPE, encoding="utf-8")

# # #         for line in output.stdout:
# # #             data = data + line
# # #             ping_test = findall("TTL", data)

# # #         if ping_test:
# # #             print(1, end=" ")
# # #         else:
# # #             print(0, end=" ")
            
# # # # pingt(['192.168.1.212','192.168.1.211','192.168.1.215'],2)

# # # import platform    # For getting the operating system name
# # # import subprocess  # For executing a shell command

# # # def ping(host):
# # #     param = '-n' if platform.system().lower()=='windows' else '-c'
# # #     command = ['ping', param, '2', host]
# # #     if subprocess.call(command) == 0:
# # #         return True
# # #     else:
# # #         return False
    
# # # print(ping('192.168.1.212'))
# # # print(ping('192.168.1.213'))
# # # print(ping('192.168.1.215'))

# from ping3 import ping, verbose_ping
# from time import sleep
# from datetime import datetime
# from app import User, app
# # # print(ping('192.168.1.211'))
# # # print(ping('192.168.1.212'))
# # # verbose_ping('192.168.1.212')

# # def minute5(m):
# #     return (m % 5) == 0

# # def minute30(m):
# #     return (m % 30) == 0

# # def pings(nodes, interval): 
# #     res = [0]*len(nodes)
# #     temp = nodes[:]
# #     now_ = datetime.now()
# #     m = int(now_.strftime("%M"))
# #     while (m+1 % interval) != 0 and len(nodes) != 0:
# #         print('masuk1')
# #         sleep(5)
# #         print(len(temp), len(nodes))
# #         now_ = datetime.now()
# #         m = int(now_.strftime("%M"))
# #         for ip in nodes:
# #             print('masuk2')
# #             print(ping(ip), ip, temp)
# #             if ping(ip):
# #                 print('masuk none')
# #                 res[temp.index(ip)] = 1
# #                 nodes.remove(ip)
# #         print(len(nodes) != 0)
# #     save(res, temp)
    
# # def save(res, nodes):
# #     with app.app_context():
# #         now_ = datetime.now()
# #         stamp = now_.strftime("%H:%M")
# #         # stamp = '14:30'
# #         for i in range(len(nodes)):
# #             user_id = User.query.filter(User.mac == nodes[i]).first().id
# #             user_name = User.query.filter(User.mac == nodes[i]).first().name
            
# #             user = user_id, user_name, now_.strftime("%d/%m/%Y"), stamp, res[i]
# #             print(user)
# #         # user = Harian(user_id, user_name, now_.strftime("%d/%m/%Y"), stamp, res[i])
# #         # db.session.add(user)
# #         # db.session.commit()

# # nodes=['192.168.1.211', '192.168.1.214', '192.168.1.117']
# # # nodes2=['192.168.1.211', '192.168.1.214', '192.168.1.117']
# # # pings(nodes, 5)
# # save([0,1,1],nodes)

# # # if not None:
# # #     print('oke')

# # # def starts():
# # #     with app.app_context():
# # #         all_id = User.query.filter(User.mac.contains('.')).order_by(User.id.asc()).all()
# # #         emp_data = User.query.all()
# # #         nodes = [i.mac for i in all_id]
        
# # #         while True:
# # #             print('masuk')
# # #             now_ = datetime.now()
# # #             jam = int(now_.strftime("%H"))
# # #             m = int(now_.strftime("%M"))
# # #             if jam < 9 and jam >= 7:
# # #                 pings(nodes, 5)
# # #                 print('masuk 5')
# # #             elif jam >= 9 and jam < 17:
# # #                 if minute30(m):
# # #                     if str(jam)+':'+str(m) == '12:30':
# # #                         pass
# # #                     else:
# # #                         ping(nodes,5)
# # #                         print('masuk 30')
# # #             elif (jam >= 17) and (jam <= 18):
# # #                 if minute5(m): 
# # #                     ping(nodes,5)
# # #                     print('masuk 5')
# # #             else : break
# # #             sleep(58)
# # #             print(str(jam)+':'+str(m))

# def pembulatan(n):
#     h, m = n.split(':')
#     m = str(int(m) - (int(m) % 5))
#     return(h+':'+m)
    


# def pings(nodes, interval): 
#     res = [0]*len(nodes)
#     temp = nodes[:]
#     now_ = datetime.now()
#     stamp = now_.strftime("%H:%M")
#     # stamp = '16:00'
#     m = int(now_.strftime("%M"))
#     # timecheck = now_.strftime("%H:%M")
#     print(nodes)
#     while stamp != '8:59' and len(nodes) != 0:
#         print('masuk1')
#         print(len(temp), len(nodes))
#         # m = int(now_.strftime("%M"))
#         for ip in nodes:
#             print('masuk2')
#             print(ping(ip), ip, nodes)
#             if ping(ip) or res[temp.index(ip)] == 1:
#                 print('masuk none')
#                 res[temp.index(ip)] = 1
#                 nodes.remove(ip)
#         print(len(nodes) != 0, ((m+1)%interval) != 0)
#         now_ = datetime.now()
#         stamp = now_.strftime("%H:%M")
#         save(res, temp, pembulatan(stamp))
#         sleep(290)


import pandas as pd
import glob
import os

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

# print(li)

# frame = pd.concat(li, axis=0, ignore_index=True)
