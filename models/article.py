from database.connection import get_db_connection
conn = get_db_connection()
cursor = conn.cursor()

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self._id = id
        self._title = title
        self._content = content
        self._author_id = author_id
        self._magazine_id = magazine_id
        # self.add_article_to_db()

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
      if hasattr(self, '_name'):
        raise AttributeError("Title cannot be changed after initialization")
      if not isinstance(title, str) and 5 <= len(title) <= 50:
         raise ValueError("Title must be a string between 5 and 50 characters inclusive")
      self._title = title

    def author_name(self,id):
     sql = """SELECT authors.id, authors.name FROM authors 
             INNER JOIN articles
             ON authors.id = articles.author_id
             WHERE articles.id = ?"""
     cursor.execute(sql, (id,))
     result = cursor.fetchone()
     if result:
        return result[1]
     else:
        return None

    def magazine_names(self):
        sql = """SELECT magazines.id, magazines.name FROM magazines
                 INNER JOIN articles
                 ON magazines.id = articles.magazine_id
                 WHERE articles.id = ? """
        cursor.execute(sql, (self._id,))
        result = cursor.fetchone()
        if result:
            return result[1]
        else:
            return None
        
    
    def save(self):
        cursor.execute("SELECT id FROM articles WHERE id = ?", (self._id,))
        if cursor.fetchone():
                raise ValueError(f"Article with id {self._id} already exists")
        sql = """
         INSERT INTO articles (
         id, title, content, author_id, magazine_id)  
         VALUES (?, ?, ?, ?, ?)  
        """
        cursor.execute(sql,(self._id, self._title, self._content,self._author_id,self._magazine_id))
        conn.commit()

       

    def __repr__(self):
        return f'<Article {self.title}>'

