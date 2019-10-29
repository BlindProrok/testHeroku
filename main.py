import cx_Oracle
from flask import Flask, render_template, request, flash
from forms.login import LoginForm


def create_app():

    app = Flask(__name__)

    return app


app = create_app()
app.secret_key = 'development key'


class Adapter:

    def __enter__(self):
        self.__db = cx_Oracle.connect("BlindProrok", "prorok2000", "User-PC/XE")
        self.__cursor = self.__db.cursor()
        return self

    def __exit__(self, type, value, traceback):
        self.__cursor.close()
        self.__db.close()

    def get_var2(self, my_var1):
        res = self.__cursor.callfunc("my_pack.get_var2", cx_Oracle.NUMBER, [my_var1])
        return res

adapter = Adapter()

@app.route('/', methods=['GET', 'POST'])
def index():

    return "Hello world!"


@app.route('/<a>+<b>', methods=['GET', 'POST'])
def addition(a, b):

    return str(eval(a) + eval(b))

@app.route('/secret_cheat_code', methods=['GET', 'POST'])
def contact():
    form = LoginForm()

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            print("Go to hell!")
            return render_template('login.html', form=form)
        else:
            print("Иди в пекло!")
            adapter.__enter__()
            adapter.get_var2(9)
            return 'success'

    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
