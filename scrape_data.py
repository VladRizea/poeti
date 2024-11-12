import requests
from bs4 import BeautifulSoup
import re
import os
import csv


def count_files_in_folder(root_folder):
    file_count = 0
    # parcurge toate subfolderele și fișierele din folderul rădăcină
    for root, dirs, files in os.walk(root_folder):
        file_count += len(files)  # numără fișierele în directorul curent
    return file_count

def count_folders_in_folder(root_folder):
    folder_count = 0
    # parcurge toate subfolderele și fișierele din folderul rădăcină
    for root, dirs, files in os.walk(root_folder):
        folder_count += len(dirs)  # numără folderele în directorul curent
    return folder_count

def saveFileWrite(index1, index2):
    with open('./index_variables.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([index1, index2])


def saveFileRead():
    # Verificăm dacă fișierul există
    if not os.path.exists('./index_variables.csv'):
        # Dacă fișierul nu există, îl creăm cu valorile implicite 0 0
        with open('./index_variables.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([0, 0])  # Salvăm valorile implicite
        return [0, 0]

    # Citirea fișierului CSV
    with open('./index_variables.csv', 'r') as f:
        reader = csv.reader(f)
        row = list(reader)  # Citim toate rândurile

    # Dacă fișierul este gol, îl creăm cu valorile implicite
    if not row:
        with open('./index_variables.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([0, 0])  # Scrierea valorilor implicite
        return [0, 0]

    # Extragem și returnăm valorile citite
    loaded_index1, loaded_index2 = map(int, row[0])  # Prima linie cu valorile
    return [loaded_index1, loaded_index2]

def getContentFrom(URL):
    response = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'})
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def getAuthors(URL):
    soup = getContentFrom(URL)
    # Find all links in the lists
    links = soup.find('div', class_="col-main")


    links = links.find_all("a")
    poets = []
    poet_name = []

    #  Extract the link to the poets
    for link in links:
        href = link.get('href')
        text = link.get('title')
        if href and text:
            poets.append(href)
            poet_name.append(text)

    poets = poets[3:]
    poet_name = poet_name[3:]
    poets = [element for index, element in enumerate(poets) if index % 2 != 0]
    poet_name = [element for index, element in enumerate(poet_name) if index % 2 == 0]
    return [poets, poet_name]


def main():
    # Fetch the webpage content with headers
    url = 'https://poetii-nostri.ro/poeti/'
    url_straini = 'https://poetii-nostri.ro/poeti-straini/'

    poet_search = getAuthors(url)
    poet_search_straini = getAuthors(url_straini)

    poets = [item for item in poet_search[0] if item not in poet_search_straini[0]]
    poet_name = [item for item in poet_search[1] if item not in poet_search_straini[1]]
    poet_name = [item.rstrip() for item in poet_name]
    saveFile = saveFileRead()

    # Parse the content using BeautifulSoup
    for poetIndex in range(saveFile[0], len(poets)):
        folder_path = './poezii/' + poet_name[poetIndex]
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        url = 'https://poetii-nostri.ro' 
        soup = getContentFrom(url + poets[poetIndex])
        links = soup.find('div', class_="category-products")

        links = links.find_all('a')

        poetry = []
        for link in links:
            href = link.get('href')
            poetry.append(href)

        poetry = [item for item in poetry if "poezie-id" in item]
        #Start from the index we last started
        if(saveFile[1] != 0):
            start = saveFile[1]
            saveFile[1] = 0
        else:
            start =0
        for poemindex in range(start, len(poetry)):
            soup = getContentFrom(url + poetry[poemindex])
            content = soup.find('div', class_="col-main")
            invalid_chars = r'[\/:*?\"<>|]'
            poem_title = content.find('h1').get_text().split(' - ')[0]
            poem_title = re.sub(invalid_chars, '', poem_title).replace("'", "")
            poem_title = poem_title.strip()
            poem_content = content.find('p').get_text()

            file_path = os.path.join(folder_path, poem_title + '.txt')
            saveFileWrite(poetIndex,poemindex)
            print(poem_title + "  #  " + poet_name[poetIndex])
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(poem_content)
                file.close()
    folder_path = './poezii'  # Înlocuiește cu calea ta
    print(f"Numărul total de poeți: {count_folders_in_folder(folder_path)}")
    print(f"Numărul total de poezii: {count_files_in_folder(folder_path)}")



if __name__=="__main__":
    main()