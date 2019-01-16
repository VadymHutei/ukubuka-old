from db import DB

class Test():

    def __init__(self):
        self.view = 'test view'

    def test(self):
        db = DB()
        # query = "SELECT * FROM ku_setting WHERE `property` = 'baz'"
        query = "INSERT INTO ku_setting (`property`, `value`) VALUES (%s, %s)"
        # query = "DELETE FROM ku_setting"
        print(db.exec(query, 'qwe', 'asd'))
        return 'd'