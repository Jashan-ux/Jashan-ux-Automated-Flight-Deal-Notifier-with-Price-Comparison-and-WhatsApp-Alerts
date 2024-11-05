import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from flight_data import find_cheapest_flight
import os
from dotenv import load_dotenv


load_dotenv()


ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
FROM_WHATSAPP_NO = os.getenv("FROM_WHATSAPP_NO")
TO_WHATSAPP_NO = os.getenv("TO_WHATSAPP_NO")

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
 
ORIGIN_CITY_IATA = "DEL"


for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        # slow down requests
        time.sleep(2)
print(f"sheet_data:\n {sheet_data}")

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()


tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    print(f"Getting flights for {destination['city']}...")
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: £{cheapest_flight.price}")
    time.sleep(2)
    
lowest_price_sheet = float(destination["lowestPrice"])
current_price = cheapest_flight.price
notification = NotificationManager(ACCOUNT_SID ,AUTH_TOKEN ,FROM_WHATSAPP_NO ,TO_WHATSAPP_NO)
if current_price < lowest_price_sheet:
    notification.send_price_alert(current_price, destination['city'], tomorrow)
else:
    print(f"No alert for {destination['city']}, current price (£{current_price}) is not lower than the lowest recorded (£{lowest_price_sheet}).")






