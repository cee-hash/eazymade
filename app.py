from flask import Flask, request, redirect, session
import os, base64

app = Flask(__name__)
app.secret_key = 'v27green'

shops = {
    'Rongai Shoe Center': {'own': 'admin', 'ok': True, 'lat': -1.3956, 'lng': 36.7562, 'area': 'Rongai Town', 'till': '0116782556'},
    'Kitengela Sneakers': {'own': 'kiten', 'ok': True, 'lat': -1.38, 'lng': 36.78, 'area': 'Kitengela', 'till': '0712345678'},
    'Kware Market': {'own': 'kware', 'ok': True, 'lat': -1.40, 'lng': 36.74, 'area': 'Kware', 'till': '0722000000'}
}

prods = [
    {'id': 1, 'name': 'Jordan 1', 'price': 4500, 'img': 'https://via.placeholder.com/400', 'shop': 'Rongai Shoe Center', 'stock': 10},
    {'id': 2, 'name': 'Air Max', 'price': 3800, 'img': 'https://via.placeholder.com/400', 'shop': 'Kitengela Sneakers', 'stock': 15}
]

def get_style():
    a = 'body{margin:0;background:#f5f5f5;padding-bottom:90px;font-family:Arial}'
    b = '.top{background:#f68b1e;padding:10px;display:flex;gap:8px;align-items:center}'
    c = '.logo{background:white;color:#f68b1e;width:40px;height:40px;border-radius:50%;'
    d = 'display:flex;align-items:center;justify-content:center;font-weight:bold}'
    e = '.card{background:white;border-radius:12px;padding:14px;margin:8px;box-shadow:0 1px 4px #0002}'
    f = '.btn{padding:14px;border-radius:10px;width:100%;border:none;font-weight:bold;font-size:16px}'
    g = '.btn-o{background:#f68b1e;color:white}'
    h = '.btn-b{background:#111;color:white}'
    i = '.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;'
    j = 'justify-content:space-around;padding:8px 0;border-top:2px solid #f68b1e}'
    k = '#map{height:60vh;width:100%;border-radius:10px}'
    return a + b + c + d + e + f + g + h + i + j + k

def bottom_nav():
    c = len(session.get('cart', []))
    txt = str(c)
    if c == 0:
        txt = ''
    return '<div class=bottom><a href=/>Market</a><a href=/map>GPS</a><a href=/post>Post</a><a href=/cart>Cart ' + txt + '</a><a href=/register>Join</a></div>'

@app.route('/')
def home():
    st = get_style()
    html = '<style>' + st + '</style>'
    html += '<div class=top><div class=logo>E</div><b style=color:white>EAZYMADE MARKET</b></div>'
    html += '<div class=card style=background:#111;color:white;text-align:center><h3>ALL SHOPS - Friendly UI V27</h3><p>Big font - Map 60vh - User friendly</p><a href=/map><button class=btn style=background:white;color:#f68b1e>VIEW MAP ALL SHOPS</button></a></div>'
    for name in shops:
        sh = shops[name]
        tot = 0
        for p in prods:
            if p['shop'] == name:
                tot += int(p['stock'])
        html += '<div class=card style=border-left:5px solid #f68b1e><b>' + name + '</b><br>' + sh['area'] + ' - ' + str(tot) + ' pairs TOTAL<br><a href=/shop/' + sh['own'] + '><button class=btn btn-o>Enter Whole Shop</button></a></div>'
    for p in prods:
        html += '<div class=card><img src=' + p['img'] + ' style=width:100%;height:180px;object-fit:cover;border-radius:10px><br><b>' + p['name'] + '</b> ' + p['shop'] + '<br>KSh ' + str(p['price']) + ' Stock ' + str(p['stock']) + '<br><a href=/add/' + str(p['id']) + '><button class=btn btn-o>Add to Cart BIG</button></a></div>'
    html += '<div class=card><div id=map></div></div>'
    html += '<link rel=stylesheet href=https://unpkg.com/leaflet@1.9.4/dist/leaflet.css>'
    html += '<script src=https://unpkg.com/leaflet@1.9.4/dist/leaflet.js></script>'
    html += '<script>var m=L.map("map").setView([-1.3956,36.7562],12);L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(m);'
    html += 'L.marker([-1.3956,36.7562]).addTo(m).bindPopup("Rongai Shoe Center");'
    html += 'L.marker([-1.38,36.78]).addTo(m).bindPopup("Kitengela Sneakers");'
    html += 'L.marker([-1.40,36.74]).addTo(m).bindPopup("Kware Market");</script>'
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
    html = '<style>' + st + '</style><div class=top><div class=logo>E</div><b style=color:white>CART</b></div>'
    tot = 0
    cnt = 0
    for pid in c:
        for p in prods:
            if p['id'] == pid:
                html += '<div class=card>' + p['name'] + ' KSh ' + str(p['price']) + '</div>'
                tot += int(p['price'])
                cnt += 1
    html += '<div class=card style=background:#111;color:white><b>TOTAL ' + str(cnt) + ' pairs KSh ' + str(tot) + '</b></div>'
    html += '<div class=card><a href=/><button class=btn btn-b>Continue Shopping</button></a><a href=/clear><button class=btn>Clear</button></a></div>'
    html += bottom_nav()
    return html

