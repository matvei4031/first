from HabrClone import App, db
from flask import render_template, flash, redirect, url_for, request
from HabrClone.forms import LoginForm, RegistrationFrom, AccountUpdateForm
from flask_login import  current_user, login_user, logout_user

@App.route('/')
@App.route('/index')
def index():
    return render_template('index.html')


@App.route('/sign_in', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильное имя пользователя или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        return redirect(url_for('index'))
    return render_template('login.html', form=form, title='вход')

@App.route('/sign_out')
def logout():
    logout_user()
    return redirect(url_for('index'))






@App.route('/account', methods=('GET','POST'))
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.eamil = form.email.data
        db.session.commit()
        flash('Обновлено!')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    avatar = url_for('static', filename='img/avatars/' + current_user.avatar)
    return render_template('account.html', avatar=avatar, form=form)

@App.route('/sign_up', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password((form.password.data))
        db.session.addd(user)
        db.session.commit()

        flash('Вы успешно зарегистрировались')

        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Регистрация')



