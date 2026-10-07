from flask import Flask
app = Flask(__name__)
import os

shops = ["Rongai Shoe Center", "Kitengela Sneakers", "Kware Market"]

@app.route("/")
def home():
    html = """
    <style>
    body{margin:0;background:#f0f2f5;padding-bottom:80px;font-family:Arial;font-size:22px}
    .card{background:white;margin:10px;padding:16px;border-radius:12px}
    .btn{padding:16px;width:100%;background:#f68b1e;color:white;border:none;border-radius:10px;font-size:20px;font-weight:bold}
    .bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:10px;border-top:3px solid #f68b1e}
    #map{height:85vh;width:100%}
    </style>
    <div style=background:#f68b1e;padding:12px><b style=color:white;font-size:24px>EAZYMADE MARKET - ALL SHOPS LIVE</b></div>
    <div style=background:black;color:white;padding:16px;margin:10px;border-radius:12px;text-align:center>
    <h2>ALL SHOPS - WHOLE PAGE MAP - BIG FONT</h2>
    <p>Green deploy test - V24</p>
    </div>
    """
    for s in shops:
        html += "<div class=card><b>" + s + "</b><br>20 pairs TOTAL - Whole Shop<br><button class=btn>Enter Whole Shop</button></div>"
    
    html += """
    <div class=card><b>Jordan 1</b><br>KSh 4500 - Stock 10<br><button class=btn>Add to Cart BIG</button></div>
    <div id=map></div>
    <link rel=stylesheet href=https://unpkg.com/leaflet@1.9.4/dist/leaflet.css>
    <script src=https://unpkg.com/leaflet@1.9.4/dist/leaflet.js></script>
    <script>
    var m=L.map('map').setView([-1.3956,36.7562],12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(m);
    L.marker([-1.3956,36.7562]).addTo(m).bindPopup('Rongai Shoe Center');
    L.marker([-1.38,36.78]).addTo(m).bindPopup('Kitengela Sneakers');
    L.marker([-1.40,36.74]).addTo(m).bindPopup('Kware Market');
    </script>
    <div class=bottom><a href=/>Market</a><a href=/map>GPS</a><a href=/post>Post</a><a href=/cart>Cart</a><a href=/register>Join</a></div>
    """
    return html

@app.route("/map")
def mp():
    return home()

@app.route("/post")
def post():
    return "<h2>Post page - Phone upload coming</h2><a href=/>Back</a>"

@app.route("/cart")
def cart():
    return "<h2>Cart - Whole Shop Total</h2><a href=/>Back</a>"

@app.route("/register")
def reg():
    return "<h2>Register Shop - All Shops Join</h2><a href=/>Back</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
