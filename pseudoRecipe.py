"""
Pseudo code before refactoring
"""

# from datetime import datetime
# from tkinter import *
# from tkcalendar import Calendar
# import sqlite3

# # Connect to SQLite database
# conn = sqlite3.connect('recipes.db')
# c = conn.cursor()

# # Create the Recipes table
# # c.execute("""CREATE TABLE recipes (
# #      id INTEGER PRIMARY KEY AUTOINCREMENT,
# #      title TEXT NOT NULL, 
# #      description TEXT,
# #      ingredients TEXT NOT NULL, 
# #      instructions TEXT NOT NULL,
# #      serving_size INTEGER, 
# #      prep_time INTEGER, 
# #      tags TEXT, 
# #      date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
# #      last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
# #      )""")

# conn.commit()


# # GUI SETUP
# root = Tk()
# root.title("Personal Recipe Manager")
# root.geometry("480x700")  # Set initial window size

# # List to store ingredients
# ingredients_list = []

# # Function to center widgets
# def center_widgets():
#     for widget in root.winfo_children():
#         widget.grid_configure(padx=5, pady=5)  # Added padding  

# # Function to add ingredient
# def add_ingredient():
#     ingredient_text = ingredient.get()
#     if ingredient_text:
#         ingredients_list.append(ingredient_text)
#         ingredient_display.config(text="\n".join(ingredients_list))
#         ingredient.delete(0, END)

# # Function to remove the last ingredient
# def remove_ingredient():
#     if ingredients_list:
#         ingredients_list.pop()
#         ingredient_display.config(text="\n".join(ingredients_list))

# # Function to add recipe to the database
# def add_recipe():
#     title_text = title.get()
#     description_text = description.get("1.0", END).strip()
#     ingredients_text = "; ".join(ingredients_list)
#     instructions_text = instructions.get("1.0", END).strip()
#     serving_size_value = serving_size.get()
#     prep_time_value = prep_time.get()
#     tags_text = tags.get()

#     if not title_text or not ingredients_text or not instructions_text:
#         print("Title, Ingredients, and Instructions are required fields.")
#         return

#     date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     last_updated = date_added

#     c.execute("""INSERT INTO recipes 
#                 (title, description, ingredients, instructions, serving_size, prep_time, tags, date_added, last_updated) 
#                 VALUES (:title, :description, :ingredients, :instructions, :serving_size, :prep_time, :tags, :date_added, :last_updated)""",
#               {
#                   'title': title_text,
#                   'description': description_text,
#                   'ingredients': ingredients_text,
#                   'instructions': instructions_text,
#                   'serving_size': serving_size_value,
#                   'prep_time': prep_time_value,
#                   'tags': tags_text,
#                   'date_added': date_added,
#                   'last_updated': last_updated
#               })
#     conn.commit()

#     # Clear the ingredients list and update the display
#     ingredients_list.clear()
#     ingredient_display.config(text="")
#     print("Recipe added to database.")
    
#     # Clear all the entry boxes
#     title.delete(0, END)
#     description.delete("1.0", END)
#     ingredient.delete(0, END)
#     instructions.delete("1.0", END)
#     serving_size.delete(0, END)
#     prep_time.delete(0, END)
#     tags.delete(0, END)

# # Function to handle date selection for start and end date
# def open_calendar(entry_widget):
#     def submit_date():
#         selected_date = calendar.get_date()
#         entry_widget.delete(0, END)
#         entry_widget.insert(0, selected_date)
#         calendar_window.destroy()

#     calendar_window = Toplevel(root)
#     calendar_window.title("Select Date")
#     calendar = Calendar(calendar_window, selectmode='day', date_pattern='yyyy-mm-dd')
#     calendar.pack(pady=20)

#     submit_button = Button(calendar_window, text="Submit", command=submit_date)
#     submit_button.pack(pady=20)
    

# # Function to show the selected recipe
# def show_recipes(listbox):
#     selected = listbox.curselection()
#     if selected:
#         selected_recipe = listbox.get(selected[0])
#         recipe_id = int(selected_recipe.split(":")[1].split(" -")[0].strip())
        
#         c.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
#         recipe = c.fetchone()

#         if recipe:
            
#             show_window = Toplevel(root)
#             show_window.title("Show Recipe")
#             show_window.geometry("400x500")

#             # Add vertical scrollbar to the show window
#             canvas = Canvas(show_window)
#             v_scrollbar = Scrollbar(show_window, orient="vertical", command=canvas.yview)
#             scrollable_frame = Frame(canvas)

