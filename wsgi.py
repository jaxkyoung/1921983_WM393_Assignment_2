from app.app import app
app.secret_key = ('super secret key')
if __name__ == "__main__":
    app.run(debug=True)