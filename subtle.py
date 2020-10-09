#!/usr/bin/python3.6
import requests
from bs4 import BeautifulSoup
import os
import sys

from concurrent import futures

subtle_link = {}   # Dict. for holding movie names
all_names = []
all_links = []


moviename_main = input("\n\t\tEnter moviename ??? ")

moviename_main.strip()

mainURL = "https://opensubtitles.co"
searchurl = "https://opensubtitles.co/search?q=" + \
    moviename_main.replace(" ", "+")

r = requests.get(searchurl).text
soup = BeautifulSoup(r, 'html5lib')
scratch_link = soup.find_all("a", class_="list-group-item")

name_Count = 0
print()
for moviename in scratch_link[:-5]:
    name_Count += 1
    # print(moviename)

    imdb = moviename.find(
        'div', attrs={'class': 'col-xs-2 col-md-2 text-center'}).text.replace(" ", "").replace("\n", " ")

    print(
        f"\t\t[ {str(name_Count)} ]  {imdb}  {moviename['href'].split('/')[-1]}")

    # adding values to "subtle_link" Dictionary
    subtle_link[name_Count] = moviename['href']

if len(subtle_link) != 0:
    Uesrs_Choice = int(input("\nEnter your choice : "))
    if Uesrs_Choice <= len(subtle_link):
        MV_name = subtle_link[Uesrs_Choice].split('/')[-1]
        r2 = requests.get(subtle_link[Uesrs_Choice]).text
        sub2 = BeautifulSoup(r2, 'html5lib')
    else:
        print("Wrong choice....")
        sys.exit()
else:
    print("No movies found....")
    sys.exit()


def singleDownload():
    links = sub2.find('ul', class_="list-group").a['href']
    r3 = requests.get(links).text
    sub3 = BeautifulSoup(r3, 'html5lib')
    half_Link = sub3.find('a', class_="btn btn-danger")['href']
    full_Link = mainURL + half_Link
    # Downloading Content
    generateDown = requests.get(full_Link)
    with open(f"{MV_name}.srt", 'wb') as file:
        file.write(generateDown.content)
        print("\n" + MV_name +
              " Downloaded in ==> " + os.getcwd() + "  \n")


def multiDownload():
    links = sub2.find_all(
        'ul', class_="list-group")[0].find_all(class_="list-group-item")
    i = 0

    for eachlink in links:

        new_link = eachlink['href']
        new_name = eachlink.div.strong.text
        all_names.append(new_name)

        r3 = requests.get(new_link).text

        sub3 = BeautifulSoup(r3, 'html5lib')
        half_Link = sub3.find(
            'a', class_="btn btn-danger")['href']

        full_Link = mainURL + half_Link
        all_links.append(full_Link)

    return ""


def Thread_download(single_link, single_name, ):

    generateDown = requests.get(single_link)
    with open(f"{MV_name}/{single_name}.srt", 'wb') as file:
        file.write(generateDown.content)
    return ""


def main():

    if moviename_main.split(":")[-1] == "a":

        multiDownload()
        print("\nDownloading Multiple subtitles......\n")
        print(f"Downloading ==>  {len(all_links)} subtitles.. ")
        os.makedirs(MV_name, exist_ok=True)

        exe = futures.ThreadPoolExecutor(max_workers=3)
        results = exe.map(Thread_download,  all_links,
                          all_names)

        for r in results:
            r

        print(
            f"\n All {MV_name} sucessfuly Donwloaded in ==> {os.getcwd()} \n\n")

    else:
        singleDownload()


if __name__ == "__main__":
    main()