#             scrollable_frame.bind(
#                 "<Configure>",
#                 lambda e: canvas.configure(
#                     scrollregion=canvas.bbox("all")
#                 )
#             )

#             canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
#             canvas.configure(yscrollcommand=v_scrollbar.set)

#             canvas.pack(side="left", fill="both", expand=True)
#             v_scrollbar.pack(side="right", fill="y")

#             # Recipe title
#             title_label = Label(scrollable_frame, text=f"============================================\n{recipe[1]}\n============================================", font=("Helvetica", 14), justify="left")
#             title_label.pack(anchor="w", pady=(10, 5), padx=10)

#             # Description
#             description_label = Label(scrollable_frame, text=f"{recipe[2]}\n\nServes {recipe[5]} | Takes {recipe[6]} minutes", font=("Helvetica", 12, "italic"), justify="left", wraplength=350)
#             description_label.pack(anchor="w", pady=(5, 10), padx=10)

#             # Ingredients
#             ingredients_label = Label(scrollable_frame, text="---------------------------------------------------------------------------------------------------\nIngredients:\n---------------------------------------------------------------------------------------------------", font=("Helvetica", 12), justify="left")
#             ingredients_label.pack(anchor="w", pady=(10, 5), padx=10)

#             ingredients = recipe[3].split(";")
#             for ingredient in ingredients:
#                 ingredient_label = Label(scrollable_frame, text=f"- {ingredient.strip()}", font=("Helvetica", 12), justify="left")
#                 ingredient_label.pack(anchor="w", padx=10)

#             # Instructions
#             instructions_label = Label(scrollable_frame, text="---------------------------------------------------------------------------------------------------\nInstructions:\n----------------------------------------------------------------------------------------------------", font=("Helvetica", 12), justify="left")
#             instructions_label.pack(anchor="w", pady=(10, 5), padx=10)

#             instruction_label = Label(scrollable_frame, text=f"{recipe[4]}", font=("Helvetica", 12), justify="left", wraplength=350)
#             instruction_label.pack(anchor="w", padx=10)

#             # Tags, Date added, and Last updated
#             tags_label = Label(scrollable_frame, text=f"\n---------------------------------------------------------------------------------------------------\n\nTags: {recipe[7]}", font=("Helvetica", 12), justify="left")
#             tags_label.pack(anchor="w",padx=10)

#             date_added_label = Label(scrollable_frame, text=f"Date Added: {recipe[8]}", font=("Helvetica", 12), justify="left")
#             date_added_label.pack(anchor="w", padx=10)

#             last_updated_label = Label(scrollable_frame, text=f"Last Updated: {recipe[9]}\n\n", font=("Helvetica", 12), justify="left")
#             last_updated_label.pack(anchor="w", padx=10)


# # Modify the search_recipes function to include the show_recipes call
# def search_recipes():
    
    
#     search_window = Toplevel(root)
#     search_window.title("Search Recipes")
#     search_window.geometry("480x600")

#     # Function to handle searching
#     def perform_search():
#         search_listbox.delete(0, END)
#         search_term = search_entry.get()
#         start_date = start_date_entry.get()
#         end_date = end_date_entry.get()

#         query = "SELECT id, title, date(date_added) FROM recipes WHERE 1=1"
#         params = []

#         if search_term:
#             query += " AND (title LIKE ? OR tags LIKE ?)"
#             params.extend([f'%{search_term}%', f'%{search_term}%'])

#         if start_date and end_date:
#             query += " AND date(date_added) BETWEEN ? AND ?"
#             params.extend([start_date, end_date])

#         c.execute(query, params)
#         results = c.fetchall()

#         if results:
#             for result in results:
#                 search_listbox.insert(END, f"ID:{result[0]} - {result[1]} [{result[2]}]")
#         else:
#             search_listbox.insert(END, "No recipes found")

#     # Function to handle deleting the selected recipe
#     def delete_selected_recipe(listbox):
#         selected = listbox.curselection()
#         if selected:
#             selected_recipe = listbox.get(selected[0])
#             recipe_id = int(selected_recipe.split(":")[1].split(" -")[0].strip())
#             c.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
#             conn.commit()
#             perform_search()
#             print("Recipe deleted from database.")
    
#     def update_recipe(listbox):
#         selected = listbox.curselection()
#         if selected:
#             selected_recipe = listbox.get(selected[0])
#             recipe_id = int(selected_recipe.split(":")[1].split(" -")[0].strip())

#             c.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
#             recipe = c.fetchone()

