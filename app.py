
import requests, os
from bs4 import BeautifulSoup as bs
from flask import Flask, request, render_template
from flask_socketio import SocketIO

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

    from vicksbase import firebase as vix
    firebase_obj = vix.FirebaseApplication('https://home-automation-336c0-default-rtdb.firebaseio.com/', None)

    from Adafruit_IO import Client, Data

    aio = Client('imvickykumar999', 'aio_rUez595dIZJqRRdHq8zUdy1nefYP')
    feed = 'ledswitch'

    data = aio.receive(feed).value
    if data == 'ON':
        d=1
    else:
        d=0

    firebase_obj.put('A/B/C','Switch', d)
    result1 = firebase_obj.get('A/B/C/Switch', None)
    data1="{}".format(result1)

    if data1 == '1':
        img = 'static/logo/bulbon.jpg'
    else:
        img = '../static/logo/bulboff.jpg'

    return render_template("iotled.html",
                            data=data1,
                            img = img
                          )

# ============================================

if __name__ == "__main__":
    socketio.run(app, debug=True)
