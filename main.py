import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv
import os
import googletrans
from discord import Embed
import asyncio
import azure.functions as func

# Load environment variables from .env file
load_dotenv()

# Initialize the translator
translator = googletrans.Translator()

flag_emoji_dict = {
    "🇺🇸": "en",
    "🇩🇪": "de",
    "🇫🇷": "fr",
    "🇪🇸": "es",
    "🇮🇹": "it",
    "🇵🇹": "pt",
    "🇷🇺": "ru",
    "🇦🇱": "sq",
    "🇸🇦": "ar",
    "🇧🇦": "bs",
    "🇧🇬": "bg",
    "🇨🇳": "zh-CN",
    "🇭🇷": "hr",
    "🇨🇿": "cs",
    "🇩🇰": "da",
    "🇪🇪": "et",
    "🇫🇮": "fi",
    "🇬🇷": "el",
    "🇭🇺": "hu",
    "🇮🇩": "id",
    "🇮🇳": "hi",
    "🇮🇪": "ga",
    "🇮🇸": "is",
    "🇮🇱": "he",
    "🇯🇵": "ja",
    "🇰🇷": "ko",
    "🇱🇻": "lv",
    "🇱🇹": "lt",
    "🇲🇹": "mt",
    "🇲🇪": "sr",
    "🇳🇱": "nl",
    "🇳🇴": "no",
    "🇵🇰": "ur",
    "🇵🇱": "pl",
    "🇵🇹": "pt",
    "🇷🇴": "ro",
    "🇷🇸": "sr",
    "🇸🇦": "ar",
    "🇸🇰": "sk",
    "🇸🇮": "sl",
    "🇸🇪": "sv",
    "🇹🇭": "th",
    "🇹🇷": "tr",
    "🇹🇼": "zh-TW",
    "🇺🇦": "uk",
    "🇻🇳": "vi",
    "🇻🇦": "la"
}

# Fetch the token from the environment variable
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents and bot setup
intents = discord.Intents.all()
prefix = './'
bot = commands.Bot(command_prefix=prefix, intents=intents)

# Event handler
@bot.event
async def on_reaction_add(reaction, user):
    if reaction.emoji in flag_emoji_dict:
        lang_code = flag_emoji_dict[reaction.emoji]
        message = reaction.message
        
        try:
            detected_lang = translator.detect(message.content)
            translated_message = translator.translate(message.content, dest=lang_code).text
            pronunciation_message = translator.translate(message.content, dest=lang_code).pronunciation

            print(f"Detected language: {detected_lang.lang}, Confidence: {detected_lang.confidence}")

            confidence = detected_lang.confidence if detected_lang.confidence is not None else 0
            confidence_percentage = confidence * 100

            embed = Embed(title='Translated Text', description=f'{translated_message}\n\nTranslated by: {user.mention}', color=0x00ff00)
            translated_message_response = await reaction.message.channel.send(content=f'{user.mention}', embed=embed)
            
            await reaction.message.remove_reaction(reaction.emoji, user)
            await asyncio.sleep(30)
            await translated_message_response.delete()

        except Exception as e:
            print(f"Error translating message: {e}")

# Azure Function entry point
async def main(req: func.HttpRequest) -> func.HttpResponse:
    await bot.start(TOKEN)
    return func.HttpResponse("Bot is running", status_code=200)
