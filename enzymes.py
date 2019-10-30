import db


connection, cursor = db.connect_to('enzymes.db')


class Enzymes():
    def __init__(self, enzymes_id):
        self.id = enzymes_id
        response = cursor.execute("SELECT * FROM enzymes WHERE id=?", (self.id, ))
        data = response.fetchall()
        self.name = data[0][1]
        self.amount = data[0][2]
        self.volume = data[0][3]