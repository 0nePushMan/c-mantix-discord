import os
import discord
import requests
import time
from datetime import date
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

            async def clearChannel():
                await message.channel.purge()
                return await message.channel.send('Le mot du ' + str(date.today()) + ' était ' + MyClient.found)

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
                        MyClient.found = first
                        return True
                    else:
                        return r['score'] * 100

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

            if message.content == '/clear':
                await clearChannel()
                return

            score = await req_word(first)

            if score == True:
                await message.delete()
                if len(MyClient.founders) > 0:
                    for user in MyClient.founders:
                        if user != message.author.id:
                            MyClient.founders.append(message.author.id)
                else:
                    MyClient.founders.append(message.author.id)
                if len(MyClient.founders) == 2:
                    await clearChannel()
                await message.channel.send(message.author.name + ' a trouvé le mot du jour 🔥🔥🔥')
            elif score == False:
                await message.channel.send('Je ne connais pas le mot ' + first)
            else:
                temp = await temperature(score)
                await message.channel.send(message.author.name + ' le mot ' + first + ' a une température de ' + str(round(score, 2)) + '°C  ' + temp)


client = MyClient()
client.run(token)
