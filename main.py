from flask import Flask,render_template,request,redirect,url_for,session,flash

from mydatabase import insert_users, fetch_users, fetch_user,update_users, delete_user, insert_campaign, fetch_campaign, update_campaigns, delete_campaigns, insert_blogs, fetch_blogs, update_blogs, delete_blogs, insert_donation_items, fetch_donation_items, update_donation_items, delete_donation_items, insert_donations, fetch_donations, update_donations, delete_donations, insert_events, fetch_events, update_events, delete_events, check_user, update_user_role, fetch_volunteer, fetch_volunteers, approve_volunteer, decline_volunteer

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

def admin_required(f):
    @wraps(f)
    def protected(*args, **kwargs):

        if 'role' not in session or session['role'] != 'admin':
            flash("Access denied. Admins only.", "danger")
            return redirect(url_for('home'))

        return f(*args, **kwargs)

    return protected

@app.route('/blogs')
def blogs():
    blogs = fetch_blogs()
    return render_template('blogs.html', blogs = blogs)

@app.route('/add_blogs', methods = ['GET','POST'])
def add_blogs():

    if request.method == 'POST':
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

@app.route('/add_campaigns', methods = ['GET','POST'])
def add_campaigns():

    if request.method == 'POST':
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

@app.route('/add_events', methods = ['GET', 'POST'])
def add_events():

    if request.method == 'POST':

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


# admin users route
@app.route('/admin/users')
@login_required
@admin_required
def manage_users():

    users = fetch_users()

    return render_template(
        'admin/users.html',
        users=users
    )
    
  
# make admin route  
@app.route('/admin/users/make_admin/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def make_admin(user_id):

    user = fetch_user(user_id)

    if not user:

        flash("User not found.", "danger")
        return redirect(url_for('manage_users'))

    if user[4] == "admin":

        flash("This user is already an administrator.", "warning")
        return redirect(url_for('manage_users'))

    update_user_role(user_id)

    flash("User promoted to Admin successfully.", "success")

    return redirect(url_for('manage_users'))


# Dashboard Route
@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():

    users = fetch_users()
    campaigns = fetch_campaign()
    blogs = fetch_blogs()
    events = fetch_events()
    donations = fetch_donations()

    return render_template(
        'admin/dashboard.html',

        total_users=len(users),

        total_volunteers=0,

        total_campaigns=len(campaigns),

        total_blogs=len(blogs),

        total_events=len(events),

        total_donations=len(donations)
    )
    
# logout route
@app.route('/logout')
def logout():

    session.clear()

    flash("Logged out successfully.", "success")

    return redirect(url_for('home'))

# manage volunteers route
@app.route('/admin/volunteers')
@login_required
@admin_required
def manage_volunteers():

    volunteers = fetch_volunteers()

    return render_template(
        'admin/volunteers.html',
        volunteers=volunteers
    )
    
# approve volunteer route
@app.route('/admin/volunteers/approve/<int:application_id>', methods=['POST'])
@login_required
@admin_required
def approve_volunteer_route(application_id):

    volunteer = fetch_volunteer(application_id)

    if not volunteer:

        flash("Volunteer application not found.", "danger")
        return redirect(url_for('manage_volunteers'))

    if volunteer[5] == 'approved':

        flash("This volunteer has already been approved.", "warning")
        return redirect(url_for('manage_volunteers'))

    approve_volunteer(application_id)

    flash("Volunteer approved successfully.", "success")

    return redirect(url_for('manage_volunteers'))

# decline volunteer route
@app.route('/admin/volunteers/decline/<int:application_id>', methods=['POST'])
@login_required
@admin_required
def decline_volunteer_route(application_id):

    volunteer = fetch_volunteer(application_id)

    if not volunteer:

        flash("Volunteer application not found.", "danger")
        return redirect(url_for('manage_volunteers'))

    if volunteer[5] == 'declined':

        flash("This volunteer has already been declined.", "warning")
        return redirect(url_for('manage_volunteers'))

    decline_volunteer(application_id)

    flash("Volunteer application declined.", "success")

    return redirect(url_for('manage_volunteers'))

app.run(debug=True)
    