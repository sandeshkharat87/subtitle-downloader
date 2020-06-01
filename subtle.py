#!/usr/bin/python3.6
import requests
from bs4 import BeautifulSoup
import os
import sys
import zipfile

subtle_link = {}   # Dict. for holding movie names


print("\n")
#

#              Take movie name

moviename = input("\n   Enter movie name : ").strip()

# moviename = "ironman"


#               URLS
baseurl = "https://www.yifysubtitles.com"
searchurl = "https://www.yifysubtitles.com/search?q=" + \
    moviename.replace(" ", "+")


# Request to webpage
try:
    r = requests.get(searchurl).text

    soup = BeautifulSoup(r, 'html5lib')

    scratch_link = soup.find_all("div", class_="media-body")

    # print(scratch_link[0].a['href'])

    name_Count = 0
    for mname in scratch_link:
        name_Count += 1
        Imdb_score = mname.a.find_all("div", class_="col-sm-6 col-xs-12 movie-genre")[
            1].find_all("span", class_="movinfo-section")[2].text.replace("I", " I")
        uU = mname.a['href']
        MV_name = mname.h3.text
        subtle_link[name_Count] = [baseurl + uU, MV_name, Imdb_score]

    print()
    print()

    for num, v in subtle_link.items():
        print(f"    [ {num} ]  {v[2]} -- {v[1]}    ")

    print()
    print()

    tempdata = []
    try:

        if len(subtle_link) == 0:
            print(" \n      Zero Results\n ")
            sys.exit()

        Uesrs_Choice = int(input("  Enter ur Choice: "))
        # Uesrs_Choice = int(1)

        if Uesrs_Choice > len(subtle_link):
            print("\n   Invalid Choice  ")
            sys.exit()

        # print(subtle_link[Uesrs_Choice][0])
        y_page = requests.get(subtle_link[Uesrs_Choice][0]).text
        print()
        print()
        sub2 = BeautifulSoup(y_page, 'html5lib')

        links = sub2.find_all("tr")

        # print(links)

        for k in links:
            # print(k.find_all("td", "flag-cell"))
            for j in k.find_all("td", "flag-cell"):
                if j.text == "English":
                    tempdata.append(k)

        u_half = tempdata[0].a["href"]
        f_url = baseurl + u_half

        z_page = requests.get(f_url).text

        sub3 = BeautifulSoup(z_page, 'html5lib')

        half_Link = sub3.find("a", class_="btn-icon download-subtitle")["href"]

        # print(half_Link)

        generateDown = requests.get(half_Link)

        MV_name = subtle_link[Uesrs_Choice][1]

        with open(f"{MV_name}.zip", 'wb') as file:
            file.write(generateDown.content)
            print("\n" + MV_name + " succesfully downloaded in > " +
                  os.getcwd() + " :) \n")

        with zipfile.ZipFile(f"{MV_name}.zip", "r") as zip_ref:
            zip_ref.extractall()

    except Exception as e:
        print("\n   Invalid Choice\n\n")
        # print(e)


except Exception as e:
    print("\nNo Internet Connection\n")
