import tweepy
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Twitter API credentials
consumer_key = 
consumer_secret = ''
access_token = '
access_token_secret = ''

# Telegram Bot Token

# Keywords to monitor
keywords = ['check-in', 'pool']

# Initialize the Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitter_api = tweepy.API(auth)

# Initialize the Telegram Bot
updater = Updater(token=telegram_token, use_context=True)
dispatcher = updater.dispatcher

# Store user IDs for future notifications
subscribers = set()

# Command to start the bot
def start(update, context):
    update.message.reply_text("Bot is running. Use /subscribe to receive notifications.")

# Command to subscribe to notifications
def subscribe(update, context):
    user_id = update.message.chat_id
    subscribers.add(user_id)
    update.message.reply_text("You are now subscribed to notifications.")

# Command to unsubscribe
def unsubscribe(update, context):
    user_id = update.message.chat_id
    if user_id in subscribers:
        subscribers.remove(user_id)
        update.message.reply_text("You have been unsubscribed from notifications.")
    else:
        update.message.reply_text("You are not currently subscribed.")

# Function to check for new tweets and send notifications
def check_tweets(context):
    for keyword in keywords:
        tweets = twitter_api.user_timeline(screen_name='1337FIL', count=10, tweet_mode='extended')
        for tweet in tweets:
            if any(keyword in tweet.full_text.lower() for keyword in keywords):
                for user_id in subscribers:
                    context.bot.send_message(chat_id=user_id, text=f"New tweet from 1337FIL: {tweet.full_text}")

# Timer to check for new tweets every 5 minutes
updater.job_queue.run_repeating(check_tweets, interval=300, first=0)

# Register command handlers
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('subscribe', subscribe))
dispatcher.add_handler(CommandHandler('unsubscribe', unsubscribe))

# Start the bot
updater.start_polling()
updater.idle()
