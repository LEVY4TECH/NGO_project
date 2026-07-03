from flask import Flask,render_template,request,redirect,url_for,session,flash

from mydatabase import insert_users, fetch_users, fetch_user,update_users, delete_user, count_users,insert_campaign, fetch_campaign, update_campaign, delete_campaign, fetch_single_campaign,insert_blog, fetch_blogs, fetch_single_blog, update_blog, delete_blog, insert_donation_items, fetch_donation_items, update_donation_items, delete_donation_items, insert_donations, fetch_donations, update_donations, delete_donations, insert_event, fetch_events, fetch_single_event, fetch_campaign_dropdown, update_event, delete_event, check_user, update_user_role, insert_volunteer,fetch_volunteer, fetch_volunteers, approve_volunteer, decline_volunteer

from datetime import datetime

from flask_bcrypt import Bcrypt

from functools import wraps

app=Flask(__name__)
app.secret_key='levyyy'

bcrypt=Bcrypt(app)

@app.route('/')
def home():
    return render_template('/user/index.html')

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
    return render_template('/user/blogs.html', blogs = blogs)

# viewing one blog in users page
@app.route('/user/blog/<int:blog_id>')
def blog_details(blog_id):

    blog = fetch_single_blog(blog_id)

    if not blog:

        flash("Blog not found.", "danger")

        return redirect(url_for('blogs'))

    return render_template(

        'user/blog_details.html',

        blog=blog

    )

# admin blog route
@app.route('/admin/blogs')
@login_required
@admin_required
def manage_blogs():

    blogs = fetch_blogs()

    return render_template(
        'admin/blogs.html',
        blogs=blogs
    )

