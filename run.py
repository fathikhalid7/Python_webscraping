from bs4 import BeautifulSoup
from urllib.request import urlopen
import pymysql
import time
import datetime

today_date = datetime.datetime.now()
today = today_date.strftime("%Y-%m-%d %H:%M:%S")

try:
    try:
        conn = pymysql.connect("localhost", "root", "", "py_test")
        cursor = conn.cursor()
    except:
        print("Error connecting to database")

    else:
        url = "https://pba.com.my/penang-dams-effective-capacity/"
        page = urlopen(url)

        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        updatedAt = soup.find("span", {"class" : "updated"}).contents[0]
        updatedAt_date = updatedAt[:10]
        updatedAt_time = updatedAt[11:19]
        updatedAt_dt = updatedAt_date + " " +updatedAt_time
        print(updatedAt_dt)

        dams = ["AIR ITAM", "TELUK BAHANG", "MENGKUANG"]

        dams_id = 0
        count = -1
        for value in soup.find_all("span", {"class": "display-counter"}):
            # print(dams[count] + " - " + value.get("data-value"))
            dams_id = dams_id + 1
            capacity = value.get("data-value")
            count = count + 1

            sql_insert = "INSERT INTO pba_dams (dams, capacity, dams_id, updated_at) VALUES ('" +dams[count]+ "', '"+capacity+"', '" + str(dams_id)+ "', '" + updatedAt_dt + "')"
            cursor.execute(sql_insert)
            print(sql_insert)

        conn.commit()
except:
    print("Error")
