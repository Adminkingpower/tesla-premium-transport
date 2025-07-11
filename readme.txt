KingPower Premium Transport - Web App

Hi! This project is a simple web application I developed for IFQ557 Rapid Web Development. It allows users to book premium transport services (such as Tesla Model Y rides), 
either for point-to-point trips or by the hour with a driver. The main focus was to create a stylish, premium-looking page, using a black, gold, and white color scheme.

------------------------------------------------------------
Main Features

- Book three types of services: direct transfers, point-to-point, or hourly chauffeur service.
- Shopping cart functionality and booking submission.
- Responsive and clean layout using Flask and Bootstrap.
- Data stored in a lightweight SQLite database.
- Premium look and feel, with a consistent color palette.

------------------------------------------------------------
Project Structure

Inside the main `kp` folder, you'll find:

- __init__.py    – Starts the Flask app.
- admin.py       – Admin tools and data seeding.
- forms.py       – Booking forms.
- models.py      – SQLAlchemy database models.
- views.py       – Main routes and business logic.

Other important folders:
- static/        – Styles (CSS) and images.
- templates/     – HTML templates.

You'll also find a database file (kingpower.sqlite) with test data inside the instance/ folder.

------------------------------------------------------------
Setup Instructions

1. Open the project folder in VS Code.
2. Open a terminal in the project directory.
3. Make sure you have Python installed and updated.
4. Install the required Python packages:

   pip install flask flask_sqlalchemy flask_wtf

   (or, if there's a requirements.txt file: pip install -r requirements.txt)

5. (First-time only) Initialize the database by running the following lines in a Python terminal:

   from kp import create_app, db
   app = create_app()
   with app.app_context():
       db.create_all()

------------------------------------------------------------
How to Run

1. In the terminal, right-click run.py and select "Run Python File in Terminal".
2. Open your web browser (preferably Chrome) and go to http://127.0.0.1:5000
3. Check that the index page loads correctly (note: some sections might still be missing).
4. Go to /admin/seed in your browser to seed the database. Wait for the success message.
5. Return to the main page and test the app's functionality.

------------------------------------------------------------
Extra Information

- The database file (kingpower.sqlite) is optional; you can delete it to start fresh if needed.
- There is no login or authentication system (demo purposes only).
- You can visit /admin/bookings to view current bookings.

------------------------------------------------------------
Contact

Any questions or issues? Feel free to email me:
Santiago Osorio Ramirez  
n11949732@qut.edu.com

Thanks for checking out my project!
