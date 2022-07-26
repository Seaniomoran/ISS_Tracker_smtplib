import requests
from datetime import datetime
import smtplib
import time
import os

MY_LAT = 40.0000
MY_LONG = -73.0000
my_email =  os.getenv("EMAIL_17") #enter your email
my_password = os.getenv("EMAIL_17_PASSWORD")  #enter google account, security, app password
iss_latitude = 0.0000
iss_longitude = 0.000
sunrise = ""
sunset = ""
hour = ""
is_overhead = False

def get_iss_location():

    global iss_latitude, iss_longitude
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])


def compare_locations():

    if hour >= sunset or hour <= sunrise and abs(MY_LAT - iss_latitude) <= 5 and abs(MY_LONG - iss_longitude) <= 5:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()  # makes connection secure
            connection.login(user=my_email, password=my_password)
            connection.sendmail(from_addr=my_email, to_addrs=my_email,
                                msg=f"Subject: ISS is overhead!\n\nLook up at the "
                                    f"International Space Station which is currently"
                                    f"above you at {round(iss_longitude, 2)} "
                                    f"longitude and {round(iss_latitude, 2)} "
                                    f"latitude!")


#your position is within +5 or -5 degrees of ISS position
def find_sun_hours():
    global hour, sunrise, sunset
    parameters = {
        "lat": MY_LAT,
        "long": MY_LONG,
        "formatted": 0
    }

    day_info = datetime.now()
    hour = day_info.hour

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])


def iss_tracker():
    global is_overhead
    while not is_overhead:
        find_sun_hours()
        get_iss_location()
        compare_locations()
        time.sleep(60)
    time.sleep(600)
    iss_tracker()


iss_tracker()