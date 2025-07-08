from ext import app



if __name__ == '__main__':
    from routes import home,register, about, login, food, profile, booking
    app.run(debug=True)



