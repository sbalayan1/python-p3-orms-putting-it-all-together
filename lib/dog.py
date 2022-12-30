import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    pass
    all = []

    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        pass
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """

        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        pass
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)

    def save(self):
        pass
        sql = """
            INSERT INTO dogs (name, breed) VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.breed))
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]

    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        # print(dog.id)
        dog.id = row[0]
        # print(dog.id)
        return dog

    @classmethod
    def get_all(cls):
        all = CURSOR.execute("SELECT * FROM dogs").fetchall()
        cls.all = [cls.new_from_db(row) for row in all]
        return cls.all

    @classmethod
    def find_by_name(cls, name):
        pass
        sql = """
            SELECT * FROM dogs WHERE name = ? LIMIT 1
        """
        row = CURSOR.execute(sql, (name,)).fetchone()
        if not row:
            return None

        dog = Dog(
            name=row[1],
            breed=row[2]
        )

        dog.id = row[0]
        return dog
    
    @classmethod
    def find_by_id(cls, id):
        pass
        sql = """
            SELECT * FROM dogs WHERE id = ? LIMIT 1
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        dog = Dog(row[1], row[2])
        dog.id = row[0]
        return dog

    @classmethod
    def find_or_create_by(cls, name, breed):
        pass
        sql = """
            SELECT * FROM dogs WHERE (name, breed) = (?, ?) LIMIT 1
        """

        row = CURSOR.execute(sql, (name, breed)).fetchone()
        if not row:
            dog = cls.create(name, breed)
            # print(dog)
            return dog

        cls.new_from_db(row)
        # return dog

    # @classmethod
    def update(self):
        pass
        sql = """
            UPDATE dogs
            SET name = ?,
                breed = ?
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.name, self.breed, self.id))


