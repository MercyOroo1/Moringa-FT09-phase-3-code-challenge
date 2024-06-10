import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from database.connection import get_db_connection
from database.setup import create_tables
conn = get_db_connection()
cursor = conn.cursor()
class Author:
    def __init__(self, id, name):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string")
        self._id = id
        self._name = name
    
    @property
    def name(self):
        return self._name
    @property
    def id(self):
        return self._id
    @id.setter    
    def id(self, id):
        if not isinstance (id , int):
            raise   TypeError("id must be an integer")
        self._id = id


    
    def save (self):
        cursor.execute("SELECT id FROM authors WHERE id = ?", (self._id,))
        if cursor.fetchone():
                raise ValueError(f"Author with id {self._id} already exists")
        sql = """
         INSERT INTO authors (
         id, name)  
         VALUES (?, ?)  
        """
        cursor.execute(sql,(self._id, self._name))
        conn.commit()
    def articles(self):
        sql = """
            SELECT articles.title
            FROM articles
            LEFT JOIN authors
            ON articles.author_id = authors.id
            WHERE authors.id = ?
        """
        cursor.execute(sql, (self._id,))
        articles = cursor.fetchall()
        return [article[0] for article in articles] if articles else None
    def magazines(self):
        sql = """
            SELECT magazines.name
            FROM magazines
            LEFT JOIN articles
            ON magazines.id = articles.magazine_id
            LEFT JOIN authors
            ON articles.author_id = authors.id
            WHERE authors.id = ?
        """
        cursor.execute(sql,(self._id,))
        magazines = cursor.fetchall()
        return [magazine[0] for magazine in magazines] if magazines else None
   
    def __repr__(self):
        return f'<Author {self.name}>'