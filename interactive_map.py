import folium
import webbrowser
import os
import requests

class ParkingArea:
    def __init__(self, id, name, lat, lon, video_path):
        self.id = id
        self.name = name
        self.lat = lat
        self.lon = lon
        self.video_path = video_path
        self.available_spaces = 0
        self.total_spaces = 0

class InteractiveMapInterface:
    def __init__(self):
        self.parking_areas = {}
        self.html_file = os.path.join(os.path.dirname(__file__), 'interactive_parking_map.html')
        self.initialize_areas()

    def initialize_areas(self):
        self.add_parking_area(1, 'Parking Area 1', 12.842972222222222, 80.14816666666667, 'carPark.mp4')
        self.add_parking_area(2, 'Parking Area 2', 12.841166666666668, 80.15013888888889, 'carPark2.mp4')
        self.add_parking_area(3, 'Parking Area 3', 12.838805555555556, 80.15438888888889, 'carPark3.mp4')

    def add_parking_area(self, id, name, lat, lon, video_path):
        self.parking_areas[id] = ParkingArea(id, name, lat, lon, video_path)

    def update_area_availability(self, area_id, available, total):
        area = self.parking_areas.get(area_id)
        if area:
            area.available_spaces = available
            area.total_spaces = total

    def _get_route_osrm(self, origin, destination):
        lon1, lat1 = origin[1], origin[0]
        lon2, lat2 = destination[1], destination[0]
        url = (
            f"http://router.project-osrm.org/route/v1/driving/"
            f"{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson"
        )
        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            js = resp.json()
            coords = js['routes'][0]['geometry']['coordinates']
            return [[lat, lon] for lon, lat in coords]
        except Exception as e:
            print(f"[OSRM ERROR] {e}")
            return None

    def create_map(self, user_lat, user_lon):
        m = folium.Map(location=[user_lat, user_lon], zoom_start=15)

        folium.Marker([user_lat, user_lon], popup='You', icon=folium.Icon(color='blue')).add_to(m)

        for area in self.parking_areas.values():
            popup = f"<b>{area.name}</b><br>Free: {area.available_spaces}/{area.total_spaces}"
            color = 'green' if area.available_spaces > 0 else 'red'
            folium.Marker(
                [area.lat, area.lon],
                popup=popup,
                icon=folium.Icon(color=color, icon='car', prefix='fa')
            ).add_to(m)

            route = self._get_route_osrm((user_lat, user_lon), (area.lat, area.lon))
            if route:
                folium.PolyLine(route, weight=4, color='blue', opacity=0.7).add_to(m)
            else:
                folium.PolyLine(
                    [[user_lat, user_lon], [area.lat, area.lon]],
                    weight=2,
                    color='gray',
                    opacity=0.5,
                    dash_array='5,10'
                ).add_to(m)

        m.save(self.html_file)
        return self.html_file

    def show_map(self, user_lat, user_lon):
        html = self.create_map(user_lat, user_lon)
        webbrowser.open('file://' + os.path.realpath(html))
