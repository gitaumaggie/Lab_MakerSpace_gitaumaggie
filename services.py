from datetime import datetime
from database import (
    add_member,
    get_members,
    update_member_email,
    delete_member as db_delete_member,
    add_equipment,
    get_equipment,
    update_equipment,
    delete_equipment as db_delete_equipment,
    update_equipment_availability,
    create_loan,
    get_loans,
    return_loan,
    get_active_loans
)


def validate_date(date_text):
    """Validate and format a date as YYYY-MM-DD."""
    try:
        date = datetime.strptime(date_text, "%Y-%m-%d")

        if date.strftime("%Y-%m-%d") != date_text:
            return False, "Invalid date format. Use YYYY-MM-DD."

        return True, date.strftime("%Y-%m-%d")

    except ValueError:
        return False, "Invalid date. Please use YYYY-MM-DD."


def register_member(connection, name, email):
    """Register a new MakerSpace member."""
    name = name.strip()
    email = email.strip()

    if not name:
        return False, "Error: Member name cannot be empty."

    if not name.replace(" ", "").isalpha():
        return False, (
            "Error: Member name must contain letters only. "
            "Please enter the member's registered name."
        )

    if not email:
        return False, "Error: Member email cannot be empty."

    if "@" not in email or "." not in email:
        return False, (
            "Error: Invalid email address. "
            "Please enter a valid email such as name@example.com."
        )

    add_member(connection, name, email)
    return True, "Member registered successfully."


def member_exists(connection, member_id):
    """Check whether a member exists in the database."""
    members = get_members(connection)

    for member in members:
        if member[0] == member_id:
            return True

    return False


def register_equipment(connection, name, category, serial_number):
    """Register new equipment."""
    if not name.strip():
        return False, "Equipment name cannot be empty."

    if not category.strip():
        return False, "Category cannot be empty."

    if not serial_number.strip():
        return False, "Serial number cannot be empty."

    try:
        add_equipment(
            connection,
            name.strip(),
            category.strip(),
            serial_number.strip()
        )
        return True, "Equipment registered successfully."

    except Exception:
        return False, "Serial number already exists."


def check_equipment_available(connection, equipment_id):
    """Check whether equipment exists and is available."""
    equipment = get_equipment(connection)

    equipment_record = next(
        (item for item in equipment if item[0] == equipment_id),
        None
    )

    if equipment_record is None:
        return False, "Equipment does not exist."

    if equipment_record[4] == 0:
        return False, "Equipment is currently unavailable."

    return True, "Equipment is available."


def equipment_exists(connection, equipment_id):
    """Check whether equipment exists in the database."""
    equipment = get_equipment(connection)

    for item in equipment:
        if item[0] == equipment_id:
            return True

    return False


def borrow_equipment(connection, member_id, equipment_id, loan_date):
    """Create a loan if the input and equipment are valid."""
    date_valid, message = validate_date(loan_date)

    if not date_valid:
        return False, message

    members = get_members(connection)
    equipment = get_equipment(connection)

    member_found = any(
        member[0] == member_id
        for member in members
    )

    equipment_record = next(
        (item for item in equipment if item[0] == equipment_id),
        None
    )

    if not member_found:
        return False, "Member does not exist."

    if equipment_record is None:
        return False, "Equipment does not exist."

    if equipment_record[4] == 0:
        return False, "Equipment is currently unavailable."

    create_loan(
        connection,
        member_id,
        equipment_id,
        loan_date
    )

    update_equipment_availability(
        connection,
        equipment_id,
        0
    )

    return True, "Equipment borrowed successfully."


