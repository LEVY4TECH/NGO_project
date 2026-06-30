# database connection
import psycopg2
conn=psycopg2.connect(user='postgres',password='leshan1234',host='localhost',port='5432',database='ngo')
cur = conn.cursor()

# inserting users
def insert_users(values):
    insert = "insert into users(name, email, password, role, status) values(%s, %s, %s, %s, %s)"
    cur.execute(insert, values)
    conn.commit()

# fetching users
def fetch_users():
    cur.execute('select * from users;')
    users = cur.fetchall()
    return users

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


# insert campaigns
def insert_campaign(values):
    insert = "insert into campaigns(user_id, title, description, goal_amount, start_date, end_date, status, created_at) values(%s, %s, %s, %s, %s, %s, %s, %s)"
    cur.execute(insert, values)
    conn.commit()

# fetch campaigns
def fetch_campaign():
    cur.execute('select * from campaigns;')
    campaigns = cur.fetchall()
    return campaigns

# update campaigns
def update_campaigns(values):
    cur.execute("update campaigns set user_id = %s, title = %s, description = %s, goal_amount = %s, start_date = %s, end_date = %s, status = %s, created_at = %s", values)
    conn.commit()

# delete campaigns
def delete_campaigns(values):
    cur.execute("DELETE FROM campaigns WHERE campaign_id = %s", values)
    conn.commit()

# insert blogs
def insert_blogs(values):
    insert = "insert into blogs(user_id, title, content, published_at) values(%s, %s, %s, %s)"
    cur.execute(insert, values)
    conn.commit()

# fetch blogs
def fetch_blogs():
    cur.execute('select * from blogs;')
    blogs = cur.fetchall()
    return blogs

# update blogs
def update_blogs(values):
    cur.execute("update blogs set user_id = %s, title = %s, content = %s, published_at = %s", values)
    conn.commit()

# delete blogs
def delete_blogs(values):
    cur.execute("DELETE FROM blogs WHERE blog_id = %s", values)
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
def insert_events(values):
    insert = "insert into events(campaign_id, title, description, event_date, location, created_at) values(%s, %s, %s, %s, %s, %s)"
    cur.execute(insert, values)
    conn.commit()

# fetch events
def fetch_events():
    cur.execute("select * from events;")
    events = cur.fetchall()
    return events

# update events
def update_events(values):
    cur.execute("update events set campaign_id = %s, title = %s, description = %s, event_date = %s, location = %s, created_at = %s", values)
    conn.commit()

# delete_events
def delete_events(values):
    cur.execute("DELETE FROM events WHERE event_id = %s", values)
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





