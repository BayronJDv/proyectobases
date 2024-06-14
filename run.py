from venv import create
from app import create_app, db
from app.auth.models import User,Client


easydel =  create_app("prod")
with easydel.app_context():
    db.create_all()
    if not Client.query.filter_by(client_name="testclient").first():
        Client.create_client(
            name="testclient",
            address="test adress",
            email="test-testing@test.com",
            telephone="test**123"
        )
    if not User.query.filter_by(user_name="test").first():
        User.create_user(
            user="test",
            email="test-testing@test.com",
            password="test**123",
            address="test-address",
            clientid=1
        )
easydel.run()