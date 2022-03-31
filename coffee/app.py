from flask import Flask, redirect, render_template, request, make_response
import waitress
from sqlalchemy.orm import scoped_session

from coffee.db.database import engine, SessionLocal, Base
from coffee.entities import User, Auth, Shift, Sell, CoffeeType
from coffee.util import load_host_port

Base.metadata.create_all(bind=engine)

app = Flask(__name__)

app.db = scoped_session(SessionLocal)


@app.route('/')
def index():
    with app.app_context():
        me = Auth.me()

        if me is None:
            return redirect('/auth_page')

        if me.type == User.CASHIER:
            return redirect('/cashier')

        if me.type == User.MANAGER:
            return redirect('/manager')


@app.route('/auth', methods=['POST'])
def authorize():
    with app.app_context():
        result, answer = Auth.authorize()

        if result:
            response = make_response(redirect('/'))
            auth_id, auth_hash = answer
            response.set_cookie('auth_id', str(auth_id), max_age=Auth.AUTH_HASH_COOKIE_LIFESPAN)
            response.set_cookie('auth_hash', auth_hash, max_age=Auth.AUTH_HASH_COOKIE_LIFESPAN)
        else:
            response = make_response(redirect(f'/auth_page?error={answer}'))

        return response


@app.route('/auth_page', methods=['GET'])
def auth_page():
    with app.app_context():
        me = Auth.me()
        if me is not None:
            return redirect('/')

        error = request.values.get('error')

        result = render_template('html_begin.html', title='Авторизация')
        result += render_template('auth.html', error=error)
        result += render_template('html_end.html')

        return result


@app.route('/unauth')
def unauthorize():
    with app.app_context():
        Auth.unauthorize()

        response = make_response(redirect('/'))

        response.set_cookie('auth_id', '', expires=0)
        response.set_cookie('auth_hash', '', expires=0)

        return response


@app.route('/cashier')
def cashier():
    with app.app_context():
        me = Auth.me()
        if me is None or me.type != User.CASHIER:
            return redirect('/')

        shift = Shift.current_shift()

        result = ''
        if shift is None:
            result += render_template('html_begin.html', title='Открыть смену')
            result += render_template('cashier_top.html', name=me.name)
            result += render_template('open_shift.html')
            result += render_template('html_end.html')
        else:
            result += render_template('html_begin.html', title='Смена')
            result += render_template('cashier_top.html', name=me.name)
            result += render_template('sell.html', shift=shift.name, coffee_types=CoffeeType.get_list())
            result += render_template('html_end.html')
        return result


@app.route('/open_shift', methods=['POST'])
def open_shift():
    with app.app_context():
        me = Auth.me()
        if me is None or me.type != User.CASHIER:
            return redirect('/')

        if Shift.current_shift() is None:
            Shift.open_new(request.values.get('name'))
        return redirect('/')


@app.route('/sell', methods=['POST'])
def sell():
    with app.app_context():
        me = Auth.me()
        if me is None or me.type != User.CASHIER:
            return redirect('/')

        Sell.sell(me)
        return redirect('/')


@app.route('/close_shift')
def close_shift():
    with app.app_context():
        me = Auth.me()
        if me is None or me.type != User.CASHIER:
            return redirect('/')

        Shift.close_current()
        return redirect('/')


@app.route('/manager')
def manager():
    with app.app_context():
        me = Auth.me()
        if me is None or me.type != User.MANAGER:
            return redirect('/')

        sell_search_results = Sell.search()

        result = ''
        result += render_template('html_begin.html')
        result += render_template('manager_top.html', name=me.name)
        result += render_template('search_form.html', shifts=Shift.get_list(),
                                  cashiers=User.get_cashiers_list(), coffee_types=CoffeeType.get_list())
        if sell_search_results:
            result += render_template('search_results.html', results=sell_search_results)
        result += render_template('html_end.html')

        return result


if __name__ == '__main__':
    host, port = load_host_port.load()
    waitress.serve(app, host=host, port=port)
