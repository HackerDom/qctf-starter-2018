import re
import os

from telegram.ext import Updater, MessageHandler, BaseFilter


def getenv(name):
    value = os.getenv(name)
    if value is None:
        raise ValueError('Please provide the environment variable {}'.format(name))
    return value


FLAG_RE = re.compile(r'QCTF_?{?(\w+)}?')
TOKEN = getenv('TOKEN')
ADMIN_CHAT_ID = int(getenv('ADMIN_CHAT_ID'))
FLAGS_PATH = getenv('FLAGS_PATH')


def read_flag_patterns(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    lines = [l.strip() for l in content.split('\n')]
    lines = list(filter(bool, lines))

    flag_patterns = []
    for line in lines:
        match = FLAG_RE.match(line)
        if not match:
            raise ValueError('Invalid flag: {}'.format(line))
        flag_patterns.append(match.group(1))
    return flag_patterns


class RegexFilter(BaseFilter):
    def __init__(self, regex):
        self.regex = regex

    def filter(self, message):
        return message.text and self.regex.search(message.text)


def process_cheater(bot, update):
    message = update.message
    if message.chat.id == ADMIN_CHAT_ID:
        return
    update.message.forward(ADMIN_CHAT_ID)
    update.message.delete()


def main():
    flag_patterns = read_flag_patterns(FLAGS_PATH)
    cheater_re = re.compile('(' + '|'.join(map(re.escape, flag_patterns)) + ')')

    updater = Updater(token=TOKEN)
    updater.dispatcher.add_handler(
        MessageHandler(RegexFilter(cheater_re), process_cheater))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
