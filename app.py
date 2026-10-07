from flask import Flask, request, redirect, session
import os, base64

app = Flask(__name__)
app.secret_key = 'v28friendly'

shops = {
    'Rongai Shoe Center': {'own': 'admin', 'ok': True, 'lat': -1.3956, 'lng': 36.7562, 'area': 'Rongai Town', 'till': '0116782556'},
    'Kitengela Sneakers': {'own': 'kiten', 'ok': True, 'lat': -1.38, 'lng': 36.78, 'area': 'Kitengela', 'till': '0712345678'},
    'Kware Market': {'own': 'kware', 'ok': True, 'lat': -1.40, 'lng': 36.74, 'area': 'Kware', 'till': '0722000000'}
}

prods = [
    {'id': 1, 'name': 'Jordan 1 Retro', 'price': 4500, 'img': 'https://via.placeholder.com/400', 'shop': 'Rongai Shoe Center', 'stock': 10},
    {'id': 2, 'name': 'Air Max 90', 'price': 3800, 'img': 'https://via.placeholder.com/400', 'shop': 'Kitengela Sneakers', 'stock': 15}
]

chats = {'Rongai Shoe Center': [], 'Kitengela Sneakers': [], 'Kware Market': []}

def get_style():
    a = 'body{margin:0;background:#f0f2f5;padding-bottom:110px;font-family:Arial;font-size:20px}'
    b = '.top{background:linear-gradient(90deg,#f68b1e,#ff9a3d);padding:14px;display:flex;'
    c = 'align-items:center;gap:10px;box-shadow:0 3px 10px #0003;position:sticky;top:0;z-index:100}'
    d = '.logo{background:white;color:#f68b1e;width:46px;height:46px;border-radius:50%;'
    e = 'display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:24px}'
    f = '.card{background:white;border-radius:18px;padding:18px;margin:12px;box-shadow:0 4px 12px #0001;'
    g = 'border:1px solid #eee}'
    h = '.card-o{border-left:7px solid #f68b1e}'
    i = '.btn{padding:18px;border-radius:14px;width:100%;border:none;font-weight:bold;font-size:20px;margin-top:10px}'
    j = '.btn-o{background:linear-gradient(90deg,#f68b1e,#ff6a00);color:white;box-shadow:0 3px 8px #f68b1e66}'
    k = '.btn-b{background:#111;color:white}'
    l = '.btn-g{background:linear-gradient(90deg,#0a8a0a,#2ecc71);color:white}'
    m = '.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;'
    n = 'justify-content:space-around;padding:12px 0;border-top:3px solid #f68b1e;box-shadow:0 -2px 10px #0002;z-index:999}'
    o = '.nav{text-align:center;text-decoration:none;color:#222;font-size:15px;font-weight:bold}'
    p = '#map{height:65vh;width:100%;border-radius:16px;box-shadow:0 4px 12px #0002}'
    q = '.badge{background:red;color:white;border-radius:50%;padding:3px 8px;font-size:13px}'
    r = '.price{color:#f68b1e;font-weight:bold;font-size:22px}'
    s = '.big{font-size:24px;font-weight:bold}'
    return a + b + c + d + e + f + g + h + i + j + k + l + m + n + o + p + q + r + s

def bottom_nav():
    c = len(session.get('cart', []))
    badge = ''
    if c > 0:
        badge = '<span class=badge>' + str(c) + '</span>'
    return '<div class=bottom><a href=/ class=nav>Market<br>🏪</a><a href=/map class=nav>GPS<br>📍</a><a href=/post class=nav>Post<br>📸</a><a href=/cart class=nav>Cart ' + badge + '<br>🛒</a><a href=/ai class=nav>AI<br>🤖</a></div>'

