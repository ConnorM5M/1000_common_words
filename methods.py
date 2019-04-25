import requests
from xlwt import Workbook
from bs4 import BeautifulSoup


'''
This function checks whether the language input is in the list of possible languages scraped from the website.
@param - lang (The language the user would like to return the 1000 most common words from)
@return - boolean
'''


def check_language(lang):
    language_page = requests.get('https://1000mostcommonwords.com/').text
    language_soup = BeautifulSoup(language_page, 'lxml')
    if lang == 'myanmar' or lang == 'burmese':
        lang = 'myanmar(burmese)'
    for i in language_soup.select('.entry-content p'):
        if lang.lower() in i.text.replace(" ", "").lower().splitlines():
            return True
        else:
            continue
    return False

'''
This function checks whether the user would like to compile another excel document with another language.
@param - None
@return - boolean
'''


def check_another():
    valid = True
    while valid:
        next_language = input("Would you like to try another language? (Y/N) ")
        if next_language == 'N' or next_language == 'n':
            return False
        elif next_language == 'Y' or next_language == 'y':
            return True
        else:
            print("You have input an incorrect string.  Please try again.")
            continue


def check_correct_file_type():
    valid = True
    while valid:
        f = input("What file type would you like this saved as (0 for excel / 1 for csv)? ")
        if f == '0':
            return f
        elif f == '1':
            return f
        else:
            print("You have input an incorrect file type.  Please try again.")
            continue

'''
This will scrape the 1000 most common words of the language input.  If the language is valid it will write the values to 
an excel document.  If not it will return that the language was not found and ask for another input.
Document will be formatted as described below:
    English                                     Inputted Language
    English word (followed by a comma)      Inputted Language word
    ...                                             ...
'''


def create_xls(lang, tmp_soup):
    wb = Workbook()
    common_words = wb.add_sheet(str(lang))

    count = 0
    for title in tmp_soup.select('.entry-content table tbody tr'):
        if count == 0:
            common_words.write(count, 0, title.text.splitlines()[2])
            common_words.write(count, 1, 'English')
        else:
            common_words.write(count, 0, title.text.splitlines()[2] + ',')
            common_words.write(count, 1, title.text.splitlines()[3])
        count += 1
    wb.save('1000_words_' + lang.lower() + '.xls')


def create_csv(lang, tmp_soup):
    file = open('1000_words_' + str(lang) + '.txt', 'w')
    count = 0
    for title in tmp_soup.select('.entry-content table tbody tr'):
        if count == 0:
            file.write(title.text.splitlines()[2] + ', ' + 'English' + '\n')
        else:
            file.write(title.text.splitlines()[2] + ', ' + title.text.splitlines()[3] + '\n')
        count += 1
    file.close()