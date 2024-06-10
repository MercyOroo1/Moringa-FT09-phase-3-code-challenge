from database.connection import get_db_connection
CONN = get_db_connection()
CURSOR = CONN.cursor()

class Magazine:
    def __init__(self, id, name, category):
        self._id = id
        self._name = name
        self._category = category


    def save(self):
        CURSOR.execute("SELECT id FROM magazines WHERE id = ?", (self._id,))
        if CURSOR.fetchone():
                raise ValueError(f"Article with id {self._id} already exists")
        sql = """
         INSERT INTO magazines (
         id, name, category)  
         VALUES (?, ?, ?)  
        """
        CURSOR.execute(sql,(self._id, self._name ,self._category))
        CONN.commit()

    def find_cat_from_db(self, id):
        sql = """SELECT category FROM magazines WHERE id = ?"""
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row:
            self._category = row[0]
            return self._category
        else:
            raise ValueError("The Category is not available in the database")

 

    def magazine_articles(self):
        sql = """SELECT magazines.name, articles.id, articles.title FROM magazines
                INNER JOIN articles ON magazines.id = articles.magazine_id
                WHERE magazines.id = ?"""
        CURSOR.execute(sql, (self._id,))
        article_details = CURSOR.fetchall()
        return [row[2] for row in article_details]

    def magazine_contributors(self):
        sql = """SELECT authors.id, authors.name, magazines.name FROM authors
               INNER JOIN articles ON authors.id = articles.author_id
               INNER JOIN magazines ON articles.magazine_id = magazines.id
               WHERE magazines.id = ?"""
        CURSOR.execute(sql, (self._id,))
        contributors = CURSOR.fetchall()
        return [row[1] for row in contributors]

    def article_titles(self):
        sql = """SELECT magazines.name, articles.title FROM articles 
                INNER JOIN magazines ON articles.magazine_id = magazines.id
                WHERE magazines.id = ? """
        CURSOR.execute(sql, (self._id,))
        titles = CURSOR.fetchall()
        if not titles:
            return None
        else:
            return [row[1] for row in titles]

    def contributing_authors(self):
        sql = """
            SELECT authors.id, authors.name, COUNT(*) AS article_count
            FROM authors
            INNER JOIN articles ON authors.id = articles.author_id
            INNER JOIN magazines ON articles.magazine_id = magazines.id
            WHERE magazines.id = ?
            GROUP BY authors.id, authors.name
            HAVING COUNT(*) > 2
        """
        CURSOR.execute(sql, (self._id,))
        authors_data = CURSOR.fetchall()

        if not authors_data:
            return None
        else:
            return [row[1] for row in authors_data]
    def __repr__(self):
        return f'<Magazine {self._name}>'


# magazine1.add_mag_to_db()


# print(magazine1.magazine_articles())
# print(magazine1.magazine_contributors())
# print(magazine1.article_titles())
# print(magazine1.contributing_authors())