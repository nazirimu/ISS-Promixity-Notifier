from datetime import datetime
import requests
import smtplib
import time

# -------------------------------- CONSTANTS ----------------------------------- #
MY_LAT = 43.653225
MY_LONG = -79.383186
MY_EMAIL = ""
MY_PASSWORD = ""
# PASSWORD AND EMAIL HAVE BEEN LEFT EMPTY FOR PRIVACY CONCERNS


# -------------------------------- CHECKER ----------------------------------- #
def station_proximity_checker(iss_lat, iss_long):
    """Checks if ISS is within +5 or -5 of current location"""
    if (MY_LAT - 5 <= iss_lat <= MY_LAT + 5) and (MY_LONG - 5 <= iss_long <= MY_LONG + 5):
        return True
    else:
        return False


# ----------------------------- EMAIL SENDER ------------------------------------ #
def send_email():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL,
                            msg=f"subject: Look up 👆\n\nHello, \nThe ISS is near you.")


# --------------- SUNRISE AND SUNSET TIMES ------------------------------------ #

def is_night():
    """Checks if the current time is within night hours and returns a boolean value"""

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }
    # Using request module to get a response from the Sunrise and Sunset API
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    # Raising a status if 200 code is not received from api
    response.raise_for_status()
    # converting response into a json format data
    data = response.json()
    # getting sunrise and sunset times from data
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour
    if sunset <= time_now or time_now <= sunrise:
        return True
    else:
        return False


# --------------------- ISS LOCATION ----------------------------------------- #
def station_proximity_checker():
    """Checks if ISS is within +5 or -5 of current location and returns a boolean value"""

    # Using request module to get a response from the ISS API
    response = requests.get("http://api.open-notify.org/iss-now.json")
    # Raising a status if 200 code is not received from api
    response.raise_for_status()
    data = response.json()
    # obtaining iss latitude and longitude from data
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if (MY_LAT - 5 <= iss_latitude <= MY_LAT + 5) and (MY_LONG - 5 <= iss_longitude <= MY_LONG + 5):
        return True
    else:
        return False


# -------------------- LOOP ---------------------------------------------------#
# Loops runs every 60 secs and if the iss location is near, an email will be sent
while True:
    time.sleep(60)
    if station_proximity_checker() and is_night():
        send_email()

