import sqlite3

class Database:
    """
    A class to manage the recipe database.
    """
    def __init__(self):
        """
        Initializes the database connection and creates the table if it doesn't exist.
        """
        self.conn = sqlite3.connect('recipes.db')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """
        Creates the recipes table if it does not already exist.
        """
        self.c.execute("""CREATE TABLE IF NOT EXISTS recipes (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          title TEXT NOT NULL, 
                          description TEXT,
                          ingredients TEXT NOT NULL, 
                          instructions TEXT NOT NULL,
                          serving_size INTEGER, 
                          prep_time INTEGER, 
                          tags TEXT, 
                          date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
                          last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
                          )""")
        self.conn.commit()

    def add_recipe(self, recipe):
        """
        Adds a new recipe to the database.

        Parameters:
        - recipe: A dictionary containing the recipe details.
        """
        self.c.execute("""INSERT INTO recipes 
                          (title, description, ingredients, instructions, serving_size, prep_time, tags, date_added, last_updated) 
                          VALUES (:title, :description, :ingredients, :instructions, :serving_size, :prep_time, :tags, :date_added, :last_updated)""",
                       recipe)
        self.conn.commit()

    def search_recipes(self, query, params):
        """
        Searches for recipes in the database based on a query and parameters.

        Parameters:
        - query: The SQL query string.
        - params: A list of parameters for the query.

        Returns:
        - A list of recipes that match the query.
        """
        self.c.execute(query, params)
        return self.c.fetchall()

    def delete_recipe(self, recipe_id):
        """
        Deletes a recipe from the database.

        Parameters:
        - recipe_id: The ID of the recipe to be deleted.
        """
        self.c.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        self.conn.commit()

    def fetch_recipe_by_id(self, recipe_id):
        """
        Fetches a recipe from the database by its ID.

        Parameters:
        - recipe_id: The ID of the recipe to fetch.

        Returns:
        - The recipe details as a tuple.
        """
        self.c.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
        return self.c.fetchone()

    def update_recipe(self, recipe_id, updated_recipe):
        """
        Updates a recipe in the database.

        Parameters:
        - recipe_id: The ID of the recipe to update.
        - updated_recipe: A dictionary containing the updated recipe details.
        """
        self.c.execute("""UPDATE recipes 
                          SET title = :title, description = :description, ingredients = :ingredients, instructions = :instructions, 
                              serving_size = :serving_size, prep_time = :prep_time, tags = :tags, last_updated = :last_updated 
                          WHERE id = :id""",
                       {**updated_recipe, "id": recipe_id})
        self.conn.commit()
