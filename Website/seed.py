# Seed script for OCF OS
# Populates member, project, event, rsvp and introduction tables with test data.
# Safe to run multiple times because it clears existing rows first.

import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


# ----------------------------
# Connect to database
# ----------------------------
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME", "ocf_platform"),
)

cursor = conn.cursor()

# ----------------------------
# Clear existing data
# ----------------------------
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

for table in ["introduction", "rsvp", "project", "event", "member"]:
    cursor.execute(f"TRUNCATE TABLE {table}")

cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

# ----------------------------
# Members
# ----------------------------
members = [
    ("Sarah Mitchell", "sarah@ocf.com", "London", "", "OCF admin and community lead.", 0, 1),
    ("James Okafor", "james@ocf.com", "London", "fintech,AI", "Building payments infrastructure for SMEs.", 1, 0),
    ("Priya Sharma", "priya@ocf.com", "Oxford", "healthtech", "Founder focused on remote patient monitoring.", 1, 0),
    ("Tom Reyes", "tom@ocf.com", "Cambridge", "climate tech", "Working on carbon tracking for logistics.", 1, 0),
    ("Aisha Bello", "aisha@ocf.com", "London", "fintech", "Engineer turned founder, fintech background.", 1, 0),
    ("Liam Chen", "liam@ocf.com", "Oxford", "", "Early-stage builder, still exploring domains.", 1, 0),
]

cursor.executemany(
    """
    INSERT INTO member
    (name, email, city, domain_tags, bio, opted_in_to_matching, is_admin)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """,
    members,
)

# ----------------------------
# Projects
# ----------------------------
projects = [
    (2, "PayFlow", "fintech", "mvp"),
    (3, "MediTrack", "healthtech", "prototype"),
]

cursor.executemany(
    """
    INSERT INTO project
    (owner_id, title, domain, stage)
    VALUES (%s, %s, %s, %s)
    """,
    projects,
)

# ----------------------------
# Events
# ----------------------------
events = [
    ("London", "fintech", "2026-07-20 18:00:00", 2, 5),
    ("Oxford", "climate tech", "2026-07-25 17:00:00", 10, 4),
]

cursor.executemany(
    """
    INSERT INTO event
    (city, domain, date, capacity, host_id)
    VALUES (%s, %s, %s, %s, %s)
    """,
    events,
)

# ----------------------------
# RSVPs
# ----------------------------
rsvps = [
    (1, 2, "going"),
    (1, 3, "going"),
    (1, 5, "waitlisted"),
    (2, 6, "going"),
    (2, 2, "going"),
]

cursor.executemany(
    """
    INSERT INTO rsvp
    (event_id, member_id, status)
    VALUES (%s, %s, %s)
    """,
    rsvps,
)

# ----------------------------
# Introductions
# ----------------------------
introductions = [
    (1, 2, 3, "Recommended match", "pending", None),
]

cursor.executemany(
    """
    INSERT INTO introduction
    (event_id, requester_id, target_id, reason, status, admin_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """,
    introductions,
)

# ----------------------------
# Save changes
# ----------------------------
conn.commit()

print("Seed data inserted successfully.")

cursor.close()
conn.close()
