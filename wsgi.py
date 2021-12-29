<<<<<<< Updated upstream
from app.app import app
app.secret_key = ('super secret key')
=======
from app import create_app
app = create_app()
app.config.from_object('app.config.ProductionConfig')

>>>>>>> Stashed changes
if __name__ == "__main__":
    app.run(debug=True)