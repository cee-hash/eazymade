from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <div style='background:black;color:white;padding:20px;text-align:center'>
    <div style='background:orange;color:white;width:50px;height:50px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:auto;font-size:30px'>E</div>
    <h1>EAZYMADE ARTIFICIAL MARKET</h1>
    <p>Logo works - Market LIVE</p>
    <a href='/map'><button style='padding:15px;background:orange;color:white;width:100%'>VIEW MAP</button></a>
    <br><br>
    <a href='/register'><button style='padding:15px;background:black;color:white;width:100%;border:1px solid white'>Register - Everyone</button></a>
    </div>
    <div style='padding:10px'>Shops: Rongai Shoe Center - 15 pairs in stock - Till 0116782556 - GPS -1.3956,36.7562</div>
    """

@app.route('/map')
def m():
    return "<h1>Real GPS Map</h1><p>Rongai -1.3956,36.7562</p><a href='/'>Back</a>"

@app.route('/register')
def r():
    return "<h1>Register Works</h1><p>Buyer or Seller + Own Till + GPS</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',10000)))
