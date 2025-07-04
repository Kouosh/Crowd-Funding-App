import auth
import projects

def main_menu():
    while True:
        print("\nCrowd-Funding Console App")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Select an option: ")
        if choice == '1':
            auth.register()
        elif choice == '2':
            user = auth.login()
            if user:
                projects.project_menu(user)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu() 