import os
import re
import pandas as pd
from unidecode import unidecode

def normalize_word(word):
    # Normalize by removing diacritics and converting to lowercase
    word = unidecode(word).lower()
    return word

def count_unique_words_in_subfolder(subdir):
    unique_words = set()  # Set to store unique words
    text_files = 0        # Counter for text files (works)

    # Iterate over each file in the subfolder
    for file in os.listdir(subdir):
        if file.endswith('.txt'):
            text_files += 1
            file_path = os.path.join(subdir, file)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Extract words (use regex to split by non-word characters)
                words = re.findall(r'\w+', content)
                
                # Normalize and add words to the set
                for word in words:
                    normalized_word = normalize_word(word)
                    unique_words.add(normalized_word)
    
    return text_files, len(unique_words)

# Define the main folder path
main_folder = './poezii'

# List to store the data for the DataFrame
data = []

# Iterate over subfolders
for subdir, _, _ in os.walk(main_folder):
    if subdir != main_folder:  # Ignore the main folder itself
        subfolder_name = os.path.basename(subdir)
        works, unique_word_count = count_unique_words_in_subfolder(subdir)
        
        # Append the subfolder name, number of works, and unique words to the data list
        data.append([subfolder_name, works, unique_word_count])

# Create the DataFrame
df = pd.DataFrame(data, columns=['Name', 'Works', 'Words'])

# Write the DataFrame to a CSV file
csv_path = './output.csv'
df.to_csv(csv_path, index=False)

print(f"Data saved to {csv_path}")
