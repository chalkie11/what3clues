# What3Clues

This is a flask based web game.

You will need to sign up for a What3Words API account from https://accounts.what3words.com/create-api-key?referrer=/public-api then replace the text in `YOUR_KEY.txt` with your API key. 

Then pip install the following:
```
pip install what3words
pip install countryinfo
pip install pycountry
pip install global_land_mask
pip install folium
pip install pandas
pip install PyDictionary
pip install Flask
```

To play, run `python what3clues` then navigate to `http://127.0.0.1:5000/` in your browser. Use the `?num_coords=` URL parameter to control the number of pins to show on the map (max 100).

Use the clues to identify the location of the What3Words pin, then enter the text into the answer box.