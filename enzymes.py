import db


class Enzymes_List():
    def __init__(self, enzymes_id):
        connection, cursor = db.connect_to('enzymes.db')
        response = cursor.execute("SELECT * FROM enzymes WHERE id=?", (enzymes_id, ))
        data = response.fetchall()
        if not data:
            self.is_search = False
        else:
            self.is_search = True
            self.enzymes_dict = {}
            for index, enzymes in enumerate(data):
                self.enzymes_dict.update({index: (enzymes[0], enzymes[1], enzymes[2], enzymes[3])})
            self.enzymes_list = [Enzymes(id, name, amount, volume)
                                 for id, name, amount, volume in self.enzymes_dict.values()]

    def prepare_to_send(self):
        enzymes_list = []
        for enzymes in self.enzymes_list:
            enzymes_list.append(f'Реактив {enzymes.name}, ID: {enzymes.id}\nКоличество: {enzymes.amount} – {enzymes.volume}')
        return enzymes_list


class Enzymes():
    def __init__(self, id, name, amount, volume):
        self.id = id
        self.name = name
        self.amount = amount
        self.volume = volume
