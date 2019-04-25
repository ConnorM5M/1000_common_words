import requests
import xlwt
from xlwt import Workbook
from bs4 import BeautifulSoup

wb = Workbook()
sheet1 = wb.add_sheet('Sheet 1') 



def check_language(language):
	language_page = requests.get('https://1000mostcommonwords.com/').text
	language_soup = BeautifulSoup(language_page, 'lxml')

	languages = []

	for i in language_soup.select('.entry-content p span a'):
		if language.lower() == i.text.lower():
			return True
		else:
			continue
	return False


language = input("What language would you like to see?")
if (check_language(language)):
	link = 'https://1000mostcommonwords.com/1000-most-common-' + language.lower() + '-words/'
	#'https://1000mostcommonwords.com/1000-most-common-german-words/'
	page = requests.get(link).text
	soup = BeautifulSoup(page, 'lxml')

	words = []
	count = 0

	for title in soup.select('.entry-content table tbody tr'):
		print(type(title.text.splitlines()[1]))
		sheet1.write(count, 0, title.text.splitlines()[3] + ",")
		sheet1.write(count, 1, title.text.splitlines()[2])
		count += 1
		words.append(title.text)

	#for i in range(len(words)):
	#	print(words[i])
else:
	print("language not found")

wb.save('1000_words.xls') 



