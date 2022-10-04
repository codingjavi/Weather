from flask import Flask, render_template, request

# import json to load JSON data
import json
  
# urllib.request to make a request to api
import urllib.request
from PIL import Image
import base64
import io

app = Flask(__name__)

#creating the main web page (able to POST to it)
@app.route("/", methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        #if city is being inputed, store it in city varibles
        city = request.form["city"]
    else:
        #default city
        city = "Dallas"

    #api key
    api = "5987dce58c72394b6776ae0972cfc811"
    
    #getting coordinates using the Open Weather API
    source = urllib.request.urlopen('http://api.openweathermap.org/geo/1.0/direct?q=' + city + '&appid=5987dce58c72394b6776ae0972cfc811').read()

    #to access to json data file
    loading_data = json.loads(source)

    #creating a dictionary to store what we want from the json file
    #its a dictionary in a list so i have to acces the values like: [0]['lon']
    """
    data = {
        "lon": str(loading_data[0]['lon']),
        "lat": str(loading_data[0]['lat']),
    } """
    #getting and storing the latatude and longitude
    lon = str(loading_data[0]['lon'])
    lat = str(loading_data[0]['lat'])

    #using lat and lon to get the weather of any place
        #chaning the units from kelvin to fahrenheit
    weather_source = urllib.request.urlopen('https://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + lon + '&units=imperial&appid=5987dce58c72394b6776ae0972cfc811').read()
    
    #opening the JSON data
    weather_data = json.loads(weather_source)

    #weather_data is a dictionary
    data = {
        #There is a dictionry inside of a list in the weather key so calling it like this
        "name" : str(weather_data['name']),
        "weather" : str(weather_data['weather'][0]['main']),
        "description" : str(weather_data['weather'][0]['description']),
        "temperature" : int(weather_data['main']['temp']),
        "max" : int(weather_data['main']['temp_max']),
        "min" : int(weather_data['main']['temp_min']),
        "feels_like" : int(weather_data['main']['feels_like']),
        "wind" : int(weather_data['wind']['speed']),
        "country" : str(weather_data['sys']['country'])

    }

    #setting background images according to the weather
    if data["weather"] == "Clear":
        #selecting images
        im = Image.open("frsunny.jpg")
    elif data["weather"] == "Clouds":
        #selecting images
        im = Image.open("sunnyday.jpg")
    elif data["weather"] == "Rain":
        #selecting images
        im = Image.open("rainn.jpg")
    elif data["weather"] == "Snow":
        #selecting images
        im = Image.open("snow.jpg")
    elif data["weather"] == "Mist":
        #selecting images
        im = Image.open("mist.jpg")
    else:
        im = Image.open("snow.jpg")

    #using BytesIO we get the in-memory info to save the image we just read
    data_image = io.BytesIO()

    #saving it as JPEG
    im.save(data_image, "JPEG")

    #Then encode saved image file.
    encoded_img_data = base64.b64encode(data_image.getvalue())

    #passing weather data and image(background image)
    return render_template("index.html", data = data, img_data=encoded_img_data.decode('utf-8'))

if __name__ == '__main__':
    app.run(debug= True, port = 8000)
