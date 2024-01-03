from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, func, Float
from sqlalchemy.orm import Session, declarative_base, validates, relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

Base = declarative_base()


class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    @validates('username', 'password')
    def validate_string(self, key, value):
        if not isinstance(value, str):
            raise ValueError(f"{key} must be a string.")
    
        if len(value) >= 3:
            return value
        else:
            print(f"{key} must be at least 3 characters long.")

def create_user(username, password):
    clear_console()
    # Check for uniqueness separately
    existing_user = session.query(Users).filter_by(username=username).first()
    if existing_user:
        print(f"Error adding user '{username}': Username must be unique.")
        return  # Exit the function if username is not unique

    # Create a new User instance
    new_user = Users(username=username, password=password)

    try:
        # Add the new user to the session
        session.add(new_user)

        # Commit the changes to the database
        session.commit()
        print(f"User '{username}' added successfully.")
    except Exception as e:
        # Catch any exception and print a generic error message
        print(f"Error adding user '{username}': {e}")
        # Rollback the transaction if there is an error
        session.rollback()

def authenticate_user(username, password):
    clear_console()
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
    subscription_id = Column(Integer, unique=False, nullable=False)  # New unique identifier for each subscription
    Service_Name = Column(String, nullable=False)
    Cost = Column(Float, nullable=False)
    Bill_date = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)

# Global variable for subscription_id counter
subscription_id_counter = 1

def get_user_subscriptions(user):
    clear_console()
    try:
        # Refresh the user object to ensure it's bound to the session
        session.refresh(user)
        # Query all subscriptions for the logged-in user
        all_subscriptions = session.query(Subscriptions).filter_by(user_id=user.id).all()

        # ... (unchanged)
        # Print or process the subscriptions as needed
        for subscription in all_subscriptions:
            print(f"\033[4m{subscription.subscription_id}: Service, {subscription.Service_Name}, Cost: {subscription.Cost}, Bill Date: {subscription.Bill_date}\033[0m")

        return all_subscriptions
    except Exception as e:
        print(f"Error retrieving subscriptions: {e}")
        return []

def create_subscription(user, service_name, cost, bill_date):
    # finds the number of subscriptions the users on
    max_subscription_id = session.query(func.max(Subscriptions.subscription_id)).filter_by(user_id=user.id).scalar()

    # If there are no existing subscriptions, set max_subscription_id to 0
    if max_subscription_id is None:
        max_subscription_id = 0

    # Increment the max_subscription_id to get a unique value for the new subscription
    subscription_id = max_subscription_id + 1

    # Create a new Subscription instance
    new_sub = Subscriptions(
        subscription_id=subscription_id,
        Service_Name=service_name,  # Corrected column name
        Cost=cost,
        Bill_date=bill_date,
        user_id=user.id
    )

    try:
        # Add the new subscription to the session
        session.add(new_sub)

        # Commit the changes to the database
        session.commit()
        clear_console()
        print(f"Your '{service_name}' Subscription with ID '{subscription_id}' was added successfully.")
    except Exception as e:
        # Rollback the transaction if there is an error
        session.rollback()
        print(f"Error adding '{service_name}': {e}")
    
def delete_subscription(user, subscription_id):
    clear_console()
    try:
        # Query the subscription to be deleted
        subscription_to_delete = session.query(Subscriptions).filter_by(user_id=user.id, subscription_id=subscription_id).one()

        # Delete the subscription from the session
        session.delete(subscription_to_delete)

        # Commit the changes to the database
        session.commit()
        print(f"Subscription with ID '{subscription_id}' deleted successfully.")
    except NoResultFound:
        print(f"Error deleting subscription with ID '{subscription_id}': Subscription not found.")
    except Exception as e:
        # Rollback the transaction if there is an error
        session.rollback()
        print(f"Error deleting subscription with ID '{subscription_id}': {e}")

def edit_subscription(user, subscription_id, new_service_name=None, new_cost=None, new_bill_date=None):
    try:
        # Query the subscription to be edited
        subscription_to_edit = session.query(Subscriptions).filter_by(user_id=user.id, subscription_id=subscription_id).one()

        # Update the subscription attributes with new values if provided
        if new_service_name is not None:
            if new_service_name == '':
                pass
            else:
                subscription_to_edit.Service_Name = new_service_name

        if new_cost is not None:
            if new_cost == '':
                # Do something appropriate when new_cost is an empty string (e.g., set to None or a default value)
                pass
            else:
                subscription_to_edit.Cost = float(new_cost)
                
        if new_bill_date is not None:
            if new_bill_date == '':
                pass
            else:
                subscription_to_edit.Bill_date = new_bill_date

        # Commit the changes to the database
        session.commit()
        clear_console()
        print(f"Subscription with ID '{subscription_id}' edited successfully.")
    except NoResultFound:
        print(f"Error editing subscription with ID '{subscription_id}': Subscription not found.")
    except Exception as e:
        # Rollback the transaction if there is an error
        session.rollback()
        print(f"Error editing subscription with ID '{subscription_id}': {e}")


engine = create_engine('sqlite:///Subscription_Tracker.db')
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
with Session() as session:
    pass

# test:
# create_user("john_doe", "password123")

