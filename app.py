from sqlalchemy.orm import Session as SQLAlchemySession
from models import create_user, authenticate_user, get_user_subscriptions, create_subscription, Session, delete_subscription

if __name__ == '__main__':
    exit_program = False
    authenticated_user = None

    while not exit_program:

        if not authenticated_user:
            first_prompt = input("""
Welcome:
1) Create Profile
2) Log in
3) Exit
""")
            
            if first_prompt == "1":
                # Create a new profile
                while True:
                    username = input("Create Username: ")
                    password = input('Create Password: ')
                    
                    create_user(username, password)
                    break

            elif first_prompt == "2":
                # Log in
                while True:
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    authenticated_user = authenticate_user(username, password)

                    if authenticated_user:
                        while True:
                            second_prompt = input('''
1) See all Subscriptions
2) Add new Subscription
3) Logout
''')
                            if second_prompt == "1":
                                # Show all subscriptions
                                subscriptions = get_user_subscriptions(authenticated_user)
                                if not subscriptions:
                                    print("No subscriptions saved.")
                                while True:
                                    third_prompt = input('''
1) Delete Subscription
2) Edit Subscription
3) Exit 
''')

                                    if third_prompt == "1":
                                     # Delete Subscription
                                        subscription_id_to_delete = input("Enter the Number of the subscription to delete: ")
    
                                        # Check if the input is not an empty string
                                        if subscription_id_to_delete:
                                            try:
                                        # Attempt to convert subscription_id_to_delete to an integer
                                                subscription_id_to_delete = int(subscription_id_to_delete)
            
                                        # Call the delete_subscription function
                                                delete_subscription(authenticated_user, subscription_id_to_delete)
                                            except ValueError:
                                                print("Invalid input. Please enter a valid subscription ID.")
                                        
                                        
                                    elif third_prompt == "2":
                                        pass

                                    elif third_prompt == "3":
                                        break

                            elif second_prompt == "2":
                                # Add new subscription
                                Service_Name = input("Enter Service name: ")
                                Cost = float(input("Enter cost: "))  # Assuming cost is a float field
                                Bill_date = int(input("Enter the day of the month you will be billed: "))
                                create_subscription(authenticated_user, Service_Name, Cost, Bill_date)
                                

                            elif second_prompt == "3":
                                # Logout
                                authenticated_user = None
                                print("Logged out successfully.")
                                break  # Exit the second loop and go back to the main menu  

                            else:
                                print("Not valid selection")

                        if authenticated_user is None:
                            break

                    else:
                        # print("Login failed. Invalid username or password.")
                        break

            elif first_prompt == "3":
                # Exit program
                print("Exiting program.")
                exit_program = True
        
            else:
                print('Not valid selection')
