import secrets
import string
import os
from flask import (jsonify, render_template,
                   request, url_for, flash, redirect, send_from_directory, Response)
import json
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from sqlalchemy.sql import text
from flask_login import login_user, login_required, logout_user, current_user
from app import app, images
from app import db
from app import login_manager
from app import oauth
from app.models.blogEntry import BlogEntry
from app.models.authuser import AuthUser, Privateblog
from app.models.subscriber import Subscribe
from app.forms import forms
#import base64

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/crash')
def crash():
    return 1/0


@app.route('/db')
def db_connection():
    try:
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return '<h1>db works.</h1>'
    except Exception as e:
        return '<h1>db is broken.</h1>' + str(e)
    
#------------------------------------- Oauth Login -------------------------------------------------------

@app.route('/google/')
def google():

    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url=app.config['GOOGLE_DISCOVERY_URL'],
        client_kwargs={
            'scope': 'openid email profile'
        }
    )


   # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    app.logger.debug(str(token))


    userinfo = token['userinfo']
    app.logger.debug(" Google User " + str(userinfo))
    email = userinfo['email']
    user = AuthUser.query.filter_by(email=email).first()


    if not user:
        if 'family_name' in userinfo:
            name = userinfo['given_name'] + " " + userinfo['family_name']
        else:
            name = userinfo['given_name']
        random_pass_len = 8
        password = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                          for i in range(random_pass_len))
        picture = userinfo['picture']
        new_user = AuthUser(email=email, name=name,
                           password=generate_password_hash(
                               password, method='sha256'),
                           avatar_url=picture)
        db.session.add(new_user)
        db.session.commit()
        user = AuthUser.query.filter_by(email=email).first()
    login_user(user)
    return redirect('/openfans')

@app.route('/facebook/')
def facebook():
    # Facebook Oauth Config
    FACEBOOK_CLIENT_ID = os.environ.get('FACEBOOK_CLIENT_ID')
    FACEBOOK_CLIENT_SECRET = os.environ.get('FACEBOOK_CLIENT_SECRET')
    oauth.register(
        name='facebook',
        client_id=FACEBOOK_CLIENT_ID,
        client_secret=FACEBOOK_CLIENT_SECRET,
        access_token_url='https://graph.facebook.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://www.facebook.com/dialog/oauth',
        authorize_params=None,
        api_base_url='https://graph.facebook.com/',
        client_kwargs={'scope': 'email'},
    )
    redirect_uri = url_for('facebook_auth', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)
 
@app.route('/facebook/auth/')
def facebook_auth():
    token = oauth.facebook.authorize_access_token()
    resp = oauth.facebook.get(
        'https://graph.facebook.com/me?fields=id,name,email,picture{url}')
    profile = resp.json()
    print("Facebook User ", profile)

    email = profile['email']
    user = AuthUser.query.filter_by(email=email).first()

    if not user:
        name = profile['name']
        random_pass_len = 8
        password = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                          for i in range(random_pass_len))
        picture = profile['picture']['data']['url']
        new_user = AuthUser(email=email, name=name,
                           password=generate_password_hash(
                               password, method='sha256'),
                           avatar_url=picture)
        db.session.add(new_user)
        db.session.commit()
        user = AuthUser.query.filter_by(email=email).first()
    login_user(user)
    return redirect('/openfans')

#------------------------ Database to JSON ----------------------------------------------------------------

@app.route("/blogentry")
def db_blogentry():
    blogentry = []
    db_blogentry = Privateblog.query.all()
    for i in db_blogentry:
        #app.logger.debug(i.to_dict())
        owner_id = i.to_dict()["owner_id"]
        app.logger.debug(owner_id)
        if current_user.is_authenticated:
            sub_check = Subscribe.query.filter_by(sub_owner=owner_id, user_sub=current_user.id).first()
            if sub_check or owner_id == current_user.id:
                user_data = AuthUser.query.get(owner_id)
                user_dict = {attr: getattr(user_data, attr) for attr in ['id', 'email', 'name', 'avatar_url']}
                user_dict['can_read'] = True
            else:   
                user_data = AuthUser.query.get(owner_id)
                user_dict = {attr: getattr(user_data, attr) for attr in ['id', 'email', 'name', 'avatar_url']}
                user_dict['can_read'] = False
            blogentry.append({**user_dict, **i.to_dict()})
        else:   
            user_data = AuthUser.query.get(owner_id)
            user_dict = {attr: getattr(user_data, attr) for attr in ['id', 'email', 'name', 'avatar_url']}
            user_dict['can_read'] = False
            blogentry.append({**user_dict, **i.to_dict()})

    return jsonify(blogentry)

