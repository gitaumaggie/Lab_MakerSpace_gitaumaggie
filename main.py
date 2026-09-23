from database import (
    create_connection,
    add_member,
    get_members,
    update_member_email,
    add_equipment,
    get_equipment,
    update_equipment,
    update_equipment_availability,
    create_loan,
    get_loans,
    return_loan,
    get_active_loans
)

from services import (
    register_member,
    register_equipment,
    borrow_equipment,
    return_equipment,
    member_exists,
    equipment_exists,
    check_equipment_available,
    loan_exists,
    delete_member,
    delete_equipment,
    delete_loan,
    search_members,
    search_equipment,
    search_active_loans
)


def get_valid_integer(prompt):
    """Get a positive integer from the user."""
    while True:
        value = input(prompt).strip()

        try:
            value = int(value)

            if value <= 0:
                print("Error: Please enter a positive number.")
                continue

            return value

        except ValueError:
            print("Error: Please enter a valid number.")


def get_valid_date(prompt):
    """Get a date in YYYY-MM-DD format."""
    while True:
        date_text = input(prompt).strip()

        valid, message = validate_date(date_text)

        if valid:
            return date_text

        print(message)


def validate_date(date_text):
    """Validate a date using YYYY-MM-DD format."""
    from datetime import datetime

    try:
        date = datetime.strptime(
            date_text,
            "%Y-%m-%d"
        )

        if date.strftime("%Y-%m-%d") != date_text:
            return False, "Invalid date format. Use YYYY-MM-DD."

        return True, date.strftime("%Y-%m-%d")

    except ValueError:
        return False, "Invalid date. Please use YYYY-MM-DD."


def show_menu():
    """Display the main system menu."""
    print("\n===== CAMPUS MAKERSPACE CHECKOUT SYSTEM =====")
    print("1. Register Member")
    print("2. List Members")
    print("3. Register Equipment")
    print("4. List Equipment")
    print("5. Borrow Equipment")
    print("6. Return Equipment")
    print("7. View Active Loans")
    print("8. Delete")
    print("9. Search")
    print("10. Exit")


