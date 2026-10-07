from flask import Flask, request, redirect, session
import os, base64

app = Flask(__name__)
app.secret_key = 'v30fix'

shops = {
    'Rongai Shoe Center': {'own': 'admin', 'ok': True, 'lat': -1.3956, 'lng': 36.7562, 'area': 'Rongai Town', 'till': '0116782556'},
    'Kitengela Sneakers': {'own': 'kiten', 'ok': True, 'lat': -1.38, 'lng': 36.78, 'area': 'Kitengela', 'till': '0712345678'},
    'Kware Market': {'own': 'kware', 'ok': True, 'lat': -1.40, 'lng': 36.74, 'area': 'Kware', 'till': '0722000000'}
}

prods = [
    {'id': 1, 'name': 'Jordan 1 Retro', 'price': 4500, 'img': 'https://via.placeholder.com/400', 'shop': 'Rongai Shoe Center', 'stock': 10},
    {'id': 2, 'name': 'Air Max 90', 'price': 3800, 'img': 'https://via.placeholder.com/400', 'shop': 'Kitengela Sneakers', 'stock': 15}
]

chats = {}

def get_style():
    a = 'body{margin:0;background:#f0f2f5;padding-bottom:140px;font-family:Arial;font-size:26px;line-height:1.5}'
    b = '.top{background:linear-gradient(90deg,#f68b1e,#ff9a3d);padding:16px;display:flex;'
    c = 'align-items:center;gap:10px;box-shadow:0 3px 12px #0003;position:sticky;top:0;z-index:100}'
    d = '.logo{background:white;color:#f68b1e;width:52px;height:52px;border-radius:50%;'
    e = 'display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:30px}'
    f = '.card{background:white;border-radius:20px;padding:22px;margin:14px;box-shadow:0 5px 15px #0001}'
    g = '.card-o{border-left:8px solid #f68b1e}'
    h = '.abtn{display:block;padding:20px;border-radius:16px;width:100%;text-align:center;'
    i = 'text-decoration:none;font-weight:bold;font-size:24px;margin-top:12px;box-sizing:border-box}'
    j = '.abtn-o{background:#f68b1e;color:white}'
    k = '.abtn-b{background:#111;color:white}'
    l = '.abtn-g{background:#0a8a0a;color:white}'
    m = '.abtn-w{background:white;color:#f68b1e;border:3px solid #f68b1e}'
    n = '.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;'
    o = 'justify-content:space-around;padding:14px 0;border-top:4px solid #f68b1e;z-index:999}'
    p = '.nav{text-align:center;text-decoration:none;color:#222;font-size:18px;font-weight:bold}'
    q = '#map{height:60vh;width:100%;border-radius:18px}'
    r = '.price{color:#f68b1e;font-weight:bold;font-size:28px}'
    s = '.big{font-size:30px;font-weight:bold}'
    return a + b + c + d + e + f + g + h + i + j + k + l + m + n + o + p + q + r + s

def bottom_nav():
    c = len(session.get('cart', []))
    b = ''
    if c > 0:
        b = '(' + str(c) + ')'
    return '<div class=bottom><a href=/ class=nav>Market<br>🏪</a><a href=/map class=nav>GPS<br>📍</a><a href=/post class=nav>Post<br>📸</a><a href=/cart class=nav>Cart ' + b + '<br>🛒</a><a href=/ai class=nav>AI<br>🤖</a></div>'

