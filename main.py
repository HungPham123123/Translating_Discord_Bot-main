import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv
import os
import googletrans
from discord import Embed
import asyncio  # Import asyncio for sleep function

translator = googletrans.Translator()

# Create a dictionary of flag emojis and their corresponding language codes
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

# For a more secure, we loaded the .env file and assign the token value to a variable 
load_dotenv(".env")
TOKEN = os.getenv("TOKEN")

# Intents are permissions for the bot that are enabled based on the features necessary to run the bot.
intents = discord.Intents.all()

# Command prefix is setup here, this is what you have to type to issue a command to the bot
prefix = './'
bot = commands.Bot(command_prefix=prefix, intents=intents)

#------------------------------------------------Events------------------------------------------------------#

@bot.event
async def on_reaction_add(reaction, user):
    # Check if the reaction is a flag emoji
    if reaction.emoji in flag_emoji_dict:
        lang_code = flag_emoji_dict[reaction.emoji]
        message = reaction.message
        
        try:
            # Translate the message to the desired language
            detected_lang = translator.detect(message.content)
            translated_message = translator.translate(message.content, dest=lang_code).text
            pronunciation_message = translator.translate(message.content, dest=lang_code).pronunciation
            
            # Debugging output
            print(f"Detected language: {detected_lang.lang}, Confidence: {detected_lang.confidence}")

            # Handle cases where confidence might be None
            confidence = detected_lang.confidence if detected_lang.confidence is not None else 0
            confidence_percentage = confidence * 100

            # Create the embed with translator information
            embed = Embed(title='Translated Text', description=f'{translated_message}\n\nTranslated by: {user.mention}', color=0x00ff00)
            translated_message_response = await reaction.message.channel.send(content=f'{user.mention}', embed=embed)
            
            # Remove the reaction emoji
            await reaction.message.remove_reaction(reaction.emoji, user)

            # Delete the translated message after 30 seconds
            await asyncio.sleep(30)  # Use asyncio.sleep instead of discord.utils.sleep_until
            await translated_message_response.delete()

        except Exception as e:
            print(f"Error translating message: {e}")

# Run the bot
bot.run(TOKEN)
