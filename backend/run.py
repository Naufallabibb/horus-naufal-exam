from app import create_app
from app.extensions import db, migrate
from app.config import Config

app = create_app()

# Register migrate with app (untuk flask db commands)
# Ini sudah dilakukan di __init__.py, tapi kita perlu pastikan
# migrate bisa diakses dari run.py untuk CLI commands

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)