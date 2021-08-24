import uuid
import dataclasses

"""
@dataclasses.dataclass
  init (default : True) -  __init__() メソッドが生成される
  repr (default : True) - Room(code=UUID('23153748-dae2-4d8d-aa29-fae44136ceba'), size=200, price=10, longitude=-0.09998975, latitude=51.75436293) のような文字列が生成できるようになる
  eq (default : True) - クラスのフィールドからなるタプルを比較する
  order (default : False) - __lt__()、__le__()、__gt__()、__ge__() メソッドが生成される　フィールドタプルの比較を行う
  unsafe_hash (default : False) - __hash__() メソッドが生成される。dict や set のようなハッシュ化されたコレクションにオブジェクトを追加するときに使われる。
  frozen (default : False) - フィールドへの代入は例外を生成します。カプセル化？
  上記のことが行われる

　通常より短くかけたりするので、データの箱ってことを示したいときに使用するのがよい
"""
@dataclasses.dataclass
class Room:
    code: uuid.UUID
    size: int
    price: int
    longitude: float
    latitude: float

    # インスタンス化しなくても呼び出せる関数化　第一引数はclsの決まり
    @classmethod
    def from_dict(cls, d):
        # 複数のキーワード引数を辞書として受け取る
        return cls(**d) 

    def to_dict(self):
        # 辞書型にする dataclass使うならよく使用されるメソッド
        return dataclasses.asdict(self)
