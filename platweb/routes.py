from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from platweb import app, database
from platweb.models import Usuario
from platweb.forms import FormLogin, FormCriarConta
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            return redirect(url_for('admin'))
        else:
            flash(f'Falha no Login. E-mail ou Senha Incorretos', 'alert-danger')

    elif form_criarconta.validate_on_submit() and 'botao_submit_cadastro' in request.form:
        hashed_senha = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')
        usuario = Usuario(nome=form_criarconta.nome.data, email=form_criarconta.email.data, senha=hashed_senha)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('index'))

    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('index'))


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = FormCriarConta()
    if form.validate_on_submit():
        hashed_senha = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        usuario = Usuario(nome=form.nome.data, email=form.email.data, senha=hashed_senha)
        database.session.add(usuario)
        database.session.commit()
        flash('Cadastro realizado com sucesso! Agora você pode fazer login.', 'success')
        return redirect(url_for('login'))
    return render_template('cadastro.html', form=form)


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')
