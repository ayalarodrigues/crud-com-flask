from flask import Flask, render_template, request, url_for, redirect

from flask_sqlalchemy import SQLAlchemy

api = Flask(__name__)
api.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(api)

class Disp(db.Model):
    __tablename__ = 'dispositive'

    _id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    nome = db.Column(db.String)
    status = db.Column(db.String)

    def __init__(self, nome, status):
        self.nome = nome
        self.status = status


db.create_all()


@api.route("/index")
def index():
    return render_template("index.html")

@api.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")

@api.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method =="POST":
        nome = request.form.get("nome")
        status = request.form.get("status")

        if nome and status:
            d = Disp(nome, status)
            db.session.add(d)
            db.session.commit()
    return redirect(url_for("index"))

@api.route("/lista")
def lista():
    dispositivos = Disp.query.all()
    return render_template("lista.html", dispositivos = dispositivos)

@api.route("/excluir/<int:id>")
def excluir(id):
    dispositive = Disp.query.filter_by(_id=id).first()

    db.session.delete(dispositive)
    db.session.commit()

    dispositivos = Disp.query.all()
    return render_template("lista.html", dispositivos = dispositivos)


@api.route("/atualizar/<int:id>", methods = ['GET', 'POST'])
def atualizar(id):
    dispositive = Disp.query.filter_by(_id=id).first()
    if request.method =="POST":
        nome = request.form.get("nome")
        status = request.form.get("status")

        if nome and status:
            dispositive.nome = nome
            dispositive.status = status

            db.session.commit()

            return redirect(url_for("lista"))

    return render_template("atualizar.html", dispositive=dispositive)





if __name__ == '__main__':
    api.run(debug=True)

