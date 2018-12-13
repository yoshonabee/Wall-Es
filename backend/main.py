from flask import (
    Flask,
    request,
    render_template,
    send_from_directory
)

from lib.game.game import Game

# Create the application instance
app = Flask(__name__, template_folder="../frontend")

game = None

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

@app.route('/newGame')
def newGame():
    global game

    height = int(request.args.get("height"))
    width = int(request.args.get("width"))
    t = (height + width)/2
    game = Game(height, width)
    game.setRandomMap(5, int(t*0.4)**2, int(t*0.3)**2)
    game.printGodMap()
    game.torchNext()
    game.printConsoleMap()
    return game.jsonMap()

@app.route('/next')
def next():
    game.torchNext()
    game.printConsoleMap()
    return game.jsonMap()

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)