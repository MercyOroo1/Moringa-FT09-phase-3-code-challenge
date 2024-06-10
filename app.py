# main.py
from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    create_tables()

    while True:
        print("\n0. Add new record")
        print("1. Find the articles' author")
        print("2. Find the magazine to which the article belongs to")
        print("3. Get all articles written by the author")
        print("4. Get all magazines written by the author")
        print("5. Get all articles that belong to the magazine")
        print("6. Get all magazine contributors")
        print("7. Get all the magazine articles")
        print("8. Get all magazine contributors with more than 2 articles")
        print("9.Exit")
        choice = input("Enter choice: ")

        conn = get_db_connection()
        cursor = conn.cursor()

        if choice == "0":
            author_name = input("Enter author's name: ")
            magazine_name = input("Enter magazine name: ")
            magazine_category = input("Enter magazine category: ")
            article_title = input("Enter article title: ")
            article_content = input("Enter article content: ")

            cursor.execute('INSERT INTO authors (name) VALUES (?)', (author_name,))
            author_id = cursor.lastrowid

            cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (magazine_name, magazine_category))
            magazine_id = cursor.lastrowid

            cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                           (article_title, article_content, author_id, magazine_id))

            conn.commit()

            cursor.execute('SELECT * FROM magazines')
            magazines = cursor.fetchall()

            cursor.execute('SELECT * FROM authors')
            authors = cursor.fetchall()

            cursor.execute('SELECT * FROM articles')
            articles = cursor.fetchall()

            print("\nMagazines:")
            for magazine in magazines:
                print(Magazine(magazine["id"], magazine["name"], magazine["category"]))

            print("\nAuthors:")
            for author in authors:
                print(Author(author["id"], author["name"]))

            print("\nArticles:")
            for article in articles:
                print(Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]))

        elif choice == "1":
            article_id = input("Enter the article ID: ")
            cursor.execute("SELECT authors.id, authors.name FROM authors JOIN articles ON authors.id = articles.author_id WHERE articles.id = ?", (article_id,))
            author = cursor.fetchone()
            if author:
                print(f"Author of the article is {Author(author['id'], author['name'])}")
            else:
                print("Article not found or no author associated with this article.")

        elif choice == "2":
            article_id = input("Enter the article ID: ")
            cursor.execute("SELECT magazines.id, magazines.name, magazines.category FROM magazines JOIN articles ON magazines.id = articles.magazine_id WHERE articles.id = ?", (article_id,))
            magazine = cursor.fetchone()
            if magazine:
                print(f"The article belongs to {Magazine(magazine['id'], magazine['name'], magazine['category'])}")
            else:
                print("Article not found or no magazine associated with this article.")

        elif choice == "3":
            author_id = input("Enter the author ID: ")
            cursor.execute("SELECT * FROM articles WHERE author_id = ?", (author_id,))
            articles = cursor.fetchall()
            if articles:
                print(f"Articles written by the author with ID {author_id}:")
                for article in articles:
                    print(Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]))
            else:
                print("No articles found for this author.")

        elif choice == "4":
            author_id = input("Enter the author ID: ")
            cursor.execute("""
                SELECT DISTINCT magazines.id, magazines.name, magazines.category
                FROM magazines
                JOIN articles ON magazines.id = articles.magazine_id
                WHERE articles.author_id = ?
            """, (author_id,))
            magazines = cursor.fetchall()
            if magazines:
                print(f"Magazines that the author with ID {author_id} has written for:")
                for magazine in magazines:
                    print(Magazine(magazine["id"], magazine["name"], magazine["category"]))
            else:
                print("No magazines found for this author.")

        elif choice == "5":
            magazine_id = input("Enter the magazine ID: ")
            cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (magazine_id,))
            articles = cursor.fetchall()
            if articles:
                print(f"Articles in the magazine with ID {magazine_id}:")
                for article in articles:
                    print(Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]))
            else:
                print("No articles found for this magazine.")

        elif choice == "6":
            magazine_id = input("Enter the magazine ID: ")
            cursor.execute("""
                SELECT DISTINCT authors.id, authors.name
                FROM authors
                JOIN articles ON authors.id = articles.author_id
                WHERE articles.magazine_id = ?
            """, (magazine_id,))
            authors = cursor.fetchall()
            if authors:
                print(f"Authors who have contributed to the magazine with ID {magazine_id}:")
                for author in authors:
                    print(Author(author["id"], author["name"]))
            else:
                print("No contributors found for this magazine.")

        elif choice == "7":
            magazine_id = input("Enter the magazine ID: ")
            cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (magazine_id,))
            articles = cursor.fetchall()
            if articles:
                print(f"Articles in the magazine with ID {magazine_id}:")
                for article in articles:
                    print(Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]))
            else:
                print("No articles found for this magazine.")

        elif choice == "8":
            cursor.execute("""
                SELECT authors.id, authors.name, COUNT(articles.id) as article_count
                FROM authors
                JOIN articles ON authors.id = articles.author_id
                GROUP BY authors.id
                HAVING article_count > 2
            """)
            authors = cursor.fetchall()
            if authors:
                print("Authors with more than 2 articles:")
                for author in authors:
                    print(f"{Author(author['id'], author['name'])} - Articles: {author['article_count']}")
            else:
                print("No authors found with more than 2 articles.")

            conn.close()
        elif choice == "9":
            print("Exiting")
            break
        else:
            print("Invalid option. Please enter a valid option.")


if __name__ == "__main__":
    main()
