
# def call():
import requests, os
from bs4 import BeautifulSoup as bs
from flask import Flask, request, render_template
from flask_socketio import SocketIO

# import threading, time
# from Adafruit import livemqtt as lm

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
socketio = SocketIO(app)

# -------------------------------------------------

@app.route('/news')
def news():

    link = 'https://inshorts.com/en/read'
    req = requests.get(link)

    soup = bs(req.content, 'html5lib')
    box = soup.findAll('div', attrs = {'class':'news-card z-depth-1'})

    ha,ia,ba,la = [],[],[],[]
    for i in range(len(box)):
        h = box[i].find('span', attrs = {'itemprop':'headline'}).text

        m = box[i].find('div', attrs = {'class':'news-card-image'})
        m = m['style'].split("'")[1]

        b = box[i].find('div', attrs = {'itemprop':'articleBody'}).text
        l='link not found'

        try:
            l = box[i].find('a', attrs = {'class':'source'})['href']
        except:
            pass

        ha.append(h)
        ia.append(m)
        ba.append(b)
        la.append(l)
    return render_template('news.html', ha=ha, ia=ia, ba=ba, la=la, len = len(ha))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# ==============================================================

@app.route('/')
def iotled():

#     data1 = 'ON'
#
#     if data1 == 'ON':
#         img = 'static/logo/bulbon.jpg'
#     else:
#         img = '../static/logo/bulboff.jpg'
#
#     return render_template("iotled.html",
#                             data=data1,
#                             img = img
#                           )
#
#
# @app.route('/converted_iotled', methods=['POST'])
# def converted_iotled():

    from vicksbase import firebase as vix
    firebase_obj = vix.FirebaseApplication('https://home-automation-336c0-default-rtdb.firebaseio.com/', None)

    # data = int(request.form['iotled'])
    from Adafruit_IO import Client, Data

    with open('data.txt', 'r') as f:
        key = str(f.read())

    print(key)

    aio = Client('imvickykumar999', 'aio_VjGi39ik04Nqjj08IMaeG0d8IUDI')
    feed = 'ledswitch'

    data = aio.receive(feed).value
    if data == 'ON':
        d=1
    else:
        d=0
    firebase_obj.put('A/B/C','Switch', d)

    result1 = firebase_obj.get('led1', None)

    if d == 1:
        img = 'static/logo/bulbon.jpg'
    else:
        img = '../static/logo/bulboff.jpg'

    return render_template("iotled.html",
                            data=d,
                            img = img
                          )

# ============================================

if __name__ == "__main__":
    socketio.run(app, debug=True)


# if __name__ == "__main__":
#     t1 = threading.Thread(target=lm.threadone)
#
#     time.sleep(2)
#     t2 = threading.Thread(target=socketio.run(app, debug=True))
#
#     # starting thread 1
#     t1.start()
#     # starting thread 2
#     t2.start()
#
#     # wait until thread 1 is completely executed
#     t1.join()
#     # wait until thread 2 is completely executed
#     t2.join()
#
#     # both threads completely executed
#     print("Done!")


# -----------------------------------------------
# ValueError: signal only works in main thread
