def input_error(func):
    def inner(*args, **kwargs):
        """
        Decorator for handling user input errors.
        Catches ValueError, KeyError, and IndexError and returns
        user-friendly messages instead of stopping the program.
        """
        try:
            return func(*args, **kwargs)

        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter the argument for the command."

    return inner

def parse_input(user_input):
    """
    Parses user input into command and arguments.
    Example: 'add Bob 1234' -> ('add', 'Bob', '1234')
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts):
    """
    Adds a new contact to the contacts dictionary.
    Command format: add <name> <phone>
    """
    name = args[0]

    if name in contacts:
        return "Contact already exists."

    if len(args) != 2:
        raise ValueError

    phone = args[1]
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    """
    Updates the phone number for an existing contact.
    Command format: change <name> <phone>
    """
    name = args[0]
    if name not in contacts:
        raise KeyError

    if len(args) != 2:
        raise ValueError

    phone = args[1]
    contacts[name] = phone
    return "Contact updated."

@input_error
def show_phone(args, contacts):
    """
    Returns the phone number for the given contact.
    Command format: phone <name>
    """
    name = args[0]
    if name not in contacts:
        raise KeyError
    return contacts[name]

@input_error
def show_all(contacts):
    """
    Returns all saved contacts in formatted form.
    Command format: all
    """
    if not contacts:
        return "No contacts found."
    result = ""
    for name, phone in contacts.items():
        result += f"{name}: {phone}\n"
    return result.strip()



def main():
    """
    Main program loop for the assistant bot.
    Handles user commands until the user exits.
    """
    contacts = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            print("Enter the argument for the command.")
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()