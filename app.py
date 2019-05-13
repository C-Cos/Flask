#!/usr/bin/env python3
import os
from flask import Flask
from Controllers.controller import new, log, index, display_user, remove, update
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, current_app, jsonify
from flask.cli import with_appcontext
from Config.db import get_db
from werkzeug.security import check_password_hash


# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def show_entries():
    db = get_db()
    users = index(db)
    return render_template('index.html', users=users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        new(db, name, email, password)
        flash('New entry was successfully posted')
        return redirect(url_for('login'))
  
    return render_template('register.html')

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = log(db, username)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('show_entries'))
        flash(error)
    return render_template('login.html')

@app.route('/crud/<userid>', methods=['GET', 'PUT', 'DELETE'])
def crud(userid):
    if request.method == 'GET':
        db = get_db()
        user = display_user(db, userid)
        print(user)
        return jsonify({"user":[dict(row) for row in user]})

    if request.method == 'DELETE':
        db = get_db()
        remove(db, id)
        return jsonify(user)

    if request.method == 'PUT':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        update(db, id, name, email, password)
        return jsonify({"user":[dict(row) for row in user]})
 

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('show_entries'))



if __name__ == "__main__":
    app.run()
