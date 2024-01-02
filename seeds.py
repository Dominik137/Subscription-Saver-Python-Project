from models import *


if __name__  == '__main__':
    Users.__table__.drop(engine)
    Subscriptions.__table__.drop(engine)
    Base.metadata.create_all(engine)

