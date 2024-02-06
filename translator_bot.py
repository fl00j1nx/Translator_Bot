import discord
from googletrans import Translator
import os.path
import random

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SPREADSHEET_ID = "13-Hfwtlb_ddyEQ3-xtXeBIvPmZesbR9ZqisPbq6d2_A" 

bot_token = 'MTE5NTg0MzIyODg2MDE2MjE5NA.GrnCZs.eo9Kc25fOQBt1-Jg6TViPFmCDJ1wLjtrQRk37w'
translator = Translator()

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
client = discord.Client(intents=intents)

languages, wordsLeft = ['es'], list(range(1, 31))
toggle, gameOn, difficultySet, guessMode, answerCorrect, GG = True, False, False, False, False, False
difficulty = word = answer = ""
gameLanguage = ""
points = -1
authorID = 0

langDict = {
    'afrikaans': 'af',
    'albanian': 'sq',
    'amharic': 'am',
    'arabic': 'ar',
    'armenian': 'hy',
    'azerbaijani': 'az',
    'basque': 'eu',
    'belarusian': 'be',
    'bengali': 'bn',
    'bosnian': 'bs',
    'bulgarian': 'bg',
    'catalan': 'ca',
    'cebuano': 'ceb',
    'chichewa': 'ny',
    'chinese': 'zh-cn',
    'corsican': 'co',
    'croatian': 'hr',
    'czech': 'cs',
    'danish': 'da',
    'dutch': 'nl',
    'english': 'en',
    'esperanto': 'eo',
    'estonian': 'et',
    'filipino': 'tl',
    'finnish': 'fi',
    'french': 'fr',
    'frisian': 'fy',
    'galician': 'gl',
    'georgian': 'ka',
    'german': 'de',
    'greek': 'el',
    'gujarati': 'gu',
    'haitian creole': 'ht',
    'hausa': 'ha',
    'hawaiian': 'haw',
    'hebrew': 'he',
    'hindi': 'hi',
    'hmong': 'hmn',
    'hungarian': 'hu',
    'icelandic': 'is',
    'igbo': 'ig',
    'indonesian': 'id',
    'irish': 'ga',
    'italian': 'it',
    'japanese': 'ja',
    'javanese': 'jw',
    'kannada': 'kn',
    'kazakh': 'kk',
    'khmer': 'km',
    'korean': 'ko',
    'kurdish-kurmanji': 'ku',
    'kyrgyz': 'ky',
    'lao': 'lo',
    'latin': 'la',
    'latvian': 'lv',
    'lithuanian': 'lt',
    'luxembourgish': 'lb',
    'macedonian': 'mk',
    'malagasy': 'mg',
    'malay': 'ms',
    'malayalam': 'ml',
    'maltese': 'mt',
    'maori': 'mi',
    'marathi': 'mr',
    'mongolian': 'mn',
    'myanmar': 'my',
    'nepali': 'ne',
    'norwegian': 'no',
    'odia': 'or',
    'pashto': 'ps',
    'persian': 'fa',
    'polish': 'pl',
    'portuguese': 'pt',
    'punjabi': 'pa',
    'romanian': 'ro',
    'russian': 'ru',
    'samoan': 'sm',
    'scots gaelic': 'gd',
    'serbian': 'sr',
    'sesotho': 'st',
    'shona': 'sn',
    'sindhi': 'sd',
    'sinhala': 'si',
    'slovak': 'sk',
    'slovenian': 'sl',
    'somali': 'so',
    'spanish': 'es',
    'sundanese': 'su',
    'swahili': 'sw',
    'swedish': 'sv',
    'tajik': 'tg',
    'tamil': 'ta',
    'telugu': 'te',
    'thai': 'th',
    'turkish': 'tr',
    'ukrainian': 'uk',
    'urdu': 'ur',
    'uyghur': 'ug',
    'uzbek': 'uz',
    'vietnamese': 'vi',
    'welsh': 'cy',
    'xhosa': 'xh',
    'yiddish': 'yi',
    'yoruba': 'yo',
    'zulu': 'zu'
}