#             if recipe:
#                 def save_updated_recipe():
#                     updated_title = title_entry.get()
#                     updated_description = description_entry.get("1.0", END).strip()
#                     updated_ingredients = "; ".join(ingredients_list)
#                     updated_instructions = instructions_entry.get("1.0", END).strip()
#                     updated_serving_size = serving_size_entry.get()
#                     updated_prep_time = prep_time_entry.get()
#                     updated_tags = tags_entry.get()

#                     if not updated_title or not updated_ingredients or not updated_instructions:
#                         print("Title, Ingredients, and Instructions are required fields.")
#                         return

#                     last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#                     c.execute("""UPDATE recipes 
#                                 SET title = ?, description = ?, ingredients = ?, instructions = ?, serving_size = ?, prep_time = ?, tags = ?, last_updated = ?
#                                 WHERE id = ?""",
#                             (updated_title, updated_description, updated_ingredients, updated_instructions, updated_serving_size, updated_prep_time, updated_tags, last_updated, recipe_id))
#                     conn.commit()

#                     ingredients_list.clear()
#                     update_window.destroy()
#                     print("Recipe updated in database.")
#                     perform_search()

#                 # Creating the update window
#                 update_window = Toplevel(root)
#                 update_window.title("Update Recipe")
#                 update_window.geometry("480x700")

#                 # Add vertical scrollbar to the update window
#                 canvas = Canvas(update_window)
#                 v_scrollbar = Scrollbar(update_window, orient="vertical", command=canvas.yview)
#                 scrollable_frame = Frame(canvas)

#                 scrollable_frame.bind(
#                     "<Configure>",
#                     lambda e: canvas.configure(
#                         scrollregion=canvas.bbox("all")
#                     )
#                 )

#                 canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
#                 canvas.configure(yscrollcommand=v_scrollbar.set)

#                 canvas.pack(side="left", fill="both", expand=True)
#                 v_scrollbar.pack(side="right", fill="y")

#                 # Prepopulating the fields with the selected recipe information
#                 title_label = Label(scrollable_frame, text="Recipe Title:")
#                 title_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
#                 title_entry = Entry(scrollable_frame, width=35)
#                 title_entry.grid(row=0, column=1, columnspan=6, sticky="w", padx=5, pady=5)
#                 title_entry.insert(0, recipe[1])

#                 description_label = Label(scrollable_frame, text="Description:")
#                 description_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
#                 description_entry = Text(scrollable_frame, width=46, height=3)
#                 description_entry.grid(row=1, column=1, columnspan=6, sticky="w", padx=5, pady=5)
#                 description_entry.insert("1.0", recipe[2])

#                 ingredient_label = Label(scrollable_frame, text="Ingredient:")
#                 ingredient_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
#                 ingredient_entry = Entry(scrollable_frame, width=35)
#                 ingredient_entry.grid(row=2, column=1, columnspan=6, sticky="w", padx=5, pady=5)

#                 # Update the ingredients_list with the current ingredients
#                 ingredients_list.clear()
#                 ingredients_list.extend(recipe[3].split("; "))

#                 add_ingredient_button = Button(scrollable_frame, text="Add Ingredient", command=lambda: add_ingredient_to_list(ingredient_entry, ingredients_display), width=12, height=2)
#                 add_ingredient_button.grid(row=3, column=1, pady=(25, 5), padx=5)

#                 remove_ingredient_button = Button(scrollable_frame, text="Remove Ingredient", command=lambda: remove_ingredient_from_list(ingredients_display), width=12, height=2)
#                 remove_ingredient_button.grid(row=3, column=2, pady=(25, 5), padx=5)

#                 ingredients_display = Label(scrollable_frame, text="\n".join(ingredients_list), anchor=CENTER, justify=CENTER)
#                 ingredients_display.grid(row=4, column=0, columnspan=7, pady=(5, 15), padx=5)

#                 instructions_label = Label(scrollable_frame, text="Instructions:")
#                 instructions_label.grid(row=5, column=0, sticky="e", padx=5, pady=5)
#                 instructions_entry = Text(scrollable_frame, width=46, height=15)
#                 instructions_entry.grid(row=5, column=1, columnspan=6, sticky="w", padx=5, pady=5)
#                 instructions_entry.insert("1.0", recipe[4])

#                 # Serving Size and Prep Time frame
#                 size_prep_frame = Frame(scrollable_frame)
#                 size_prep_frame.grid(row=6, column=0, columnspan=7, pady=(5, 15), padx=5)  # Centered frame across columns

#                 # Serving size
#                 size_label = Label(size_prep_frame, text="Serving Size:")
#                 size_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
#                 serving_size_entry = Entry(size_prep_frame, width=5)
#                 serving_size_entry.grid(row=0, column=1, sticky="w", padx=(5, 40), pady=5)
#                 serving_size_entry.insert(0, recipe[5])

