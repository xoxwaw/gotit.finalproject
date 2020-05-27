from main import create_app
from main.db import db

app = create_app('dev')


@app.before_first_request
def create_table():
    db.create_all()


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=8000, debug=True)
