import vobject
import random
import io
from PIL import Image
import base64
import argparse
import matplotlib.pyplot as plt

def load_contacts(vcf_file):
    """Loads contacts from a VCF file."""
    contacts = []
    try:
        with open(vcf_file, 'r', encoding='utf-8') as f:
            vcf_data = f.read()
            for vcard in vobject.readComponents(vcf_data):
                contacts.append(vcard)
    except FileNotFoundError:
        print(f"Error: VCF file '{vcf_file}' not found.")
        return []
    except Exception as e:
        print(f"Error reading VCF file: {e}")
        return []
    return contacts

def extract_photo(contact):
    """Extracts and decodes the photo from a contact."""
    if hasattr(contact, 'photo'):
        #photo_data = contact.photo.value.decode('utf-8')
        photo_data = contact.photo.value
        photo_type = contact.photo.type_param
        if photo_type == 'JPEG':
            try:
                #img_data = base64.b64decode(photo_data)
                img = Image.open(io.BytesIO(photo_data))
                return img
            except Exception as e:
                print(f"Error processing photo: {e}")
                return None
        elif photo_type == 'PNG':
            try:
                img_data = base64.b64decode(photo_data)
                img = Image.open(io.BytesIO(img_data))
                return img
            except Exception as e:
                print(f"Error processing photo: {e}")
                return None
        else:
            print(f"Unsupported photo type: {photo_type}")
            return None
    else:
        return None

def get_name(contact):
    """Extracts the full name from a contact."""
    if hasattr(contact, 'fn'):
        return contact.fn.value
    else:
        return None

def get_first_name(contact):
    """Extracts only the first name from a contact."""
    full_name = get_name(contact)
    if full_name:
        return full_name.split()[0]  # Split by spaces and take the first part
    return None
    
def get_title(contact):
    """Extracts the title from a contact."""
    if hasattr(contact, 'title'):
        return contact.title.value
    else:
        return None

def display_image(image):
    """Displays an image using matplotlib."""
    if image:
        if plt.fignum_exists(1): #check if a figure exists.
            plt.clf() #clear it if it does.
        plt.imshow(image)
        plt.axis('off')  # Turn off axis labels and ticks
        plt.show(block=False) #show without blocking.
        plt.pause(0.001) #allow plot to be shown
    else:
        print("This contact has no photo.")
        
def play_name_game(contacts, max_count=None):

    incorrect_contacts = []
    score = 0
    if max_count:
        contacts = random.sample(contacts, min(max_count, len(contacts)))
    for contact in contacts:
        photo = extract_photo(contact)
        name = get_name(contact)

        if photo and name:
            display_image(photo)
            guess = input("Qui est-ce?")
            if guess.lower() == name.lower():
                print("Correct!")
                score += 1
            else:
                print(f"Faux, tu bois! C'était {name}.")
                incorrect_contacts.append(contact)
        else:
            print("Ce contact n'a pas de photo ou de nom.")
    print(f"\nTour terminé ! Ton score : {score}/{len(contacts)}")
    return incorrect_contacts

def play_title_game(contacts, max_count=None):

    incorrect_contacts = []
    score = 0
    if max_count:
        contacts = random.sample(contacts, min(max_count, len(contacts)))
    for contact in contacts:
        photo = extract_photo(contact)
        title = get_title(contact)

        if photo and title:
            display_image(photo)
            guess = input("Quel est le poste de cette personne ? ")
            if guess.lower() == title.lower():
                print("Correct !")
                score += 1
            else:
                print(f"Faux, tu bois! C'était {title}.")
                incorrect_contacts.append(contact)
        else:
            print("Ce contact n'a pas de photo ou de poste.")
    print(f"\nTour terminé ! Ton score : {score}/{len(contacts)}")
    return incorrect_contacts

def play_first_name_game(contacts, max_count=None):
    """Joue au jeu de deviner le prénom, renvoyant les réponses incorrectes."""
    incorrect_contacts = []
    score = 0
    if max_count:
        contacts = random.sample(contacts, min(max_count, len(contacts)))
    for contact in contacts:
        photo = extract_photo(contact)
        first_name = get_first_name(contact)

        if photo and first_name:
            display_image(photo)
            guess = input("Quel est le prénom de cette personne ? ")
            if guess.lower() == first_name.lower():
                print("Correct!")
                score += 1
            else:
                print(f"Faux, tu bois! C'était {first_name}.")
                incorrect_contacts.append(contact)
        else:
            print("Ce contact n'a pas de photo ou de prénom.")
    print(f"\nTour terminé ! Ton score : {score}/{len(contacts)}")
    return incorrect_contacts

def main():
    """Fonction principale pour exécuter le jeu."""
    parser = argparse.ArgumentParser(description="Jeu de deviner les contacts à partir d'un fichier VCF.")
    parser.add_argument("--vcf-file", required=True, help="Chemin vers le fichier VCF.")
    parser.add_argument("--max-count", type=int, help="Nombre maximal de contacts à tester.")
    args = parser.parse_args()

    contacts = load_contacts(args.vcf_file)

    if not contacts:
        return

    print("\n Choisis un mode de jeu :")
    print("1. Prénom")
    print("2. Poste")
    print("3. Nom complet")
    print("NOTE: les réponses ne sont pas sensibles à la casse, e.g. marie ou Marie, ça change rien.")

    choice = input("Ton choix : ")
    incorrect = contacts;

    while True:
        if choice == "1":
            incorrect = play_first_name_game(incorrect, args.max_count)
        elif choice == "2":
            incorrect = play_title_game(incorrect, args.max_count)
        elif choice == "3":
            incorrect = play_name_game(incorrect, args.max_count)
        else:
            print("Y a pas le mode {choice}, désolé chef.fe")
        
        if not incorrect:
            print("BIM! Tout juste!")
            break

if __name__ == "__main__":
    main()
