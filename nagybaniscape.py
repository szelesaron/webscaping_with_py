from urllib.request import urlopen as u_req
from bs4 import BeautifulSoup as soup
import os
import pandas as pd
import datetime
import smtplib

os.chdir(r"C:\Users\Áron\Desktop\nagybani")

my_url = "https://nagybani.hu/arak"

#Grabbing web page
u_client = u_req(my_url)

page_html = u_client.read()
u_client.close()

#html-parsing
page_soup = soup(page_html, "html.parser")
containers = page_soup.findAll("tr")


#Checking is its still apple
def get_apple_index():
    n = 1
    while True:
        if (containers[n].findAll("td")[0].text == "Alma"):
            return n
        n+=1

        
termék = containers[get_apple_index()].findAll("td")[0].text
print(termék)
minimum = containers[get_apple_index()].findAll("td")[3].text
maximum = containers[get_apple_index()].findAll("td")[4].text

#Get new daily data and format it
min_a = int(minimum[:4])
max_a = int(maximum[:4])
current_time = datetime.datetime.now()
date = str(current_time.year)+"-"+str(current_time.month)+"-"+str(current_time.day)


def empty_df():
    df = pd.DataFrame (columns = ["Datum","Minimum_ar", "Maximum_ar"])
    return df

#read is csv file
df = pd.read_csv("nagybani.csv")


    
 
#SEND EMAIL IF DATA CHANGES 
if df["Maximum_ar"].iloc[-1] != max_a :
    
    sender = "nagybani.ar@gmail.com"
    recevier = "csanakialma@gmail.com"
    password = "Abcd1234."
    
    diff = max_a - df["Maximum_ar"].iloc[-1]
    if diff > 0:
        text = "Uj maximum ar " + str(max_a) + " " + f"(+{diff})" + "Ft" 
    else:
        text = "Uj maximum ar " + str(max_a) + " " + f"({diff})" + "Ft" 
    
    text = "Uj Maximum ar " + str(max_a)+" " + f"({diff})" + " Ft" 
    message = 'Subject: {}\n\n{}'.format("Ar valtozas", text)

    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    print("Logged in")
    server.sendmail(sender, recevier, message)
    print("Sent")

if df["Minimum_ar"].iloc[-1] != min_a:
    sender = "nagybani.ar@gmail.com"
    recevier = "csanakialma@gmail.com"
    password = "Abcd1234."
    
    diff = min_a  - df["Minimum_ar"].iloc[-1]
    if diff > 0:
        text = "Uj minimum ar " + str(min_a) + " " + f"(+{diff})" + "Ft" 
    else:
        text = "Uj minimum ar " + str(min_a) + " " + f"({diff})" + "Ft" 
        
    message = 'Subject: {}\n\n{}'.format("Ar valtozas", text)
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    print("Logged in")
    server.sendmail(sender, recevier, message)
    print("Sent")


#daily data
new_row = {'Datum':date, 'Minimum_ar':min_a, 'Maximum_ar':max_a}

#if data is already registered and not alma do not add
if date not in df["Datum"].values and termék == "Alma":
    df = df.append(new_row, ignore_index = True)



#save csv
print("Done!")
df.to_csv("nagybani.csv", index = False)






