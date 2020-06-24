from HabrClone import App, db
from flask import render_template, flash, redirect, url_for, request
from HabrClone.forms import LoginForm, RegistrationForm, AccountUpdateForm


@App.route('/')
@App.route('/index')
def index():
    return render_template('index.html')


@App.route('/sign_in', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Пользователь {form.username.data} вошел. Поле "Запомнить меня" {form.remember_me.data} ')
        return redirect(url_for('index'))
    return render_template('login.html', form=form, title='вход')






@App.route('/account', methods('GET','POST'))
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


