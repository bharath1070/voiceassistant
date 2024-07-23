import flask 
import webbrowser
import openai
import requests
import wikipedia
import datetime
import re
import speech_recognition as sr
import pyttsx3
import pyjokes
import pywhatkit
import python_weather
import asyncio

from flask import Flask, render_template,redirect

app = Flask(__name__)

@app.route("/")
def indexpage():
    return render_template("index.html")


@app.route("/record")
def voiceAssistant():
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    r = sr.Recognizer()

    def wishMe():
        hr = datetime.datetime.now().hour
        if hr >= 0 and hr < 12: 
            speak("Good Morning")
        elif hr >= 12 and hr < 18:
            speak("Good Afternoon")
        else:
            speak("Good Evening")
    
    def select_100_words(text):
        words = text.split()
        selected_words = words[:100]
        selected_text = ' '.join(selected_words)
        return selected_text   

    def tellTime():
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time
    
    async def get_weather(location):
        substring = "weather in "
        if substring in location:
            location = location.split(substring)[1]
            async with python_weather.Client(format=python_weather.METRIC) as client:
                weather = await client.get(location)
            speak(f"The temperature in {location} is {weather.current.temperature} degrees Celsius.")
        else :
            speak("Issue in weather Module")
    

    def speak(audio):
        engine.say(audio)
        engine.runAndWait()
    
    def TakeCommand():
        with sr.Microphone() as source:
            speak("Hi i am Listening...")
            r.energy_threshold = 400
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            # speak("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            return query

        except Exception as e:
            speak("Unable to Understand")
            return "Fine"
    
    if 1:
        wishMe()
        query = TakeCommand().lower()
        speak(f"you said:-{query}")
        if(query == "Fine"):
            speak("Try to speak once again, sorry for the Inconvinence")
        elif ".com" in query:
            path = re.compile(r'[0-9a-zA-Z.%_]+[.][0-9a-zA-Z.]+')
            match = path.findall(query)
            string = match[0]
            if "www." in string:
                web = string
            else:
                web = "www." + string
            try:
                webbrowser.open(web)
            except Exception as e:
                speak("Cant find the site.")
        else:
        
            if "wikipedia" in query:
                try:
                    speak("Searching Wikipedia")
                    query = query.replace("wikipedia", "")
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia")
                    speak(results)
                except Exception as e:
                    speak("Cannot find searched item.")
            elif "time" in query:
                time = tellTime()
                speak("The time is")
                speak(time)

            elif 'open youtube' in query:
                speak("Here you go to Youtube\n")
                webbrowser.open("youtube.com")
 
            elif 'open google' in query:
                speak("Here you go to Google\n")
                webbrowser.open("google.com")
 
            elif 'open stackoverflow' in query:
                speak("Here you go to Stack Over flow.Happy coding")
                webbrowser.open("stackoverflow.com")

            elif 'how are you' in query:
                speak("I am fine, Thank you")
                speak("How are you, Sir")
 
            elif 'fine' in query or "good" in query:
                speak("It's good to know that your fine")

            elif "weather" in query and "in" in query:
                asyncio.run(get_weather(query))

            elif "who made you" in query or "who created you" in query:
                speak("I have been created by Bharath Kumar.")

            elif "who i am" in query:
                speak("If you talk then definitely your human.")
 
            elif "why you came to world" in query:
                speak("Thanks to Bharath Kumar. further It's a secret")

            elif 'is love' in query:
                speak("It is 7th sense that destroy all other senses")
 
            elif "who are you" in query:
                speak("I am your virtual assistant created by Bharath Kumar")
 
            elif 'reason for you' in query:
                speak("I was created as a Minor project by Mister Bharath kumar")
            
            elif "where is" in query:
                try:
                    query = query.replace("where is", "")
                    location = query
                    speak("User asked to Locate")
                    speak(location)
                    webbrowser.open("https://www.google.co.in/maps/place/" + location)
                except Exception as e:
                    speak("Cannot find searched item.")
            elif "will you be my gf" in query or "will you be my bf" in query:
                speak("I'm not sure about, may be you should give me some time")
            
            elif "i love you" in query:
                speak("It's hard to understand")
            
            elif "tell" and "me" and "a" and "joke" in query:
                speak(pyjokes.get_joke())
            
            elif "search" and "for"  in query or "what" in query:
                query1 = query.lower()
                query1 = query1.replace("search","")
                query1 = query1.replace("for","")
                url='https://www.google.co.in/search?q='
                search_url=url+query1
                webbrowser.open(search_url)
            
            elif "play song" in query:
                try:
                    song = query.replace('play song', '')
                    speak('playing ' + song)
                    pywhatkit.playonyt(song)
                except Exception as e:
                    speak("Cannot find the song")


            elif "game" in query:
                webbrowser.open("https://www.friv.com/")
                
            elif "exit" in query:
                speak("Good Bye")
            else :
                url = 'https://api.openai.com/v1/completions'
                headers = {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJqYWNrLmJoYXJhdGgzMEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJ1c2VyX2lkIjoidXNlci1LelVPUk96U0JYQmwxRzdFU2RyaTNKNm0ifSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA1NDQ0MDUzNzg4NDM1MDEwMzAyIiwiYXVkIjpbImh0dHBzOi8vYXBpLm9wZW5haS5jb20vdjEiLCJodHRwczovL29wZW5haS5vcGVuYWkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY4NTY5NzI2NSwiZXhwIjoxNjg2OTA2ODY1LCJhenAiOiJUZEpJY2JlMTZXb1RIdE45NW55eXdoNUU0eU9vNkl0RyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgbW9kZWwucmVhZCBtb2RlbC5yZXF1ZXN0IG9yZ2FuaXphdGlvbi5yZWFkIG9yZ2FuaXphdGlvbi53cml0ZSJ9.AXxpT9aIlek1rlKicoBkjwlPdCL92QbwjCPm-7bg1aeL-KAI3pTDTgVSux1UvZaigaqEnfZLa1qK2cx24cJvhGBFt_fz288C9OgKHOyZZVSirIe7iF6uuNS73sKLShSceepvisrqIw6ZhZKGdIq7cAIu7xFgibB2VulomJ4jA3qpJqsh_HbtogRKPS5BVz46ixU3tDIoxLAbXD1SJZsjbBbTd2zOT8fuWNxTAV8P6p_tlIRRLShd15m8K2PRNvGL-00uumWSMr0CNcUW7hBhahRhJrd4NcIPD29F-FBImbP0HvTKZbtib6tm7loXCJ-CYpwoDw9lnH8vl_ztPQ4Cfg'
                        }   

                data = { "model": "text-davinci-003", "prompt": query, "max_tokens": 7, "temperature": 0, "top_p": 1, "n": 1, "stop": "\n" }

                response = requests.post(url, headers=headers, json=data)
                if response.status_code == 200:
                    result = response.json()
                    speak(result['choices'][0]['text'])
                else:
                    response = requests.get(f'https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey=587b63d3323447aa93470e19bf73314c')
                    data = response.json()

                    if response.status_code == 200 and data['status'] == 'ok':
                        articles = data['articles']
                        i = 1
                        for article in articles:
                            title = article['title']
                            content = article['content']
                            speak("As per the article" + title + "describes"+ select_100_words(content))
                            i = i +1
                            if (i == 3):
                                break
                            # Process the article data as needed
                    else:
                        speak('Error occurred while fetching news:' + data['message'])
        return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)
