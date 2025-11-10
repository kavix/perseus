#!/usr/bin/env python3
"""
MEDUSA CTF - Database User Management
This script helps you add, update, or view users in the medusa.db database
"""

import sqlite3
import sys
import os

DB_PATH = "../assets/medusa.db"


def get_db_connection():
    """Get database connection"""
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, DB_PATH)
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at: {db_path}")
        print(f"   Please make sure you're running this from the tools/ directory")
        sys.exit(1)
    
    return sqlite3.connect(db_path)


def list_users():
    """List all users in the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, password FROM credentials ORDER BY id")
    users = cursor.fetchall()
    
    print("\n" + "=" * 60)
    print("Current Users in Database")
    print("=" * 60)
    
    if users:
        print(f"{'ID':<5} {'Username':<20} {'Password':<30}")
        print("-" * 60)
        for user_id, username, password in users:
            print(f"{user_id:<5} {username:<20} {password:<30}")
    else:
        print("No users found in database")
    
    print("=" * 60 + "\n")
    conn.close()


def add_user(username, password):
    """Add a new user to the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO credentials (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        print(f"✓ User '{username}' added successfully!")
        return True
    except sqlite3.IntegrityError:
        print(f"❌ Error: Username '{username}' already exists!")
        return False
    except Exception as e:
        print(f"❌ Error adding user: {e}")
        return False
    finally:
        conn.close()


def update_user(username, new_password):
    """Update user's password"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "UPDATE credentials SET password = ? WHERE username = ?",
            (new_password, username)
        )
        
        if cursor.rowcount > 0:
            conn.commit()
            print(f"✓ Password for '{username}' updated successfully!")
            return True
        else:
            print(f"❌ User '{username}' not found!")
            return False
    except Exception as e:
        print(f"❌ Error updating user: {e}")
        return False
    finally:
        conn.close()


def delete_user(username):
    """Delete a user from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM credentials WHERE username = ?", (username,))
        
        if cursor.rowcount > 0:
            conn.commit()
            print(f"✓ User '{username}' deleted successfully!")
            return True
        else:
            print(f"❌ User '{username}' not found!")
            return False
    except Exception as e:
        print(f"❌ Error deleting user: {e}")
        return False
    finally:
        conn.close()


def clear_all_users():
    """Clear all users (use with caution!)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    confirm = input("⚠️  Are you sure you want to delete ALL users? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Cancelled.")
        conn.close()
        return
    
    try:
        cursor.execute("DELETE FROM credentials")
        conn.commit()
        print(f"✓ All users deleted. {cursor.rowcount} user(s) removed.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()


def interactive_menu():
    """Interactive menu for database management"""
    while True:
        print("\n" + "=" * 60)
        print("MEDUSA CTF - Database User Management")
        print("=" * 60)
        print("1. List all users")
        print("2. Add new user")
        print("3. Update user password")
        print("4. Delete user")
        print("5. Clear all users")
        print("6. Exit")
        print("=" * 60)
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            list_users()
        
        elif choice == '2':
            print("\n--- Add New User ---")
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            
            if username and password:
                if add_user(username, password):
                    print("\n💡 Don't forget to update the encrypted flag in database_helper.dart")
                    print("   Run: python3 generate_encrypted_flag.py")
            else:
                print("❌ Username and password cannot be empty!")
        
        elif choice == '3':
            print("\n--- Update User Password ---")
            username = input("Username: ").strip()
            new_password = input("New Password: ").strip()
            
            if username and new_password:
                if update_user(username, new_password):
                    print("\n💡 Don't forget to update the encrypted flag in database_helper.dart")
                    print("   Run: python3 generate_encrypted_flag.py")
            else:
                print("❌ Username and password cannot be empty!")
        
        elif choice == '4':
            print("\n--- Delete User ---")
            username = input("Username: ").strip()
            
            if username:
                delete_user(username)
            else:
                print("❌ Username cannot be empty!")
        
        elif choice == '5':
            clear_all_users()
        
        elif choice == '6':
            print("\nGoodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-6.")


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # Command-line mode
        command = sys.argv[1].lower()
        
        if command == 'list':
            list_users()
        
        elif command == 'add' and len(sys.argv) >= 4:
            username = sys.argv[2]
            password = sys.argv[3]
            add_user(username, password)
        
        elif command == 'update' and len(sys.argv) >= 4:
            username = sys.argv[2]
            new_password = sys.argv[3]
            update_user(username, new_password)
        
        elif command == 'delete' and len(sys.argv) >= 3:
            username = sys.argv[2]
            delete_user(username)
        
        else:
            print("Usage:")
            print("  Interactive mode:  python3 manage_database.py")
            print("  List users:        python3 manage_database.py list")
            print("  Add user:          python3 manage_database.py add <username> <password>")
            print("  Update password:   python3 manage_database.py update <username> <new_password>")
            print("  Delete user:       python3 manage_database.py delete <username>")
    else:
        # Interactive mode
        interactive_menu()


if __name__ == "__main__":
    main()
