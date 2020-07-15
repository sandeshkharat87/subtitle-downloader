#!/usr/bin/python3.6
import requests
from bs4 import BeautifulSoup
import os
import sys

from concurrent import futures


def downsub(moviename=input("\nEnter movie name: "), lang=None):

    try:

        subtle_link = {}
        all_links = []
        all_names = []

        mainURL = "https://opensubtitles.co"
        searchurl = "https://opensubtitles.co/search?q=" + \
            moviename.replace(" ", "+")

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
            try:
                Uesrs_Choice = int(input("\nEnter your choice : "))
                # Uesrs_Choice = int(1)
                if Uesrs_Choice <= len(subtle_link):
                    MV_Folder_name = subtle_link[Uesrs_Choice].split('/')[-1]
                    r2 = requests.get(subtle_link[Uesrs_Choice]).text
                    sub2 = BeautifulSoup(r2, 'html5lib')
                    # links = sub2.find('ul', class_="list-group").a['href']
                    links = sub2.find_all(
                        'ul', class_="list-group")[0].find_all(class_="list-group-item")
                    i = 0

                    print("\nDownloading Using Threads......\n")

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

                    return all_links, all_names, MV_Folder_name

                else:
                    print(f"\n\t\tInvalid Choice....Try Agian....\n")

            except KeyboardInterrupt as e:
                print(e)
            except Exception as e:
                print()
                print("Zero search results!!! \n")
                print(e)

    except Exception as e:
        print(f"\n{e}")


x_links, y_names, z_folder = downsub()


# Downloading Using Threads
def Thread_download(single_link, single_name, ):

    generateDown = requests.get(single_link)
    with open(f"{z_folder}/{single_name}.srt", 'wb') as file:
        file.write(generateDown.content)
    return ""


def main():

    os.makedirs(z_folder, exist_ok=True)

    exe = futures.ThreadPoolExecutor(max_workers=3)
    results = exe.map(Thread_download,  x_links,
                      y_names)

    for r in results:
        r

    print(f"\n {z_folder} sucessfuly Donwloaded in  {os.getcwd()} \n\n")


if __name__ == "__main__":
    main()
