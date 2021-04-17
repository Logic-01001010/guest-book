from flask import Flask, render_template, request, redirect
import pymysql
import hashlib
import os

app = Flask(__name__)


@app.route('/clean')

def clean():

    conn = pymysql.connect(host='localhost', user='root', password='your_password', db='homepage', charset='utf8')
    cur = conn.cursor()

    query = "DELETE FROM guest_book;"

    print(query)

    cur.execute(query)
    conn.commit()

    conn.close()


    return redirect('/')



@app.route('/edit', methods=['GET', 'POST'])

def edit():

    address = request.remote_addr

    try:
        img = request.files['img']

        img_name = img.filename

        name,ext = os.path.splitext(img_name)

        result = hashlib.md5(name.encode())

        filename = result.hexdigest()
        filename = filename[:10] + ext

        img.save("static/"+filename)

        img_name = filename

    except:
        img_name = "files/default.jpg"


    try:
        comment = request.form['comment']

        comment = comment.replace("\'", "\"")
    except:
        comment = "NULL"


    print(address)
    print(img_name)
    print(comment)


    conn = pymysql.connect(host='localhost', user='root', password='your_password', db='homepage', charset='utf8')
    cur = conn.cursor()

    query = "INSERT INTO guest_book (address, img, comment, time) values("+"\'"+address+"\'"+","+"\'"+img_name+"\'"+","+"\'"+comment+"\'"+", now())"

    print(query)

    cur.execute(query)
    conn.commit()

    conn.close()


    return redirect(request.referrer)

@app.route('/')

def index():


    conn = pymysql.connect(host='localhost', user='root', password='your_password', db='homepage', charset='utf8mb4')
    cur = conn.cursor()

    query = "SELECT * FROM guest_book ORDER BY time DESC"

    cur.execute(query)

    result = cur.fetchall()

    conn.close()


    return render_template('main.html', result=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80', debug=True)

