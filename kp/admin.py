from flask import Blueprint, render_template, redirect, url_for, flash, request
from . import db
from .models import Category, Service, Booking, Customer, Admin

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/seed')
def seed_db():
    if Service.query.first():
        return "Database already loaded. Delete kingpower.sqlite if you want to reload.", 400

    cat_intercity = Category(
        name='Intercity Transfer',
        description='Premium transfers to cities like Gold Coast, Sunshine Coast, Ipswich, Toowoomba and more.',
        image='intercity.png',
        endpoint='intercity'
    )
    cat_hourly = Category(
        name='Hourly Chauffeur',
        description='Book a luxury Tesla and professional driver for hours or days.',
        image='hourly2.png',
        endpoint='hourly'
    )
    cat_point = Category(
        name='Point-to-Point',
        description='Comfortable urban transfers within Brisbane, pay only for the distance.',
        image='point2.png',
        endpoint='point'
    )
    db.session.add_all([cat_intercity, cat_hourly, cat_point])
    db.session.commit()

    intercity_services = [
        Service(name="To Gold Coast", description="$110 – From Brisbane to Gold Coast",
                price=110, detail_url="", category_id=cat_intercity.id),
        Service(name="From Gold Coast", description="$120 – From Gold Coast to Brisbane",
                price=120, detail_url="", category_id=cat_intercity.id),
        Service(name="Round Trip Gold Coast", description="$190 – Gold Coast & back (same day)",
                price=190, detail_url="", category_id=cat_intercity.id),
        Service(name="To Sunshine Coast", description="$170 – From Brisbane to Sunshine Coast",
                price=170, detail_url="", category_id=cat_intercity.id),
        Service(name="From Sunshine Coast", description="$180 – From Sunshine Coast to Brisbane",
                price=180, detail_url="", category_id=cat_intercity.id),
        Service(name="Round Trip Sunshine Coast", description="$330 – Sunshine Coast & back (same day)",
                price=330, detail_url="", category_id=cat_intercity.id),
        Service(name="To Toowoomba", description="$220 – From Brisbane to Toowoomba",
                price=220, detail_url="", category_id=cat_intercity.id),
        Service(name="From Toowoomba", description="$220 – From Toowoomba to Brisbane",
                price=220, detail_url="", category_id=cat_intercity.id),
    ]

    hourly_services = [
        Service(name="Hourly Daytime", description="$110/hour – 6am to 6pm",
                price=110, detail_url="", category_id=cat_hourly.id),
        Service(name="Hourly Night", description="$130/hour – 6pm to Midnight",
                price=130, detail_url="", category_id=cat_hourly.id),
        Service(name="Full Day Package", description="$750 – Up to 8 hours",
                price=750, detail_url="", category_id=cat_hourly.id)
    ]

    point_services = [
        Service(name="0–5 km Trip", description="$40 – Ideal for quick inner-city transfers",
                price=40, detail_url="", category_id=cat_point.id),
        Service(name="6–10 km Trip", description="$50 – Short-to-mid range luxury rides",
                price=50, detail_url="", category_id=cat_point.id),
        Service(name="11–20 km Trip", description="$70 – Stress-free longer city trips",
                price=70, detail_url="", category_id=cat_point.id),
        Service(name="21–30 km Trip", description="$90 – Ideal for airport or outer-suburb rides",
                price=90, detail_url="", category_id=cat_point.id),
        Service(name="31–40 km Trip", description="$110 – Premium comfort for longer distances",
                price=110, detail_url="", category_id=cat_point.id),
        Service(name="41–50 km Trip", description="$130 – Arrive fresh even across cities",
                price=130, detail_url="", category_id=cat_point.id)
    ]

    db.session.add_all(intercity_services + hourly_services + point_services)

    if not Admin.query.first():
        admin_user = Admin(
            name='Santiago Osorio',
            email='admin@kingpower.com',
            permissions='admin'
        )
        viewer_user = Admin(
            name='Carlos Smith',
            email='driver@kingpower.com',
            permissions='viewer'
        )
        db.session.add_all([admin_user, viewer_user])

    db.session.commit()

    return "Database uploaded successfully"

@admin_bp.route('/bookings')
def admin_bookings():
    bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
    return render_template('bookings.html', bookings=bookings)

@admin_bp.route('/delete_booking/<int:booking_id>', methods=['POST'])
def admin_delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    flash("Booking deleted successfully.", "success")
    return redirect(url_for('admin.admin_bookings'))
