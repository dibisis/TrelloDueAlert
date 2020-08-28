import datetime
import logging

import telegram
from dateutil.relativedelta import relativedelta
from trello import TrelloClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('./result.log')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

client = TrelloClient(
    api_key='trello_apikey',
    api_secret='api_api_secret',
    token='trello_auth_token',
)
result = "=24hour================================================\n"
overresult = "=over due================================================\n"
all_boards = client.list_boards()

n = 1 # board_id_sequence
for temp_card in all_boards[n].open_cards():
    # if (temp_card.list_id == '534b2b07ba315558427390eb'):
    #     continue

    card_due = temp_card.due_date

    if (card_due):
        temp_delta = relativedelta(card_due.replace(tzinfo=None), datetime.datetime.utcnow())
        if temp_delta.days < 1 and temp_delta.hours > 0:
            result = result + temp_card.name + "\n" + temp_card.short_url + "\n\n"
        elif temp_delta.hours < 0:
            overresult = overresult + temp_card.name + "\n" + temp_card.short_url + "\n\n"

result = result + overresult

bot = telegram.Bot(token='telegrambot_token')

chat_id = 'telegram_chatroom_id'
bot.send_message(chat_id=chat_id, text=result)

logger.info('chat_id: %s', chat_id)
logger.info('Return result: %s', result)