@app.route('/admin/blogs/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_blog():

    if request.method == "POST":

        user_id = session['user_id']

        title = request.form['title']

        content = request.form['content']

        values = (
            user_id,
            title,
            content
        )

        insert_blog(values)

        flash("Blog published successfully.", "success")

        return redirect(url_for('manage_blogs'))

    return render_template(
        'admin/add_blog.html'
    )
    
# admin editing blog route
@app.route('/admin/blogs/edit/<int:blog_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_blog(blog_id):

    blog = fetch_single_blog(blog_id)

    if not blog:

        flash("Blog not found.", "danger")

        return redirect(url_for('manage_blogs'))

    if request.method == "POST":

        title = request.form['title']

        content = request.form['content']

        values = (

            title,

            content,

            blog_id

        )

        update_blog(values)

        flash("Blog updated successfully.", "success")

        return redirect(url_for('manage_blogs'))

    return render_template(
        'admin/edit_blog.html',
        blog=blog
    )
    

# admin deleting blog
@app.route('/admin/blogs/delete/<int:blog_id>', methods=['POST'])
@login_required
@admin_required
def remove_blog(blog_id):

    blog = fetch_single_blog(blog_id)

    if not blog:

        flash("Blog not found.", "danger")

        return redirect(url_for('manage_blogs'))

    delete_blog(blog_id)

    flash("Blog deleted successfully.", "success")

    return redirect(url_for('manage_blogs'))

@app.route('/campaigns')
def campaigns():
    campaigns = fetch_campaign()
    return render_template('/user/campaigns.html', campaigns = campaigns)



@app.route('/events')
def events():
    events = fetch_events()
    return render_template('/user/events.html', events = events)

# viewing one event in the users page
@app.route('/event/<int:event_id>')
def event_details(event_id):

    event = fetch_single_event(event_id)

    if not event:

        flash("Event not found.", "danger")

        return redirect(url_for('events'))

    return render_template(
        'user/event_details.html',
        event=event
    )

# admin events route
@app.route('/admin/events')
@login_required
@admin_required
def manage_events():

    events = fetch_events()

    return render_template(
        'admin/events.html',
        events=events
    )

# admin adding event route
@app.route('/admin/events/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_event():

    campaigns = fetch_campaign_dropdown()

    if request.method == 'POST':

        campaign_id = request.form['campaign_id']
        title = request.form['title']
        description = request.form['description']
        event_date = request.form['event_date']
        location = request.form['location']

        values = (
            campaign_id,
            title,
            description,
            event_date,
            location
        )

        insert_event(values)

        flash("Event added successfully.", "success")

        return redirect(url_for('manage_events'))

    return render_template(
        'admin/add_event.html',
        campaigns=campaigns
    )
    

# admin editing event route
@app.route('/admin/events/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_event(event_id):

    event = fetch_single_event(event_id)

    if not event:

        flash("Event not found.", "danger")

        return redirect(url_for('manage_events'))

    campaigns = fetch_campaign_dropdown()

    if request.method == 'POST':

        campaign_id = request.form['campaign_id']
        title = request.form['title']
        description = request.form['description']
        event_date = request.form['event_date']
        location = request.form['location']

        values = (
            campaign_id,
            title,
            description,
            event_date,
            location,
            event_id
        )

        update_event(values)

        flash("Event updated successfully.", "success")

        return redirect(url_for('manage_events'))

    return render_template(
        'admin/edit_event.html',
        event=event,
        campaigns=campaigns
    )
    

# admin deleting event route
@app.route('/admin/events/delete/<int:event_id>', methods=['POST'])
@login_required
@admin_required
def remove_event(event_id):

    event = fetch_single_event(event_id)

    if not event:

        flash("Event not found.", "danger")

        return redirect(url_for('manage_events'))

    delete_event(event_id)

    flash("Event deleted successfully.", "success")

    return redirect(url_for('manage_events'))

# register route
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        fullname = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['cpassword']

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('register'))

        # Check if email already exists
        user = check_user(email)

        if user:
            flash("An account with this email already exists.", "danger")
            return redirect(url_for('register'))

        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Make the first registered user an admin
        total_users = count_users()

        if total_users == 0:
            role = "admin"
        else:
            role = "user"

        new_user = (
            fullname,
            email,
            hashed_password,
            role
        )

        insert_users(new_user)

        flash("Registration successful. You can now log in.", "success")

        return redirect(url_for('login'))

    return render_template('user/register.html')


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

    return render_template('user/login.html')




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


#  admin Dashboard Route
@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():

    users = fetch_users()
    volunteers = fetch_volunteers()
    campaigns = fetch_campaign()
    blogs = fetch_blogs()
    events = fetch_events()
    donations = fetch_donations()

    return render_template(
        'admin/dashboard.html',

        total_users=len(users),

        total_volunteers=len(volunteers),

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

# admin campaign route
@app.route('/admin/campaigns')
@login_required
@admin_required
def manage_campaigns():

    campaigns = fetch_campaign()

    return render_template(
        'admin/campaigns.html',
        campaigns=campaigns
    )
    
# user campaign route(view one campaign)
@app.route('/campaign/<int:campaign_id>')
def campaign_details(campaign_id):

    campaign = fetch_single_campaign(campaign_id)

    if not campaign:

        flash("Campaign not found.", "danger")

        return redirect(url_for('campaigns'))

    return render_template(
        'user/campaign_details.html',
        campaign=campaign
    )
    
# add campaign route
@app.route('/admin/campaigns/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_campaign():

    if request.method == "POST":

        user_id = session['user_id']
        title = request.form['title']
        description = request.form['description']
        goal_amount = request.form['goal_amount']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Automatically assign the status
        status = "verified"

        campaign = (
            user_id,
            title,
            description,
            goal_amount,
            start_date,
            end_date,
            status
        )

        insert_campaign(campaign)

        flash("Campaign added successfully.", "success")

        return redirect(url_for('manage_campaigns'))

    return render_template("admin/add_campaign.html")

# edit campaign route
@app.route('/admin/campaigns/edit/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_campaign(campaign_id):

    campaign = fetch_single_campaign(campaign_id)

    if not campaign:

        flash("Campaign not found.", "danger")

        return redirect(url_for('manage_campaigns'))

    if request.method == "POST":

        title = request.form['title']
        description = request.form['description']
        goal_amount = request.form['goal_amount']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Admin can change the status here
        status = request.form['status']

        values = (
            title,
            description,
            goal_amount,
            start_date,
            end_date,
            status,
            campaign_id
    )

    update_campaign(values)

    flash("Campaign updated successfully.", "success")

    return redirect(url_for('manage_campaigns'))
    
# Delete campaign route
@app.route('/admin/campaigns/delete/<int:campaign_id>', methods=['POST'])
@login_required
@admin_required
def remove_campaign(campaign_id):

    campaign = fetch_single_campaign(campaign_id)

    if not campaign:

        flash("Campaign not found.", "danger")

        return redirect(url_for('manage_campaigns'))

    delete_campaign(campaign_id)

    flash("Campaign deleted successfully.", "success")

    return redirect(url_for('manage_campaigns'))

# automatically generate the current year in the footer
@app.context_processor
def inject_current_year():
    return {
        "current_year": datetime.now().year
    }
    
# about route
@app.route('/about')
def about():

    return render_template('user/about.html')


# contact route
@app.route('/contact')
def contact():

    return render_template('user/contact.html')

# Admin managing donations route
@app.route('/manage_donations')
def manage_donations():

    return render_template('admin/donation.html')

# volunteer route
@app.route('/volunteer', methods=['GET', 'POST'])
@login_required
def volunteer():

    if request.method == "POST":

        user_id = session['user_id']

        preferred_area = request.form['preferred_area']
        skills = request.form['skills']
        availability = request.form['availability']

        volunteer = (
            user_id,
            preferred_area,
            skills,
            availability
        )

        insert_volunteer(volunteer)

        flash(
            "Your volunteer application has been submitted successfully. We will review it soon.",
            "success"
        )

        return redirect(url_for('home'))

    return render_template('user/volunteer.html')

# no dupicate volunteer applications
# application = check_volunteer_application(user_id)

# if application:

#     flash(
#         "You have already submitted a volunteer application.",
#         "warning"
#     )

#     return redirect(url_for('home'))

app.run(debug=True)
    