creds = None
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())
service = build("sheets", "v4", credentials = creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = (
    sheet.values()
    .get(spreadsheetId = SPREADSHEET_ID, range = "Palabras!A:F")
    .execute()
)
sp_values = result.get("values", [])
result = (
    sheet.values()
    .get(spreadsheetId = SPREADSHEET_ID, range = "Korean!A:F")
    .execute()
)
kr_values = result.get("values", [])

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

#/Users/lemons/Documents/informatica/translator_bot
@client.event
async def on_message(message):
    global languages, toggle, gameOn, difficultySet, sp_values, difficulty, word, guessMode, answer, points, answerCorrect, wordsLeft, GG, authorID, gameLanguage

    if message.author == client.user:
        return
    

    msgSplit = message.content.split(" ")
    command = msgSplit[0]
    
    if (command == "$toggle"):
        toggle = not toggle
        if (toggle):
            await message.channel.send("we back")
        else:
            await message.channel.send("we out")
    
    elif (toggle):
        if (command == "$setLang"):
            languages = []
            for language in msgSplit[1:]:
                try:
                    languages.append(langDict[language])
                    await message.channel.send(
                        f'Added destination language: {language}')
                except KeyError:
                    await message.channel.send(
                        f'{language} is not a valid language')
        
        elif (command == "$help"):
            await message.channel.send(translator.translate("$toggle = turn on/off bot temporariliy \n$setLang [lang1] [lang2]... = sets target language(s) of translated messages \n$play = test your vocab!", dest='en').text)
        
        #access Spanish words frequency Google Sheet
        elif (authorID == 0 and command == "$play"):
            authorID = message.author.id
            gameOn, toggle = True, False
            await message.channel.send("Enter difficulty level (easy, medium, hard) and language (sp, kr): \ne.g. easy sp")

        else:
            for lang in languages:
                translated_text = translator.translate(message.content, dest=lang).text
                await message.channel.send(translated_text)
    
    #game
    elif (gameOn and message.author.id == authorID):
        difficultyDict = {"easy": 0, "medium": 1, "hard": 2}
        if (msgSplit[0] == "$quit"):
            gameOn, difficultySet, toggle = False, False, True
            authorID = 0
            await message.channel.send("Game has been exited")

        elif (not difficultySet):
            if (len(msgSplit) != 2 or msgSplit[0] not in difficultyDict or msgSplit[1] != "sp" and msgSplit[1] != "kr"):
                await message.channel.send('Specify difficulty and language')
            else:
                difficulty = msgSplit[0]
                gameLanguage = msgSplit[1]
                difficultySet = True
                await message.channel.send("Press a key to start")

        else:
            #checks if list of possible answers contains what user messaged; posAnswers = array of possible answers
            posAnswers = answer.split(" ")
            for i in range(len(posAnswers)):
                if (posAnswers[i] == msgSplit[0].lower()):
                    answerCorrect = True
                    if (len(wordsLeft) == 0):
                        await message.channel.send("Wow! You know all 30 words for this difficulty level! GG")
                        gameOn, difficultySet, toggle, guessMode, answerCorrect = False, False, True, False, False, True
                        GG = True
                        wordsLeft = list(range(1, 31))
                        points = -1
                        authorID = 0
            if (GG):
                GG = False
            elif (not guessMode or answerCorrect):
                row = random.randint(0, len(wordsLeft) - 1)
                if (gameLanguage == "sp"):
                    word = sp_values[wordsLeft[row]][difficultyDict[difficulty]]
                    answer = sp_values[wordsLeft[row]][difficultyDict[difficulty] + 3]
                elif (gameLanguage == "kr"):
                    word = kr_values[wordsLeft[row]][difficultyDict[difficulty]]
                    answer = kr_values[wordsLeft[row]][difficultyDict[difficulty] + 3]
                wordsLeft.pop(row)
                await message.channel.send('What is the meaning of ' + '"' + word + '"? (type one word)')
                points += 1
                guessMode, answerCorrect = True, False
            else:
                gameOn, difficultySet, toggle, guessMode, answerCorrect = False, False, True, False, False
                authorID = 0
                await message.channel.send('Oh no! The correct answer was ' + printAnswers(answer.split(" ")) + '\nYou answered ' + str(points) + ' in a row correct')
                points = -1
                wordsLeft = list(range(1, 31))

#prints answers in "a, b, or c" format
def printAnswers(ans):
    if (len(ans) == 2):
        return '"' + ans[0] + '"' + " or " + '"' + ans[1] + '"'
    res = ""
    for i in range(len(ans) - 1):
        res += '"' + ans[i] + "," + '"'
    if (len(ans) > 1):
        return res + "or " + '"' + ans[len(ans) - 1] + '"'
    return res + '"' + ans[len(ans) - 1] + '"'

# Discord Bot
client.run(bot_token)