@app.route('/')
def home():
    st = get_style()
    html = '<style>' + st + '</style>'
    html += '<div class=top><div class=logo>E</div><b style=color:white;font-size:24px>EAZYMADE MARKET</b><span style=margin-left:auto;color:white;font-size:13px;background:#0003;padding:4px 10px;border-radius:20px>ALL SHOPS LIVE</span></div>'
    html += '<div class=card style=background:linear-gradient(135deg,#f68b1e,#000);color:white;text-align:center><h2 class=big style=margin:8px 0>🛍️ All Shops - Decorated Friendly</h2><p style=font-size:18px;opacity:.9>Big fonts 22px - Whole Shop Total - Chat + AI</p><a href=/map><button class=btn style=background:white;color:#f68b1e>📍 VIEW MAP ALL SHOPS FULL PAGE</button></a><a href=/ai><button class=btn style=background:#111;color:white;margin-top:8px>🤖 Ask AI - Find Shoes</button></a></div>'
    for name in shops:
        sh = shops[name]
        tot = 0
        cnt = 0
        for p in prods:
            if p['shop'] == name:
                tot += int(p['stock'])
                cnt += 1
        html += '<div class="card card-o"><b style=font-size:22px>🏬 ' + name + '</b><br><span style=color:#666;font-size:16px>' + sh['area'] + ' • ' + str(cnt) + ' types • ' + str(tot) + ' pairs TOTAL Whole Shop</span><br><div style=display:flex;gap:8px;margin-top:10px><a href=/shop/' + sh['own'] + ' style=flex:1><button class=btn-o style=padding:14px;width:100%;border:none;border-radius:12px;color:white;font-weight:bold>Enter Shop</button></a><a href=/chat/' + sh['own'] + ' style=flex:1><button class=btn-b style=padding:14px;width:100%;border:none;border-radius:12px;color:white;font-weight:bold>💬 Chat Shop</button></a></div></div>'
    for p in prods:
        html += '<div class=card><img src=' + p['img'] + ' style=width:100%;height:220px;object-fit:cover;border-radius:14px;background:#eee><br><b style=font-size:20px>' + p['name'] + '</b> <span style=color:#888;font-size:15px>' + p['shop'] + '</span><br><span class=price>KSh ' + str(p['price']) + '</span> <span style=color:#666>| Stock ' + str(p['stock']) + ' pairs</span><br><a href=/add/' + str(p['id']) + '><button class=btn btn-o>🛒 Add to Cart BIG 22px</button></a></div>'
    html += '<div class=card><h3 style=font-size:22px>📍 All Shops GPS Map 65vh Decorated</h3><div id=map></div></div>'
    html += '<link rel=stylesheet href=https://unpkg.com/leaflet@1.9.4/dist/leaflet.css>'
    html += '<script src=https://unpkg.com/leaflet@1.9.4/dist/leaflet.js></script>'
    html += '<script>var m=L.map("map").setView([-1.3956,36.7562],12);L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(m);'
    html += 'L.marker([-1.3956,36.7562]).addTo(m).bindPopup("Rongai Shoe Center<br><a href=/shop/admin>Enter</a>");'
    html += 'L.marker([-1.38,36.78]).addTo(m).bindPopup("Kitengela Sneakers<br><a href=/shop/kiten>Enter</a>");'
    html += 'L.marker([-1.40,36.74]).addTo(m).bindPopup("Kware Market<br><a href=/shop/kware>Enter</a>");</script>'
    html += bottom_nav()
    return html

@app.route('/map')
def mp():
    return home()

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
    html = '<style>' + st + '</style><div class=top><div class=logo>E</div><b style=color:white;font-size:22px>CART - Whole Shop</b></div>'
    tot = 0
    cnt = 0
    for pid in c:
        for p in prods:
            if p['id'] == pid:
                html += '<div class=card><b>' + p['name'] + '</b> - KSh ' + str(p['price']) + '</div>'
                tot += int(p['price'])
                cnt += 1
    html += '<div class=card style=background:#111;color:white;text-align:center><b class=big>TOTAL ' + str(cnt) + ' pairs KSh ' + str(tot) + '</b></div>'
    html += '<div class=card><a href=https://wa.me/254116782556?text=Order ' + str(cnt) + ' pairs KSh ' + str(tot) + '><button class=btn btn-g>💬 Order WhatsApp - Private Till Hidden</button></a><a href=/><button class=btn btn-b>Continue Shopping</button></a><a href=/clear><button class=btn>Clear Cart</button></a></div>'
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
    if request.method == 'POST':
        msg = request.form.get('msg', '')
        if msg!= '':
            if sn in chats:
                chats[sn].append(msg)
            else:
                chats[sn] = [msg]
    html = '<style>' + st + '</style><div class=top><div class=logo>E</div><b style=color:white>💬 Chat ' + sn + '</b></div>'
    html += '<div class=card><h3 style=font-size:22px>Chat with Shop - Whole Shop Total before visit</h3>'
    html += '<form method=post style=display:flex;gap:6px><input name=msg placeholder=Ask about stock price size required style=flex:1;padding:14px;border-radius:12px;border:2px solid #ddd><button class=btn-o style=padding:14px 20px;border:none;border-radius:12px;color:white>Send</button></form></div>'
    html += '<div class=card><b>Messages:</b><br>'
    if sn in chats:
        for m in chats[sn][-10:]:
            html += '<div style=background:#f5f5f5;padding:10px;border-radius:10px;margin:6px 0>' + m + '</div>'
    html += '</div><div class=card><a href=/shop/' + own + '><button class=btn btn-b>Back to Whole Shop ' + sn + '</button></a></div>'
    html += bottom_nav()
    return html

@app.route('/ai', methods=['GET', 'POST'])
def ai_page():
    st = get_style()
    ans
