import methods
import requests
from bs4 import BeautifulSoup

flag = True
while flag:
    file_type = methods.check_correct_file_type()
    language = input("What language would you like to see (Press Q to quit)? ")

    # Checking if the user wants to quit
    if language == 'q' or language == 'Q':
        break

    if methods.check_language(language):

        # Incredibly annoying edge case that comes up when you scrape the data from the site
        if language == 'burmese':
            language = 'myanmar'

        link = 'https://1000mostcommonwords.com/1000-most-common-' + language.lower() + '-words/'
        page = requests.get(link).text
        soup = BeautifulSoup(page, 'lxml')
        if file_type == '0':
            methods.create_xls(language, soup)
        else:
            methods.create_csv(language, soup)
        flag = methods.check_another()
    else:
        print("I'm sorry the language you input has not been found.  Please try again.")

