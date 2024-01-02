from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, func, Float
from sqlalchemy.orm import Session, declarative_base, validates, relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

Base = declarative_base()


class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

# this takes in both attributes of our table username and password and makes sure that they are boths strings, if they aren't it will raise an error
    @validates('username', 'password')
    def validate_string(self, key, value):
        if not isinstance(value, str):
            raise ValueError(f"{key} must be a string.")
    
        if len(value) < 3:
            raise ValueError(f"{key} must be at least 3 characters long.")
        
        existing_user = session.query(Users).filter_by(username=value).first()
        if existing_user:
            raise ValueError(f"{key} must be unique. The provided {key} is already in use.")
        
        return value

def create_user(username, password):
    # Create a new User instance
    new_user = Users(username=username, password=password)

    try:
        # Add the new user to the session
        session.add(new_user)
        
        # Commit the changes to the database
        session.commit()
        print(f"User '{username}' added successfully.")
    except Exception as e:
        # Rollback the transaction if there is an error
        session.rollback()
        print(f"Error adding user '{username}': {e}")
    finally:
        # Close the session
        session.close()



def authenticate_user(username, password):
    try:
        user = session.query(Users).filter_by(username=username, password=password).one()
        print(f"Login successful. Welcome, {username}!")
        return user  # Return the user object
    except NoResultFound:
        print("Login failed. Invalid username or password.")
        return None  # Return None if authentication fails

    


class Subscriptions(Base):
    __tablename__ = "Subscriptions"
    id = Column(Integer, primary_key=True)
    Service_Name = Column(String, nullable=False)
    Cost = Column(Float, nullable=False)
    Bill_date = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)


def get_user_subscriptions(user):
    try:
        # Refresh the user object to ensure it's bound to the session
        session.refresh(user)
        # Query all subscriptions for the logged-in user
        all_subscriptions = session.query(Subscriptions).filter_by(user_id=user.id).all()

        # Print or process the subscriptions as needed
        for subscription in all_subscriptions:
            print(f"Service, {subscription.Service_Name}, Cost: {subscription.Cost}, Bill Date: {subscription.Bill_date}")

        return all_subscriptions
    except Exception as e:
        print(f"Error retrieving subscriptions: {e}")
        return []

def create_subscription(user, Service_Name, Cost, Bill_date,):
    # Create a new User instance
    new_sub = Subscriptions(Service_Name=Service_Name, Cost=Cost, Bill_date=Bill_date, user_id=user.id)

    try:
        # Add the new user to the session
        session.add(new_sub)
        
        # Commit the changes to the database
        session.commit()
        print(f"Your '{Service_Name}' Subscription was added successfully.")
    except Exception as e:
        # Rollback the transaction if there is an error
        session.rollback()
        print(f"Error adding '{Service_Name}': {e}")
    finally:
        # Close the session
        session.close()



engine = create_engine('sqlite:///Subscription_Tracker.db')
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()


# test:
# create_user("john_doe", "password123")

