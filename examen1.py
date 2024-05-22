from flask import Flask, render_template, request, redirect, url_for, flash
import re

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para mostrar mensajes flash

# Lista para almacenar los productos
products = []

def calculate_iva(price):
    iva = round(price * 0.16, 2)
    total = round(price + iva, 2)
    return iva, total

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product = request.form['product'].strip()
        price = request.form['price'].strip()

        # Validación para que el nombre del producto solo contenga caracteres alfabéticos
        if not re.match("^[A-Za-záéíóúÁÉÍÓÚñÑ ]+$", product):
            flash('Por favor, ingrese un nombre de producto válido (solo caracteres alfabéticos).')
            return redirect(url_for('index'))

        if not product:
            flash('Por favor, ingrese un nombre de producto válido.')
            return redirect(url_for('index'))

        try:
            price_float = float(price)
            if price_float < 0:
                raise ValueError("El precio no puede ser negativo")

            iva, total = calculate_iva(price_float)
            products.append({
                'product': product,
                'price': f"{price_float:.2f}",
                'iva': f"{iva:.2f}",
                'total': f"{total:.2f}"
            })

            return redirect(url_for('index'))

        except ValueError:
            flash('Por favor, ingrese un precio válido (solo números y números positivos).')
            return redirect(url_for('index'))

    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
