import db


class Enzymes_List():
    def __init__(self, name):
        _, cursor = db.connect_to("enzymes.db")
        response = cursor.execute("SELECT * FROM enzymes WHERE LOWER(name)=?", (name.lower(), ))
        data_response = response.fetchall()
        if not data_response:
            self.is_search = False
        else:
            self.is_search = True
            self.enzymes_list = []
            for enzymes in data_response:
                self.enzymes_list.append(Enzymes(enzymes[0], enzymes[1], enzymes[2], enzymes[3]))
    
    def _save_enzymes(self, amount, name, volume):
        connection, cursor = db.connect_to("enzymes.db")
        if amount < 1:
            cursor.execute("DELETE FROM enzymes WHERE LOWER(name)=? AND LOWER(volume)=?",
                            (name.lower(), volume.lower()))
        else:
            cursor.execute("UPDATE enzymes SET amount=? WHERE LOWER(name)=? AND LOWER(volume)=?",
                            (amount, name.lower(), volume.lower()))
        connection.commit()
        connection.close()
        return True

    def edit_enzymes(self, amount, volume):
        for enz in self.enzymes_list:
            try:
                if enz.volume.lower() == volume:
                    enz.amount -= int(amount)
            except (IndexError, TypeError):
                return False
            else:
                return self._save_enzymes(enz.amount, enz.name, enz.volume)
    
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