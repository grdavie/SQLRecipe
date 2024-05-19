from tkinter import *
from recipeGui import GUIUtils, UpdateRecipeWindow
from recipeDatabase import Database
from datetime import datetime

class RecipeManagerApp:
    """
    The main application class for managing recipes.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Recipe Manager")
        self.root.geometry("480x700")

        self.db = Database()
        self.create_main_gui()
        self.search_listbox = None  # Initialize search_listbox
        self.last_search_term = ""
        self.last_start_date = ""
        self.last_end_date = ""

    def create_main_gui(self):
        """
        Creates the main GUI for the recipe manager application.
        """
        title_label = Label(self.root, text="Recipe Title:")
        title_label.grid(row=0, column=0, sticky="e")
        self.title_entry = Entry(self.root, width=35)
        self.title_entry.grid(row=0, column=1, columnspan=6, sticky="w")

        description_label = Label(self.root, text="Description:")
        description_label.grid(row=1, column=0, sticky="e")
        self.description_entry = Text(self.root, width=46, height=3)
        self.description_entry.grid(row=1, column=1, columnspan=6, sticky="w")

        ingredient_label = Label(self.root, text="Ingredient:")
        ingredient_label.grid(row=2, column=0, sticky="e")
        self.ingredient_entry = Entry(self.root, width=35)
        self.ingredient_entry.grid(row=2, column=1, columnspan=6, sticky="w")

        add_ingredient_button = Button(self.root, text="Add Ingredient", command=lambda: GUIUtils.add_ingredient(self), width=12, height=2)
        add_ingredient_button.grid(row=3, column=1, pady=(25, 5))

        remove_ingredient_button = Button(self.root, text="Remove Ingredient", command=lambda: GUIUtils.remove_ingredient(self), width=12, height=2)
        remove_ingredient_button.grid(row=3, column=2, pady=(25, 5))

        self.ingredients_display = Label(self.root, text="", anchor=CENTER, justify=CENTER)
        self.ingredients_display.grid(row=4, column=0, columnspan=7, pady=(5, 15))

        instructions_label = Label(self.root, text="Instructions:")
        instructions_label.grid(row=5, column=0, sticky="e")
        self.instructions_entry = Text(self.root, width=46, height=15)
        self.instructions_entry.grid(row=5, column=1, columnspan=6, sticky="w")

        size_prep_frame = Frame(self.root)
        size_prep_frame.grid(row=6, column=0, columnspan=7, pady=(5, 15))

        size_label = Label(size_prep_frame, text="Serving Size:")
        size_label.grid(row=0, column=0, sticky="e")
        self.serving_size_entry = Entry(size_prep_frame, width=5)
        self.serving_size_entry.grid(row=0, column=1, sticky="w", padx=(5, 40))

        prep_label = Label(size_prep_frame, text="Prep Time (minutes):")
        prep_label.grid(row=0, column=2, sticky="e", padx=(5, 0))
        self.prep_time_entry = Entry(size_prep_frame, width=6)
        self.prep_time_entry.grid(row=0, column=3, sticky="w", padx=(5, 0))

        tags_label = Label(self.root, text="Tags:")
        tags_label.grid(row=7, column=0, sticky="e")
        self.tags_entry = Entry(self.root, width=35)
        self.tags_entry.grid(row=7, column=1, columnspan=6, sticky="w")

        button_frame = Frame(self.root)
        button_frame.grid(row=8, column=0, columnspan=7, pady=(10, 0))

        add_recipe_button = Button(button_frame, text="Add Recipe", command=self.add_recipe, width=12, height=2)
        add_recipe_button.pack(side=LEFT, padx=5)

        search_recipe_button = Button(button_frame, text="Search Recipe", command=self.search_recipes, width=12, height=2)
        search_recipe_button.pack(side=LEFT, padx=5)

        quit_button = Button(button_frame, text="Quit", command=self.quit_program, width=12, height=2)
        quit_button.pack(side=LEFT, padx=5)

        GUIUtils.center_widgets(self.root)

    def add_recipe(self):
        """
        Adds a new recipe to the database.
        """
        title = self.title_entry.get()
        description = self.description_entry.get("1.0", END).strip()
        ingredients = "; ".join(GUIUtils.ingredients_list)
        instructions = self.instructions_entry.get("1.0", END).strip()
        serving_size = self.serving_size_entry.get()
        prep_time = self.prep_time_entry.get()
        tags = self.tags_entry.get()

        if not title or not ingredients or not instructions:
            print("Title, Ingredients, and Instructions are required fields.")
            return

        date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        last_updated = date_added

        recipe = {
            'title': title,
            'description': description,
            'ingredients': ingredients,
            'instructions': instructions,
            'serving_size': serving_size,
            'prep_time': prep_time,
            'tags': tags,
            'date_added': date_added,
            'last_updated': last_updated
        }

        self.db.add_recipe(recipe)
        print("Recipe added to database.")

        GUIUtils.ingredients_list.clear()
        self.ingredients_display.config(text="")

        self.title_entry.delete(0, END)
        self.description_entry.delete("1.0", END)
        self.ingredient_entry.delete(0, END)
        self.instructions_entry.delete("1.0", END)
        self.serving_size_entry.delete(0, END)
        self.prep_time_entry.delete(0, END)
        self.tags_entry.delete(0, END)

    def search_recipes(self):
        """
        Opens the search recipes window.
        """
        search_window = Toplevel(self.root)
        search_window.title("Search Recipes")
        search_window.geometry("480x600")

        search_label = Label(search_window, text="Search:")
        search_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        search_entry = Entry(search_window, width=30)
        search_entry.grid(row=0, column=1, columnspan=3, pady=5, sticky="w")

        search_button = Button(search_window, text="Search", command=lambda: self.perform_search(search_entry.get(), start_date_entry.get(), end_date_entry.get()), width=12, height=2)
        search_button.grid(row=1, column=0, columnspan=4, pady=10)

        button_frame = Frame(search_window)
        button_frame.grid(row=2, column=0, columnspan=4, pady=(10, 0))

        delete_button = Button(button_frame, text="Delete Recipe", command=self.delete_selected_recipe, width=12, height=2)
        delete_button.grid(row=0, column=0, padx=5)

        update_button = Button(button_frame, text="Update Recipe", command=self.open_update_recipe_window, width=12, height=2)
        update_button.grid(row=0, column=1, padx=5)

        show_button = Button(button_frame, text="Show Recipe", command=self.show_recipe, width=12, height=2)
        show_button.grid(row=1, column=0, padx=5)

        cancel_button = Button(button_frame, text="Cancel", command=search_window.destroy, width=12, height=2)
        cancel_button.grid(row=1, column=1, padx=5)

        date_label = Label(search_window, text="Filter by Date Created:")
        date_label.grid(row=3, column=0, columnspan=4, padx=10, pady=5)

        start_date_label = Label(search_window, text="Start Date:")
        start_date_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        start_date_entry = Entry(search_window, width=12)
        start_date_entry.grid(row=4, column=1, pady=5, sticky="w")
        start_date_entry.bind("<Double-1>", lambda e: GUIUtils.open_calendar(search_window, start_date_entry))

        end_date_label = Label(search_window, text="End Date:")
        end_date_label.grid(row=4, column=2, padx=10, pady=5, sticky="e")
        end_date_entry = Entry(search_window, width=12)
        end_date_entry.grid(row=4, column=3, pady=5, sticky="w")
        end_date_entry.bind("<Double-1>", lambda e: GUIUtils.open_calendar(search_window, end_date_entry))

        listbox_frame = Frame(search_window, width=200, height=300)
        listbox_frame.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

        scrollbar = Scrollbar(listbox_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.search_listbox = Listbox(listbox_frame, yscrollcommand=scrollbar.set, width=50, height=15)
        self.search_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.search_listbox.yview)

    def perform_search(self, search_term, start_date, end_date):
        """
        Performs the search operation and updates the listbox with the search results.
        """
        self.last_search_term = search_term
        self.last_start_date = start_date
        self.last_end_date = end_date

        self.search_listbox.delete(0, END)

        query = "SELECT id, title, date(date_added) FROM recipes WHERE 1=1"
        params = []

        if search_term:
            query += " AND (title LIKE ? OR tags LIKE ?)"
            params.extend([f'%{search_term}%', f'%{search_term}%'])

        if start_date and end_date:
            query += " AND date(date_added) BETWEEN ? AND ?"
            params.extend([start_date, end_date])

        results = self.db.search_recipes(query, params)

        if results:
            for result in results:
                self.search_listbox.insert(END, f"ID:{result[0]} - {result[1]} [{result[2]}]")
        else:
            self.search_listbox.insert(END, "No recipes found")

    def delete_selected_recipe(self):
        """
        Deletes the selected recipe from the database.
        """
        selected = self.search_listbox.curselection()
        if selected:
            selected_recipe = self.search_listbox.get(selected[0])
            recipe_id = int(selected_recipe.split(":")[1].split(" -")[0].strip())
            self.db.delete_recipe(recipe_id)
            self.perform_search(self.last_search_term, self.last_start_date, self.last_end_date)
            print("Recipe deleted from database.")

    def open_update_recipe_window(self):
        """
        Opens the update recipe window for the selected recipe.
        """
        selected = self.search_listbox.curselection()
        if selected:
            selected_recipe = self.search_listbox.get(selected[0])
            recipe_id = int(selected_recipe.split(":")[1].split(" -")[0].strip())
            UpdateRecipeWindow(self.root, self.db, recipe_id)

    def show_recipe(self):
        """
        Shows the selected recipe in a new window.
        """
        selected = self.search_listbox.curselection()
        if selected:
            selected_recipe = self.search_listbox.get(selected[0])
            recipe_id = int(selected_recipe.split(":")[1].split(" -")[0].strip())

            recipe = self.db.fetch_recipe_by_id(recipe_id)
            if recipe:
                show_window = Toplevel(self.root)
                show_window.title("Show Recipe")
                show_window.geometry("400x500")

                canvas = Canvas(show_window)
                v_scrollbar = Scrollbar(show_window, orient="vertical", command=canvas.yview)
                scrollable_frame = Frame(canvas)

                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(
                        scrollregion=canvas.bbox("all")
                    )
                )

                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=v_scrollbar.set)

                canvas.pack(side="left", fill="both", expand=True)
                v_scrollbar.pack(side="right", fill="y")

                title_label = Label(scrollable_frame, text=f"============================================\n{recipe[1]}\n============================================", font=("Helvetica", 14), justify="left")
                title_label.pack(anchor="w", pady=(10, 5), padx=10)

                description_label = Label(scrollable_frame, text=f"{recipe[2]}\n\nServes {recipe[5]} | Takes {recipe[6]} minutes", font=("Helvetica", 12, "italic"), justify="left", wraplength=350)
                description_label.pack(anchor="w", pady=(5, 10), padx=10)

                ingredients_label = Label(scrollable_frame, text="---------------------------------------------------------------------------------------------------\nIngredients:\n---------------------------------------------------------------------------------------------------", font=("Helvetica", 12), justify="left")
                ingredients_label.pack(anchor="w", pady=(10, 5), padx=10)

                ingredients = recipe[3].split(";")
                for ingredient in ingredients:
                    ingredient_label = Label(scrollable_frame, text=f"- {ingredient.strip()}", font=("Helvetica", 12), justify="left")
                    ingredient_label.pack(anchor="w", padx=10)

                instructions_label = Label(scrollable_frame, text="---------------------------------------------------------------------------------------------------\nInstructions:\n---------------------------------------------------------------------------------------------------", font=("Helvetica", 12), justify="left")
                instructions_label.pack(anchor="w", pady=(10, 5), padx=10)

                instruction_label = Label(scrollable_frame, text=f"{recipe[4]}", font=("Helvetica", 12), justify="left", wraplength=350)
                instruction_label.pack(anchor="w", padx=10)

                tags_label = Label(scrollable_frame, text=f"\n---------------------------------------------------------------------------------------------------\n\nTags: {recipe[7]}", font=("Helvetica", 12), justify="left")
                tags_label.pack(anchor="w", padx=10)

                date_added_label = Label(scrollable_frame, text=f"Date Added: {recipe[8]}", font=("Helvetica", 12), justify="left")
                date_added_label.pack(anchor="w", padx=10)

                last_updated_label = Label(scrollable_frame, text=f"Last Updated: {recipe[9]}\n\n", font=("Helvetica", 12), justify="left")
                last_updated_label.pack(anchor="w", padx=10)

    def quit_program(self):
        """
        Quits the application.
        """
        self.root.quit()

if __name__ == "__main__":
    root = Tk()
    app = RecipeManagerApp(root)
    root.mainloop()
