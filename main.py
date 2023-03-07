from flet import *
import requests
import folium
import re
import os
import webbrowser


def main(page:Page):
	page.scroll = "auto"
	token = "5b3ce3597851110001cf624889c9b3b654f644b293c431600f4dd356"

	cordinate_start = TextField(label="you cordinate start")
	cordinate_final = TextField(label="you cordinate destination")

	# YOU RESULT ROUTE
	route_result = Text()

	def get_route(start,end):
		api_key = token
		if not re.match(r'^\s*-?\d+(?:\.\d+)?\s*,\s*-?\d+(?:\.\d+)?\s*$',start):
			raise ValueError("invalid start cordinate")
		if not re.match(r'^\s*-?\d+(?:\.\d+)?\s*,\s*-?\d+(?:\.\d+)?\s*$',end):
			raise ValueError("invalied end cordinate")
		url = f'https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={start}&end={end}'
		
		response = requests.get(url).json()

		coordinated = response["features"][0]["geometry"]["coordinates"]
		route = [[coord[1], coord[0]] for coord in coordinated]

		# AND GET INSTRUCTION TO DESTINCATION LIKE STREET
		instructions = response['features'][0]['properties']['segments'][0]['steps']

		my_direction = []

		# AND ADD TO TEXT WIDGET THE INSTRUCTION ROUTE
		for i , step in enumerate(instructions):
			my_direction.append(f"{i+1}. {step['instruction']} {step['distance']} meter")
		route_result.value = "\n".join(my_direction)
		return route



	def findroutenow(e):
		if not cordinate_start.value or not cordinate_final.value:
			return

		# AND CONVERT AND REMOVE , FROM YOU INPUT CORDINATE
		# THEN GET LATITUDE AND LONGITUDE FROM YOU INPUT
		start_lat, start_lon = map(float,cordinate_start.value.split(","))
		end_lat, end_lon = map(float,cordinate_final.value.split(","))
		
		start = f'{start_lon},{start_lat}'
		end = f'{end_lon},{end_lat}'

		route = get_route(start,end)

		# AND NOW DRAW MAPS AND CREATE MARKER AND LINE DIRECTION
		m = folium.Map(location=[start_lat,start_lon],zoom_start=13)

		# AND NOW CREATE MARKER START AND END DESTINATION

		folium.Marker(location=[start_lat,start_lon],tooltip=" start ").add_to(m)
		folium.Marker(location=[end_lat,end_lon],tooltip="end ").add_to(m)

		# AND NOW CREATE LINE 
		folium.PolyLine(locations=route,color="red",weight=5).add_to(m)

		# AND LAST SAVE HTML FILE
		m.save("route.html")
		print("YOU SUCCESS CREATE MAPS GUYSS !!!")
		page.update()







	def showmaps(e):
		filename = "route.html"
		if not os.path.exists(filename):
			print(f"{filename} not found")
			return
		browser = webbrowser.get("firefox")
		browser.open(f"file://{os.path.abspath(filename)}")

		# AND NOW OPEN MAPS WITHOUT NO ROOT USER
		 # I AM OPEN WITH FIREFOX




	page.add(
	AppBar(
	title=Text("flet Route",size=25,weight="bold",
		color="white"),
	bgcolor="blue"
		),

	Column([
		cordinate_start,
		cordinate_final,
		ElevatedButton("find you route location",
		bgcolor="blue",color="white",
		on_click=findroutenow
			),
		Text("you route",weight="bold",size=25),
		route_result ,
		ElevatedButton("show maps route",
		bgcolor="green",color="white",
		on_click=showmaps
			)


		])

		)

flet.app(target=main)

