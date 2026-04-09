from flask import Flask
from flasgger import Swagger
from routes import routes

app = Flask(__name__)
Swagger(app, template_file='swagger.yml')

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
