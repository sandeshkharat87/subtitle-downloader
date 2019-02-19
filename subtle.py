#!/usr/bin/python3.6
import requests
from bs4 import BeautifulSoup
import os
import sys


subtle_link = {}   # Dict. for holding movie names


print("\n")

#              Take movie name

moviename = input("\nEnter movie name : ")

if moviename == '':
    print("You didnot enter anything!!!!\n")
    sys.exit()
# moviename = 'spider man'

#               URLS
mainURL = "https://opensubtitles.co"
searchurl = "https://opensubtitles.co/search?q=" + moviename.replace(" ", "+")

print("\n\nSearching movies.... \n\n")  # + searchurl + "\n")

# Request to webpage

r = requests.get(searchurl).text

soup = BeautifulSoup(r, 'html5lib')


#               finding links and names


scratch_link = soup.find_all("a", class_="list-group-item")


name_Count = 0

for moviename in scratch_link[:-5]:
    name_Count += 1
    print(f"{str(name_Count)})  {moviename['href'].split('/')[-1]}")
    subtle_link[name_Count] = moviename['href']  # adding values to "subtle_link" Dictionary


if len(subtle_link) == 0:
    print(" Zero search Resultss :( !!!\n")
    sys.exit()
print()


try:
    Uesrs_Choice = int(input("Enter your choice : "))
    if Uesrs_Choice > len(subtle_link):
        print(" \n INVALID CHOICE \n")
        sys.exit()

    MV_name = subtle_link[Uesrs_Choice].split('/')[-1]  # actual movie name

# except ValueError:
#     print("\nInvalid choice\n")
#     sys.exit

    r2 = requests.get(subtle_link[Uesrs_Choice]).text

    sub2 = BeautifulSoup(r2, 'html5lib')

    links = sub2.find('ul', class_="list-group").a['href']

    # print(links)

    r3 = requests.get(links).text

    sub3 = BeautifulSoup(r3, 'html5lib')

    half_Link = sub3.find('a', class_="btn btn-danger")['href']

    # print("\n ", half_Link)

    full_Link = mainURL + half_Link

    # print(full_Link)

    generateDown = requests.get(full_Link)

    with open(f"{MV_name}.srt", 'wb') as file:
        file.write(generateDown.content)
        print("\n" + MV_name + " succesfully downloaded in > " + os.getcwd() + "  \n")

except ValueError:
    print("\nInvalid choice\n")
