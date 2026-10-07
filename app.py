from flask import Flask, request, redirect, session
import os, base64
app = Flask(__name__)
app.secret_key = 'v23green'
shops = {'Rongai Shoe Center': {'own': 'admin', 'till': '0116782556', 'ok': True, 'lat': -1.3956, 'lng': 36.7562, 'area': 'Rongai Town'}}
prods = [{'id': 1, 'name': 'Jordan 1', 'price': 4500, 'img': 'https://via.placeholder.com/400', 'shop': 'Rongai Shoe Center', 'stock': 10}]

STYLE = 'body{margin:0;background:#f0f2f5;padding-bottom:90px;font-size:22px;font-family:Arial}.card{background:white;border-radius:14px;padding:16px;margin:10px}.btn{padding:16px;border-radius:10px;width:100%;margin-top:8px;font-weight:bold;border:none;font-size:20px}.btn-o{background:#f68b1e;color:white}.btn-b{background:#000;color:white}.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:10px 0;border-top:3px solid #f68b1e}#map{height:85vh;width:100%}input,select{width:100%;padding:14px;margin:6px 0;border-radius:10px;border:2px solid #ddd}'

def nav():
    c = len(session.get('cart', []))
    return '<div class=bottom><a href=/>Market</a><a href=/map>GPS Map</a><a href=/post>Post</a><a href=/cart>Cart ' + str(c) + '</a><a href=/register>Join</a></div>'

@app.route('/')
def home():
    h = '<style>' + STYLE + '</style><div style=background:#f68b1e;padding:12px><b style=color:white;font-size:24px>EAZYMADE MARKET</b></div>'
    h = h + '<div style=background:linear-gradient(135deg,#f68b1e,#000);color:white;padding:18px;border-radius:12px;margin:10px;text-align:center><h2>ALL SHOPS MARKET</h2><a href=/map><button class=btn style=background:white;color:#f68b1e>VIEW MAP ALL SHOPS FULL PAGE</button></a></div>'
    for name in shops:
        s = shops[name]
        if not s['ok']:
            continue
        tot = 0
        for p in prods:
            if p['shop'] == name:
                tot = tot + int(p['stock'])
        h = h + '<div class=card><b>' + name + '</b><br>' + s['area'] + ' - ' + str(tot) + ' pairs TOTAL Whole Shop<br><a href=/shop/' + s['own'] + '><button class=btn-o>Enter Whole Shop ' + str(tot) + ' pairs</button></a></div>'
    for p in prods:
        h = h + '<div class=card><img src=' + p['img'] + ' style=width:100%;height:200px;object-fit:cover><br><b>' + p['name'] + '</b> ' + p['shop'] + '<br>KSh ' + str(p['price']) + ' Stock ' + str(p['stock']) + '<br><a href=/add/' + str(p['id']) + '><button class=btn-o>Add to Cart BIG</button></a></div>'
    h = h + nav()
    return h

@app.route('/map')
def mp():
    mks = ''
    for n in shops:
        s = shops[n]
        if s['ok']:
            mks = mks + 'L.marker([' + str(s['lat']) + ',' + str(s['lng']) + ']).addTo(m).bindPopup("' + n + '");'
    return '<style>' + STYLE + '</style><div id=map></div><link rel=stylesheet href=https://unpkg.com/leaflet@1.9.4/dist/leaflet.css><script src=https://unpkg.com/leaflet@1.9.4/dist/leaflet.js></script><script>var m=L.map("map").setView([-1.3956,36.7562],13);L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(m);' + mks + '</script>' + nav()

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        img = 'https://via.placeholder.com/400'
        f = request.files.get('pic')
        if f:
            if f.filename!= '':
                img = 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode()
        prods.append({'id': len(prods)+1, 'name': request.form['name'], 'price': request.form['price'], 'img': img, 'shop': request.form.get('shop') or 'Rongai Shoe Center', 'stock': request.form['stock']})
        return redirect('/')
    opts = ''
    for n in shops:
        if shops[n]['ok']:
            opts = opts + '<option>' + n + '</option>'
    return '<style>' + STYLE + '</style><div class=card><h2>Post Upload From Phone</h2><form method=post enctype=multipart/form-data>Shop:<select name=shop>' + opts + '</select>Name:<input name=name required>Price:<input name=price required>Stock:<input
