import requests

class TravelAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://booking-com15.p.rapidapi.com/api/v1/"

    def get_headers(self):
        return {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "booking-com15.p.rapidapi.com"
        }

    def search_destination(self, query):
        url = f"{self.base_url}hotels/searchDestination"
        params = {"query": query}

        try:
            response = requests.get(url, headers=self.get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la llamada a la API de Booking: {e}")
            return None

    def search_hotels(self, dest_id, checkin_date, checkout_date, adults=1, children_age="0", room_qty=1, page_number=1):
        url = f"{self.base_url}hotels/searchHotels"
        print("Destination id: ", dest_id)
        params = {
            "dest_id": dest_id,
            "search_type": "CITY",
            "arrival_date": checkin_date,
            "departure_date": checkout_date,
            "adults": adults,
            "children_age": children_age,
            "room_qty": room_qty,
            "page_number": page_number,
            "units": "metric",
            "temperature_unit": "c",
            "languagecode": "en-us",
            "currency_code": "USD"
        }

        try:
            response = requests.get(url, headers=self.get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la llamada a la API de Booking: {e}")
            return None

    def get_hotel_details(self, hotel_id, arrival_date, departure_date, adults=1, children_age="0", room_qty=1):
        url = f"{self.base_url}hotels/getHotelDetails"
        params = {
            "hotel_id": hotel_id,
            "arrival_date": arrival_date,
            "departure_date": departure_date,
            "adults": adults,
            "children_age": children_age,
            "room_qty": room_qty,
            "units": "metric",
            "temperature_unit": "c",
            "languagecode": "en-us",
            "currency_code": "USD"
        }

        try:
            response = requests.get(url, headers=self.get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la llamada a la API de Booking: {e}")
            return None


    def get_flight_info(self, origin, destination, departure_date, return_date=None, adults=1, children=0, infants=0,
                        cabin_class="economy"):
        url = f"{self.base_url}flights/search"
        params = {
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date,
            "return_date": return_date,
            "adults": adults,
            "children": children,
            "infants": infants,
            "cabin_class": cabin_class,
            "lang": "en-us"
        }

        try:
            response = requests.get(url, headers=self.get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la llamada a la API de Booking: {e}")
            return None

    def get_restaurant_info(self, location, adults=1, children=0):
        url = f"{self.base_url}restaurants/search"
        params = {
            "location": location,
            "adults": adults,
            "children": children,
            "lang": "en-us"
        }

        try:
            response = requests.get(url, headers=self.get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la llamada a la API de Booking: {e}")
            return None

    def get_flight_prices(self, origin, destination, departure_date, return_date=None, adults=1, children=0, infants=0,
                          cabin_class="economy"):
        url = f"{self.base_url}flights/search/prices"
        params = {
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date,
            "return_date": return_date,
            "adults": adults,
            "children": children,
            "infants": infants,
            "cabin_class": cabin_class,
            "lang": "en-us"
        }

        try:
            response = requests.get(url, headers=self.get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la llamada a la API de Booking: {e}")
            return None

    def get_car_rental_info(self, location, pickup_date, dropoff_date, driver_age=30):
        url = f"{self.base_url}car_rentals/search"
        params = {
            "location": location,
            "pickup_date": pickup_date,
            "dropoff_date": dropoff_date,
            "driver_age": driver_age,
            "lang": "en-us"
        }

        try:
            response = requests.get(url, headers=self.get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la llamada a la API de Booking: {e}")
            return None

    def get_transport_info(self, location):
        url = f"{self.base_url}transport/search"
        params = {
            "location": location,
            "lang": "en-us"
        }

        try:
            response = requests.get(url, headers=self.get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la llamada a la API de Booking: {e}")
            return None


#if __name__ == "__main__":
    #api_key = "6eb7659adbmshe5fc3c22f1bddbbp19d5eajsnf7dd83dc13fc"
    #travel_api = TravelAPI(api_key)

    #hotel_info = travel_api.get_hotel_info(location="New York", checkin_date="2023-07-01", checkout_date="2023-07-10")
    #flight_info = travel_api.get_flight_info(origin="JFK", destination="LAX", departure_date="2023-07-01",return_date="2023-07-10")
    #restaurant_info = travel_api.get_restaurant_info(location="New York")
    #flight_prices = travel_api.get_flight_prices(origin="JFK", destination="LAX", departure_date="2023-07-01",return_date="2023-07-10")
    #car_rental_info = travel_api.get_car_rental_info(location="New York", pickup_date="2023-07-01",dropoff_date="2023-07-10")
    #transport_info = travel_api.get_transport_info(location="London")
