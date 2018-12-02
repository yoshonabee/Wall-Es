from flask import (
    Flask,
    render_template,
    send_from_directory
)

# Create the application instance
app = Flask(__name__, template_folder="../frontend")

# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """
    return render_template('index.html')

# frontend files
@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('../frontend', path)

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)