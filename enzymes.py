import db


class Enzymes_List():
    def __init__(self, id):
        connection, cursor = db.connect_to("enzymes.db")
        response = cursor.execute("SELECT * FROM enzymes WHERE id=?", (id, ))
        data_response = response.fetchall()
        if not data_response:
            self.is_search = False
        else:
            self.is_search = True
            self.enzymes_list = []
            for enzymes in data_response:
                self.enzymes_list.append(Enzymes(enzymes[0], enzymes[1], enzymes[2], enzymes[3]))
    
    def get_list_enzymes(self):
        list_for_join = []
        for enzymes in self.enzymes_list:
            list_for_join.append(f'Реактив {enzymes.name}, ID: {enzymes.id}, количество: {enzymes.amount} – {enzymes.volume}')
        return '\n'.join(list_for_join)





class Enzymes():
    def __init__(self, id, name, amount, volume):
        self.id = id
        self.name = name         
        self.amount = amount
        self.volume = volume


search_enzymes = Enzymes_List('R005')
search_enzymes.get_list_enzymes()