@app.route("/user_blogentry")
def db_user_blogentry():
    blogentry = []
    db_user_blogentry = Privateblog.query.filter(Privateblog.owner_id == current_user.id)
    
    for i in db_user_blogentry:
        #app.logger.debug(i.to_dict())
        owner_id = i.to_dict()["owner_id"]
        app.logger.debug(owner_id)
        user_data = AuthUser.query.get(owner_id)
        user_dict = {attr: getattr(user_data, attr) for attr in ['id', 'email', 'name', 'avatar_url']}
        blogentry.append({**user_dict, **i.to_dict()})
    app.logger.debug("DB BlogEntry: " + str(blogentry))

    return jsonify(blogentry)

@app.route("/select_blogentry/<string:blog_email>")
def db_select_blogentry(blog_email):
    blogentry = []
    user = AuthUser.query.filter_by(email=blog_email).first_or_404()
    db_select_blogentry = Privateblog.query.filter_by(owner_id=user.id).all()
    
    for i in db_select_blogentry:
        #app.logger.debug(i.to_dict())
        owner_id = i.to_dict()["owner_id"]
        app.logger.debug(owner_id)
        user_data = AuthUser.query.get(owner_id)
        user_dict = {attr: getattr(user_data, attr) for attr in ['id', 'email', 'name', 'avatar_url']}
        blogentry.append({**user_dict, **i.to_dict(), 'email': user.email})

    return jsonify(blogentry)

@app.route('/images/<path:filename>/<int:owner_id>')
@login_required
def image_path(filename, owner_id):
    app.logger.debug(f"owwner = {owner_id}, current_id = {current_user.id}")
    if Subscribe.query.filter_by(user_sub=current_user.id, sub_owner=owner_id).first() or current_user.id == owner_id:
        app.logger.debug(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], '', filename ))
        return send_from_directory(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], ''), filename)
    return send_from_directory(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], ''), '404.jpg')

#--------------------------- Subs ---------------------------------------------------------------------------

@app.route("/sub_table")
def db_subscription(var=None):
    subscription = []
    db_subscription = Subscribe.query.all()
    subscription = list(map(lambda x: x.to_dict(), db_subscription))
    app.logger.debug("DB sub table: " + str(subscription))
    return jsonify(data=subscription, message=var)

@app.route("/subscribe/<string:blog_email>")
@login_required
def subscribe(blog_email):
    id_ = current_user.id
    sub_owner = AuthUser.query.get(email=blog_email)
    auth = Subscribe.query.filter_by(user_sub=id_, sub_owner=sub_owner).first()
    app.logge.debug(auth)
    if auth:
        app.logge.debug("Pass")
        return render_template('user_post.html', sub_owner=sub_owner)
    else:
        app.logge.debug("Didn't pass condition.")
        return render_template('user_post.html', sub_owner=sub_owner)
    
@app.route("/add-sub/<string:blog_email>", methods=('GET', 'POST'))
@login_required
def ToSubscribe(blog_email):
    if request.method == 'POST':
        id_ = current_user.id
        sub_owner = AuthUser.query.filter_by(email=blog_email).first()
        sub_check = Subscribe.query.filter_by(sub_owner=sub_owner.id, user_sub=id_).first()
        if not sub_check:
            app.logger.debug(sub_owner.id)
            entry = Subscribe(user_sub=current_user.id, sub_owner=sub_owner.id)
            db.session.add(entry)
            db.session.commit()
            return db_subscription('subscribed')
        else:
            db.session.delete(sub_check)
            db.session.commit()
            return db_subscription('unsubscribed')
        
    return Response(status=300)

# ------------------------- Web Page -------------------------------------------------------------------------

@app.route('/openfans', methods=('GET', 'POST'))
@login_required
def freeFan():
    form = forms.BlogForm()
    if form.validate_on_submit():
        app.logger.debug(current_user.id)
        id_ = form.entryid.data
        message = form.message.data
        pic = form.image.data
        filename = None
        app.logger.debug(pic)
        if pic:
            filename = secure_filename(images.save(pic))
            app.logger.debug(filename)

        if not id_:
            entry = Privateblog(message=message, avatar_url=current_user.avatar_url, img=filename, owner_id=current_user.id)
            #app.logger.debug(str(entry))
            db.session.add(entry)
        else:
            blogentry = Privateblog.query.get(id_)
            if blogentry.owner_id == current_user.id:
                if not filename:
                    blogentry.update(message=message, avatar_url=current_user.avatar_url,img=blogentry.img)
                else:
                    blogentry.update(message=message, avatar_url=current_user.avatar_url,img=filename)
        db.session.commit()
        return db_blogentry()
    return render_template('freeFan.html', form=form)

