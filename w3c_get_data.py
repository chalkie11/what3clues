# Local 
import countries # from github

# Inbuilt
import os
import json
from random import uniform, randrange
import requests

# For geo stuff
import what3words
from global_land_mask import globe
import folium
from folium import plugins
import pycountry # to get country name from 2-alpha code
from countryinfo import CountryInfo # to get info from the country name
import pandas as pd
from PyDictionary import PyDictionary
# import branca

def w3w(num_coords_to_plot=10, show_status=True):
	global answer_words

	# import the dictionary from PyDictionary 
	dictionary=PyDictionary()

	# get country names from shapefile
	dir_path = os.path.dirname(os.path.realpath(__file__))
	cc = countries.CountryChecker(dir_path+"\\TM_WORLD_BORDERS-0.3\\TM_WORLD_BORDERS_0_3.shp")

	# access what3words api
	with open('YOUR_KEY.txt', 'r') as file:
		w3w_key = file.read().replace('\n', '')

	geocoder = what3words.Geocoder(w3w_key)


	# set num of points to plot
	num_coords = num_coords_to_plot

	# set max num times a country can appear
	max_occur = 5

	country_list=[]
	tw_list=[]

	#find points that are land and are not excluded countries
	exclude = ["AQ", "GL"] # antarctica and greenland

	count_water=0
	count_land_valid=0
	count_land_invalid=0

	while len(tw_list)<num_coords:
		# select random coords
		lat = uniform(-90, 90)
		lon = uniform(-180, 180)
		# check they are on land
		is_on_land = globe.is_land(lat, lon)
		if is_on_land:
			try:
				# get country code from coords
				country = cc.getCountry(countries.Point(lat, lon)).iso
				# add to list if not excluded country or if not already in list N times
				if country not in exclude and country_list.count(country)<=max_occur:
					# get what3words info
					tw_dict = geocoder.convert_to_3wa(what3words.Coordinates(lat, lon))
					# add to list
					tw_list.append(tw_dict)
					country_list.append(country)
					count_land_valid+=1
				else:
					count_land_invalid+=1
			except:
				count_land_invalid+=1
		else:
			count_water+=1
		if show_status:
			print("Valid land = "+str(count_land_valid)+" | Invalid land = "+str(count_land_invalid)+" | Water = "+str(count_water), end='\r')

	# randomly choose the correct answer loc of deduped country list
	country_list_dedup = list(dict.fromkeys(country_list))
	answer_no = randrange(len(country_list_dedup)+1)

	# w3w answer and country name
	answer_words = tw_list[answer_no]['words']
	clue_code = tw_list[answer_no]['country']


	# CLUES.........
	clues = {}


	# get iso to gec loopkup
	csv_url = 'https://raw.githubusercontent.com/dieghernan/Country-Codes-and-International-Organizations/master/outputs/Countrycodes.csv'
	csv = pd.read_csv(csv_url)

	# keep relevant cols
	keep_cols = ['ISO_3166_2','FIPS_GEC']
	csv = csv[keep_cols]

	# drop blanks and keep where both codes match
	csv = csv.dropna(subset=keep_cols).loc[csv['ISO_3166_2'] == csv['FIPS_GEC']]
	val = clue_code

	# if country code ISO matches GEC then use either ISO or GEC data library (randomly), else use ISO data library
	gec = 0
	if val in csv['ISO_3166_2'].values:
		gec = randrange(0,2)

	# get data
	if gec:
		folders = ['africa', 'australia-oceania', 'central-america-n-caribbean', 'central-asia', 'east-n-southeast-asia', 'europe', 'middle-east', 'north-america', 'south-america', 'south-asia']

		ctry_gec = val

		# loop through folders in github project until one is found
		for ctry_github in folders:
			# get data in json format from github
			r = requests.get("https://raw.githubusercontent.com/factbook/factbook.json/master/"+ctry_github+"/"+ctry_gec.lower()+".json")
			if r.status_code == 200:
				data = json.loads(r.text)

				# get the data
				name = data['Government']['Country name']['conventional short form']['text']
				size = data['Geography']['Area - comparative']['text']
				capital = data['Government']['Capital']['name']['text']
				final_data = {
					'area-comparative': {'name': 'Comparative area', 'difficulty':2, 'value': str(data['Geography']['Area - comparative']['text'])},
					'capital-city': {'name': 'Capital', 'difficulty':2, 'value': str(data['Government']['Capital']['name']['text'])},
					'location': {'name': 'Capital', 'difficulty':2, 'value': str(data['Geography']['Location']['text'])},
					'climate': {'name': 'Climate', 'difficulty':2, 'value': str(data['Geography']['Climate']['text'])},
					'elevation': {'name': 'Elevation (high point)', 'difficulty':2, 'value': str(data['Geography']['Elevation']['highest point']['text'])},
					'population-distribution': {'name': 'Population distribution', 'difficulty':2, 'value': str(data['Geography']['Population distribution']['text'])},
					'population': {'name': 'Population', 'difficulty':2, 'value': str(data['People and Society']['Population']['text'])},
					'ethnicity': {'name': 'Ethnic groups', 'difficulty':2, 'value': str(data['People and Society']['Ethnic groups']['text'])},
					'languages': {'name': 'Languages', 'difficulty':2, 'value': str(data['People and Society']['Languages']['text'])},
					'religion': {'name': 'Religions', 'difficulty':2, 'value': str(data['People and Society']['Religions']['text'])},
	 				'flag-description': {'name': 'Flag description', 'difficulty':2, 'value': str(data['Government']['Flag description']['text'])},
				}
	else:
		# get country name
		r = requests.get('https://raw.githubusercontent.com/samayo/country-json/master/src/country-by-abbreviation.json')
		if r.status_code == 200:
			data = json.loads(r.text)
			for country in data:
				if country['abbreviation'] == val:
					country_name = str(country['country'])
					print(country_name)
					# now that have country name, loop through the datasets
					data_jsons = {	'currency-name': {'name': 'Currency', 'varname':'currency_name', 'difficulty': 2, 'value': ''},
									'capital-city': {'name': 'Capital', 'varname': 'city', 'difficulty': 2, 'value':''},
									'costline': {'name': 'Coastline', 'varname': 'costline', 'difficulty': 2, 'value':''},
									'domain-tld': {'name': 'Domain address', 'varname': 'tld', 'difficulty': 2, 'value':''},
									'elevation': {'name': 'Elevation', 'varname': 'elevation', 'difficulty': 2, 'value':''},
									'languages': {'name': 'Languages', 'varname': 'languages', 'difficulty': 2, 'value':''},
									'national-dish': {'name': 'National dish', 'varname': 'dish', 'difficulty': 2, 'value':''},
									'national-symbol': {'name': 'National symbol', 'varname': 'symbol', 'difficulty': 2, 'value':''},
									'population-density': {'name': 'Population density', 'varname': 'density', 'difficulty': 2, 'value':''},
									'religion': {'name': 'Religion', 'varname': 'religion', 'difficulty': 2, 'value':''},
									'surface-area': {'name': 'Surface area', 'varname': 'area', 'difficulty': 2, 'value':''}
								}
					for data_json, meta in data_jsons.items():
						# get the data and check it exists
						r = requests.get('https://raw.githubusercontent.com/samayo/country-json/master/src/country-by-'+data_json+'.json')
						if r.status_code == 200:
							data = json.loads(r.text)
							# loop through all json data 
							for country in data:
								# if country name is the one we are looking for then get the data
								if country['country'] == country_name:
									# if data is list then append into a string, else just get the data
									varname = meta['varname']
									if type(country[varname]) is list:
										# if national dish then choose random
										# FIX THIS AS IT IS A COMMA SEPARATED LIST NOT A PYTHON LIST
										if data_json == 'national-dish':
											value = country[varname][randrange(0,len(country[varname]+1))]
										else:
											value = ''.join(str(e)+' ' for e in country[varname])
									else:
										value = str(country[varname])								

									print(meta['name']+': '+value)

									# update values
									data_jsons[data_json]['value'] = value
							final_data = data_jsons

	clues.update(final_data)

	# nearest place
	clue_near_place=tw_list[answer_no]['nearestPlace']
	clues.update({'nearest-place': {'name': 'Nearest place', 'varname': 'nearestPlace', 'difficulty': 1, 'value':clue_near_place}})

	
	# select a random word from the what 3 words aswer
	word_clues = {}
	word_no = randrange(3)
	word_answer = answer_words.split('.')[word_no]

	# get the first meaning of the first word type (noun, verb etc)
	word_dictionary_entry = dictionary.meaning(word_answer)
	word_type = list(word_dictionary_entry.items())[0][0]
	word_meaning = list(word_dictionary_entry.items())[0][1][0]

	word_type_meaning = word_type+': '+word_meaning

	word_clues.update({'word_type_meaning': {'name': 'Meaning of one of the words', 'varname': 'word_type_meaning', 'difficulty': 0, 'value':word_type_meaning}})

	# get the synonym of the word
	if dictionary.synonym(word_answer) is not None: 
		synonym = dictionary.synonym(word_answer)
		word_clues.update({'synonym': {'name': 'Synonym of one of the words', 'varname': 'synonym', 'difficulty': 0, 'value':synonym}})

	clues.update(word_clues)

	# get a clues into dictionary with diffculty as key
	clues_diff = {0: {}, 1: {}, 2: {}}
	for i, val in clues.items():
		if val['value']:
			clues_diff[val['difficulty']][i] = val




	# init map
	m = folium.Map( width='75%', height='75%',max_bounds=True)

	# add points to map
	for point in tw_list:
		lat = point['coordinates']['lat']
		lon = point['coordinates']['lng']
		words = point['words']
		html=words

		'''
		TODO ADD THIS BACK IN WHEN IFRAME WORKING
		html = 	words+"""
					<form action="https://google.com">
					    <input type="submit" value="Select" />
					</form>
				"""
		'''

		# pp = folium.Html(html, script=True)
		# iframe = branca.element.IFrame(html=pp, height='150px', width='200px')

		iframe = folium.IFrame(html=html, height=150, width=200)


		popup = folium.Popup(iframe, max_width=2650, parse_html=True)
		folium.Marker(
		    location=[lat, lon],
		    popup=popup, # pop-up label for the marker
		    icon=folium.Icon()
		).add_to(m)

	# Display the map
	m.save(outfile= dir_path+"\\templates\\map.html")

	'''
	To-do: return the map as html object and embed within home.html
	map_html = m._repr_html_()
	'''


	# return all of the clues and answers
	return answer_words, clues_diff #, map_html

