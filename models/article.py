from database.connection import get_db_connection
conn = get_db_connection()
cursor = conn.cursor()

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self._title = None
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id
        self.add_article_to_db()

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
        if not hasattr(self, '_id') or self._id is None:  
            if isinstance(title, str) and 5 <= len(title) <= 50:
                self._title = title
            else:
                raise ValueError("Title must be a string between 5 and 50 characters inclusive")
        else:  
            if hasattr(self, '_title'):  
                raise AttributeError("Title cannot be changed once initialized")
            else:
                if isinstance(title, str) and 5 <= len(title) <= 50:
                    self._title = title
                else:
                    raise ValueError("Title must be a string between 5 and 50 characters inclusive")

    @property
    def author(self):
     sql = """SELECT authors.id, authors.name FROM authors 
             INNER JOIN articles
             ON authors.id = articles.author_id
             WHERE articles.magazine_id = ?"""
     cursor.execute(sql, (self.id,))
     result = cursor.fetchone()
     if result:
        return {"author_id": result[0], "author_name": result[1]}
     else:
        return None

    @property
    def magazine(self):
        sql = """SELECT magazines.id, magazines.name FROM magazines
                 INNER JOIN articles
                 ON magazines.id = articles.magazine_id
                 WHERE articles.id = ? """
        cursor.execute(sql, (self.id,))
        result = cursor.fetchone()
        if result:
            return{"magazine_id": result[0],"magazine_name":result[1]}
        else:
            return None
        
    def add_article_to_db(self):
        sql = """INSERT INTO articles (title,content,author_id,magazine_id) VALUES (?,?,?,?)"""
        cursor.execute(sql,  (self.title, self.content, self.author_id, self.magazine_id))
        conn.commit()
    
    def find_by_id(self):
        sql = """SELECT title FROM articles WHERE id = ?"""
        cursor.execute(sql, (self.id,))
        row = cursor.fetchone()
        if row:
            self._title = row[0]
        else:
            raise ValueError(f"There is no article with Id {self.id} in the database")
        return self._title

    def __repr__(self):
        return f'<Article {self.title}>'

# # article = Article(12,"qwerty","qwertyuio",2,1)
# article = Article(1,"sdfqw","sqedf",2,2)
# print(article.author)
# print(article.magazine)
