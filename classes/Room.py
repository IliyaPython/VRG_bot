import uuid
class Room:
    def __init__(self, owner_id):
        unic_id = uuid.uuid1()
        self.data = {
            "uid": unic_id,
            "users": [owner_id],
            "owner": owner_id,
            "banned": []
        }
