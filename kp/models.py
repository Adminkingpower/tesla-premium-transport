from datetime import datetime
from . import db

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)  
    image = db.Column(db.String(120), nullable=True)        
    endpoint = db.Column(db.String(100), nullable=False) 
    services = db.relationship('Service', back_populates='category')

    def __repr__(self):
        return f"Category(id={self.id}, name='{self.name}', description='{self.description}', image='{self.image}')"


class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    detail_url = db.Column(db.String(120), nullable=True)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', back_populates='services')

    bookings = db.relationship('Booking', back_populates='service')

    def __repr__(self):
        return (f"Service(id={self.id}, name='{self.name}', description='{self.description}', "
                f"price={self.price}, image='{self.image}', detail_url='{self.detail_url}', "
                f"category_id={self.category_id})")


class Admin(db.Model):
    __tablename__ = 'admins'
    admin_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    permissions = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Admin(id={self.admin_id}, name='{self.name}', email='{self.email}', permissions='{self.permissions}')"


class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(80), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    suburb = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)

    bookings = db.relationship('Booking', back_populates='customer')

    def __repr__(self):
        return (
            f"Customer(id={self.customer_id}, full_name='{self.full_name}', "
            f"email='{self.email}', phone='{self.phone}', country='{self.country}', "
            f"address='{self.address}', suburb='{self.suburb}', city='{self.city}')"
        )

class Booking(db.Model):
    __tablename__ = 'bookings'
    booking_id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    pickup_address = db.Column(db.String(200), nullable=True)
    dropoff_address = db.Column(db.String(200), nullable=True)
    notes = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), nullable=True)

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'))
    customer = db.relationship('Customer', back_populates='bookings')

    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    service = db.relationship('Service', back_populates='bookings')

    def __repr__(self):
        return (f"Booking(id={self.booking_id}, date={self.booking_date}, pickup='{self.pickup_address}', "
                f"dropoff='{self.dropoff_address}', hours={self.hours_requested}, notes='{self.notes}', "
                f"status='{self.status}', customer_id={self.customer_id}, service_id={self.service_id})")
