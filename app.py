from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
x1=''
class sign_data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(5000))

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods = ['POST', 'GET'])
def index():
    global x1
    # signed_file =
    if request.method == "POST":
        data = request.form['data']
        key = Fernet.generate_key()
        fernet = Fernet(key) 
        encrypted_data = fernet.encrypt(data.encode())
        x1=encrypted_data
        new_data = sign_data(data = encrypted_data)
        try:
            # Adding new task to our db session
            db.session.add(new_data)
            print(encrypted_data)
            print("------------------------------")
            print(x1)
            # commit
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your data"

    else:
        # signed_data_ = sign_data.query.filterby().first()
        signed_data_ = sign_data.query.with_entities(sign_data.data).first()
        # db.session.delete(signed_data_)
        print("-----",x1)
        ani=x1
        return render_template('index.html', signed_data_ = ani)
        

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
