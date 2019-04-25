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
            print("You have input an incorrect string please try again")
            continue

'''
This will scrape the 1000 most common words of the language input.  If the language is valid it will write the values to 
an excel document.  If not it will return that the language was not found and ask for another input.
Document will be formatted as described below:
    English                                     Inputted Language
    English word (followed by a comma)      Inputted Language word
    ...                                             ...

'''


flag = True
while flag:
    language = input("What language would you like to see? (Press Q to quit) ")

    if language == 'q' or language == 'Q':
        break

    if check_language(language):
        if language == 'burmese':
            language = 'myanmar'
        wb = Workbook()
        common_words = wb.add_sheet(str(language))

        link = 'https://1000mostcommonwords.com/1000-most-common-' + language.lower() + '-words/'
        page = requests.get(link).text
        soup = BeautifulSoup(page, 'lxml')
        count = 0
        for title in soup.select('.entry-content table tbody tr'):
            if count == 0:
                common_words.write(count, 0, title.text.splitlines()[2])
                common_words.write(count, 1, 'English')
            else:
                common_words.write(count, 0, title.text.splitlines()[2] + ',')
                common_words.write(count, 1, title.text.splitlines()[3])
            count += 1
        wb.save('1000_words_' + language.lower() + '.xls')
        flag = check_another()
    else:
        print("I'm sorry the language you input has not been found.  Please try again.")

