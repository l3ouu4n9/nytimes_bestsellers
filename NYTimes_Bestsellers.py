#!/usr/bin/env python3

import urllib
import requests
from bs4 import BeautifulSoup

"""
Author: Ting-Wei Wang
Date: March 7, 2020

Find books from The New York Times Fiction Best Sellers
in New Taipei City Library
"""

# Year can be modified
year = 2020

def getNYT_Best_Sellers(year):
	# Get book titles and authors from The New York Times Fiction Best Sellers in Wikipedia

	#https://en.wikipedia.org/wiki/The_New_York_Times_Fiction_Best_Sellers_of_2020

	url = 'https://en.wikipedia.org/wiki/The_New_York_Times_Fiction_Best_Sellers_of_' + str(year)
	r = requests.get(url)

	soup = BeautifulSoup(r.text, 'html.parser')
	#print(soup.prettify().encode('utf-8'))

	title_list = []
	author_list = []

	table = soup.find_all('table', class_='wikitable sortable')
	for t in table:
		for row in t.find_all('tr')[1:]:
			if row != None:

				author = ''
				td = row.find_all('td')
				if len(td) > 1:
					# Title
					if row.i.string in title_list:
						continue

					title_list.append(row.i.string)

					# Find author
					td = td[-1]
					if '<a' in str(td):
						a_tag = td.find_all('a')
						if len(a_tag) > 1:
							# Co-author exists
							for idx, s in enumerate(a_tag):
								if idx + 1 == len(a_tag):
									author += s.string
								else:
									author += s.string + ' and '
						else:
							# No Co-author
							author = a_tag[0].string
					else:
						author = td.string.replace('\n', '')
				if author != '':
					author_list.append(author)
	
	return title_list, author_list

def search_in_library(title_list, author_list):
	# Search books in New Taipei City Library

	# English book
	book_type = '%E8%A5%BF%E6%96%87%E6%9B%B8'
	# English
	book_language = '%E8%8B%B1%E6%96%87'


	for i in range(len(title_list)):
		title = title_list[i]
		author = author_list[i]

		book_params = {
			'm': 'as',
			'k0': title,
			't0': 't',
			'c0': 'and',
			'k1': author,
			't1': 'a',
			'c1': 'and',
			'dt0': urllib.request.unquote(book_type),
			'l0': 'eng',
			'lv0': urllib.request.unquote(book_language)
		}

		r = requests.get('https://webpac.tphcc.gov.tw/webpac/search.cfm', params = book_params)

		soup = BeautifulSoup(r.text, 'html.parser')
		#print(soup.prettify().encode('utf-8'))

		print(title)
		getResult = False
		book_tag = soup.find_all('div', class_='book-box')
		for b in book_tag:
			a_tag = b.find("a")
			if a_tag != None and title.lower() in a_tag.get('title').replace('/', '').lower():
				getResult = True
				print('\n\t!!!!! The Book Exists !!!!!')
				print('\t' + a_tag.get('title').replace('/', '') + '\n')
		if not getResult:
			print('\tNo Results Found')

if __name__ == '__main__':

	print('============START LOOKING FOR BOOKS FROM THE NEW YORK TIMES FICTION BEST SELLERS OF' + \
	' ' + str(year) + ' ' + 'IN NEW TAIPEI CITY LIBRARY============\n')
	print('*****Start fetching data from The New York Times Fiction Best Sellers ...')
	title_list, author_list = getNYT_Best_Sellers(year)

	# No information in that given year
	if not title_list:
		print('\n!!!!!Error!!!!!THERE IS NO INFORMATION FROM THE NEW YORK TIMES FICTION BEST SELLERS OF' + \
			' ' + str(year))
	else:
		print('*****Complete*****')

		print('*****Start looking for result in New Taipei City Library ...\n')
		search_in_library(title_list, author_list)
		print('\n*****All results are shown*****\n')
	print('============DONE FOR THE NEW YORK TIMES FICTION BEST SELLERS OF' + \
	' ' + str(year) + ' ' + 'IN NEW TAIPEI CITY LIBRARY============\n')

