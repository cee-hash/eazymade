from flask import Flask, render_template_string, request, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = "eazymade-rongai-2026"

# YOUR REAL TILL
TILL = "0116782556"
TILL_NAME = "John Thuo"

# PRODUCTS - you can add more here
products = [
    {"id":1, "name":"Jordan 1 Rongai", "price":4500, "image":"https://images.unsplash.com/photo-1600269452121-4f2416e55c28?w=500", "seller":"John", "size":"42"},
    {"id":2, "name":"Air Max 90", "price":3800, "image":"https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500", "seller":"John", "size":"41"},
    {"id":3, "name":"Yeezy Boost", "price":4200, "image":"https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=500", "seller":"Mike", "size":"43"},
]

HTML_HOME = """
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{font-family:Arial;margin:0;background:#f5f5f5}
.header{background:#f68b1e;padding:12px;color:white;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:10}
.logo{font-weight:bold;font-size:20px}
.search{width:50%;padding:8px;border-radius:4px;border:none}
.cart{color:white;text-decoration:none;font-weight:bold}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:10px}
.card{background:white;border-radius:8px;padding:10px;text-align:center;box-shadow:0 2px 4px #ddd}
.card img{width:100%;height:130px;object-fit:cover;border-radius:6px}
.btn{background:#f68b1e;color:white;border:none;padding:8px 12px;border-radius:4px;width:100%;margin-top:6px;font-weight:bold}
.btn-lipa{background:green}
.price{color:#f68b1e;font-weight:bold;font-size:18px}
.till{background:#000;color:#0f0;padding:8px;text-align:center;font-weight:bold}
</style>
</head>
<body>
<div class="till">LIPA REAL: {{till}} - {{till_name}} (M-PESA)</div>
<div class="header">
<div class="logo">EazyMade</div>
<input class="search" placeholder="Search Jordan, Yeezy..." onkeyup="search(this.value)">
<a class="cart" href="/cart">🛒 Cart ({{cart_count}})</a>
</div>
<div class="grid">
{% for p in products %}
<div class="card" data-name="{{p.name.lower()}}">
<img src="{{p.image}}">
<div><b>{{p.name}}</b><br><small>Size {{p.size}} | Seller: {{p.seller}}</small></div>
<div class="price">KSh {{p.price}}</div>
<a href="/add/{{p.id}}"><button class="btn">Add to Cart</button></a>
<a href="/buy/{{p.id}}"><button class="btn btn-lipa">Lipa {{p.price}}</button></a>
</div>
{% endfor %}
</div>
<script>
function search(v){
 v=v.toLowerCase();
 document.querySelectorAll('.card').forEach(c=>{
  c.style.display=c.dataset.name.includes(v)?'block':'none'
 })
}
</script>
</body>
</html>
"""

HTML_CART = """
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{font-family:Arial;margin:0;padding:10px;background:#f5f5f5}
.card{background:white;padding:12px;margin:8px 0;border-radius:8px;display:flex;gap:10px}
img{width:80px;height:80px;object-fit:cover;border-radius:6px}
.btn{background:#f68b1e;color:white;border:none;padding:12px;width:100%;border-radius:6px;font-weight:bold;font-size:18px}
.total{font-size:22px;font-weight:bold;text-align:right;margin:10px 0}
</style>
</head>
<body>
<h2>Your Cart ({{count}})</h2>
{% for p in cart_items %}
<div class="card">
<img src="{{p.image}}">
<div><b>{{p.name}}</b><br>KSh {{p.price}}<br><a href="/remove/{{p.id}}">Remove</a></div>
</div>
{% endfor %}
<div class="total">Total: KSh {{total}}</div>
{% if total>0 %}
<a href="/checkout"><button class="btn">LIPA KSh {{total}} to {{till}}<br><small>{{till_name}}</small></button></a>
{% else %}
<p>Cart empty - <a href="/">Continue Shopping</a></p>
{% endif %}
</body>
</html>
"""

HTML_CHECKOUT = """
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{font-family:Arial;text-align:center;padding:20px;background:#f5f5f5}
.box{background:white;padding:20px;border-radius:12px;max-width:400px;margin:auto}
.big{font-size:48px}
</style>
</head>
<body>
<div class="box">
<div class="big">✅</div>
<h2>Order Received!</h2>
<p>Total: <b>KSh {{total}}</b></p>
<p>Pay to Till:</p>
<h1 style="color:green">{{till}}</h1>
<p>{{till_name}}</p>
<hr>
<p><b>Steps:</b><br>1. Go M-Pesa<br>2. Lipa na M-Pesa > Buy Goods<br>3. Till: {{till}}<br>4. Amount: {{total}}</p>
<p>We will deliver in Rongai in 2hrs!</p>
<a href="/">Back to Shop</a>
</div>
</body>
</html>
"""

@app.route('/')
def home():
    cart = session.get('cart', [])
    return render_template_string(HTML_HOME, products=products, till=TILL, till_name=TILL_NAME, cart_count=len(cart))

@app.route('/add/<int:pid>')
def add(pid):
    cart = session.get('cart', [])
    cart.append(pid)
    session['cart'] = cart
    return redirect('/')

@app.route('/buy/<int:pid>')
def buy(pid):
    session['cart'] = [pid]
    return redirect('/cart')

@app.route('/cart')
def cart_page():
    cart_ids = session.get('cart', [])
    cart_items = [p for p in products if p['id'] in cart_ids]
    total = sum(p['price'] for p in cart_items)
    return render_template_string(HTML_CART, cart_items=cart_items, total=total, count=len(cart_items), till=TILL)

@app.route('/remove/<int:pid>')
def remove(pid):
    cart = session.get('cart', [])
    if pid in cart: cart.remove(pid)
    session['cart'] = cart
    return redirect('/cart')

@app.route('/checkout')
def checkout():
    cart_ids = session.get('cart', [])
    cart_items = [p for p in products if p['id'] in cart_ids]
    total = sum(p['price'] for p in cart_items)
    session['cart'] = []
    return render_template_string(HTML_CHECKOUT, total=total, till=TILL, till_name=TILL_NAME)

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        new_id = max([p['id'] for p in products]) + 1 if products else 1
        products.append({
            "id": new_id,
            "name": request.form['name'],
            "price": int(request.form['price']),
            "image": request.form['image'],
            "seller": request.form['seller'],
            "size": request.form['size']
        })
        return redirect('/')
    return '''
    <form method="post" style="padding:20px;font-family:Arial">
    <h2>Add New Shoe - EazyMade Admin</h2>
    Name: <input name="name" style="width:100%;padding:8px"><br><br>
    Price: <input name="price" type="number" style="width:100%;padding:8px"><br><br>
    Size: <input name="size" style="width:100%;padding:8px"><br><br>
    Seller: <input name="seller" value="John" style="width:100%;padding:8px"><br><br>
    Image URL: <input name="image" style="width:100%;padding:8px" value="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500"><br><br>
    <button style="background:#f68b1e;color:white;padding:12px;width:100%;border:none;border-radius:6px;font-weight:bold">ADD SHOE</button>
    </form>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