#                 # Prep Time
#                 prep_label = Label(size_prep_frame, text="Prep Time (minutes):")
#                 prep_label.grid(row=0, column=2, sticky="e", padx=(5, 0), pady=5)
#                 prep_time_entry = Entry(size_prep_frame, width=6)
#                 prep_time_entry.grid(row=0, column=3, sticky="w", padx=(5, 0), pady=5)
#                 prep_time_entry.insert(0, recipe[6])

#                 tags_label = Label(scrollable_frame, text="Tags:")
#                 tags_label.grid(row=7, column=0, sticky="e", padx=5, pady=5)
#                 tags_entry = Entry(scrollable_frame, width=35)
#                 tags_entry.grid(row=7, column=1, columnspan=6, sticky="w", padx=5, pady=5)
#                 tags_entry.insert(0, recipe[7])

#                 save_button = Button(scrollable_frame, text="Save Recipe", command=save_updated_recipe, width=12, height=2)
#                 save_button.grid(row=8, column=0, columnspan=7, pady=(10, 20), padx=5)

#                 def add_ingredient_to_list(entry_widget, display_widget):
#                     ingredient_text = entry_widget.get()
#                     if ingredient_text:
#                         ingredients_list.append(ingredient_text)
#                         display_widget.config(text="\n".join(ingredients_list))
#                         entry_widget.delete(0, END)

#                 def remove_ingredient_from_list(display_widget):
#                     if ingredients_list:
#                         ingredients_list.pop()
#                         display_widget.config(text="\n".join(ingredients_list))


                    


#     # Search bar
#     search_label = Label(search_window, text="Search:")
#     search_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
#     search_entry = Entry(search_window, width=30)
#     search_entry.grid(row=0, column=1, columnspan=3, pady=5, sticky="w")

#     # Search button
#     search_button = Button(search_window, text="Search", command=perform_search, width=12, height=2)
#     search_button.grid(row=1, column=0, columnspan=4, pady=10)

#     # Add buttons below the search button
#     button_frame = Frame(search_window)
#     button_frame.grid(row=2, column=0, columnspan=4, pady=(10, 0))

#     delete_button = Button(button_frame, text="Delete Recipe", command=lambda: delete_selected_recipe(search_listbox), width=12, height=2)
#     delete_button.grid(row=0, column=0, padx=5)

#     update_button = Button(button_frame, text="Update Recipe", command=lambda: update_recipe(search_listbox), width=12, height=2)
#     update_button.grid(row=0, column=1, padx=5)

#     show_button = Button(button_frame, text="Show Recipe", command=lambda: show_recipes(search_listbox), width=12, height=2)
#     show_button.grid(row=1, column=0, padx=5)

#     cancel_button = Button(button_frame, text="Cancel", command=search_window.destroy, width=12, height=2)
#     cancel_button.grid(row=1, column=1, padx=5)

#     # Filter by date
#     date_label = Label(search_window, text="Filter by Date Created:")
#     date_label.grid(row=3, column=0, columnspan=4, padx=10, pady=5)

#     start_date_label = Label(search_window, text="Start Date:")
#     start_date_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
#     start_date_entry = Entry(search_window, width=12)
#     start_date_entry.grid(row=4, column=1, pady=5, sticky="w")
#     start_date_entry.bind("<Button-1>", lambda e: open_calendar(start_date_entry))

#     end_date_label = Label(search_window, text="End Date:")
#     end_date_label.grid(row=4, column=2, padx=10, pady=5, sticky="e")
#     end_date_entry = Entry(search_window, width=12)
#     end_date_entry.grid(row=4, column=3, pady=5, sticky="w")
#     end_date_entry.bind("<Button-1>", lambda e: open_calendar(end_date_entry))

#     # Create a frame for the listbox and scrollbar
#     listbox_frame = Frame(search_window, width=200, height=300)
#     listbox_frame.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

#     # Create a scrollbar
#     scrollbar = Scrollbar(listbox_frame)
#     scrollbar.pack(side=RIGHT, fill=Y)

#     # Create a listbox with the scrollbar
#     search_listbox = Listbox(listbox_frame, yscrollcommand=scrollbar.set, width=50, height=15)
#     search_listbox.pack(side=LEFT, fill=BOTH, expand=True)
#     scrollbar.config(command=search_listbox.yview)


