import sqlite3

CONN = sqlite3.connect("./dogs.db")
CURSOR = CONN.cursor()

class Dog:
    all = []

    #initialize method: name, breed, id
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed
    
    #create table class method
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """

        CURSOR.execute(sql)

    #drop table class method

    @classmethod
    def drop_table(cls):
        sql="""
            DROP TABLE IF EXISTS dogs
        """

        CURSOR.execute(sql)


    #save() instance method
    def save(self):
        sql = """
            INSERT INTO dogs (name, breed) VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.breed))
        self.id = CURSOR.execute("SELECT last_insert_rowid()").fetchone()[0]


    #create() class method
    @classmethod
    def create(cls, name, breed):
        pass
        dog = Dog(name, breed)
        dog.save()
        return dog
        


    #new_from_db() class method
    @classmethod
    def new_from_db(cls, row):
        pass
        dog = Dog(id=row[0], name=row[1], breed=row[2])
        return dog
    
    @classmethod
    def get_all(cls):
        pass
        # use sql to grab all dog rows. 
        sql = """
            SELECT * FROM dogs
        """

        all = CURSOR.execute(sql).fetchall()

        #create an array of dog instances using list comprehension and the new_from_db class method
        cls.all = [cls.new_from_db(row) for row in all]

        return cls.all

    #find_by_name class method
    @classmethod
    def find_by_name(cls, name):
        pass
        #use sql to grab the dog. The query may or may not return a row
        sql = """
            SELECT * FROM dogs WHERE name = ? LIMIT 1
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        if not row:
            return None

        return cls.new_from_db(row)

    #find_by_id class method
    @classmethod
    def find_by_id(cls, id):
        pass
        #use sql to grab the dog. The query may or may not return a row
        sql = """
            SELECT * FROM dogs WHERE id = ? LIMIT 1
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        if not row:
            return None

        return cls.new_from_db(row)

    #find_or_create class method
    @classmethod
    def find_or_create_by(cls, name, breed):
        pass
        sql = """
            SELECT * FROM dogs WHERE (name, breed) = (?, ?) LIMIT 1
        """

        row = CURSOR.execute(sql, (name, breed)).fetchone()
        if not row:
            #if no row is found, create a new dog in the database
            return cls.create(name, breed)
 
        return cls.new_from_db(row)

    #update method
    def update(self):
        pass
        sql = """
            UPDATE dogs 
            SET name = ?, breed = ?
             WHERE id = ?
        """

        CURSOR.execute(sql, (self.name, self.breed, self.id))
