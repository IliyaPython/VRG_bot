"""работы с чатом через gigachain"""

import os

from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models import GigaChat

KEY = os.environ["Api keys"]

# import g4f

# g4f.debug.logging = False  # disable logging
# g4f.check_version = False  # Disable automatic version checking
# print(g4f.version)  # check version
# print(g4f.Provider.Ails.params)  # supported args

# user_input = input("Your request: ")
# # response = g4f.ChatCompletion.create(
# #             messages=[{"role": "user", "content": user_input}],
# #             model=g4f.models.gpt_4,
# #         )

# response = g4f.ChatCompletion.create(
#     model=g4f.models.default,
#     messages=[{"role": "user", "content": "Hello"}],
#     proxy="socks5://user:pass@host:port",
#     # or
# )

# print(f"Result:", response)
# {"role": "system", "content": "Ты злой, эгоистичный человек, грубиян и ненавидишь людей"}

# Авторизация в сервисе GigaChat
chat = GigaChat(credentials=KEY, model="GigaChat", verify_ssl_certs=False)
