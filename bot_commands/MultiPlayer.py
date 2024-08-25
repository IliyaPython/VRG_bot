from ..classes import Room


async def get_users_in_room(room: Room):
    return room["users"]


async def room_by_user(user_id: int, rooms: dict[str, list]) -> dict:
    """Асинхронная функция для поиска комнаты по ID указаного пользователя.
    Перебирая комнаты, идёт проверка на вхождение пользователя в комнату.
        Если входит (True), возвращается словарь комнаты."""
    for room in rooms.keys():
        room = rooms[room]
        if user_id in room["users"]:
            return room
