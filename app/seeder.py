import random
from app.models import Requisites, PaymentRequests


def generate_random_name():
    names = ['John', 'Jane', 'Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace', 'Hank']
    return random.choice(names)


def seed(db):
    try:
        for _ in range(100):
            requisites = Requisites(
                account = str(random.randint(10**15, 10**16 - 1)),
                payment_type = random.choice(['Card', 'Pay amount']),
                account_type = random.choice(['Credit', 'Debit']),
                owner_name = generate_random_name(),
                phone_number = str(random.randint(10**9, 10**10 - 1)),
                limit = round(random.uniform(0, 20000), 2)
            )
            db.session.add(requisites)
            db.session.commit()

        for _ in range(5000):
            payment_requests = PaymentRequests(
                amount = round(random.uniform(0, 20000), 2),
                status = random.choice(['Wait', 'Success', 'Cancel']),
                requisites_id = random.randint(1, 100)
            )
            db.session.add(payment_requests)
            db.session.commit()
        print('Seed OK')
    except Exception as e:
        print(e)
        db.session.rollback()
