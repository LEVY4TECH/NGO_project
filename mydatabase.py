# database connection
import psycopg2
conn=psycopg2.connect(user='postgres',password='leshan1234',host='localhost',port='5432',database='ngo')
cur = conn.cursor()

# inserting users
# inserting users
def insert_users(values):

    insert = """
        INSERT INTO users(name, email, password, role)
        VALUES (%s, %s, %s, %s);
    """

    cur.execute(insert, values)

    conn.commit()

# fetching users
def fetch_users():
    cur.execute('select * from users;')
    users = cur.fetchall()
    return users

# fetching one user
def fetch_user(user_id):

    cur.execute(
        "SELECT * FROM users WHERE user_id = %s;",
        (user_id,)
    )

    return cur.fetchone()

# update users
def update_users(values):
    cur.execute("update users set name = %s, email = %s, password = %s, role = %s, status = %s", values)
    conn.commit()

# delete users
def delete_user(values):
    cur.execute("DELETE FROM users WHERE user_id = %s", values)
    conn.commit()

# checking user
def check_user(email):
    query="select * from users where email = %s"
    cur.execute(query,(email,))
    user=cur.fetchone()
    return user


# count all users so as to make the first regiistered user an admin
def count_users():

    query = "SELECT COUNT(*) FROM users;"

    cur.execute(query)

    total_users = cur.fetchone()[0]

    return total_users


# insert campaigns
def insert_campaign(values):

    query = """
        INSERT INTO campaigns(

            user_id,

            title,

            description,

            goal_amount,

            start_date,

            end_date,

            status

        )

        VALUES(%s,%s,%s,%s,%s,%s,%s);
    """

    cur.execute(query, values)

    conn.commit()

# fetch campaigns
def fetch_campaign():

    query = """
        SELECT

        campaigns.campaign_id,

        campaigns.title,

        campaigns.description,

        campaigns.goal_amount,

        campaigns.start_date,

        campaigns.end_date,

        campaigns.status,

        campaigns.created_at,

        users.name,

        users.email

        FROM campaigns

        JOIN users

        ON campaigns.user_id = users.user_id

        ORDER BY campaigns.created_at DESC;
    """

    cur.execute(query)

    campaigns = cur.fetchall()

    return campaigns

# fetch one campaign
def fetch_single_campaign(campaign_id):

    query = """
        SELECT *

        FROM campaigns

        WHERE campaign_id = %s;
    """

    cur.execute(query, (campaign_id,))

    campaign = cur.fetchone()

    return campaign

# update campaigns
def update_campaign(values):

    query = """
        UPDATE campaigns

        SET

        title=%s,

        description=%s,

        goal_amount=%s,

        start_date=%s,

        end_date=%s,

        status=%s

        WHERE campaign_id=%s;
    """

    cur.execute(query, values)

    conn.commit()

# delete campaigns
def delete_campaign(campaign_id):

    query = """
        DELETE FROM campaigns

        WHERE campaign_id=%s;
    """

    cur.execute(query, (campaign_id,))

    conn.commit()

# insert blogs
def insert_blog(values):

    query = """

        INSERT INTO blogs(

            user_id,

            title,

            content

        )

        VALUES(%s,%s,%s);

    """

    cur.execute(query, values)

    conn.commit()


# fetching all blogs
def fetch_blogs():

    query = """
        SELECT

        blogs.blog_id,

        blogs.title,

        blogs.content,

        blogs.published_at,

        users.name,

        users.email

        FROM blogs

        JOIN users

        ON blogs.user_id = users.user_id

        ORDER BY blogs.published_at DESC;
    """

    cur.execute(query)

    return cur.fetchall()

# fetch one blog
def fetch_single_blog(blog_id):

    query = """

        SELECT *

        FROM blogs

        WHERE blog_id=%s;

    """

    cur.execute(query, (blog_id,))

    return cur.fetchone()
    

# update blogs
def update_blog(values):

    query = """

        UPDATE blogs

        SET

        title=%s,

        content=%s

        WHERE blog_id=%s;

    """

    cur.execute(query, values)

    conn.commit()

# delete blogs
def delete_blog(blog_id):

    query = """

        DELETE

        FROM blogs

        WHERE blog_id=%s;

    """

    cur.execute(query, (blog_id,))

    conn.commit()

# insert donations
def insert_donations(values):
    insert = "insert into donations(total_amount) values(%s)"
    cur.execute(insert, values)
    conn.commit()

# fetch donations
def fetch_donations():
    cur.execute('select * from donations;')
    donations = cur.fetchall()
    return donations

