TITLE = 'Майнинг криптовалюты в браузерах достиг нового уровня'

STATEMENT = '''
Многие сайты скрывают, что наживаются на своих пользователях, используя скрытый браузерный майнинг. 
Но появился [сайт](https://browser-mining.contest.qctf.ru), который предлагает вам самим получить немного монет. 
Вам даже делать ничего не нужно. Просто зарегестрируйтесь и начните зарабатывать!

(Не используйте IE и выключите AdBlock для корректной работы)
'''

def generate(context):
    return TaskStatement(TITLE, STATEMENT)