@app.route('/')
def home():
    st = get_style()
    html = '<style>' + st + '</style>'
    html += '<div class=top><div class=logo>E</div><b style=color:white;font-size:30px>EAZYMADE MARKET</b></div>'
    html += '<div class=card style=background:linear-gradient(135deg,#f68b1e,#000);color:white;text-align:center><h2 class=big>All Shops - Big Font 26px</h2><p>Buttons Fixed - All Routes Restored</p><a href=/map class=abtn style=background:white;color:#f68b1e>📍 VIEW MAP</a><a href=/ai class="abtn abtn-b">🤖 AI Assistant</a></div>'
    for name in shops:
        sh = shops[name]
        tot = 0
        for p in prods:
            if p['shop'] == name:
                tot += int(p['stock'])
        html += '<div class="card card-o"><b style=font-size:28px>' + name + '</b><br><span style=font-size:20px>' + sh['area'] + ' - ' + str(tot) + ' pairs TOTAL</span><a href=/shop/' + sh['own'] + ' class="abtn abtn-o">Enter Whole Shop</a><a href=/chat/' + sh['own'] + ' class="abtn abtn-b">💬 Chat Shop</a><a href=https://www.google.com/maps?q=' + str(sh['lat']) + ',' + str(sh['lng']) + ' target=_blank class="abtn abtn-w">📍 GPS Navigate</a></div>'
    for p in prods:
        html += '<div class=card><img src=' + p['img'] + ' style=width:100%;height:240px;object-fit:cover;border-radius:16px><br><b style=font-size:26px>' + p['name'] + '</b><br><span class=price>KSh ' + str(p['price']) + '</span> Stock ' + str(p['stock']) + '<a href=/add/' + str(p['id']) + ' class="abtn abtn-o">🛒 Add to Cart - FIXED</a></div>'
    html += '<div class=card><h3 class=big>Map</h3><div id=map></div></div>'
    html += '<link rel=stylesheet href=https://unpkg.com/leaflet@1.9.4/dist/leaflet.css>'
    html += '<script src=https://unpkg.com/leaflet@1.9.4/dist/leaflet.js></script>'
    html += '<script>var m=L.map("map").setView([-1.3956,36.7562],12);L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(m);'
    html += 'L.marker([-1.3956,36.7562]).addTo(m).bindPopup("Rongai");'
    html += 'L.marker([-1.38,36.78]).addTo(m).bindPopup("Kitengela");'
    html += 'L.marker([-1.40,36.74]).addTo(m).bindPopup("Kware");</script>'
    html += bottom_nav()
    return html

@app.route('/map')
def mp():
    return home()

@app.route('/shop/<own>')
def shop_page(own):
    st = get_style()
    sn = 'Rongai Shoe Center'
    for n in shops:
        if shops[n]['own'] == own:
            sn = n
    sh = shops[sn]
    tot = 0
    for p in prods:
        if p['shop'] == sn:
            tot += int(p['stock'])
    html = '<style>' + st + '</style><div class=top><div class=logo>E</div><b style=color:white>' + sn + '</b></div>'
    html += '<div class=card><h2 class=big>' + sn + ' WHOLE SHOP ' + str(tot) + ' pairs</h2><a href=/chat/' + own + ' class="abtn abtn-b">Chat Shop</a></div>'
    for p in prods:
        if p['shop'] == sn:
            html += '<div class=card><b>' + p['name'] + '</b> KSh ' + str(p['price']) + '<a href=/add/' + str(p['id']) + ' class="abtn abtn-o">Add to Cart</a></div>'
    html += bottom_nav()
    return html

@app.route('/add/<int:pid>')
def add(pid):
    c = session.get('cart', [])
    c.append(pid)
    session['cart'] = c
    return redirect('/cart')

@app.route('/cart')
def cart():
    st = get_style()
    c = session.get('cart', [])
    html = '<style>' + st + '</style><div class=top><div class=logo>E</div><b style=color:white>CART</b></div>'
    tot = 0
    cnt = 0
    for pid in c:
        for p in prods:
            if p['id'] == pid:
                html += '<div class=card>' + p['name'] + ' KSh ' + str(p['price']) + '</div>'
                tot += int(p['price'])
                cnt += 1
    html += '<div class=card style=background:#111;color:white><b class=big>TOTAL ' + str(cnt) + ' pairs KSh ' + str(tot) + '</b></div>'
    html += '<div class=card><a href=/ class="abtn abtn-b">Continue Shopping</a><a href=/clear class="abtn abtn-w">Clear Cart</a></div>'
    html += bottom_nav()
    return html

@app.route('/clear')
def clear():
    session['cart'] = []
    return redirect('/')

@app.route('/chat/<own>', methods=['GET', 'POST'])
def chat_page(own):
    st = get_style()
    sn = 'Rongai Shoe Center'
    for n in shops:
        if shops[n]['own'] == own:
            sn = n
    if sn not in chats:
        chats[sn] = []
    if request.method == 'POST':
