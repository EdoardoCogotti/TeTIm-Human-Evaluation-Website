from flask_tetim import app
from flask_tetim import routes

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, use_reloader=False)
