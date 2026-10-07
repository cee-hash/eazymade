from flask import Flask, request, render_template_string

app = Flask(__name__)

REAL_PHONE = "0116782556"
REAL_NAME = "John Thuo"

products = [
    {"id": 1, "name": "Jordan 4 Rongai", "price": 4500},
    {"id": 2, "name": "Nike Airforce Rongai", "price": 3800},
    {"id": 3, "name": "Adidas Rongai", "price": 4200},
]

HOME_HTML = """
<html>
<head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{font-family:Arial;background:#f2f2f7;margin:0;padding:15px}
.card{background:white;border-radius:15px;padding:15px;margin:15px 0;box-shadow:0 2px 10px #ccc}
.btn{background:#0a5c36;color:white;padding:12px 20px;border:none;border-radius:10px;width:100%;font-size:16px}
.real{color:#0a5c36;font-weight:bold;font-size:18px}
</style></head>
<body>
<h2 style="text-align:center">EazyMade - Rongai Shoes</h2>
<h3 style="text-align:center;color:green">LIPA REAL: {{phone}} - {{name}}</h3>
{% for p in products %}
<div class="card">
<h3>{{p.name}}</h3>
<p>Ksh {{p.price}}</p>
<a href="/lipa?id={{p.id}}"><button class="btn">Lipa {{p.price}}</button></a>
</div>
{% endfor %}
</body></html>
"""

LIPA_HTML = """
<html>
<head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{font-family:Arial;background:#f2f2f7;padding:15px}
.box{background:white;padding:20px;border-radius:15px;max-width:400px;margin:auto;border:2px solid #0a5c36}
.green{color:#0a5c36;font-size:22px;font-weight:bold}
input{width:100%;padding:12px;border-radius:8px;border:1px solid #ccc;margin:10px 0}
.btn{background:#0a5c36;color:white;padding:15px;border:none;border-radius:10px;width:100%;font-size:18px}
</style></head>
<body>
<div class="box">
<h2 style="text-align:center;color:#0a5c36">LIPA NA M-PESA REAL</h2>
<p>Product: <b>{{prod.name}}</b></p>
<p>Amount: <b>Ksh {{prod.price}}</b></p>
<hr>
<p class="green">Send to: {{phone}}</p>
<p>Name: <b>{{name}}</b></p>
<hr>
<p><b>1.</b> M-Pesa → Send Money</p>
<p><b>2.</b> Phone: <b>{{phone}}</b></p>
<p><b>3.</b> Amount: <b>{{prod.price}}</b></p>
<p><b>4.</b> PIN</p>
<p>Enter M-Pesa Code:</p>
<input id="code" placeholder="e.g. QGH7X9Y2ZJ">
<button class="btn" onclick="confirmPay()">CONFIRM PAYMENT</button>
<p id="msg" style="color:green;text-align:center;margin-top:15px"></p>
</div>
<script>
function confirmPay(){
 let c=document.getElementById('code').value;
 if(c.length<5){alert('Enter M-Pesa code');return;}
 document.getElementById('msg').innerHTML='✅ Payment '+c+' received! John will call you for delivery. Money sent to {{phone}}';
}
</script>
</body></html>
"""

@app.route("/")
def home():
    return render_template_string(HOME_HTML, products=products, phone=REAL_PHONE, name=REAL_NAME)

@app.route("/lipa")
def lipa():
    pid = int(request.args.get("id",1))
    prod = next((x for x in products if x["id"]==pid), products[0])
    return render_template_string(LIPA_HTML, prod=prod, phone=REAL_PHONE, name=REAL_NAME)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
