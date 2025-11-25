from cryptography.fernet import Fernet
import os
import getpass
import csv
from io import StringIO

# --- Σταθερές Αρχείων ---
KEY_FILE = "secret.key"
CREDENTIALS_FILE = "credentials.dat"

# --- Βήμα 2: Δημιουργία & Διαχείριση Κλειδιού ---
def load_or_generate_key():
    """
    Φορτώνει το κλειδί από το secret.key. Αν δεν υπάρχει, το δημιουργεί και το αποθηκεύει.
    """
    if os.path.exists(KEY_FILE):
        # 1. Φόρτωση του υπάρχοντος κλειδιού
        try:
            with open(KEY_FILE, "rb") as key_file:
                key = key_file.read()
            if not key:
                raise ValueError("Το αρχείο κλειδιού είναι κενό.")
        except Exception as e:
            print(f"❌ Σφάλμα φόρτωσης κλειδιού: {e}. Δημιουργείται νέο.")
            key = Fernet.generate_key()
            with open(KEY_FILE, "wb") as key_file:
                key_file.write(key)
            print(f"Δημιουργήθηκε και αποθηκεύτηκε νέο κλειδί στο {KEY_FILE}")
    else:
        # 2. Δημιουργία νέου κλειδιού
        key = Fernet.generate_key()
        # 3. Αποθήκευση του νέου κλειδιού
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        print(f"Δημιουργήθηκε νέο κλειδί και αποθηκεύτηκε στο {KEY_FILE}")
    
    return key

# Φόρτωση του κλειδιού και δημιουργία του Fernet αντικειμένου
encryption_key = load_or_generate_key()
fernet_cipher = Fernet(encryption_key)

print("Το κλειδί κρυπτογράφησης φορτώθηκε με επιτυχία.")

# --- Βήμα 3: Αποθήκευση Credentials ---
def save_credentials(service, username, password):
    """
    Κρυπτογραφεί τον κωδικό και αποθηκεύει την καταχώρηση στο credentials.dat.
    """
    try:
        # Κωδικοποίηση string σε bytes, κρυπτογράφηση, και μετατροπή bytes σε string (base64)
        encrypted_password = fernet_cipher.encrypt(password.encode()).decode()
        
        # Χρησιμοποιούμε CSV writer για να χειριστούμε σωστά κόμματα μέσα στα δεδομένα
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow([service, username, encrypted_password])
        record = output.getvalue()
        
        # Αποθήκευση στο αρχείο (προσθήκη στο τέλος)
        with open(CREDENTIALS_FILE, "a", newline='') as f:
            f.write(record)
            
        print(f"\n✅ Αποθηκεύτηκε: {service}")
        
    except Exception as e:
        print(f"❌ Σφάλμα κατά την αποθήκευση: {e}")

# --- Βήμα 4: Αναζήτηση & Αποκρυπτογράφηση ---
def find_credentials(service_name):
    """
    Αναζητά την υπηρεσία και αποκρυπτογραφεί τον κωδικό.
    """
    try:
        with open(CREDENTIALS_FILE, "r", newline='') as f:
            reader = csv.reader(f)
            
            for row in reader:
                if len(row) == 3:
                    service, username, encrypted_password = row
                    
                    if service.lower() == service_name.lower():
                        # Αποκρυπτογράφηση
                        # Το encrypted_password είναι string, το κάνουμε bytes (base64)
                        decrypted_password_bytes = fernet_cipher.decrypt(encrypted_password.encode())
                        
                        # Μετατροπή των bytes σε string για εμφάνιση
                        decrypted_password = decrypted_password_bytes.decode()
                        
                        return username, decrypted_password
        
        return None, "Δεν βρέθηκε ο λογαριασμός."

    except FileNotFoundError:
        return None, "Το αρχείο δεδομένων δεν υπάρχει ακόμα."
    except Exception as e:
        # Αυτό μπορεί να είναι σφάλμα αποκρυπτογράφησης αν το κλειδί είναι λάθος
        return None, f"❌ Σφάλμα κατά την ανάγνωση/αποκρυπτογράφηση: {e}"

# --- Βήμα 5: Κύριο Μενού Εφαρμογής ---
def main():
    print("\n*** 🔐 Password Manager (Fernet) ***")
    
    while True:
        print("\n--- Επιλογές ---")
        print("1: Αποθήκευση νέου λογαριασμού")
        print("2: Αναζήτηση λογαριασμού")
        print("3: Έξοδος")
        
        choice = input("Επιλέξτε ενέργεια (1/2/3): ")
        
        if choice == '1':
            service = input("Όνομα Υπηρεσίας (π.χ. Netflix): ")
            username = input("Όνομα Χρήστη / Email: ")
            # Χρήση getpass για ασφαλή εισαγωγή κωδικού (δεν φαίνεται στον χρήστη)
            password = getpass.getpass("Κωδικός Πρόσβασης: ")
            save_credentials(service, username, password)
            
        elif choice == '2':
            service = input("Ποια υπηρεσία ψάχνετε: ")
            username, password = find_credentials(service)
            if username:
                print(f"\n🔑 Βρέθηκε!")
                print(f"   Υπηρεσία: {service}")
                print(f"   Όνομα Χρήστη: {username}")
                # Προσοχή: Εμφάνιση ευαίσθητων δεδομένων
                print(f"   Κωδικός: {password}")
            else:
                print(f"\n{password}")
                
        elif choice == '3':
            print("Ευχαριστούμε που χρησιμοποιήσατε τον Password Manager. Αντίο!")
            break
        else:
            print("Μη έγκυρη επιλογή. Παρακαλώ δοκιμάστε ξανά.")

if __name__ == "__main__":
    main()