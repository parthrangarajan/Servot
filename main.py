import os
import discord
import requests, json
import random
from replit import db 
from jokeapi import Jokes
import numpy as np
from keepalive import keep_alive


# creating connection to discord
client=discord.Client()

sad_words=["sad","depressed","unhappy","angry","death","suicide","guilt","empty","hopeless","sorrowful","dejected","regretful","downcast","miserable","downhearted","down","despondent","despairing","disconsolate","out of sorts","grief","heartache","heartbreak","hopelessness","melancholy","mourning","poignancy","sorrow"]

starter_encouraging_msg=["Don't give up","Feel Alive","Cheer up!","You are an amazing person","It's a great day to be happy!","You're almost there!","Have faith in yourself"]




# helper function
def get_quote():
  response= requests.get("https://zenquotes.io/api/random")


  # converting into json now
  json_data=json.loads(response.text)

  quote= json_data[0]["q"]+" -"+json_data[0]["a"]
  return(quote)



def get_encouragement():
  response= requests.get("https://type.fit/api/quotes")

  json_data= json.loads(response.text)
  quote_ind=np.random.choice(range(0, 1644))
  encouragement= json_data[quote_ind]["text"]+" -"+json_data[quote_ind]["author"]
  return(encouragement)



# registering an event
@client.event
# will be called when bot is ready
async def on_ready():
  print("We have loggied in as : {0.user}".format(client))
  # print(type(db["encouragements"]))


@client.event
# on recieving a message
async def on_message(msg):
  
  if msg.author == client.user:
    return

  
  if msg.content.startswith("$hello"):
    await msg.channel.send("Hey! I'm Servot. These are my features :\n \n 1>Welcome! Key in $hello \n 2>Where are my manners? Try $introduce! \n 3>Need some inspiration? Use $inspire. \n 4>Want a good laugh? Type in $joke.\n 5>Oh! Don't I will also try my best to encourage you to move forward\n \n \u00A9ParthRangarajan @2021")


  
  if msg.content.startswith("$introduce"):
    await msg.channel.send("Hey! I'm so happy you are here. I'm a service bot who is here to inspire and encourage you. \n")


  if msg.content.startswith("$inspire"):
    quote= get_quote()
    await msg.channel.send(quote)


  if msg.content.startswith("$joke"):
    page = requests.get('https://official-joke-api.appspot.com/random_joke')
    jokesource = json.loads(page.content)
    joke = jokesource['setup']
    await msg.channel.send(joke)
    answer = jokesource['punchline']
    await msg.channel.send(answer)
    

  # Encouraging with user recommendations
  
  options = starter_encouraging_msg
  if "encouragements" in db.keys():
    for i,row in enumerate(db["encouragements"]):
      options+=db["encouragements"]




  if any(word in msg.content for word in sad_words):
    insp_quote=get_encouragement()
    await msg.channel.send(insp_quote)
  

  
  
'''
  if msg.content.startswith("$new"):
    encouraging_message=msg.content.split("$new",1)[1]
    update_encouragements(encouraging_message)

    await msg.channel.send("New encouraging message added.")

  if msg.content.startswith("$delete"):
    encouragements=[]
    if "encouragements" in db.keys():
      index= int(msg.content.split("$del",1)[1])
      del_encouragements(index)
      encouragements=db["encouragements"]

    await msg.channel.send(encouragements)

'''


# to run the bot
keep_alive()
client.run(os.getenv("SERVEBOT_TOKEN"))
