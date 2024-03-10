from views import views
from handlers.extensions import bcrypt
from flask import Flask, render_template


# Declare the app
app = Flask(__name__)
app.register_blueprint(views, url_prefix='/')
app.config['SECRET_KEY'] = 'LECI'
bcrypt.init_app(app)

# Define a custom error handler for 403 (Not Found) errors
@app.errorhandler(403)
def page_not_found(error):
    return render_template('403.html'), 403


# Define a custom error handler for 404 (Not Found) errors
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# Define a custom error handler for 500 (Not Found) errors
@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
