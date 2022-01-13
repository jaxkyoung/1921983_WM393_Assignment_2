'''
run.py: Used to run development server on local host
version: 1.0
author: 1921983
'''
# import create app factory from app package
from app import create_app

# create app
app = create_app()
# set app config to dev config
app.config.from_object('app.config.DevelopmentConfig')

# run app
if __name__ == "__main__":
    app.run()