@app.route('/yourblog', methods=('GET', 'POST'))
@login_required
def userfreeFan():
    form = forms.BlogForm()
    if form.validate_on_submit():
        app.logger.debug(current_user.id)
        id_ = form.entryid.data
        message = form.message.data
        pic = form.image.data
        filename = None

        if pic:
            filename = secure_filename(images.save(pic))
            
        if not id_:
            entry = Privateblog(message=message, avatar_url=current_user.avatar_url, img=filename, owner_id=current_user.id)
            #app.logger.debug(str(entry))
            db.session.add(entry)
        else:
            blogentry = Privateblog.query.get(id_)
            if blogentry.owner_id == current_user.id:
                app.logger.debug(f"img = {blogentry.img}")
                if not filename:
                    blogentry.update(message=message, avatar_url=current_user.avatar_url, img=blogentry.img)
                else:
                    img_path = os.path.join('../' + app.config["UPLOADED_PHOTOS_DEST"] , blogentry.img)
                    app.logger.debug(img_path)
                    # if os.path.exists(img_path):
                    #     os.remove(img_path)
                    # else:
                    #     print(f"File {img_path} does not exist.")
                    blogentry.update(message=message, avatar_url=current_user.avatar_url, img=filename)
                    
        db.session.commit()
        return db_user_blogentry()
    following = Subscribe.query.filter_by(user_sub=current_user.id).count()
    followers = Subscribe.query.filter_by(sub_owner=current_user.id).count()
    app.logger.debug(f"followers = {followers}")
    app.logger.debug(f"following = {following}")
    
    return render_template('yourfreeFan.html', form=form, followers=followers, following=following)

@app.route("/user/<string:blog_email>")
@login_required
def user_posts(blog_email):
    form = forms.BlogForm()
    id_ = current_user.id
    user = AuthUser.query.filter_by(email=blog_email).first_or_404()
    user_posts = Privateblog.query.filter_by(owner_id=user.id).all()
    check_sub = Subscribe.query.filter_by(sub_owner=user.id, user_sub=id_).first()
    following = Subscribe.query.filter_by(user_sub=user.id).count()
    followers = Subscribe.query.filter_by(sub_owner=user.id).count()
    app.logger.debug(f"followers = { followers }")
    app.logger.debug(f"following = { following }")
    
    return render_template('user_post.html', user=user, posts=user_posts, form=form, check_sub=check_sub, followers=followers, following=following)


@app.route('/remove_blog', methods=('GET', 'POST'))
def remove_blog():
    app.logger.debug("REMOVE")
    if request.method == 'POST':
        result = request.form.to_dict()
        id_ = result.get('id', '')
        try:
            entry = Privateblog.query.get(id_)
            if entry.owner_id == current_user.id:
                db.session.delete(entry)
            db.session.commit()
        except Exception as ex:
            app.logger.debug(ex)
            raise
    return db_blogentry()


@app.route('/remove_blog_profile', methods=('GET', 'POST'))
def remove_blog_profile():
    app.logger.debug("REMOVE")
    if request.method == 'POST':
        result = request.form.to_dict()
        id_ = result.get('id', '')
        try:
            entry = Privateblog.query.get(id_)
            if entry.owner_id == current_user.id:
                db.session.delete(entry)
            db.session.commit()
        except Exception as ex:
            app.logger.debug(ex)
            raise
    return db_user_blogentry()

@app.route('/profile')
@login_required
def freeFan_profile():
    return render_template('freeFan/setting.html', current_user=current_user)

@app.route('/', methods=('GET', 'POST'))
def freeFan_login():
    if current_user.is_authenticated:
        return redirect(url_for('freeFan'))

    if request.method == 'POST':
        # login code goes here
        email = request.form.get('email')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))

        user = AuthUser.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the
        # hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            # if the user doesn't exist or password is wrong, reload the page
            return redirect(url_for('freeFan_login'))

        # if the above check passes, then we know the user has the right
        # credentials
        login_user(user, remember=remember)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('freeFan')
        return redirect(next_page)

    return render_template('freeFan/login.html')