@app.route('/clear')
def clear():
    session['cart'] = []
    return redirect('/')

@app.route('/post', methods=['GET', 'POST'])
def post_page():
    st = get_style()
    if request.method == 'POST':
        img = 'https://via.placeholder.com/400'
        f = request.files.get('pic')
        if f:
            if f.filename!= '':
                img = 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode()
        prods.append({'id': len(prods)+1, 'name': request.form['name'], 'price': request.form['price'], 'img': img, 'shop': 'Rongai Shoe Center', 'stock': request.form['stock']})
        return redirect('/')
    html = '<style>' + st + '</style><div class=top><div class=logo>E</div><b style=color:white>Post Phone Upload</b></div>'
    html += '<div class=card><form method=post enctype=multipart/form-data>Name:<input name=name required>Price:<input name=price required>Stock:<input name=stock required><input type=file name=pic accept=image/* capture=environment><button class=btn btn-o>POST</button></form></div>'
    html += bottom_nav()
    return html

@app.route('/shop/<own>')
def shop_page(own):
    st = get_style()
    sn = 'Rongai Shoe Center'
    for n in shops:
        if shops[n]['own'] == own:
            sn = n
    html = '<style>' + st + '</style><div class=top><div class=logo>E</div><b style=color:white>' + sn + '</b></div>'
    html += '<div class=card><b>' + sn + ' WHOLE SHOP</b></div>'
    for p in prods:
        if p['shop'] == sn:
            html += '<div class=card>' + p['name'] + ' KSh ' + str(p['price']) + '<br><a href=/add/' + str(p['id']) + '><button class=btn btn-o>Add to Cart</button></a></div>'
    html += bottom_nav()
    return html

@app.route('/register', methods=['GET', 'POST'])
def reg():
    st = get_style()
    if request.method == 'POST':
        sn = request.form['shop']
        u = request.form['user'].lower()
        shops[sn] = {'own': u, 'ok': False, 'lat': -1.3956, 'lng': 36.7562, 'area': 'New', 'till': '0000'}
        return redirect('/')
    html = '<style>' + st + '</style><div class=card><form method=post>User:<input name=user required>Shop:<input name=shop required><button class=btn btn-o>Register</button></form></div>' + bottom_nav()
    return html

@app.route('/office', methods=['GET', 'POST'])
def off():
    st = get_style()
    if request.method == 'POST':
        if request.form.get('password') == '0116782556':
            session['off'] = True
    if not session.get('off'):
        return '<style>' + st + '</style><div class=card><form method=post><input name=password type=password placeholder=pass><button class=btn btn-b>Enter</button></form></div>'
    html = '<style>' + st + '</style><div class=card><h3>Office</h3></div>'
    for n in shops:
        html += '<div class=card>' + n + '</div>'
    html += bottom_nav()
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
