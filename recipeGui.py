from tkinter import *
from tkcalendar import Calendar
from datetime import datetime

class GUIUtils:
    """
    A utility class for common GUI operations.
    """
    ingredients_list = []

    @staticmethod
    def create_recipe_form(window):
        """
        Creates the form for entering recipe details.

        Parameters:
        - window: The parent Tkinter window.

        Returns:
        - A tuple of Tkinter widgets for the form fields.
        """
        title_label = Label(window, text="Recipe Title:")
        title_label.grid(row=0, column=0, sticky="e")
        title_entry = Entry(window, width=35)
        title_entry.grid(row=0, column=1, columnspan=6, sticky="w")

        description_label = Label(window, text="Description:")
        description_label.grid(row=1, column=0, sticky="e")
        description_entry = Text(window, width=46, height=3)
        description_entry.grid(row=1, column=1, columnspan=6, sticky="w")

        ingredient_label = Label(window, text="Ingredient:")
        ingredient_label.grid(row=2, column=0, sticky="e")
        ingredient_entry = Entry(window, width=35)
        ingredient_entry.grid(row=2, column=1, columnspan=6, sticky="w")

        add_ingredient_button = Button(window, text="Add Ingredient", command=lambda: GUIUtils.add_ingredient(window), width=12, height=2)
        add_ingredient_button.grid(row=3, column=1, pady=(25, 5))

        remove_ingredient_button = Button(window, text="Remove Ingredient", command=lambda: GUIUtils.remove_ingredient(window), width=12, height=2)
        remove_ingredient_button.grid(row=3, column=2, pady=(25, 5))

        ingredients_display = Label(window, text="", anchor=CENTER, justify=CENTER)
        ingredients_display.grid(row=4, column=0, columnspan=7, pady=(5, 15))

        instructions_label = Label(window, text="Instructions:")
        instructions_label.grid(row=5, column=0, sticky="e")
        instructions_entry = Text(window, width=46, height=15)
        instructions_entry.grid(row=5, column=1, columnspan=6, sticky="w")

        size_prep_frame = Frame(window)
        size_prep_frame.grid(row=6, column=0, columnspan=7, pady=(5, 15))

        size_label = Label(size_prep_frame, text="Serving Size:")
        size_label.grid(row=0, column=0, sticky="e")
        serving_size_entry = Entry(size_prep_frame, width=5)
        serving_size_entry.grid(row=0, column=1, sticky="w", padx=(5,40))

        prep_label = Label(size_prep_frame, text="Prep Time (minutes):")
        prep_label.grid(row=0, column=2, sticky="e", padx=(5,0))
        prep_time_entry = Entry(size_prep_frame, width=6)
        prep_time_entry.grid(row=0, column=3, sticky="w", padx=(5,0))

        tags_label = Label(window, text="Tags:")
        tags_label.grid(row=7, column=0, sticky="e")
        tags_entry = Entry(window, width=35)
        tags_entry.grid(row=7, column=1, columnspan=6, sticky="w")

        return title_entry, description_entry, ingredient_entry, ingredients_display, instructions_entry, serving_size_entry, prep_time_entry, tags_entry

    @staticmethod
    def add_ingredient(window):
        """
        Adds an ingredient to the ingredients list and updates the display.

        Parameters:
        - window: The parent Tkinter window.
        """
        ingredient_text = window.ingredient_entry.get()
        if ingredient_text:
            GUIUtils.ingredients_list.append(ingredient_text)
            window.ingredients_display.config(text="\n".join(GUIUtils.ingredients_list))
            window.ingredient_entry.delete(0, END)

    @staticmethod
    def remove_ingredient(window):
        """
        Removes the last ingredient from the ingredients list and updates the display.

        Parameters:
        - window: The parent Tkinter window.
        """
        if GUIUtils.ingredients_list:
            GUIUtils.ingredients_list.pop()
            window.ingredients_display.config(text="\n".join(GUIUtils.ingredients_list))

    @staticmethod
    def center_widgets(window):
        """
        Adds padding to all widgets in the window for better layout.

        Parameters:
        - window: The parent Tkinter window.
        """
        for widget in window.winfo_children():
            widget.grid_configure(padx=5, pady=5)

    @staticmethod
    def open_calendar(window, entry_widget):
        """
        Opens a calendar window to select a date.

        Parameters:
        - window: The parent Tkinter window.
        - entry_widget: The entry widget to populate with the selected date.
        """
        def submit_date():
            selected_date = calendar.get_date()
            entry_widget.delete(0, END)
            entry_widget.insert(0, selected_date)
            calendar_window.destroy()

        calendar_window = Toplevel(window)
        calendar_window.title("Select Date")
        calendar_window.transient()
        calendar = Calendar(calendar_window, selectmode='day', date_pattern='yyyy-mm-dd')
        calendar.pack(pady=20)

        submit_button = Button(calendar_window, text="Submit", command=submit_date)
        submit_button.pack(pady=20)

class UpdateRecipeWindow:
    """
    A class for creating and managing the update recipe window.
    """
    def __init__(self, parent, db, recipe_id):
        self.window = Toplevel(parent)
        self.db = db
        self.recipe_id = recipe_id
        self.window.title("Update Recipe")
        self.window.geometry("480x700")


        self.title_entry, self.description_entry, self.ingredient_entry, self.ingredients_display, self.instructions_entry, self.serving_size_entry, self.prep_time_entry, self.tags_entry = GUIUtils.create_recipe_form(self.window)
        
        self.populate_fields()
        GUIUtils.center_widgets(self.window)

        save_button = Button(self.window, text="Save Recipe", command=self.save_updated_recipe, width=12, height=2)
        save_button.grid(row=8, column=0, columnspan=7, pady=(10, 20), padx=5)

    def populate_fields(self):
        """
        Populates the form fields with the details of the selected recipe.
        """
        recipe = self.db.fetch_recipe_by_id(self.recipe_id)
        if recipe:
            self.title_entry.insert(0, recipe[1])
            self.description_entry.insert("1.0", recipe[2])
            GUIUtils.ingredients_list.extend(recipe[3].split("; "))
            self.ingredients_display.config(text="\n".join(GUIUtils.ingredients_list))
            self.instructions_entry.insert("1.0", recipe[4])
            self.serving_size_entry.insert(0, recipe[5])
            self.prep_time_entry.insert(0, recipe[6])
            self.tags_entry.insert(0, recipe[7])

    def save_updated_recipe(self):
        """
        Saves the updated recipe details to the database.
        """
        updated_title = self.title_entry.get()
        updated_description = self.description_entry.get("1.0", END).strip()
        updated_ingredients = "; ".join(GUIUtils.ingredients_list)
        updated_instructions = self.instructions_entry.get("1.0", END).strip()
        updated_serving_size = self.serving_size_entry.get()
        updated_prep_time = self.prep_time_entry.get()
        updated_tags = self.tags_entry.get()

        if not updated_title or not updated_ingredients or not updated_instructions:
            print("Title, Ingredients, and Instructions are required fields.")
            return

        last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.db.update_recipe(self.recipe_id, {
            "title": updated_title,
            "description": updated_description,
            "ingredients": updated_ingredients,
            "instructions": updated_instructions,
            "serving_size": updated_serving_size,
            "prep_time": updated_prep_time,
            "tags": updated_tags,
            "last_updated": last_updated
        })

        GUIUtils.ingredients_list.clear()
        self.window.destroy()
        print("Recipe updated in database.")
