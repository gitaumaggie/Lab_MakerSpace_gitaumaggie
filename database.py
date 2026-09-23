import sqlite3


def create_connection():
    """Create and return a connection to the SQLite database."""
    connection = sqlite3.connect("makerspace.db")
    return connection

def create_tables(connection):
    """Create all MakerSpace database tables."""

    connection.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            serial_number TEXT UNIQUE NOT NULL,
            available INTEGER NOT NULL DEFAULT 1
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY,
            member_id INTEGER NOT NULL,
            equipment_id INTEGER NOT NULL,
            loan_date TEXT NOT NULL,
            return_date TEXT,
            FOREIGN KEY (member_id) REFERENCES members(id),
            FOREIGN KEY (equipment_id) REFERENCES equipment(id)
        )
    """)

    connection.commit()



def add_member(connection, name, email):
    """Add a new member to the database"""
    sql = """
        INSERT INTO members (name, email)
        VALUES (?, ?)
    """
    connection.execute(sql, (name, email))
    connection.commit()


def get_members(connection):
    """Return all members from the database."""
    cursor = connection.execute(
        "SELECT id, name, email FROM members"
    )
    return cursor.fetchall()


def update_member_email(connection, member_id, new_email):
    """Update a member's email address."""
    sql = """
        UPDATE members
        SET email = ?
        WHERE id = ?
    """
    connection.execute(sql, (new_email, member_id))
    connection.commit()


def delete_member(connection, member_id):
    """Delete a member from the database."""
    sql = "DELETE FROM members WHERE id = ?"
    connection.execute(sql, (member_id,))
    connection.commit()


def add_equipment(connection, name, category, serial_number):
    """Add new equipment to the database."""
    sql = """
        INSERT INTO equipment (name, category, serial_number)
        VALUES (?, ?, ?)
    """
    connection.execute(sql, (name, category, serial_number))
    connection.commit()


def get_equipment(connection):
    """Return all equipment from the database."""
    cursor = connection.execute(
        """
        SELECT id, name, category, serial_number, available
        FROM equipment
        """
    )
    return cursor.fetchall()


def update_equipment(connection, equipment_id, name, category):
    """Update equipment details."""
    sql = """
        UPDATE equipment
        SET name = ?, category = ?
        WHERE id = ?
    """
    connection.execute(sql, (name, category, equipment_id))
    connection.commit()


def delete_equipment(connection, equipment_id):
    """Delete equipment from the database."""
    sql = "DELETE FROM equipment WHERE id = ?"
    connection.execute(sql, (equipment_id,))
    connection.commit()


def update_equipment_availability(connection, equipment_id, available):
    """Update whether equipment is available."""
    sql = """
        UPDATE equipment
        SET available = ?
        WHERE id = ?
    """
    connection.execute(sql, (available, equipment_id))
    connection.commit()


def create_loan(connection, member_id, equipment_id, loan_date):
    """Create a new equipment loan."""
    sql = """
        INSERT INTO loans (member_id, equipment_id, loan_date)
        VALUES (?, ?, ?)
    """
    connection.execute(sql, (member_id, equipment_id, loan_date))
    connection.commit()


def get_loans(connection):
    """Return all loans from the database."""
    cursor = connection.execute(
        """
        SELECT id, member_id, equipment_id, loan_date, return_date
        FROM loans
        """
    )
    return cursor.fetchall()


def return_loan(connection, loan_id, return_date):
    """Record the return date for a loan."""
    sql = """
        UPDATE loans
        SET return_date = ?
        WHERE id = ?
    """
    connection.execute(sql, (return_date, loan_id))
    connection.commit()


def get_active_loans(connection):
    """Return all currently active loans."""
    cursor = connection.execute(
        """
        SELECT id, member_id, equipment_id, loan_date
        FROM loans
        WHERE return_date IS NULL
        """
    )
    return cursor.fetchall()


if __name__ == "__main__":
    connection = create_connection()
    create_tables(connection)
    print("Database and tables created successfully!")
    connection.close()