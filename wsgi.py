from app import create_app

app = create_app()
app.config.from_object('app.config.ProductionConfig')
app.app_context().push()
