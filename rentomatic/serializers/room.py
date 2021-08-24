import json


class RoomJsonEncoder(json.JSONEncoder):
    def default(self, o):
        """
        o = Room(
            code=UUID('b60cc3d0-82f3-4365-b320-302838c93fad'), 
            size=200, 
            price=10, 
            longitude=-0.09998975, 
            latitude=51.75436293
        )
        という形式になってしまうので、codeを文字列に変換する
        """
        try:
            to_serialize = {
                "code": str(o.code),
                "size": o.size,
                "price": o.price,
                "latitude": o.latitude,
                "longitude": o.longitude,
            }
            return to_serialize
        except AttributeError:  # pragma: no cover
            return super().default(o)
