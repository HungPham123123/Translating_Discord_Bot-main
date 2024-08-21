import googletrans

# Create a Translator object
translator = googletrans.Translator()

# Get the list of supported languages
supported_languages = googletrans.LANGUAGES

# Print the supported languages
for lang_code, lang_name in supported_languages.items():
    print(f"{lang_code}: {lang_name}")
