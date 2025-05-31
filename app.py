from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__, template_folder='.')

db = {
    'host': 'localhost',
    'user': 'root',
    'password': 'alvaro321',
    'database': 'presupuesto_db'
}

def leer(campo):
    return float(request.form.get(campo, 0) or 0)

@app.route('/', methods=['GET', 'POST'])
def index():
    resultados = None
    nombre = ""
    error = None

    if request.method == 'POST':
        conn = mysql.connector.connect(**db)
        cur = conn.cursor()

        nombre = request.form.get('nombre', '').strip()
        ingresos = leer('salario') + leer('adicionales')

        datos = {
            'Hogar': leer('alquiler') + leer('internet') + leer('cable'),
            'Transporte': leer('combustible') + leer('publico'),
            'Educacion': leer('matricula') + leer('libros'),
            'Otros': leer('otros'),
            'Ahorro / Inversión': leer('ahorro'),
            'Ingresos': ingresos
        }

        gastos_totales = sum(monto for cat, monto in datos.items() if cat != 'Ingresos')

        if gastos_totales > ingresos:
            error = "ERROR, Los gastos superan los ingresos!"
        else:
     
            cur.execute("DELETE FROM movimientos WHERE nombre = %s", (nombre,))
            conn.commit()

        
            for cat, monto in datos.items():
                cur.execute("INSERT INTO movimientos (nombre, tipo, descripcion, monto) VALUES (%s, %s, %s, %s)",
                            (nombre, cat, cat, monto))
            conn.commit()


            cur.execute("SELECT tipo, SUM(monto) FROM movimientos WHERE nombre = %s GROUP BY tipo", (nombre,))
            resumen = dict(cur.fetchall())
            total = resumen.get('Ingresos', 1)
            resultados = {k: (round(v / total * 100, 2), v) for k, v in resumen.items()}

        cur.close()
        conn.close()

    return render_template('index.html', resultados=resultados, nombre=nombre, error=error)

if __name__ == '__main__':
    app.run(debug=True)
