import os
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

PORT = int(os.environ.get("PORT", 5000))

# Register routes (we will build these in next steps)
from routes.lobby_routes import lobby_bp
from routes.game_routes import game_bp

app.register_blueprint(lobby_bp, url_prefix='/api/lobby')
app.register_blueprint(game_bp, url_prefix='/api/game')

@app.route("/")
def index():
    return {"msg": "🎰 Blackjack Flask API Online"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
