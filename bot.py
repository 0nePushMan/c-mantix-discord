import os
import discord
import requests
import time
from dotenv import load_dotenv
load_dotenv()

token = os.environ['token']


class MyClient(discord.Client):
    hot = []
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.channel.id == 994154345778126858 or message.channel.id == 994184781573140493:
            first = message.content.split()[0].lower()

            # async def checkHot(score):
            #     if len(MyClient.hot) > 0:
            #         for index, value in MyClient.hot:
            #             if value[1] < score:
            #                 MyClient.hot[index] = [first, score, message.id]
            #                 return True
            #             else:
            #                 return False
            #     else:
            #         MyClient.hot.append([first, score, message.id])
            #         return True

            async def temperature(score):
                if score <= 0:
                    return '🧊'
                if score <= 20:
                    return '🥶'
                if score <= 30:
                    return '😎'
                if score <= 40:
                    return '🥵'
                else:
                    return '🔥'

            async def req_word(word):
                r = requests.post(
                    "https://cemantix.herokuapp.com/score", data={"word": first}).json()
                print(r)
                if "error" in r and "tapez trop vite" in r["error"]:
                    time.sleep(.2)
                    return req_word(word)
                if "error" in r:
                    return False
                if "score" in r:
                    if r["score"] == 1:
                        return True
                    else:
                        return r['score'] * 100

            score = await req_word(first)
            if score == True:
                await message.channel.send(message.author.name + ' a trouvé le mot ' + first)
            if score == False:
                await message.channel.send('Je ne connais pas le mot ' + first)
            else:
                temp = await temperature(score)
                await message.channel.send(message.author.name + ' le mot ' + first + ' a la température de ' + str(round(score, 2)) + '°C  ' + temp)


client = MyClient()
client.run(token)
