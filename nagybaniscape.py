from urllib.request import urlopen as u_req
from bs4 import BeautifulSoup as soup
import os
import pandas as pd
import datetime

os.chdir(r"C:\Users\Áron\Desktop\nagybani")

my_url = "https://nagybani.hu/arak"

#Grabbing web page
u_client = u_req(my_url)

page_html = u_client.read()
u_client.close()

#html-parsing
page_soup = soup(page_html, "html.parser")
containers = page_soup.findAll("tr")


#Checking is its still apples
termék = containers[67].findAll("td")[0].text
print(termék)
minimum = containers[67].findAll("td")[3].text
maximum = containers[67].findAll("td")[4].text


min_a = int(minimum[:4])
max_a = int(maximum[:4])
current_time = datetime.datetime.now()
date = str(current_time.year)+"-"+str(current_time.month)+"-"+str(current_time.day)


def empty_df():
    df = pd.DataFrame (columns = ["Datum","Minimum_ar", "Maximum_ar"])
    return df

#read is csv file
df = pd.read_csv("nagybani.csv")

#daily data
new_row = {'Datum':date, 'Minimum_ar':min_a, 'Maximum_ar':max_a}

#if data is already registered and not alma do not add
if date not in df["Datum"].values and termék == "Alma":
    df = df.append(new_row, ignore_index = True)

print("Done!")
df.to_csv("nagybani.csv", index = False)