# # Placeholder function for Quit button
# def quit_program():
#     root.quit()
    
    
# # Function to fetch the most recent recipe from the database
# def fetch_recent_recipe():
#     c.execute("SELECT * FROM recipes ORDER BY date_added DESC LIMIT 1")
#     recent_recipe = c.fetchone()
#     if recent_recipe:
#         print("Most recent recipe added to the database:")
#         print(f"ID: {recent_recipe[0]}")
#         print(f"Title: {recent_recipe[1]}")
#         print(f"Description: {recent_recipe[2]}")
#         print(f"Ingredients: {recent_recipe[3]}")
#         print(f"Instructions: {recent_recipe[4]}")
#         print(f"Serving Size: {recent_recipe[5]}")
#         print(f"Prep Time: {recent_recipe[6]}")
#         print(f"Tags: {recent_recipe[7]}")
#         print(f"Date Added: {recent_recipe[8]}")
#         print(f"Last Updated: {recent_recipe[9]}")
#     else:
#         print("No recipes found in the database.")

# # Recipe title
# title_label = Label(root, text="Recipe Title:")
# title_label.grid(row=0, column=0, sticky="e")
# title = Entry(root, width=35)
# title.grid(row=0, column=1, columnspan=6, sticky="w")

# # Description
# description_label = Label(root, text="Description:")
# description_label.grid(row=1, column=0, sticky="e")
# description = Text(root, width=46, height=3)  # Increased height
# description.grid(row=1, column=1, columnspan=6, sticky="w")

# # Ingredients
# ingredient_label = Label(root, text="Ingredient:")
# ingredient_label.grid(row=2, column=0, sticky="e")
# ingredient = Entry(root, width=35)
# ingredient.grid(row=2, column=1, columnspan=6, sticky="w")

# # Add Ingredient button
# add_ingredient_button = Button(root, text="Add Ingredient", command=add_ingredient, width=12, height=2)
# add_ingredient_button.grid(row=3, column=1, pady=(25, 5))  # Position adjusted
# # Centered button across all columns

# # Remove Ingredient button
# remove_ingredient_button = Button(root, text="Remove Ingredient", command=remove_ingredient, width=12, height=2)
# remove_ingredient_button.grid(row=3, column=2, pady=(25, 5))  # Positioned next to the add button

# # Ingredient display label
# ingredient_display = Label(root, text="", anchor=CENTER, justify=CENTER)
# ingredient_display.grid(row=4, column=0, columnspan=7, pady=(5, 15)) 

# # Instructions
# instructions_label = Label(root, text="Instructions:")
# instructions_label.grid(row=5, column=0, sticky="e")
# instructions = Text(root, width=46, height=15)  # Increased height
# instructions.grid(row=5, column=1, columnspan=6, sticky="w")

# # Serving Size and Prep Time frame
# size_prep_frame = Frame(root)
# size_prep_frame.grid(row=6, column=0, columnspan=7, pady=(5, 15))  # Centered frame across columns

# # Serving size
# size_label = Label(size_prep_frame, text="Serving Size:")
# size_label.grid(row=0, column=0, sticky="e")
# serving_size = Entry(size_prep_frame, width=5)
# serving_size.grid(row=0, column=1, sticky="w", padx=(5,40))

# # Prep Time
# prep_label = Label(size_prep_frame, text="Prep Time (minutes):")
# prep_label.grid(row=0, column=2, sticky="e", padx=(5,0))
# prep_time = Entry(size_prep_frame, width=6)
# prep_time.grid(row=0, column=3, sticky="w", padx=(5,0))

# # Tags
# tags_label = Label(root, text="Tags:")
# tags_label.grid(row=7, column=0, sticky="e")
# tags = Entry(root, width=35)
# tags.grid(row=7, column=1, columnspan=6, sticky="w")

# # Buttons alignment
# button_frame = Frame(root)
# button_frame.grid(row=8, column=0, columnspan=7, pady=(10, 0))  # Added a frame to center buttons

# # Add Recipe button
# add_recipe_button = Button(button_frame, text="Add Recipe", command=add_recipe, width=12, height=2)  # Decreased width, increased height
# add_recipe_button.pack(side=LEFT, padx=5)  # Centered button

# # Search Recipe button
# search_recipe_button = Button(button_frame, text="Search Recipe", command=search_recipes, width=12, height=2)  # Decreased width, increased height
# search_recipe_button.pack(side=LEFT, padx=5)  # Centered button

# # Quit button
# quit_button = Button(button_frame, text="Quit", command=quit_program, width=12, height=2)  # Decreased width, increased height
# quit_button.pack(side=LEFT, padx=5)  # Centered button

# center_widgets()
# fetch_recent_recipe()
# root.mainloop()

# conn.close()