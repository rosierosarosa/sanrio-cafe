from flask import abort, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash

from forms import BookingForm, FoodForm, RegisterForm, LoginForm, ProfileForm, RatingForm
from os import path
from ext import app, db
from models import Food, User, Booking, Rating
from flask_login import login_user, logout_user, login_required, current_user





@app.route("/")
def home():
    food_list = Food.query.all()
    return render_template("index.html", food_list=food_list)




admin_emails = ["mmyrosie@gmail.com"]

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user_role = 'admin' if form.email.data.lower() in admin_emails else 'guest'

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            role=user_role
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html", form=form)






@app.route('/about')
def about():
    return render_template('about.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Welcome!")
            return redirect("/")
        else:
            flash("Invalid email or password.")
    return render_template("login.html", form=form)





@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route('/foodlist')
def food():
    food_list = Food.query.all()
    return render_template('food.html', food_list=food_list, role="admin")




@app.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():
    form = BookingForm()
    if form.validate_on_submit():
        new_booking = Booking(
            name=form.name.data,
            date=form.date.data,
            num_guests=form.guests.data,
            special_requests=form.comment.data,
            user_id=current_user.id
        )
        db.session.add(new_booking)
        db.session.commit()
        flash("Booking successful!", "success")
        return render_template(
            'booking_success.html',
            name=form.name.data,
            date=form.date.data,
            guests=form.guests.data,
            comment=form.comment.data
        )
    return render_template('booking.html', form=form)







@app.route('/booking_success')
@login_required
def booking_success():
    return render_template('booking_success.html')



@app.route("/add_food", methods=["POST", "GET"])
def add_food():
    form = FoodForm()
    if form.validate_on_submit():
        new_food = Food(name=form.name.data, description=form.description.data)
        image = form.image.data
        directory = path.join(app.root_path, "static", "images", image.filename)
        image.save(directory)
        new_food.image = image.filename

        db.session.add(new_food)
        db.session.commit()

        return redirect("/foodlist")
    return render_template("add_food.html", form=form)







def admin_required():
    if not current_user.is_authenticated or current_user.role.lower() != "admin":
        abort(403)

@app.route("/edit_food/<int:food_id>", methods=["GET", "POST"])
@login_required
def edit_food(food_id):
    admin_required()

    food = Food.query.get_or_404(food_id)
    form = FoodForm()

    if form.validate_on_submit():
        food.name = form.name.data
        food.description = form.description.data

        image = form.image.data
        if image:
            filename = image.filename
            image_path = path.join(app.root_path, "static", "images", filename)
            image.save(image_path)
            food.image = filename

        db.session.commit()
        flash("Food updated successfully!")
        return redirect("/")

    form.name.data = food.name
    form.description.data = food.description
    form.image.data = None

    return render_template("edit_food.html", form=form)


@app.route("/delete_food/<int:food_id>", methods=["POST"])
@login_required
def delete_food(food_id):
    admin_required()

    food = Food.query.get_or_404(food_id)
    db.session.delete(food)
    db.session.commit()
    flash("Food deleted!")
    return redirect("/")







@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.commit()
        flash("Profile updated!", "success")
        return redirect("/profile")

    return render_template("profile.html", user=current_user, form=form)







@app.route("/admin/bookings")
@login_required
def admin_bookings():
    if current_user.role.lower() != "admin":
        abort(403)

    all_bookings = Booking.query.order_by(Booking.date.desc()).all()
    return render_template("admin_bookings.html", bookings=all_bookings)







@app.route('/food/<int:food_id>', methods=['GET', 'POST'])
@login_required
def food_detail(food_id):
    food = Food.query.get_or_404(food_id)
    form = RatingForm()


    existing_rating = Rating.query.filter_by(user_id=current_user.id, food_id=food_id).first()

    if form.validate_on_submit():
        score = int(form.score.data)
        if existing_rating:
            existing_rating.score = score
        else:
            new_rating = Rating(score=score, user_id=current_user.id, food_id=food_id)
            db.session.add(new_rating)
        db.session.commit()
        flash('Thanks for rating! 💖', 'success')
        return redirect(url_for('food_detail', food_id=food_id))

    if existing_rating:
        form.score.data = str(existing_rating.score)

    ratings = [r.score for r in food.ratings]
    avg_rating = round(sum(ratings) / len(ratings), 1) if ratings else None

    return render_template('food_detail.html', food=food, form=form, avg_rating=avg_rating)
