from collections import defaultdict
import pickle

class Database():
    def __init__(self) -> None:
        self.db = None
        
    def storeData(self):
        """
        It opens db.pkl file in write binary mode, and then dumps our db to the file.
        """
        with open('./db.pkl', 'wb') as dbfile:
            pickle.dump(self.db, dbfile)

    def loadData(self):
        """
        Load the dictionary from the db.pkl file if it exists, otherwise create it.

        Return a dictionary with two keys, "passwords" and "messages".
        """
        try:
            with open('./db.pkl', 'rb')  as dbfile:
                self.db = pickle.load(dbfile)
        except:
            self.db = {
                "passwords" : dict(),
                "messages": defaultdict(list)
            }
        return self.db

    def get_db(self):
        """
        Return the database
        """
        return self.db