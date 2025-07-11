from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from .models import Service, Category, db, Customer, Booking
from .forms import CheckoutForm
import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    categories = Category.query.all()
    return render_template('index.html', categories=categories)

@bp.route('/intercity')
def intercity():
    category = Category.query.filter_by(endpoint='intercity').first()
    services = category.services if category else []
    other_categories = Category.query.filter(Category.endpoint != 'intercity').all()
    return render_template('intercity.html', services=services, other_categories=other_categories)

@bp.route('/hourly')
def hourly():
    category = Category.query.filter_by(endpoint='hourly').first()
    services = category.services if category else []
    other_categories = Category.query.filter(Category.endpoint != 'hourly').all()
    return render_template('hourly.html', services=services, other_categories=other_categories)

@bp.route('/point')
def point():
    category = Category.query.filter_by(endpoint='point').first()
    services = category.services if category else []
    other_categories = Category.query.filter(Category.endpoint != 'point').all()
    return render_template('point.html', services=services, other_categories=other_categories)

@bp.route('/add_to_cart/<int:service_id>', methods=['POST'])
def add_to_cart(service_id):
    cart = session.get('cart', [])
    if service_id not in cart:
        cart.append(service_id)
        session['cart'] = cart
        flash('Service added to cart.')
    else:
        flash('Service is already in the cart.')
    ref = request.referrer or url_for('main.home')
    if "#services" not in ref:
        if "?" in ref:
            ref = ref.split("?")[0]
        ref = ref.rstrip('/') + "#services"
    return redirect(ref)

@bp.route('/remove_from_cart/<int:service_id>', methods=['POST'])
def remove_from_cart(service_id):
    cart = session.get('cart', [])
    if service_id in cart:
        cart.remove(service_id)
        session['cart'] = cart
        flash('Service removed from cart.')
    return redirect(url_for('main.cart'))

@bp.route('/clear_cart', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    flash('All items have been deleted from the cart.')
    return redirect(url_for('main.cart'))

@bp.route('/cart')
def cart():
    cart = session.get('cart', [])
    services = Service.query.filter(Service.id.in_(cart)).all() if cart else []
    totalprice = sum(service.price for service in services)
    return render_template('cart.html', services=services, totalprice=totalprice)

@bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    now = datetime.datetime.now()
    cart = session.get('cart', [])
    services = Service.query.filter(Service.id.in_(cart)).all() if cart else []
    total_price = sum(service.price for service in services)

    if not services:
        flash("Your basket is empty. Please select at least one service.", "warning")
        return redirect(url_for('main.cart'))

    if request.method == 'POST':
        print("Data received:", request.form)
        print("WTForms errors:", form.errors)
        print("Validator:", form.validate())

        if form.validate():
            missing_fields = False
            for service in services:
                if (
                    not request.form.get(f'pickup_address_{service.id}') or 
                    not request.form.get(f'dropoff_address_{service.id}') or 
                    not request.form.get(f'booking_date_{service.id}')
                ):
                    missing_fields = True
                    flash(f"Please complete all fields for {service.name}.", "danger")
            if missing_fields:
                return render_template('checkout.html', form=form, services=services, total_price=total_price, now=now)

            new_customer = Customer(
                full_name=form.fullName.data,
                email=form.email.data,
                phone=form.phone.data,
                country=form.country.data,
                address=form.address.data,
                suburb=form.suburb.data,
                city=form.city.data
            )
            db.session.add(new_customer)
            db.session.commit()

            for service in services:
                pickup_address = request.form.get(f'pickup_address_{service.id}')
                dropoff_address = request.form.get(f'dropoff_address_{service.id}')
                booking_date_str = request.form.get(f'booking_date_{service.id}')
                notes = request.form.get(f'notes_{service.id}')
                try:
                    booking_date = datetime.datetime.strptime(booking_date_str, "%Y-%m-%dT%H:%M")
                except Exception:
                    booking_date = now 

                new_booking = Booking(
                    booking_date=booking_date,
                    pickup_address=pickup_address,
                    dropoff_address=dropoff_address,
                    notes=notes,
                    status="Pending",
                    customer_id=new_customer.customer_id,
                    service_id=service.id
                )
                db.session.add(new_booking)
            db.session.commit()

            session.pop('cart', None)
            flash("We have received your request. We will contact you soon.", "success")
            return redirect(url_for('main.home'))

    return render_template(
        'checkout.html',
        form=form,
        services=services,
        total_price=total_price,
        now=now
    )
