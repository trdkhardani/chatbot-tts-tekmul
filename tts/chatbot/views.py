from django.shortcuts import render
from django.http import HttpResponse
# from django.http import FileResponse
from django.shortcuts import render
from django.http import HttpResponse
import speech_recognition as sr 
import os 
import time
from pygame import mixer
from gtts import gTTS
from datetime import datetime
import openai

# Create your views here.
def index(request):
    # return to template
    context = {'botname': 'Mel'}
    # views.py
openai.api_key = "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" # Insert your OpenAI Secret Key here
openai.Model.list()

r = sr.Recognizer()
greet = "Hello! I'm Mel. Nice to meet you!"
text = f"\nMel:{greet}\nHuman:"
newText = ""
bot_name = "Mel"

def playaudio(text): #Text-to-speech
    ttsObj = gTTS(text=text, lang='en', slow=False)
    date_string = datetime.now().strftime("%d%m%Y%H%M%S")
    audiofile = "voice"+date_string+".mp3"
    ttsObj.save(audiofile)
    mixer.init()
    mixer.music.load(audiofile)
    mixer.music.play()
    while mixer.music.get_busy():
        pass
    mixer.music.unload()
    os.remove(audiofile)

def chatRes(text): #GPT-3 Model Using Davinci
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=text,
      temperature=0.9,
      max_tokens=2000,
      top_p=1,
      frequency_penalty=0.0,
      presence_penalty=0.6,
      stop=["Human:", "Mel:"]
    )
    return response

playaudio(greet)

# If any of these words are not spoken, the program loop will not stop
sampleDone = ["see you", "goodbye", "farewell", "we will meet again", "see you soon", "we'll meet again", "gotta go", "have to go"]

def index(request):
    global newText, text
    context = {}
    if request.method == 'POST':
        newText = request.POST.get('text_input')
        text = text + f"{newText}\nMel:"
        resp = chatRes(text).choices[0].text
        playaudio(resp)
        text = text + f"{resp}\nHuman:"
    elif request.method == 'GET':
        newText = ""
        text = f"\nMel:{greet}\nHuman:"
    context['text'] = text
    return render(request, 'index.html', context)

def speech_to_text(request):
    global newText
    with sr.Microphone() as source:
        print("================= Say something ===================")
        audio_data = r.record(source, duration=200)
        print("Recognizing...")
        newText = r.recognize_google(audio_data)
        return HttpResponse(newText)


    # return render(request, 'index.html', context)