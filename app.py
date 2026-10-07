from flask import Flask, request, redirect
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED = {'png','jpg','jpeg','webp'}

COMMISSION_RATE = 0.03
ADMIN_PASSWORD = "eazy2024"

def allowed_file(f):
    return '.' in f and f.rsplit('.',1)[1].lower() in ALLOWED

def safe_get(p, key, default=""):
    v = p.get(key, default)
    return default if v is None else v

products = [
    {"id":1,"name":"Jordan 4 Rongai","price":4500,"shop":"Rongai Shoes","location":"Rongai","image":"👟","desc":"Size 40-45 Original","phone":"254712345678","photo":""},
]

MPESA_SHORTCODE = os.getenv("MPESA_SHORTCODE", "174379")
MPESA_KEY = os.getenv("MPESA_KEY", "YOUR_CONSUMER_KEY")
MPESA_SECRET = os.getenv("MPESA_SECRET", "YOUR_CONSUMER_SECRET")


    print(f"REAL PAYMENT to 0116782556 Ksh {amount} from {phone}")
    return f"REAL LIPA: Send {amount} to 0116782556 - Name John Thuo"

def ai_search(query):
    query = query.lower()
    results = []
    for p in products:
        if query in safe_get(p,"name","").lower() or query in safe_get(p,"desc","").lower() or query in safe_get(p,"shop","").lower():
            results.append(p)
    return results

