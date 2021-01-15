from flask import Flask, render_template, url_for, request, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL(app)

app.config['SECRET_KEY'] = 'app developer secrets'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'buku'

@app.route('/')
def index():
    query = mysql.connect.cursor()
    query.execute('SELECT * FROM buku')
    data = query.fetchall()
    return render_template('book.html', data=data)

@app.route('/create', methods=["GET", "POST"])
def create():
    if request.method == "POST":
        
        judul = request.form['judul']
        penulis = request.form['penulis']
        penerbit = request.form['penerbit']
        tahun = request.form['tahun']

        query = mysql.connection.cursor()
        query.execute('INSERT INTO buku VALUES (NULL, %s, %s, %s, %s)', (
            judul, penulis, penerbit, tahun
        ))
        mysql.connection.commit()

        flash("Data buku berhasil ditambahkan....")
        return redirect(url_for('index'))
        
    return render_template('create.html')

@app.route('/update/<id>', methods=["GET", "POST"])
def update(id):

    if request.method == "POST":

        judul = request.form['judul']
        penulis = request.form['penulis']
        penerbit = request.form['penerbit']
        tahun = request.form['tahun']

        query = mysql.connection.cursor()
        query.execute('UPDATE buku SET judul=%s, penulis=%s, penerbit=%s, tahun=%s WHERE id_buku=%s', (
            judul, penulis, penerbit, tahun, id
        ))
        mysql.connection.commit()

        flash("Data buku berhasil diperbarui....")
        return redirect(url_for('index'))
    
    query = mysql.connection.cursor()
    query.execute('SELECT * FROM buku WHERE id_buku=%s', (id,))
    data = query.fetchall()
    return render_template('update.html', data=data)

@app.route('/delete/<id>')
def delete(id):

    query = mysql.connection.cursor()
    query.execute('DELETE FROM buku WHERE id_buku=%s', (id,))
    mysql.connection.commit()

    flash("Data buku berhasil dihapus....")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)