from flask import Blueprint, render_template, request, redirect, url_for, flash

from .models import Member, Project, Event, RSVP, Introduction

from . import db

CURRENT_MEMBER = 2
CURRENT_ADMIN = 1

views = Blueprint('views', __name__) #views is the blueprint name for routes: Blueprint indicates reusability for putting them together into files/blocks
#__name__ tells Flask: 'There's a group of routes called 'views', and you can find them in views.py file.
#Ensure these routes are registered in __init__, else routes will not work

@views.route('/')
def home():
    return render_template('home.html')

#-----------------------------------------------------------------------------------------------------------------------
@views.route("/administrator")
def admin():

    # Temporary logged in admin
    admin = Member.query.get(1)

    members = Member.query.order_by(Member.name).all()

    projects = Project.query.order_by(Project.title).all()

    events = Event.query.order_by(Event.date).all()

    introductions = Introduction.query.order_by(
        Introduction.id.desc()
    ).all()

    return render_template(
        "admin.html",
        admin=admin,
        members=members,
        projects=projects,
        events=events,
        introductions=introductions
    )

#-----------------------------------------------------------------------------------------------------------------------
@views.route("/member")
def member():

    member = Member.query.get(CURRENT_MEMBER)

    projects = Project.query.filter_by(
        owner_id=member.id
    ).all()

    events = Event.query.order_by(
        Event.date
    ).all()

    # Get THIS MEMBER'S RSVPs
    member_rsvps = {
        rsvp.event_id: rsvp
        for rsvp in RSVP.query.filter_by(
            member_id=CURRENT_MEMBER
        ).all()
    }

    return render_template(
        "member.html",
        member=member,
        projects=projects,
        events=events,
        member_rsvps=member_rsvps
    )


@views.route("/member/toggle_matching", methods=["POST"])
def toggle_matching():

    member = Member.query.get_or_404(CURRENT_MEMBER)

    member.opted_in_to_matching = not member.opted_in_to_matching

    db.session.commit()

    if member.opted_in_to_matching:
        flash("Matching enabled.")
    else:
        flash("Matching disabled.")

    return redirect(url_for("views.member"))

@views.route("/member/rsvp/<int:event_id>", methods=["POST"])
def rsvp(event_id):

    member = Member.query.get_or_404(CURRENT_MEMBER)

    event = Event.query.get_or_404(event_id)

    existing = RSVP.query.filter_by(
        event_id=event.id,
        member_id=member.id
    ).first()

    if existing:

        flash("Already registered for this event.")

        return redirect(url_for("views.member"))

    going = RSVP.query.filter_by(
        event_id=event.id,
        status="going"
    ).count()

    if going >= event.capacity:

        status = "waitlisted"

        flash("Event full. Added to waitlist.")

    else:

        status = "going"

        flash("Successfully registered.")

    rsvp = RSVP(
        event_id=event.id,
        member_id=member.id,
        status=status
    )

    db.session.add(rsvp)

    db.session.commit()

    return redirect(url_for("views.member"))

@views.route("/member/cancel_rsvp/<int:event_id>", methods=["POST"])
def cancel_rsvp(event_id):

    rsvp = RSVP.query.filter_by(
        member_id=CURRENT_MEMBER,
        event_id=event_id
    ).first()

    if not rsvp:

        flash("RSVP not found.")

        return redirect(url_for("views.member"))

    was_going = rsvp.status == "going"

    db.session.delete(rsvp)

    db.session.commit()

    if was_going:

        waitlisted = RSVP.query.filter_by(
            event_id=event_id,
            status="waitlisted"
        ).first()

        if waitlisted:

            waitlisted.status = "going"

            db.session.commit()

    flash("RSVP cancelled.")

    return redirect(url_for("views.member"))

