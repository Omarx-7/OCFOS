from . import db


# ==========================================================
# MEMBER
# ==========================================================

class Member(db.Model):
    __tablename__ = "member"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(
        db.String(150),
        nullable=False,
        unique=True,
        index=True
    )

    city = db.Column(db.String(100), nullable=False)

    domain_tags = db.Column(db.String(255))

    bio = db.Column(db.Text)

    opted_in_to_matching = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    is_admin = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    # ---------------- Relationships ----------------

    projects = db.relationship(
        "Project",
        backref="owner",
        foreign_keys="Project.owner_id",
        lazy=True
    )

    hosted_events = db.relationship(
        "Event",
        backref="host",
        foreign_keys="Event.host_id",
        lazy=True
    )

    rsvps = db.relationship(
        "RSVP",
        backref="member",
        lazy=True,
        cascade="all, delete-orphan"
    )

    requested_introductions = db.relationship(
        "Introduction",
        foreign_keys="Introduction.requester_id",
        backref="requester",
        lazy=True
    )

    target_introductions = db.relationship(
        "Introduction",
        foreign_keys="Introduction.target_id",
        backref="target",
        lazy=True
    )

    administered_introductions = db.relationship(
        "Introduction",
        foreign_keys="Introduction.admin_id",
        backref="admin",
        lazy=True
    )

    def __repr__(self):
        return f"<Member {self.name}>"


# ==========================================================
# PROJECT
# ==========================================================

class Project(db.Model):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("member.id"),
        nullable=False
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    domain = db.Column(
        db.String(50),
        nullable=False
    )

    stage = db.Column(
        db.String(30),
        nullable=False
    )

    def __repr__(self):
        return f"<Project {self.title}>"


# ==========================================================
# EVENT
# ==========================================================

class Event(db.Model):
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True)

    city = db.Column(
        db.String(100),
        nullable=False
    )

    domain = db.Column(
        db.String(50),
        nullable=False
    )

    date = db.Column(
        db.DateTime,
        nullable=False
    )

    capacity = db.Column(
        db.Integer,
        nullable=False
    )

    host_id = db.Column(
        db.Integer,
        db.ForeignKey("member.id"),
        nullable=False
    )

    rsvps = db.relationship(
        "RSVP",
        backref="event",
        lazy=True,
        cascade="all, delete-orphan"
    )

    introductions = db.relationship(
        "Introduction",
        backref="event",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Event {self.id} - {self.city}>"


# ==========================================================
# RSVP
# ==========================================================

class RSVP(db.Model):
    __tablename__ = "rsvp"

    event_id = db.Column(
        db.Integer,
        db.ForeignKey("event.id"),
        primary_key=True
    )

    member_id = db.Column(
        db.Integer,
        db.ForeignKey("member.id"),
        primary_key=True
    )

    status = db.Column(
        db.Enum(
            "going",
            "waitlisted",
            "cancelled",
            name="rsvp_status"
        ),
        nullable=False,
        default="going"
    )

    def __repr__(self):
        return f"<RSVP Event={self.event_id} Member={self.member_id}>"


# ==========================================================
# INTRODUCTION
# ==========================================================

class Introduction(db.Model):
    __tablename__ = "introduction"

    id = db.Column(db.Integer, primary_key=True)

    event_id = db.Column(
        db.Integer,
        db.ForeignKey("event.id"),
        nullable=False
    )

    requester_id = db.Column(
        db.Integer,
        db.ForeignKey("member.id"),
        nullable=False
    )

    target_id = db.Column(
        db.Integer,
        db.ForeignKey("member.id"),
        nullable=False
    )

    reason = db.Column(
        db.String(255),
        nullable=False
    )

    status = db.Column(
        db.Enum(
            "pending",
            "approved",
            "rejected",
            name="introduction_status"
        ),
        nullable=False,
        default="pending"
    )

    admin_id = db.Column(
        db.Integer,
        db.ForeignKey("member.id"),
        nullable=True
    )

    def __repr__(self):
        return (
            f"<Introduction "
            f"{self.requester_id}->{self.target_id} "
            f"({self.status})>"
        )