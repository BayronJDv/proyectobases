from venv import create
from app import create_app, db
from app.auth.models import User,Client,Userm,Delivery


easydel =  create_app("prod")
with easydel.app_context():
    db.create_all()

    if not Client.query.filter_by(client_name="admin").first():
        Client.create_client(
            name="admin",
            address="admin",
            email="admin@admin.com",
            telephone="admin"
        )
    if not User.query.filter_by(user_name="admin").first():
        User.create_admin(
            user="admin",
            email="admin@admin.com",
            password="admin",
            address="admin",
            clientid=1
        )
    
    if not Delivery.query.filter_by(delivery_name="testD").first():
        Delivery.create_delivery(
            name="testDelivery",
            address="test adress",
            email="test-testing@test.com",
            telephone="test**123"
        ) 
          
    if not Userm.query.filter_by(userm_name="test_APARECE").first():
        Userm.create_userm(
            user="test_APARECE",
            email="testA-testing@test.com",
            password="testA**123",
            address="test-address",
            deliveryid=1
        )
        # create a client and a user for testing 
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
            clientid=2
        )
    
easydel.run()
