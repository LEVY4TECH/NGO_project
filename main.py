from flask import Flask,render_template,request,redirect,url_for,session,flash

from mydatabase import insert_users, fetch_users, update_users, delete_user, insert_campaign, fetch_campaign, update_campaigns, delete_campaigns, insert_blogs, fetch_blogs, update_blogs, delete_blogs, insert_donation_items, fetch_donation_items, update_donation_items, delete_donation_items, insert_donations, fetch_donations, update_donations, delete_donations, insert_events, fetch_events, update_events, delete_events, check_user

from flask_bcrypt import Bcrypt

from functools import wraps

app=Flask(__name__)
app.secret_key='levyyy'

bcrypt=Bcrypt(app)

@app.route('/')
def home():
    return render_template('index.html')

def login_required(f):
    @wraps(f)
    def protected(*args,**kwargs):
        if 'email' not in session:
            return redirect(url_for('login'))
        return f(*args,**kwargs)
    return protected

@app.route('/blogs')
def blogs():
    blogs = fetch_blogs()
    return render_template('blogs.html', blogs = blogs)

@app.route('/add_blogs', method = ['POST'])
def add_blogs():

    email = request.form['email']
    name = request.form['name']
    title = request.form['title']
    content = request.form['content']
    new_blog = (email, name, title, content)
    insert_blogs(new_blog)
    return redirect(url_for('blogs'))

@app.route('/campaigns')
def campaigns():
    campaigns = fetch_campaign()
    return render_template('campaigns.html', campaigns = campaigns)

@app.route('/add_campaigns', method = ['POST'])
def add_campaigns():

    email = request.form['email']
    name = request.form['name']
    title = request.form['title']
    description = request.form['description']
    goal_amount = request.form['amount']
    start_date = request.form['start']
    end_date = request.form['end']
    new_campaign = (email, name, title, description, goal_amount, start_date, end_date)
    insert_campaign(new_campaign)
    return redirect(url_for('campaigns'))

@app.route('/events')
def events():
    events = fetch_events()
    return render_template('events.html', events = events)

@app.route('/add_events')
def add_events():

    email = request.form['email']
    name = request.form['name']
    title = request.form['title']
    description = request.form['descriptiion']
    event_date = request.form['date']
    location = request.form['location']
    new_event = (email, name, title, description, event_date, location)
    insert_events(new_event)
    return redirect(url_for('events'))

# register route
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        
        fullname=request.form['name']
        email=request.form['email']
        password=request.form['password']
        confirm_password = request.form['cpassword']

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('register'))

        hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')

        # checking if user exists
        user=check_user(email)

        if not user:
            new_user=(fullname,email,hashed_password)
            insert_users(new_user)
            flash("You're Registered Successfully.", "success")
            return redirect(url_for('login'))
        else:
            print('Already Registered')
    return render_template('register.html')


# login route
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        # Check whether the email exists
        user = check_user(email)

        if not user:
            flash("Please register first.", "danger")
            return redirect(url_for('register'))

        # Verify the password
        if not bcrypt.check_password_hash(user[3], password):
            flash("Incorrect password. Please try again.", "danger")
            return redirect(url_for('login'))

        # Create the user session
        session['user_id'] = user[0]
        session['name'] = user[1]
        session['email'] = user[2]
        session['role'] = user[4]

        flash("Logged in successfully.", "success")

        # Redirect based on role
        if user[4] == 'admin':
            return redirect(url_for('admin_dashboard'))

        return redirect(url_for('home'))

    return render_template('login.html')

# admin route
@app.route('/admin')
def admin_dashboard():

    if 'user_id' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))

    if session['role'] != 'admin':
        flash("You are not authorized to access this page.", "danger")
        return redirect(url_for('home'))

    return render_template('admin/index.html')


    