HOME_HTML = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>
body{margin:0;font-family:Arial;background:#f2f2f2}
.top{background:#0a5c36;color:#fff;padding:15px;font-weight:900;display:flex;justify-content:space-between}
.top a{color:orange;text-decoration:none;font-size:13px}
.ban{background:#ff3b30;color:#fff;text-align:center;padding:8px;font-weight:900;font-size:12px}
.search{padding:10px;background:#fff;display:flex;gap:5px}
.search input{flex:1;padding:10px;border-radius:8px;border:1px solid #ccc}
.search button{padding:10px;background:#0a5c36;color:#fff;border:none;border-radius:8px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:10px}
.card{background:#fff;border-radius:12px;overflow:hidden;text-decoration:none;color:#000;border:1px solid #ddd}
.pic{height:170px;background:#e8f5e9;display:flex;align-items:center;justify-content:center;overflow:hidden}
.pic img{width:100%;height:100%;object-fit:cover}
.info{padding:8px}.price{color:green;font-weight:900}.loc{font-size:11px;color:#666}
.sell{position:fixed;bottom:20px;right:15px;background:#0a5c36;color:#fff;padding:14px 22px;border-radius:30px;text-decoration:none;font-weight:900;border:2px solid orange}
</style></head><body>
<div class="top"><span>EAZY MADE</span><a href="/admin?pwd=eazy2024">OWNER</a></div>
<div class="ban">M-Pesa + AI Ready | Commission 3% | Delivery 80</div>
<form class="search" action="/ai-search"><input name="q" placeholder="AI tafuta: 'shoes black size 42 Rongai'"><button>AI Search</button></form>
<div class="grid">{items}</div>
<a class="sell" href="/sell">+ Uza FREE</a></body></html>
"""

SELL_HTML = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>
body{margin:0;font-family:Arial;background:#f2f2f2;padding:15px}
.box{background:#fff;border-radius:12px;padding:20px;max-width:500px;margin:auto}
input,select{width:100%;padding:12px;margin:8px 0;border:1px solid #ccc;border-radius:8px;box-sizing:border-box}
button{width:100%;padding:14px;background:#0a5c36;color:#fff;border:none;border-radius:8px;font-weight:900;font-size:18px}
</style></head><body><div class="box">
<h3>Uza Bidhaa - M-Pesa Ready</h3>
<form method="POST" enctype="multipart/form-data">
<input name="name" placeholder="Jina e.g. Jordan 4" required>
<input name="price" type="number" placeholder="Bei e.g. 4500" required>
<input name="shop" placeholder="Duka" required>
<input name="phone" placeholder="WhatsApp 2547..." required>
<select name="location"><option>Rongai</option><option>Kware</option><option>Nkoroi</option><option>Tuala</option></select>
<label>Picha Halisi:</label><input type="file" name="photo" accept="image/*" required>
<select name="image"><option>👟 Shoes</option><option>🥬 Mboga</option><option>🧥 Clothes</option><option>📱 Phone</option></select>
<input name="description" placeholder="Maelezo">
<button type="submit">Chapisha FREE</button>
</form><br><a href="/">← Rudi</a></div></body></html>
"""

@app.route("/")
def home():
    items=""
    for p in products:
        name = safe_get(p,"name","No name")[:18]
        shop = safe_get(p,"shop","")
        price = safe_get(p,"price",0)
        photo = safe_get(p,"photo","")
        emoji = safe_get(p,"image","👟") or "👟"
        pic = f'<img src="/{photo}">' if photo else f'<span style="font-size:60px">{emoji[0]}</span>'
        items+=f'<a class="card" href="/product/{p["id"]}"><div class="pic">{pic}</div><div class="info"><b>{name}</b><br><span class="loc">{shop}</span><br><span class="price">Ksh {price}</span></div></a>'
    return HOME_HTML.replace("{items}",items)

@app.route("/ai-search")
def aisearch():
    q=request.args.get("q","")
    results=ai_search(q) if q else products
    items=""
    for p in results:
        name = safe_get(p,"name","No name")[:18]
        shop = safe_get(p,"shop","")
        price = safe_get(p,"price",0)
        photo = safe_get(p,"photo","")
        emoji = safe_get(p,"image","👟") or "👟"
        pic = f'<img src="/{photo}">' if photo else f'<span style="font-size:60px">{emoji[0]}</span>'
        items+=f'<a class="card" href="/product/{p["id"]}"><div class="pic">{pic}</div><div class="info"><b>{name}</b><br><span class="loc">{shop}</span><br><span class="price">Ksh {price}</span></div></a>'
    if not items: items="<p style='padding:20px'>AI haijapata, jaribu 'shoes' au 'mboga'</p>"
    return HOME_HTML.replace("{items}",items)

@app.route("/sell", methods=["GET","POST"])
def sell():
    if request.method=="POST":
        file=request.files.get('photo')
        filename=""
        if file and file.filename and allowed_file(file.filename):
            safe=secure_filename(file.filename)
            nid=max(x["id"] for x in products)+1 if products else 1
            safe=f"{nid}_{safe}"
            path=os.path.join(app.config['UPLOAD_FOLDER'],safe)
            file.save(path)
            filename=path.replace("\\","/")
        nid=max(x["id"] for x in products)+1 if products else 1
        try:
            price=int(request.form.get("price",0) or 0)
        except:
            price=0
        products.append({
            "id":nid,
            "name":request.form.get("name") or "No name",
            "price":price,
            "shop":request.form.get("shop") or "Unknown",
            "location":request.form.get("location") or "Rongai",
            "image":request.form.get("image") or "👟",
            "phone":request.form.get("phone") or "254700000000",
            "desc":request.form.get("description") or "",
            "photo":filename
        })
        return redirect("/")
    return SELL_HTML

@app.route("/product/<int:pid>")
def prod(pid):
    p=next((x for x in products if x["id"]==pid), products[0] if products else None)
    if not p: return redirect("/")
    photo = safe_get(p,"photo","")
    emoji = safe_get(p,"image","👟") or "👟"
    pic=f'<img src="/{photo}">' if photo else f'<span style="font-size:100px">{emoji[0]}</span>'
    comm=int(safe_get(p,"price",0)*COMMISSION_RATE)
    return f"""<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>
    body{{margin:0;font-family:Arial;background:#f2f2f2;padding:15px}}.box{{background:#fff;border-radius:12px;padding:20px;max-width:500px;margin:auto;text-align:center}}
  .pic{{height:320px;background:#e8f5e9;border-radius:12px;overflow:hidden}}.pic img{{width:100%;height:100%;object-fit:cover}}
  .btn{{display:block;padding:14px;margin:8px 0;border-radius:8px;text-decoration:none;font-weight:900;color:#fff}}
  .wa{{background:#25D366}}.mpesa{{background:#0a5c36}}.back{{background:#ddd;color:#000}}</style></head><body><div class="box">
    <a href="/" class="btn back">← Rudi</a><div class="pic">{pic}</div><h2>{safe_get(p,"name")}</h2><p>{safe_get(p,"shop")} - {safe_get(p,"location")}</p>
    <h2 style="color:green">Ksh {safe_get(p,"price")}</h2><p>{safe_get(p,"desc")}</p><p>Your 3% = Ksh {comm}</p>
    <a class="btn wa" href="https://wa.me/{safe_get(p,"phone")}?text=Habari! Nimeona {safe_get(p,"name")} EAZY MADE">WhatsApp Seller</a>
    <a class="btn mpesa" href="/pay/{p["id"]}">Lipa na M-Pesa (STK Push)</a></div></body></html>"""

@app.route("/pay/<int:pid>")
def pay(pid):
    p=next((x for x in products if x["id"]==pid),None)
    if not p: return redirect("/")
    lipa_mpesa(safe_get(p,"phone"), safe_get(p,"price",0))
    return f"<h2 style='font-family:Arial;text-align:center;padding:40px'>M-Pesa STK sent! Check phone 254...<br>Ksh {safe_get(p,'price')}<br><br>When you get Daraja keys, this will be REAL.<br><br><a href='/'>Back</a></h2>"

@app.route("/admin")
def admin():
    if request.args.get("pwd","")!=ADMIN_PASSWORD:
        return f'<div style="padding:40px;font-family:Arial"><h2>Owner</h2><input id="p" type="password"><button onclick="location.href=\'/admin?pwd=\'+document.getElementById(\'p\').value">Login</button><br>pwd:{ADMIN_PASSWORD}</div>'
    total=len(products); val=sum(safe_get(p,"price",0) for p in products); earn=int(val*COMMISSION_RATE)
    rows="".join(f"<tr><td>{p['id']}</td><td>{safe_get(p,'name')}</td><td>{safe_get(p,'price')}</td><td style='color:green'>{int(safe_get(p,'price',0)*COMMISSION_RATE)}</td><td>{safe_get(p,'phone')}</td></tr>" for p in products)
    return f"<html><body style='font-family:Arial;padding:15px'><h2>OWNER OFFICE - M-Pesa + AI Ready</h2><h1 style='color:green'>Earning: Ksh {earn}</h1><p>Total {total} products, Value {val}</p><table border=1 cellpadding=5>{rows}</table><br><a href='/'>Home</a></body></html>"

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT",5000)), debug=False)
