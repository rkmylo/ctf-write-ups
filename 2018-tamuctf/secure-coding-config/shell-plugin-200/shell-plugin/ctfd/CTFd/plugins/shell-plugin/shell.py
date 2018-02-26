import logging
import os
import re
import time
import urllib
from threading import Thread
import xmlrpclib
from Queue import Queue

from flask import current_app as app, render_template, request, redirect, abort, jsonify, json as json_mod, url_for, session, Blueprint

from itsdangerous import TimedSerializer, BadTimeSignature, Signer, BadSignature
from passlib.hash import bcrypt_sha256

from CTFd.utils import sha512, is_safe_url, authed, can_send_mail, sendmail, can_register, get_config, verify_email
from CTFd.models import db, Teams, Pages
import CTFd.auth
import CTFd.views


def create_user_thread(q):
    while True:
        user_pair = q.get(block=True)
        
        shell = xmlrpclib.ServerProxy('http://localhost:8000',allow_none=True)
        if user_pair[2] == "create":
            shell.add_user(user_pair[0], user_pair[1])
        elif user_pair[2] == "change":
            shell.change_user(user_pair[0], user_pair[1])   

def load(app):
    
    shell = Blueprint('shell', __name__, template_folder='shell-templates')
    app.register_blueprint(shell, url_prefix='/shell')
    page = Pages('shell',""" """ )
    auth = Blueprint('auth', __name__)
    
    shellexists = Pages.query.filter_by(route='shell').first()
    if not shellexists:
        db.session.add(page)
        db.session.commit()



    @app.route('/shell', methods=['GET'])
    def shell_view():
        if not authed():
            return redirect(url_for('auth.login', next=request.path))

        return render_template('shell.html',root=request.script_root) 
    
    @app.route('/register', methods=['POST', 'GET'])
    def register():
        if not can_register():
            return redirect(url_for('auth.login'))
        if request.method == 'POST':
            errors = []
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']

            name_len = len(name) < 2  
            names = Teams.query.add_columns('name', 'id').filter_by(name=name).first()
            emails = Teams.query.add_columns('email', 'id').filter_by(email=email).first()
            pass_short = len(password) == 0
            pass_long = len(password) > 32
            valid_email = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", request.form['email'])
            
            if not valid_email:
                errors.append("That email doesn't look right")
            if names:
                errors.append('That team name is already taken')
            if emails:
                errors.append('That email has already been used')
            if pass_short:
                errors.append('Pick a longer password')
            if pass_long:
                errors.append('Pick a shorter password')
            if name_len:
                errors.append('Pick a longer team name')
            
            if len(errors) > 0:
                return render_template('register.html', errors=errors, name=request.form['name'], email=request.form['email'], password=request.form['password'])
            else:
                with app.app_context():
                    team = Teams(name, email.lower(), password)
                    db.session.add(team)
                    db.session.commit()
                    db.session.flush()
                    shell = xmlrpclib.ServerProxy('http://localhost:8000',allow_none=True)            
                    shell.add_user(name, password)
            
                    session['username'] = team.name
                    session['id'] = team.id
                    session['admin'] = team.admin
                    session['nonce'] = sha512(os.urandom(10))

                    if can_send_mail() and get_config('verify_emails'): # Confirming users is enabled and we can send email.
                        db.session.close()
                        logger = logging.getLogger('regs')

                        logger.warn("[{0}] {1} registered (UNCONFIRMED) with {2}".format(time.strftime("%m/%d/%Y %X"),
                                                         request.form['name'].encode('utf-8'),
                                                         request.form['email'].encode('utf-8')))
                        return redirect(url_for('auth.confirm_user'))
                    else: # Don't care about confirming users
                        if can_send_mail(): # We want to notify the user that they have registered.
                            sendmail(request.form['email'], "You've successfully registered for {}".format(get_config('ctf_name')))

            db.session.close()

            logger = logging.getLogger('regs')
            logger.warn("[{0}] {1} registered with {2}".format(time.strftime("%m/%d/%Y %X"), request.form['name'].encode('utf-8'), request.form['email'].encode('utf-8')))
            return redirect(url_for('challenges.challenges_view'))
        else:
            return render_template('register.html')

    def reset_password(data=None):
        if data is not None and request.method == "GET":
            return render_template('reset_password.html', mode='set')
        if data is not None and request.method == "POST":
            try:
                s = TimedSerializer(app.config['SECRET_KEY'])
                name = s.loads(urllib.unquote_plus(data.decode('base64')), max_age=1800)
            except BadTimeSignature:
                return render_template('reset_password.html', errors=['Your link has expired'])
            except:
                return render_template('reset_password.html', errors=['Your link appears broken, please try again.'])
            team = Teams.query.filter_by(name=name).first_or_404()
            password = request.form['password'].strip()
            name = team.name
            
            pass_short = len(password) == 0
            pass_long = len(password) > 32
            #http://stackoverflow.com/questions/19605150/regex-for-password-must-be-contain-at-least-8-characters-least-1-number-and-bot
            
            errors = []
            
            if pass_short:
                errors.append('Pick a longer password')
            if pass_long:
                errors.append('Pick a shorter password')
            if len(errors) > 0:
                return render_template('reset_password.html', errors=errors)

            shell = xmlrpclib.ServerProxy('http://localhost:8000',allow_none=True)
            shell.change_user(name, password)       

            team.password = bcrypt_sha256.encrypt(password)
            db.session.commit()
            db.session.close()
            

            return redirect(url_for('auth.login'))

        if request.method == 'POST':
            email = request.form['email'].strip()
            team = Teams.query.filter_by(email=email).first()
            if not team:
                return render_template('reset_password.html', errors=['If that account exists you will receive an email, please check your inbox'])
            s = TimedSerializer(app.config['SECRET_KEY'])
            token = s.dumps(team.name)
            text = """
        Did you initiate a password reset?
        {0}/{1}
        """.format(url_for('auth.reset_password', _external=True), urllib.quote_plus(token.encode('base64')))

            sendmail(email, text)

            return render_template('reset_password.html', errors=['If that account exists you will receive an email, please check your inbox'])
        return render_template('reset_password.html')

    def profile():
        if authed():
            if request.method == "POST":
                errors = []

                name = request.form.get('name')
                email = request.form.get('email')
                website = request.form.get('website')
                affiliation = request.form.get('affiliation')
                country = request.form.get('country')

                user = Teams.query.filter_by(id=session['id']).first()

                if not get_config('prevent_name_change'):
                    names = Teams.query.filter_by(name=name).first()
                    name_len = len(request.form['name']) < 2

                emails = Teams.query.filter_by(email=email).first()
                valid_email = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)
                
                password = request.form['password'].strip()
                pass_short = len(password) == 0
                pass_long = len(password) > 32
                
                    
                if ('password' in request.form.keys() and not len(request.form['password']) == 0) and \
                    (not bcrypt_sha256.verify(request.form.get('confirm').strip(), user.password)):
                    errors.append("Your old password doesn't match what we have.")
                if not valid_email:
                    errors.append("That email doesn't look right")
                if not get_config('prevent_name_change') and names and name != session['username']:
                    errors.append('That team name is already taken')
                if emails and emails.id != session['id']:
                    errors.append('That email has already been used')
                if not get_config('prevent_name_change') and name_len:
                    errors.append('Pick a longer team name')
                if website.strip() and not validate_url(website):
                    errors.append("That doesn't look like a valid URL")
                if pass_short:
                        errors.append('Pick a longer password')
                if pass_long:
                        errors.append('Pick a shorter password')
                
    
                if len(errors) > 0:
                    return render_template('profile.html', name=name, email=email, website=website,
                               affiliation=affiliation, country=country, errors=errors)
                else:
                    team = Teams.query.filter_by(id=session['id']).first()
                    if not get_config('prevent_name_change'):
                        team.name = name
                    if team.email != email.lower():
                        team.email = email.lower()
                        if get_config('verify_emails'):
                            team.verified = False
                    session['username'] = team.name

                    if 'password' in request.form.keys() and not len(request.form['password']) == 0:
                        team.password = bcrypt_sha256.encrypt(request.form.get('password'))
                        password = request.form['password'].strip()
                        
                    team.website = website
                    team.affiliation = affiliation
                    team.country = country
                        
                    name = team.name

                    if password:
                        shell = xmlrpclib.ServerProxy('http://localhost:8000',allow_none=True)
                        shell.change_user(name, password)
                        
                    db.session.commit()
                    db.session.close()
                    return redirect(url_for('views.profile'))
            else:
                user = Teams.query.filter_by(id=session['id']).first()
                name = user.name
                email = user.email
                website = user.website
                affiliation = user.affiliation
                country = user.country
                prevent_name_change = get_config('prevent_name_change')
                confirm_email = get_config('verify_emails') and not user.verified
                return render_template('profile.html', name=name, email=email, website=website, affiliation=affiliation,
                           country=country, prevent_name_change=prevent_name_change, confirm_email=confirm_email)
        else:
            return redirect(url_for('auth.login'))



    app.view_functions['auth.reset_password'] = reset_password
    app.view_functions['auth.register'] = register
    app.view_functions['views.profile'] = profile   