@views.route("/member/request_introduction/<int:event_id>/<int:target_id>", methods=["POST"])
def request_introduction(event_id, target_id):

    requester = Member.query.get_or_404(CURRENT_MEMBER)

    target = Member.query.get_or_404(target_id)

    # Cannot introduce yourself
    if requester.id == target.id:
        flash("You cannot introduce yourself.")
        return redirect(url_for("views.recommendations"))

    # Target must be opted in
    if not target.opted_in_to_matching:
        flash("That member has not opted in.")
        return redirect(url_for("views.recommendations"))

    # Already connected?
    existing = Introduction.query.filter(
        (
            (Introduction.requester_id == requester.id) &
            (Introduction.target_id == target.id)
        ) |
        (
            (Introduction.requester_id == target.id) &
            (Introduction.target_id == requester.id)
        )
    ).filter(
        Introduction.status == "approved"
    ).first()

    if existing:
        flash("You are already connected.")
        return redirect(url_for("views.recommendations"))

    intro = Introduction(
        event_id=event_id,
        requester_id=requester.id,
        target_id=target.id,
        reason="Recommended match",
        status="pending"
    )

    db.session.add(intro)
    db.session.commit()

    flash("Introduction request sent.")

    return redirect(url_for("views.recommendations"))

@views.route("/admin/approve/<int:introduction_id>", methods=["POST"])
def approve_introduction(introduction_id):

    intro = Introduction.query.get_or_404(introduction_id)

    duplicate = Introduction.query.filter(
        (
            (Introduction.requester_id == intro.requester_id) &
            (Introduction.target_id == intro.target_id)
        ) |
        (
            (Introduction.requester_id == intro.target_id) &
            (Introduction.target_id == intro.requester_id)
        )
    ).filter(
        Introduction.status == "approved",
        Introduction.id != intro.id
    ).first()

    if duplicate:

        flash("These members are already connected.")

        return redirect(url_for("views.admin"))

    intro.status = "approved"

    intro.admin_id = CURRENT_ADMIN

    db.session.commit()

    flash("Introduction approved.")

    return redirect(url_for("views.admin"))

@views.route("/admin/reject/<int:introduction_id>", methods=["POST"])
def reject_introduction(introduction_id):

    intro = Introduction.query.get_or_404(introduction_id)

    intro.status = "rejected"

    intro.admin_id = CURRENT_ADMIN

    db.session.commit()

    flash("Introduction rejected.")

    return redirect(url_for("views.admin"))

@
    )views.route("/member/recommendations")
def recommendations():

    current_member = Member.query.get_or_404(CURRENT_MEMBER)

    recommendations = []

    members = Member.query.filter(
        Member.id != CURRENT_MEMBER,
        Member.opted_in_to_matching == True
    ).all()

    for member in members:

        # Don't recommend someone already connected
        existing = Introduction.query.filter(
            (
                    (Introduction.requester_id == CURRENT_MEMBER) &
                    (Introduction.target_id == member.id)
            ) |
            (
                    (Introduction.requester_id == member.id) &
                    (Introduction.target_id == CURRENT_MEMBER)
            )
        ).filter(
            Introduction.status == "approved"
        ).first()

        if existing:
            continue

        score = 0

        # Domain match
        # Domain match
        if current_member.domain_tags and member.domain_tags:

            current_tags = {
                tag.strip().lower()
                for tag in current_member.domain_tags.split(",")
            }

            target_tags = {
                tag.strip().lower()
                for tag in member.domain_tags.split(",")
            }

            if current_tags.intersection(target_tags):
                score += 60

        # Same city
        if current_member.city == member.city:
            score += 20

        current_project = Project.query.filter_by(
            owner_id=current_member.id
        ).first()

        target_project = Project.query.filter_by(
            owner_id=member.id
        ).first()

        if current_project and target_project:
            if current_project.stage == target_project.stage:
                score += 20

        recommendations.append({
            "member": member,
            "score": score
        })

        recommendations.append({

            "member": member,

            "score": score

        })

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return render_template(
        "recommendations.html",
        recommendations=recommendations