def main():
    """Run the Campus MakerSpace Checkout System."""
    connection = create_connection()

    while True:
        show_menu()

        choice = input(
            "Enter your choice: "
        ).strip()

        # Register Member
        if choice == "1":
            print("\n--- REGISTER MEMBER ---")

            name = input(
                "Enter member name: "
            ).strip()

            email = input(
                "Enter member email: "
            ).strip()

            success, message = register_member(
                connection,
                name,
                email
            )

            print(message)

        # List Members
        elif choice == "2":
            print("\n--- MEMBERS ---")

            members = get_members(connection)

            if not members:
                print("No members registered.")
            else:
                for member in members:
                    print(
                        f"ID: {member[0]} | "
                        f"Name: {member[1]} | "
                        f"Email: {member[2]}"
                    )

        # Register Equipment
        elif choice == "3":
            print("\n--- REGISTER EQUIPMENT ---")

            name = input(
                "Enter equipment name: "
            ).strip()

            category = input(
                "Enter equipment category: "
            ).strip()

            serial_number = input(
                "Enter equipment serial number: "
            ).strip()

            success, message = register_equipment(
                connection,
                name,
                category,
                serial_number
            )

            print(message)

        # List Equipment
        elif choice == "4":
            print("\n--- EQUIPMENT ---")

            equipment = get_equipment(connection)

            if not equipment:
                print("No equipment registered.")
            else:
                for item in equipment:
                    status = (
                        "Available"
                        if item[4]
                        else "Unavailable"
                    )

                    print(
                        f"ID: {item[0]} | "
                        f"Name: {item[1]} | "
                        f"Category: {item[2]} | "
                        f"Serial: {item[3]} | "
                        f"Status: {status}"
                    )

        # Borrow Equipment
        elif choice == "5":
            print("\n--- BORROW EQUIPMENT ---")

            member_id = get_valid_integer(
                "Enter member ID: "
            )

            if not member_exists(
                connection,
                member_id
            ):
                print(
                    f"Error: Member ID {member_id} "
                    "does not exist."
                )
                continue

            equipment_id = get_valid_integer(
                "Enter equipment ID: "
            )

            if not equipment_exists(
                connection,
                equipment_id
            ):
                print(
                    f"Error: Equipment ID {equipment_id} "
                    "does not exist."
                )
                continue

            available, message = check_equipment_available(
                connection,
                equipment_id
            )

            if not available:
                print(message)
                continue

            loan_date = get_valid_date(
                "Enter loan date (YYYY-MM-DD): "
            )

            success, message = borrow_equipment(
                connection,
                member_id,
                equipment_id,
                loan_date
            )

            print(message)

        # Return Equipment
        elif choice == "6":
            print("\n--- RETURN EQUIPMENT ---")

            loan_id = get_valid_integer(
                "Enter loan ID: "
            )

            if not loan_exists(
                connection,
                loan_id
            ):
                print(
                    f"Error: Active loan ID {loan_id} "
                    "does not exist."
                )
                continue

            equipment_id = get_valid_integer(
                "Enter equipment ID: "
            )

            if not equipment_exists(
                connection,
                equipment_id
            ):
                print(
                    f"Error: Equipment ID {equipment_id} "
                    "does not exist."
                )
                continue

            return_date = get_valid_date(
                "Enter return date (YYYY-MM-DD): "
            )

            success, message = return_equipment(
                connection,
                loan_id,
                equipment_id,
                return_date
            )

            print(message)

        # View Active Loans
        elif choice == "7":
            print("\n--- ACTIVE LOANS ---")

            loans = get_active_loans(connection)

            if not loans:
                print("No active loans.")
            else:
                for loan in loans:
                    print(
                        f"Loan ID: {loan[0]} | "
                        f"Member ID: {loan[1]} | "
                        f"Equipment ID: {loan[2]} | "
                        f"Loan Date: {loan[3]}"
                    )

        # Delete
        elif choice == "8":
            while True:
                print("\n--- DELETE ---")
                print("1. Delete Member")
                print("2. Delete Equipment")
                print("3. Delete Loan")
                print("4. Back to Main Menu")

                delete_choice = input(
                    "Enter your choice: "
                ).strip()

                if delete_choice == "1":
                    member_id = get_valid_integer(
                        "Enter member ID: "
                    )

                    success, message = delete_member(
                        connection,
                        member_id
                    )

                    print(message)

                elif delete_choice == "2":
                    equipment_id = get_valid_integer(
                        "Enter equipment ID: "
                    )

                    success, message = delete_equipment(
                        connection,
                        equipment_id
                    )

                    print(message)

                elif delete_choice == "3":
                    loan_id = get_valid_integer(
                        "Enter loan ID: "
                    )

                    confirm = input(
                        "Are you sure you want to delete "
                        "this loan? (yes/no): "
                    ).strip().lower()

                    if confirm != "yes":
                        print("Loan deletion cancelled.")
                        continue

                    success, message = delete_loan(
                        connection,
                        loan_id
                    )

                    print(message)

                elif delete_choice == "4":
                    break

                else:
                    print(
                        "Invalid delete option. "
                        "Please select an option from 1 to 4."
                    )

        # Search
        elif choice == "9":
            while True:
                print("\n--- SEARCH ---")
                print("1. Search Members")
                print("2. Search Equipment")
                print("3. Search Active Loans")
                print("4. Back to Main Menu")

                search_choice = input(
                    "Enter your choice: "
                ).strip()

                if search_choice == "1":
                    keyword = input(
                        "Enter member ID, name, or email: "
                    ).strip()

                    if not keyword:
                        print(
                            "Error: Search term cannot be empty."
                        )
                        continue

                    results = search_members(
                        connection,
                        keyword
                    )

                    if not results:
                        print("No members found.")
                    else:
                        print(
                            "\n--- MEMBER SEARCH RESULTS ---"
                        )

                        for member in results:
                            print(
                                f"ID: {member[0]} | "
                                f"Name: {member[1]} | "
                                f"Email: {member[2]}"
                            )

                elif search_choice == "2":
                    keyword = input(
                        "Enter equipment ID, name, "
                        "category, or serial number: "
                    ).strip()

                    if not keyword:
                        print(
                            "Error: Search term cannot be empty."
                        )
                        continue

                    results = search_equipment(
                        connection,
                        keyword
                    )

                    if not results:
                        print("No equipment found.")
                    else:
                        print(
                            "\n--- EQUIPMENT SEARCH RESULTS ---"
                        )

                        for equipment in results:
                            status = (
                                "Available"
                                if equipment[4]
                                else "Unavailable"
                            )

                            print(
                                f"ID: {equipment[0]} | "
                                f"Name: {equipment[1]} | "
                                f"Category: {equipment[2]} | "
                                f"Serial: {equipment[3]} | "
                                f"Status: {status}"
                            )

                elif search_choice == "3":
                    keyword = input(
                        "Enter loan ID, member ID, "
                        "or equipment ID: "
                    ).strip()

                    if not keyword:
                        print(
                            "Error: Search term cannot be empty."
                        )
                        continue

                    results = search_active_loans(
                        connection,
                        keyword
                    )

                    if not results:
                        print("No active loans found.")
                    else:
                        print(
                            "\n--- ACTIVE LOAN SEARCH RESULTS ---"
                        )

                        for loan in results:
                            print(
                                f"Loan ID: {loan[0]} | "
                                f"Member ID: {loan[1]} | "
                                f"Equipment ID: {loan[2]} | "
                                f"Loan Date: {loan[3]}"
                            )

                elif search_choice == "4":
                    break

                else:
                    print(
                        "Invalid search option. "
                        "Please select an option from 1 to 4."
                    )

        # Exit
        elif choice == "10":
            print(
                "\nThank you for using the "
                "Campus MakerSpace Checkout System!"
            )
            break

        else:
            print(
                "Invalid choice. "
                "Please enter a number from 1 to 10."
            )

    connection.close()


if __name__ == "__main__":
    main()