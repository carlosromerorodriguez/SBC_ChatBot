import requests

class TravelAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://booking-com.p.rapidapi.com/v1/"

    def get_headers(self):
        return {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "booking-com15.p.rapidapi.com"
        }

    def get_hotel_info(self, dest_id, checkin_date, checkout_date, adults=1, children=0, rooms=1, currency="USD", locale="en-us"):
        url = f"{self.base_url}hotels/search"
        params = {
            "dest_id": dest_id,
            "checkin_date": checkin_date,
            "checkout_date": checkout_date,
            "adults_number": adults,
            "children_number": children,
            "room_number": rooms,
            "locale": locale,
            "currency": currency,
            "units": "metric"
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