@app.route('/signup', methods=('GET', 'POST'))
def freeFan_signup():

    def fix_email_domain(email):
        # function to fix email domain to @opf.com
        return email.split('@')[0] + '@opf.com'

    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(str(result))
        validated = True
        validated_dict = {}
        valid_keys = ['email', 'name', 'password']

        # validate the input
        for key in result:
            app.logger.debug(str(key)+": " + str(result[key]))
            # screen of unrelated inputs
            if key not in valid_keys:
                continue

            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            validated_dict[key] = value
        
        # fix email domain to @opf.com
        validated_dict['email'] = fix_email_domain(validated_dict['email'])
        
        # code to validate and add user to database goes here
        app.logger.debug("validation done")
        if validated:
            app.logger.debug('validated dict: ' + str(validated_dict))
            email = validated_dict['email']
            name = validated_dict['name']
            password = validated_dict['password']
            # if this returns a user, then the email already exists in database
            user = AuthUser.query.filter_by(email=email).first()

            if user:
                # if a user is found, we want to redirect back to signup
                # page so user can try again
                flash('Email address already exists')
                return redirect(url_for('freeFan_signup'))

            # create a new user with the form data. Hash the password so
            # the plaintext version isn't saved.
            app.logger.debug("preparing to add")
            avatar_url = gen_avatar_url(email, name)
            new_user = AuthUser(email=email, name=name,
                                password=generate_password_hash(
                                    password, method='sha256'),
                                avatar_url=avatar_url)
            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for('freeFan_login'))
    
    return render_template('freeFan/signup.html')


@app.route('/logout')
@login_required
def freeFan_logout():
    logout_user()
    return redirect(url_for('freeFan_login'))

@app.route('/submit-form', methods=['POST'])
@login_required
def submit_form():
    current_password = request.form['password']
    new_name = request.form['name']
    new_email = request.form['email']
    new_avatar = gen_avatar_url(new_email, new_name)
    userEmail = AuthUser.query.filter_by(email=new_email).first()
    userName = AuthUser.query.filter_by(name=new_name).first()
    
    
        
    # Check if the current password is correct
    if check_password_hash(current_user.password, current_password):
        if userEmail and current_user.email != request.form['email']:
            flash('This email is already taken.')
            return redirect(url_for('freeFan_profile'))
        
        elif userName and current_user.name != request.form['name']:
            flash('This username is already taken.')
            return redirect(url_for('freeFan_profile'))
        # Update the user's name and email
        old_name = current_user.name
        old_email = current_user.email
        current_user.name = new_name
        current_user.email = new_email
        current_user.avatar_url = new_avatar
        db.session.commit()
        
         # Update all records in the database with the old name and email
        #BlogEntry.query.filter_by(name=old_name, email=old_email).update({BlogEntry.name: new_name, BlogEntry.email: new_email, BlogEntry.avatar_url: new_avatar})
        AuthUser.query.filter_by(name=old_name, email=old_email).update({AuthUser.name: new_name, AuthUser.email: new_email, Privateblog.avatar_url: new_avatar})
        Privateblog.query.filter_by(owner_id=current_user.id).update({BlogEntry.avatar_url: new_avatar})
        
        db.session.commit()
        flash('Your changes have been saved.', 'success')
        
    else:
        flash('Incorrect password. Please try again.', 'error')
        
    return redirect(url_for('freeFan_profile'))

@app.route('/change-password', methods=['POST'])
def change_password():
    current_password = request.form.get("curr_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")
    
    if not check_password_hash(current_user.password, current_password):
        flash("Incorrect password.")
        return redirect(url_for("freeFan_profile"))

    if new_password != confirm_password:
        flash("Password do not match.")
        return redirect(url_for("freeFan_profile"))

    if new_password == current_password:
        flash("New password cannot be the same as old password.")
        return redirect(url_for("freeFan_profile"))

    current_user.name = request.form['name']
    current_user.email = request.form['email']
    db.session.commit()
    
    current_user.password = generate_password_hash(new_password, method='sha256')
    
    db.session.commit()

    flash("Your password has been changed successfully.")
    return redirect(url_for("freeFan_profile"))

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our
    # user table, use it in the query for the user
    return AuthUser.query.get(int(user_id))

def gen_avatar_url(email, name):
    bgcolor = generate_password_hash(email, method='sha256')[-6:]
    color = hex(int('0xffffff', 0) -
                int('0x'+bgcolor, 0)).replace('0x', '')
    lname = ''
    temp = name.split()
    fname = temp[0][0]
    if len(temp) > 1:
        lname = temp[1][0]

    avatar_url = "https://ui-avatars.com/api/?name=" + \
        fname + "+" + lname + "&background=" + \
        bgcolor + "&color=" + color
    return avatar_url

