# -*- coding: utf-8 -*-
import requests
import time
import csv
from bs4 import BeautifulSoup

url = "https://www.rokomari.com/book/category/2407/book-fair-2020-?page=1"
try:
    response = requests.get(url)
    if response.status_code == 200:
        soup_requests = BeautifulSoup(response.content, 'lxml')
        pagination_get = soup_requests.find("div", {"class": "pagination"})
        total_page_get = pagination_get.find_all("a")
        total_page = int(total_page_get[len(total_page_get) - 2].text)
        book_data_set=[]
        serial_no = 1
        for page_counter in range(1, total_page + 1):
            get_book_fair_books_url = f"https://www.rokomari.com/book/category/2407/book-fair-2020-?page={page_counter}"
            requests_for_books = requests.get(get_book_fair_books_url,verify = False)
            if requests_for_books.status_code == 200:
                print(f"Scrapping {get_book_fair_books_url} This Url")
                soup_requests_for_books = BeautifulSoup(requests_for_books.content, "lxml")
                book_list_get = soup_requests_for_books.find_all("div", {"class": "book-text-area"})
               
                for book_data in book_list_get:
                    book_title = book_data.find("p", {"class": "book-title"}).text
                    book_author = book_data.find("p", {"class": "book-author"}).text
                    book_price_tag = book_data.find("p", {"class": "book-price"})
                    book_original_price = book_data.find("strike", {"class": "original-price"}).text if book_data.find("strike", {"class": "original-price"}) else book_price_tag.find("span").text
                    book_new_price = book_price_tag.find("span").text

                    book_data_set.append([
                       serial_no,book_title,book_author,book_original_price,book_new_price
                    ])
                    serial_no += 1

                    # book_data_set.append({
                    #     'book_title':book_title,
                    #     'book_author':book_author,
                    #     'book_original_price':book_original_price,
                    #     'book_new_price':book_new_price
                    # })
                    # print(f"Book Title {book_title}")
                    # print(f"Book Author {book_author}")
                    # print(f" Book Price Tag {book_price_tag}")
                    # print(f"Book Original Price {book_original_price}")
                    # print(f"Book New Price {book_new_price}")
                    # print("---")
            else:
                print("Internal Server Error")
        time.sleep(3)

    else:
        print("Internal Server Error")
except Exception as e:
    print(e)
with open("rokomari_2020_book_fair.csv",'w',newline='') as csvfile:
    fieldnames=['SlNo','BookTitle','BookAuthor','BookOriginalPrice','BookNewPrice']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC, delimiter=';')
    writer.writerows(book_data_set)
    #sl_no = 1
    # for data_set in book_data_set:
    #     #writer.writerow([sl_no,data_set['book_title'].strip(),data_set['book_author'].strip(),data_set['book_original_price'].strip(),data_set['book_new_price'].strip()])
    #     writer.writerow({
    #         'SlNo': sl_no, 
    #         'BookName': data_set['book_title'].strip(),
    #         'BookAuthor': data_set['book_author'].strip(),
    #         'BookOriginalPrice': data_set['book_original_price'].strip(),
    #         'BookNewPrice': data_set['book_new_price'].strip(),
    #         })
    #     sl_no+=1