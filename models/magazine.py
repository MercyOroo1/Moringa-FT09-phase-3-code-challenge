from database.connection import get_db_connection
CONN = get_db_connection()
CURSOR = CONN.cursor()

class Magazine:
    def __init__(self, id, name, category):
        self._id = id
        self._name = name
        self._category = category



    def add_mag_to_db(self):
        sql = """INSERT INTO magazines(name, category) VALUES (?,?)"""
        CURSOR.execute(sql, (self._name, self._category))
        CONN.commit()

   
    def find_by_id(self, id):
        sql = """SELECT name FROM magazines WHERE id = ?"""
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row:
            self._name = row[0]
            return self._name
        else:
            raise ValueError(f"There is no magazine with Id {id} in the database")

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
        return [{"magazine_name": row[0], "article_id": row[1], "article_title": row[2]} for row in article_details]

    def magazine_contributors(self):
        sql = """SELECT authors.id, authors.name, magazines.name FROM authors
               INNER JOIN articles ON authors.id = articles.author_id
               INNER JOIN magazines ON articles.magazine_id = magazines.id
               WHERE magazines.id = ?"""
        CURSOR.execute(sql, (self._id,))
        contributors = CURSOR.fetchall()
        return [{"authors_id": row[0], "authors_name": row[1], "magazine_name": row[2]} for row in contributors]

    def article_titles(self):
        sql = """SELECT magazines.name, articles.title FROM articles 
                INNER JOIN magazines ON articles.magazine_id = magazines.id
                WHERE magazines.id = ? """
        CURSOR.execute(sql, (self._id,))
        titles = CURSOR.fetchall()
        if not titles:
            return None
        else:
            return [{"magazines_name": row[0], "articles_title": row[1]} for row in titles]

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
            return [{"authors_id": row[0], "authors_name": row[1]} for row in authors_data]

# Create a Magazine object
magazine1 = Magazine(1, "Magazine 1", "Category 1")

# Add the magazine to the database
magazine1.add_mag_to_db()

# Retrieve the magazine's articles, contributors, article titles, and contributing authors
print(magazine1.magazine_articles())
print(magazine1.magazine_contributors())
print(magazine1.article_titles())
print(magazine1.contributing_authors())