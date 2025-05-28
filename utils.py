from textblob import TextBlob

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity < -0.2:
        return "Sad"
    elif polarity > 0.2:
        return "Happy"
    else:
        return "Neutral"

def get_suggestion(mood):
    if mood == "Sad":
        return "You seem a bit down. Try going for a walk or talk to a loved one."
    elif mood == "Happy":
        return "You're doing great! Keep it up and enjoy your day."
    else:
        return "A balanced day! Maybe unwind with a book or some music."
