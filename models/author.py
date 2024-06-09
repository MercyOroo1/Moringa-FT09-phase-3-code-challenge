from database.connection import get_db_connection
conn = get_db_connection()
cursor = conn.cursor()


class Author:
    def __init__(self,id,name):
        self._name = name
        self.add_author_to_db()
        self.id = id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if isinstance(id, int):
            self._id = id
        else:
            raise ValueError("Id must be a number")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
     if self.find_by_id(self.id):
        if not hasattr(self, '_name'):
            if not isinstance(name, str) or len(name) == 0:
                raise ValueError("Name must be a non-empty string")
            self._name = name
        else:
            raise AttributeError("Author name cannot be changed after initialization")

    def add_author_to_db(self):
            sql = "INSERT INTO authors (name) VALUES (?)"
            cursor.execute(sql, (self._name,))
            conn.commit()
    def find_by_id (self,id):
        sql = """SELECT name FROM authors WHERE id = ?"""
        cursor.execute(sql,(id,))
        row = cursor.fetchone()
        if row:
            self._name = row[0]
            return self._name
        else:
            raise ValueError(f"There is no author with Id {self.id} in the database")

    def articles(self):
        sql = """SELECT articles.id, articles.title,articles.content FROM articles
                INNER JOIN authors
                ON articles.author_id = authors.id
                WHERE authors.id = ? """
        cursor.execute(sql,(self.id,))
        article_details = cursor.fetchall()
        return [{"articles_id": row[0], "articles_title": row[1], "articles_content": row[2]} for row in article_details] if article_details else None

    def magazines(self,id):
        sql = """
                SELECT magazines.id ,magazines.name FROM magazines
                INNER JOIN articles ON magazines.id = articles.magazine_id
                INNER JOIN authors ON articles.author_id = authors.id
                WHERE authors.id = ?
                   """
        cursor.execute(sql,(id,))
        magazine_details = cursor.fetchall()
        return [{"magazine_id": row[0], "magazine_name": row[1]} for row in magazine_details] if magazine_details else None
    

# author = Author(1,"Mercy")
# print(author.find_by_id(20))
# print(author.articles(1))
# print(author.magazines(2))
