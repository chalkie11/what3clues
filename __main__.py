from flask import Flask, render_template, jsonify, request, make_response, session

app = Flask(__name__)
app.secret_key = 'random string of chars'

@app.before_first_request                                                   
def import_the_big_packages():                                                        
	from global_land_mask import load_npz_data
	load_npz_data()



@app.route("/",methods= ['POST', 'GET'])
def home():

	# Default 10, maximum 100, minimum 1
	num_coords_input = max(min(request.args.get('num_coords', default = 10, type = int),100),1)

	answer, clues_diff = w3w(num_coords_to_plot=num_coords_input) # add this back on when html code is done.....      , map_html
	session['answer'] = answer
	# session['map_html'] = map_html

	# get random clues from the data
	clue_vals = {0: {}, 1: {}, 2: {}}
	for i, val in clues_diff.items():
		counter = 0
		found = 0
		while not found and counter <10:
			if len(val)==1:
				rand_key=list(val)[0]
			else:
				try:
					rand_key = list(val)[randrange(len(list(val)))]
				except Exception as e:
					print(e)
					rand_key = False
					pass
			counter += 1
			
			if rand_key:
				clue_val = {'Name': val[rand_key]['name'], 'Value': val[rand_key]['value']}
				if val[rand_key]['value'] != 'None':
					found=1
			if not found:
				error_msg = 'There was an error getting this clue.'
				clue_val = {'Name': 'Clue '+str(i), 'Value': error_msg}
			clue_vals[i] = clue_val

	return render_template("home.html", 
		answer=answer,
		clue0_name=clue_vals[0]['Name'],
		clue0_val=clue_vals[0]['Value'],
		clue1_name=clue_vals[1]['Name'],
		clue1_val=clue_vals[1]['Value'],
		clue2_name=clue_vals[2]['Name'],
		clue2_val=clue_vals[2]['Value'],
		)


'''
To-do: put folium map within an iframe and post/get data to main page
'''
# @app.route("/test1",methods= ['POST', 'GET'])
# def test1():
# 	import folium
# 	map_html = session.get('map_html', None)
# 	return map_html


@app.route('/process',methods= ['POST'])
def process():
	user_input = request.form['user_input']
	answer = session.get('answer', None)
	if not user_input:
		return jsonify({'output':'Please enter an answer', 'newgame_button':'<b></b>'})
	elif user_input==answer:
		return jsonify({'output':'Correct!!', 'newgame_button': '<button onClick="window.location.reload();">New game</button>'})
	else:
		return jsonify({'output':'Try again', 'newgame_button':'<b></b>'})



def main():
	app.run(debug=True)


if __name__ == "__main__":

	# Inbuilt
	import os
	import json
	from random import uniform, randrange
	import requests

	# Flask
	from flask import Flask, render_template, jsonify, request, make_response, session

	# Local
	import w3c_get_data 
	from w3c_get_data import w3w

	main()