# update donations
def update_donations(values):
    cur.execute("update_donations set total_amount = %s", values)
    conn.commit()

# delete donations
def delete_donations(values):
    cur.execute("DELETE FROM donations WHERE donation_id = %s", values)
    conn.commit()

# insert events
def insert_event(values):

    query = """

        INSERT INTO events(

            campaign_id,

            title,

            description,

            event_date,

            location

        )

        VALUES(%s,%s,%s,%s,%s);

    """

    cur.execute(query, values)

    conn.commit()

# fetch all events
def fetch_events():

    query = """

        SELECT

        events.event_id,

        campaigns.title,

        events.title,

        events.description,

        events.event_date,

        events.location,

        events.created_at

        FROM events

        JOIN campaigns

        ON events.campaign_id = campaigns.campaign_id

        ORDER BY events.event_date DESC;

    """

    cur.execute(query)

    events = cur.fetchall()

    return events

# fetch campaigns dropdown to be used in the admin events page
def fetch_campaign_dropdown():

    query = """
        SELECT campaign_id, title
        FROM campaigns
        WHERE status = 'verified'
        ORDER BY title;
    """

    cur.execute(query)

    campaigns = cur.fetchall()

    return campaigns

# fetch one event
def fetch_single_event(event_id):

    query = """

        SELECT *

        FROM events

        WHERE event_id=%s;

    """

    cur.execute(query, (event_id,))

    return cur.fetchone()

# update events
def update_event(values):

    query = """

        UPDATE events

        SET

        campaign_id=%s,

        title=%s,

        description=%s,

        event_date=%s,

        location=%s

        WHERE event_id=%s;

    """

    cur.execute(query, values)

    conn.commit()

# delete_events
def delete_event(event_id):

    query = """

        DELETE

        FROM events

        WHERE event_id=%s;

    """

    cur.execute(query, (event_id,))

    conn.commit()

# insert donation_items
def insert_donation_items(values):
    insert = "insert into donation_items(donation_id, campaign_id, amount) values(%s, %s, %s)"
    cur.execute(insert, values)
    conn.commit()

# fetch donation_items
def fetch_donation_items():
    cur.execute('select * from donation_items;')
    donation_items = cur.fetchall()
    return donation_items

# update donation_items
def update_donation_items(values):
    cur.execute("update donation_items set doantion_id = %s, campaign_id =%s, amount =%s", values)
    conn.commit()

# delete donation_items
def delete_donation_items(values):
    cur.execute("DELETE FROM donation_items WHERE item_id = %s", values)
    conn.commit()
    
# making admin
def make_admin(user_id):

    cur.execute(
        """
        UPDATE users
        SET role='admin'
        WHERE user_id=%s
        """,
        (user_id,)
    )
    
# updating role
def update_user_role(user_id):

    update = """
        UPDATE users
        SET role = 'admin'
        WHERE user_id = %s;
    """

    cur.execute(update, (user_id,))
    conn.commit()

    conn.commit()
    
# inserting volunteer
def insert_volunteer(values):

    query = """
        INSERT INTO volunteer_application(

            user_id,

            preferred_area,

            skills,

            availability

        )

        VALUES(%s,%s,%s,%s);
    """

    cur.execute(query, values)

    conn.commit()
    
# fetching volunteer
def fetch_volunteers():

    query = """
        SELECT

        volunteer_application.application_id,

        users.name,

        users.email,

        volunteer_application.preferred_area,

        volunteer_application.skills,

        volunteer_application.availability,

        volunteer_application.status

        FROM volunteer_application

        JOIN users

        ON volunteer_application.user_id = users.user_id

        ORDER BY volunteer_application.application_id DESC;
    """

    cur.execute(query)

    volunteers = cur.fetchall()

    return volunteers

# approve volunteer
def approve_volunteer(application_id):

    query = """
        UPDATE volunteer_application
        SET status = 'approved'
        WHERE application_id = %s;
    """

    cur.execute(query, (application_id,))

    conn.commit()
    
# decline volunteer
def decline_volunteer(application_id):

    query = """
        UPDATE volunteer_application
        SET status = 'declined'
        WHERE application_id = %s;
    """

    cur.execute(query, (application_id,))

    conn.commit()
    
# fetch one volunteer
def fetch_volunteer(application_id):

    query = """
        SELECT *
        FROM volunteer_application
        WHERE application_id = %s;
    """

    cur.execute(query, (application_id,))

    volunteer = cur.fetchone()

    return volunteer






