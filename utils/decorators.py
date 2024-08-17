from typing import Union
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

async def send_params(func, **params):
    """Функция-декоратор. Дополняет функцию необходимыми аргументами.

    :param func: декорируемая функция. Обязательно.
    :param params: дополнительные параметры, нужные для функции. Если их нет, возвращается """
    if params:
        for key, value in params:
            if value:
                setattr(func, key, value)
                
    return func
async def send_params_to_FSM(message: Message,
                            state: FSMContext,
                            data: Union[any, dict] = None):
    print("ONE TIME")
    #print(handler)
    print(message)
    print(state)
    #setattr(handler, "message", message)
    #setattr(handler, "state", state)
    #setattr(handler, "data", data)
    return handler