def return_equipment(connection, loan_id, equipment_id, return_date):
    """Return equipment and close the associated loan."""
    date_valid, message = validate_date(return_date)

    if not date_valid:
        return False, message

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT equipment_id, loan_date
        FROM loans
        WHERE id = ? AND return_date IS NULL
        """,
        (loan_id,)
    )

    loan = cursor.fetchone()

    if not loan:
        return False, "Error: Active loan does not exist."

    loan_equipment_id = loan[0]
    loan_date = loan[1]

    if equipment_id != loan_equipment_id:
        return (
            False,
            f"Error: Equipment ID {equipment_id} "
            f"does not belong to loan ID {loan_id}."
        )

    if return_date < loan_date:
        return (
            False,
            "Error: Return date cannot be earlier "
            "than the loan date."
        )

    cursor.execute(
        """
        UPDATE loans
        SET return_date = ?
        WHERE id = ?
        """,
        (return_date, loan_id)
    )

    cursor.execute(
        """
        UPDATE equipment
        SET available = 1
        WHERE id = ?
        """,
        (equipment_id,)
    )

    connection.commit()

    return True, "Equipment returned successfully."


def loan_exists(connection, loan_id):
    """Check whether an active loan exists."""
    loans = get_active_loans(connection)

    for loan in loans:
        if loan[0] == loan_id:
            return True

    return False


def delete_loan(connection, loan_id):
    """Delete a loan and restore equipment availability if necessary."""
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT equipment_id, return_date
        FROM loans
        WHERE id = ?
        """,
        (loan_id,)
    )

    loan = cursor.fetchone()

    if not loan:
        return False, f"Loan ID {loan_id} does not exist."

    equipment_id = loan[0]
    return_date = loan[1]

    if return_date is None:
        cursor.execute(
            """
            UPDATE equipment
            SET available = 1
            WHERE id = ?
            """,
            (equipment_id,)
        )

    cursor.execute(
        """
        DELETE FROM loans
        WHERE id = ?
        """,
        (loan_id,)
    )

    connection.commit()

    return True, "Loan deleted successfully."


def delete_member(connection, member_id):
    """Delete a member if they have no loan history."""
    members = get_members(connection)

    member_record = next(
        (member for member in members if member[0] == member_id),
        None
    )

    if member_record is None:
        return (
            False,
            f"Member ID {member_id} does not exist."
        )

    loans = get_loans(connection)

    member_has_loans = any(
        loan[1] == member_id
        for loan in loans
    )

    if member_has_loans:
        return (
            False,
            f"Cannot delete Member ID {member_id}. "
            "The member has loan records."
        )

    db_delete_member(
        connection,
        member_id
    )

    return True, "Member deleted successfully."



def delete_equipment(connection, equipment_id):
    """Delete equipment if it is not currently borrowed."""
    equipment = get_equipment(connection)

    equipment_record = next(
        (item for item in equipment if item[0] == equipment_id),
        None
    )

    if equipment_record is None:
        return (
            False,
            f"Equipment ID {equipment_id} does not exist."
        )

    if equipment_record[4] == 0:
        return (
            False,
            f"Cannot delete Equipment ID {equipment_id}. "
            "The equipment is currently borrowed."
        )

    db_delete_equipment(
        connection,
        equipment_id
    )

    return True, "Equipment deleted successfully."


# Search functions


def search_members(connection, keyword):
    """Search members by ID, name, or email."""
    keyword = keyword.strip()

    if not keyword:
        return []

    cursor = connection.cursor()
    search_term = f"%{keyword}%"

    cursor.execute(
        """
        SELECT id, name, email
        FROM members
        WHERE CAST(id AS TEXT) LIKE ?
           OR name LIKE ?
           OR email LIKE ?
        ORDER BY id
        """,
        (search_term, search_term, search_term)
    )

    return cursor.fetchall()


def search_equipment(connection, keyword):
    """Search equipment by ID, name, category, or serial number."""
    keyword = keyword.strip()

    if not keyword:
        return []

    cursor = connection.cursor()
    search_term = f"%{keyword}%"

    cursor.execute(
        """
        SELECT id, name, category, serial_number, available
        FROM equipment
        WHERE CAST(id AS TEXT) LIKE ?
           OR name LIKE ?
           OR category LIKE ?
           OR serial_number LIKE ?
        ORDER BY id
        """,
        (
            search_term,
            search_term,
            search_term,
            search_term
        )
    )

    return cursor.fetchall()


def search_active_loans(connection, keyword):
    """Search active loans by loan, member, or equipment ID."""
    keyword = keyword.strip()

    if not keyword:
        return []

    cursor = connection.cursor()
    search_term = f"%{keyword}%"

    cursor.execute(
        """
        SELECT id, member_id, equipment_id, loan_date
        FROM loans
        WHERE return_date IS NULL
          AND (
              CAST(id AS TEXT) LIKE ?
              OR CAST(member_id AS TEXT) LIKE ?
              OR CAST(equipment_id AS TEXT) LIKE ?
          )
        ORDER BY id
        """,
        (
            search_term,
            search_term,
            search_term
        )
    )

    return cursor.fetchall()