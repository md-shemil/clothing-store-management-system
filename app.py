from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# In-memory product data
products = [
    {"id": 1, "name": "T-shirt", "price": 200, "stock": 50},
    {"id": 2, "name": "Jeans", "price": 499, "stock": 30},
    {"id": 3, "name": "Sweater", "price": 500, "stock": 40},
]

# In-memory cart data
cart = []

@app.route("/")
def index():
    return render_template("index.html", products=products, cart=cart)

@app.route("/add_product_page")
def add_product_page():
    return render_template("add_product.html")

@app.route("/add_product", methods=["POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price"])
        stock = int(request.form["stock"])

        new_product = {
            "id": len(products) + 1,
            "name": name,
            "price": price,
            "stock": stock,
        }

        products.append(new_product)

    return redirect("/")

@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    product = next((p for p in products if p["id"] == product_id), None)

    if product and product["stock"] > 0:
        # Add the selected product to the cart
        cart.append(product.copy())

        # Reduce the stock of the product
        product["stock"] -= 1

    return redirect("/")

@app.route("/view_cart")
def view_cart():
    return render_template("cart.html", cart=cart)

@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    product = next((p for p in cart if p["id"] == product_id), None)

    if product:
        # Increase the stock of the product
        original_product = next((p for p in products if p["id"] == product_id), None)
        if original_product:
            original_product["stock"] += 1

        # Remove the selected product from the cart
        cart.remove(product)

    return redirect("/view_cart")

@app.route("/checkout", methods=["POST"])
def checkout():
    total = sum(item["price"] for item in cart)
    return render_template("bill.html", cart=cart, total=total)

if __name__ == "__main__":
    app.run(debug=True)
