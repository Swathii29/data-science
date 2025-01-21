import json
import os

# Function to tokenize the paragraph and save it to a JSON file
def tokenize_paragraph(paragraph, json_filename="words.json"):
    # Tokenize the paragraph by splitting on spaces and removing punctuation
    words = [word.strip(".,!?()[]{};:") for word in paragraph.split()]
    
    # Check if the JSON file already exists, then load the current data
    if os.path.exists(json_filename):
        with open(json_filename, "r") as file:
            existing_words = json.load(file)
    else:
        existing_words = []

    # Add the words from the paragraph to the existing list
    existing_words.extend(words)

    # Remove duplicates by converting to a set and back to a list
    unique_words = list(set(existing_words))

    # Write the updated list back to the JSON file
    with open(json_filename, "w") as file:
        json.dump(unique_words, file, indent=4)

    print(f"Words have been tokenized and saved to {json_filename}.")

# Function to check if a word exists in the JSON file and add it if not
def check_and_store_word(word, json_filename="words.json"):
    # Load existing words from the JSON file if it exists
    if os.path.exists(json_filename):
        with open(json_filename, "r") as file:
            words = json.load(file)
    else:
        words = []

    # Check if the word exists in the list
    if word in words:
        print(f"'{word}' is present in the list.")
    else:
        words.append(word)
        with open(json_filename, "w") as file:
            json.dump(words, file, indent=4)
        print(f"'{word}' has been added to the list.")

# Example of how the program works
if __name__ == "__main__":
    # Step 1: Tokenizing a sample paragraph
    paragraph = "Hello! How are you doing today? I hope you're doing well."
    tokenize_paragraph(paragraph)

    # Step 2: Checking if a user-provided word exists
    user_word = input("Enter a word to check: ").strip()
    check_and_store_word(user_word)