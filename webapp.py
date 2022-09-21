from pickle import GET
from flask import Flask, render_template, request, redirect, url_for, session
import requests
from bs4 import BeautifulSoup


import datetime




app = Flask(__name__)


@app.route('/' , methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# Create route that displays the form
@app.route('/music' , methods=['GET', 'POST'])
# Create a function that will show the top 100 songs of the year that the user inputs
def music():
    if request.method == 'POST':
        date = request.form['date']
        url = f"https://www.billboard.com/charts/hot-100/{date}"
        response = requests.get(url)
        data_from_songs = response.text
        soup = BeautifulSoup(data_from_songs, "html.parser")
        raw_song_names = soup.find_all(name='h3', id='title-of-a-story')
        top_songs = []
        for song in raw_song_names:
            s = song.text.strip()
            if s != "Songwriter(s):":
                if s != "Producer(s):":
                    if s != "Imprint/Promotion Label:":
                        top_songs.append(s)
        top_100_songs = top_songs[3: 103]
        return render_template('music.html', songs=top_100_songs)
    else:
        return render_template('music.html')



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')





if __name__ == '__main__':
    app.run(debug=True)
    