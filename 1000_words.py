import requests
from xlwt import Workbook
from bs4 import BeautifulSoup

wb = Workbook()
common_words = wb.add_sheet('1000 common words')


def check_language(lang):
	language_page = requests.get('https://1000mostcommonwords.com/').text
	language_soup = BeautifulSoup(language_page, 'lxml')

	for i in language_soup.select('.entry-content p span a'):
		if lang.lower() == i.text.lower():
			return True
		else:
			continue
	return False


language = input("What language would you like to see? ")


if check_language(language):
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
else:
	print("language not found")

wb.save('1000_words.xls') 



