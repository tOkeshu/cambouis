from cambouis.bot import bot

@bot.on('!len (.*)')
def length(event, message):
    bot.irc.reply(event, str(len(message)))

