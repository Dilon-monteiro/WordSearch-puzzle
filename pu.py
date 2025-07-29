# # # import streamlit as st
# # # import random
# # # import string
# # # import streamlit.components.v1 as components # Make sure this is imported

# # # # --- Custom Component Loading ---
# # # # We'll use the HTML file that's part of the component logic for a more interactive grid
# # # # For a pure Streamlit-only grid (which your original code provides, but without drag-and-drop),
# # # # we don't need components. But since you asked for `experimental_rerun` earlier,
# # # # and implied an interactive grid, I'll provide the component loading for the *future*
# # # # if you decide to go back to the HTML/JS interactive component.
# # # # For *this* specific code (the all-Python one you just provided), the `components` import
# # # # is not strictly necessary for rendering, but it's good to keep if you plan to
# # # # re-integrate the custom component for drag-selection.

# # # _RELEASE = True # Keep this as True for direct HTML file loading

# # # if not _RELEASE:
# # #     # This path is for a local dev server (e.g., webpack) - not applicable for this purely Python version
# # #     _word_search_grid_component = components.declare_component(
# # #         "word_search_grid_component",
# # #         url="http://localhost:3001",
# # #     )
# # # else:
# # #     # This path is for directly loading index.html from the component folder
# # #     # NOTE: Since the current code you provided is pure Python, you DO NOT need this
# # #     # `declare_component` or the `word_search_grid_component` function if you're not using
# # #     # the interactive JS frontend.
# # #     # However, if you *were* to re-introduce the interactive HTML/JS part,
# # #     # then the following lines (corrected as per our last discussion) would be needed.
# # #     import os
# # #     parent_dir = os.path.dirname(os.path.abspath(__file__))
# # #     component_dir = os.path.join(parent_dir, "word_search_component")
# # #     # Uncomment the next line if you re-introduce the custom HTML/JS component
# # #     #_word_search_grid_component = components.declare_component("word_search_grid_component", path=component_dir)


# # # # --- Constants ---
# # # ALPHABET = string.ascii_uppercase # All uppercase letters for the puzzle

# # # # --- Session State Initialization ---
# # # if 'grid' not in st.session_state:
# # #     st.session_state.grid = []
# # # if 'words_to_find' not in st.session_state:
# # #     st.session_state.words_to_find = {}
# # # if 'placed_words_data' not in st.session_state:
# # #     st.session_state.placed_words_data = {}
# # # if 'found_words_coords' not in st.session_state:
# # #     st.session_state.found_words_coords = []
# # # if 'message' not in st.session_state:
# # #     st.session_state.message = ""

# # # # --- Helper Functions (No changes needed in these logic functions) ---

# # # def is_valid_placement(grid, word, r, c, dr, dc):
# # #     rows, cols = len(grid), len(grid[0])
# # #     for i, char in enumerate(word):
# # #         nr, nc = r + i * dr, c + i * dc
# # #         if not (0 <= nr < rows and 0 <= nc < cols):
# # #             return False
# # #         if grid[nr][nc] != '' and grid[nr][nc] != char:
# # #             return False
# # #     return True

# # # def place_word(grid, word, r, c, dr, dc):
# # #     coords = []
# # #     for i, char in enumerate(word):
# # #         nr, nc = r + i * dr, c + i * dc
# # #         grid[nr][nc] = char
# # #         coords.append((nr, nc))
# # #     return coords

# # # def generate_word_search(words, rows, cols):
# # #     grid = [['' for _ in range(cols)] for _ in range(rows)]
# # #     placed_words_data = {}
# # #     directions = [
# # #         (0, 1), (0, -1),
# # #         (1, 0), (-1, 0),
# # #         (1, 1), (1, -1),
# # #         (-1, 1), (-1, -1)
# # #     ]
# # #     words_to_place = sorted(words, key=len, reverse=True)
# # #     for word in words_to_place:
# # #         word = word.upper()
# # #         placed = False
# # #         attempts = 0
# # #         max_attempts = rows * cols * len(directions) * 2
# # #         while not placed and attempts < max_attempts:
# # #             dr, dc = random.choice(directions)
# # #             r = random.randint(0, rows - 1)
# # #             c = random.randint(0, cols - 1)
# # #             if is_valid_placement(grid, word, r, c, dr, dc):
# # #                 word_coords = place_word(grid, word, r, c, dr, dc)
# # #                 placed_words_data[word] = word_coords
# # #                 placed = True
# # #             attempts += 1
# # #         if not placed:
# # #             st.warning(f"Could not place word: '{word}'. Try a larger grid or fewer/shorter words.")
# # #     for r in range(rows):
# # #         for c in range(cols):
# # #             if grid[r][c] == '':
# # #                 grid[r][c] = random.choice(ALPHABET)
# # #     return grid, placed_words_data

# # # # --- MODIFIED render_grid function for Responsiveness ---
# # # def render_grid(grid, found_coords_list):
# # #     rows = len(grid)
# # #     cols = len(grid[0])

# # #     # Dynamic cell size based on grid size and total width
# # #     # A base size in vw (viewport width) that shrinks for larger grids
# # #     # and ensures a minimum size.
# # #     # We want the total width of the grid to fit well. Let's aim for 90-95% of column width.
# # #     # Total column width is around 3 parts of 4 (75%) if using st.columns([3,1])
# # #     # So, cell size should be (0.75 * 100vw) / cols.
# # #     # Or, simpler: calculate based on the number of columns to fill the space.
# # #     # Let's target the grid to be about 95% of its parent container width.
# # #     # (100 / cols) * 0.95 % of the container width per cell.
# # #     # Or simply set a max-width and let cells flex.

# # #     # Option 1: Using flexbox for responsiveness (simpler with fixed height/width inside, but flexes container)
# # #     # This CSS is more adaptive
# # #     st.markdown(f"""
# # #         <style>
# # #         .grid-container {{
# # #             display: grid;
# # #             /* Use a flexible repeat. minmax(min_size, max_size) */
# # #             /* This makes cells try to be 35px, but can shrink if needed */
# # #             grid-template-columns: repeat({cols}, minmax(15px, 1fr)); /* 1fr makes them take equal space, min 15px */
# # #             /* Max width to prevent grid from becoming too stretched on very large screens */
# # #             max-width: 800px; /* Adjust as needed */
# # #             margin: auto; /* Center the grid container */

# # #             border: 2px solid #a0a0a0;
# # #             padding: 5px;
# # #             background-color: #ffffff;
# # #             border-radius: 12px;
# # #             box-shadow: 0 8px 16px rgba(0,0,0,0.2);
# # #             gap: 1px; /* Small gap between cells */
# # #             user-select: none;
# # #             cursor: default;
# # #         }}
# # #         .grid-cell {{
# # #             /* Use padding for proportional height/width based on content or parent */
# # #             /* Or use aspect-ratio for modern browsers for square cells */
# # #             width: 100%; /* Take full width of its grid track */
# # #             padding-top: 100%; /* Makes cell height equal to its width (for a square) */
# # #             position: relative; /* For absolutely positioned content */
# # #             display: flex; /* For centering text */
# # #             justify-content: center;
# # #             align-items: center;
            
# # #             font-family: 'Inter', sans-serif;
# # #             font-weight: bold;
# # #             font-size: clamp(0.8em, 2vw, 1.2em); /* Responsive font size */
            
# # #             border-radius: 6px;
# # #             background-color: #e0e0e0;
# # #             color: #333;
# # #             transition: background-color 0.1s ease, transform 0.1s ease;
# # #             box-sizing: border-box; /* Include padding and border in the element's total width and height */
# # #         }}
# # #         /* Inner div for the actual character, to allow padding-top on parent for square aspect */
# # #         .grid-cell-content {{
# # #             position: absolute;
# # #             top: 0;
# # #             left: 0;
# # #             width: 100%;
# # #             height: 100%;
# # #             display: flex;
# # #             justify-content: center;
# # #             align-items: center;
# # #         }}
# # #         .grid-cell-found {{
# # #             background-color: #4CAF50 !important;
# # #             color: white !important;
# # #             box-shadow: inset 0 0 8px rgba(0, 0, 0, 0.3);
# # #             transform: scale(1.05);
# # #         }}
# # #         /* Ensure columns stack on small screens */
# # #         @media (max-width: 768px) {{
# # #             .st-emotion-cache-1cypn85 {{ /* Target Streamlit column container for small screens */
# # #                 flex-direction: column !important;
# # #             }}
# # #             .grid-container {{
# # #                 width: 95vw; /* Take almost full viewport width */
# # #                 max-width: none; /* No max width restriction on small screens */
# # #             }}
# # #         }}
# # #         </style>
# # #     """, unsafe_allow_html=True)


# # #     grid_html = f"<div class='grid-container'>"

# # #     for r_idx in range(rows):
# # #         for c_idx in range(cols):
# # #             char = grid[r_idx][c_idx]
# # #             cell_class = "grid-cell"
# # #             if (r_idx, c_idx) in found_coords_list:
# # #                 cell_class += " grid-cell-found"

# # #             # Added an inner div to handle the square aspect ratio properly
# # #             grid_html += f"<div class='{cell_class}'><div class='grid-cell-content'>{char}</div></div>"
# # #     grid_html += "</div>"
# # #     st.markdown(grid_html, unsafe_allow_html=True)


# # # def generate_puzzle_callback(words_input, rows, cols):
# # #     words_list = [word.strip().upper() for word in words_input.split(',') if word.strip()]
# # #     if not words_list:
# # #         st.session_state.message = "Please enter some words to generate the puzzle!"
# # #         return

# # #     st.session_state.grid, st.session_state.placed_words_data = generate_word_search(words_list, rows, cols)
# # #     st.session_state.words_to_find = {word: False for word in words_list}
# # #     st.session_state.found_words_coords = []
# # #     st.session_state.message = "Puzzle generated! Find the words."
# # #     st.rerun() # Use st.rerun() instead of experimental_rerun()

# # # def check_found_word(found_word_input, words_to_find_dict, placed_words_data):
# # #     found_word_input = found_word_input.strip().upper()
# # #     if not found_word_input:
# # #         st.session_state.message = "Please type a word to check."
# # #         return

# # #     if found_word_input in words_to_find_dict:
# # #         if not words_to_find_dict[found_word_input]:
# # #             st.session_state.words_to_find[found_word_input] = True
# # #             if found_word_input in placed_words_data:
# # #                 st.session_state.found_words_coords.extend(placed_words_data[found_word_input])
# # #             st.session_state.message = f"Congratulations! You found '{found_word_input}'!"
# # #             st.rerun() # Use st.rerun()
# # #         else:
# # #             st.session_state.message = f"You already found '{found_word_input}'."
# # #     else:
# # #         st.session_state.message = f"'{found_word_input}' is not in the list or not placed in the puzzle."

# # # # --- Streamlit App Layout ---
# # # # Use 'wide' layout and set page title
# # # st.set_page_config(layout="wide", page_title="Interactive Word Search")

# # # st.title("Word Search Puzzle Generator & Solver")

# # # with st.sidebar:
# # #     st.header("Settings")
# # #     words_input = st.text_area(
# # #         "Enter words (comma-separated):",
# # #         "PYTHON,STREAMLIT,CODING,PUZZLE,GENERATOR,DEVELOPER,AI,MOBILE,WEB",
# # #         height=150
# # #     )
# # #     grid_rows = st.slider("Grid Rows:", min_value=10, max_value=30, value=15)
# # #     grid_cols = st.slider("Grid Columns:", min_value=10, max_value=30, value=15)

# # #     st.button(
# # #         "Generate New Puzzle",
# # #         on_click=generate_puzzle_callback,
# # #         args=(words_input, grid_rows, grid_cols),
# # #         type="primary"
# # #     )

# # # # Display messages to the user
# # # if st.session_state.message:
# # #     st.info(st.session_state.message) # Use st.info for messages

# # # col1, col2 = st.columns([3, 1])

# # # with col1:
# # #     st.subheader("The Puzzle")
# # #     if st.session_state.grid:
# # #         render_grid(st.session_state.grid, st.session_state.found_words_coords)
# # #     else:
# # #         st.info("Enter words and click 'Generate New Puzzle' to start!")

# # # with col2:
# # #     st.subheader("Words to Find")
# # #     if st.session_state.words_to_find:
# # #         words_found_count = 0
# # #         for word, found in st.session_state.words_to_find.items():
# # #             if found:
# # #                 st.markdown(f"<span style='text-decoration: line-through; color: green;'>{word}</span>", unsafe_allow_html=True)
# # #                 words_found_count += 1
# # #             else:
# # #                 st.write(word)
# # #         st.write(f"Words Found: {words_found_count} / {len(st.session_state.words_to_find)}")
# # #     else:
# # #         st.info("No words to find yet. Generate a puzzle!")

# # #     st.subheader("Check Your Word")
# # #     found_word_input = st.text_input("Type a word you found:", key="found_word_input")
# # #     st.button(
# # #         "Check Word",
# # #         on_click=check_found_word,
# # #         args=(found_word_input, st.session_state.words_to_find, st.session_state.placed_words_data)
# # #     )

# # # # Initial puzzle generation on first load if the grid is empty
# # # if not st.session_state.grid:
# # #     generate_puzzle_callback(words_input="PYTHON,STREAMLIT,CODING,PUZZLE", rows=15, cols=15)
# # #     st.rerun() # Ensure the grid renders immediately

# # # # Check if all words are found
# # # if st.session_state.words_to_find and all(st.session_state.words_to_find.values()):
# # #     st.balloons()
# # #     st.success("Congratulations! You found all the words!")

# # # # Optional: Button to reset the puzzle (moved to sidebar for better layout)
# # # with st.sidebar:
# # #     st.markdown("---")
# # #     if st.button("Reset Puzzle"):
# # #         st.session_state.grid = []
# # #         st.session_state.words_to_find = {}
# # #         st.session_state.placed_words_data = {}
# # #         st.session_state.found_words_coords = []
# # #         st.session_state.message = "Puzzle reset! Generate a new one."
# # #         st.rerun()

# import streamlit as st
# import random
# import string
# import os

# # --- Constants ---
# ALPHABET = string.ascii_uppercase # All uppercase letters for the puzzle

# # --- Define Genres and their Words ---
# GENRE_WORDS = {
#     "Select a Genre": "", # Default empty option for selectbox
#     "Animals": "LION,TIGER,BEAR,ELEPHANT,MONKEY,ZEBRA,GIRAFFE,SNAKE,WOLF,FOX,EAGLE,OWL,PANDA,KOALA,FROG,SHARK,DOLPHIN,WHALE,OCTOPUS",
#     "Fruits": "APPLE,BANANA,CHERRY,DATES,GRAPE,LEMON,MANGO,ORANGE,PEAR,PLUM,BERRY,KIWI,LIME,PEACH,MELON,AVOCADO,PINEAPPLE",
#     "Sports": "SOCCER,BASKETBALL,TENNIS,GOLF,SWIMMING,RUNNING,CYCLING,VOLLEYBALL,BASEBALL,HOCKEY,FOOTBALL,BADMINTON,BOXING,CRICKET",
#     "Technology": "PYTHON,STREAMLIT,CODING,COMPUTER,NETWORK,SOFTWARE,HARDWARE,PROGRAMMING,ALGORITHM,DATA,INTERNET,WEBSITE,MOBILE,CLOUD,SECURITY",
#     "Countries": "INDIA,USA,CANADA,BRAZIL,GERMANY,FRANCE,JAPAN,CHINA,AUSTRALIA,EGYPT,UK,MEXICO,ITALY,SPAIN,RUSSIA,SOUTHAFRICA,NIGERIA",
#     "Food": "PIZZA,BURGER,PASTA,SUSHI,SALAD,SOUP,BREAD,CHEESE,CHOCOLATE,COFFEE,TEA,WATER,JUICE,COOKIE,CAKE,RICE,CHICKEN,FISH"
# }

# # --- Session State Initialization ---
# # Initialize session state variables to store the puzzle state across reruns.
# # IMPORTANT: All session state variables linked to widgets (via `key=`)
# # MUST be initialized *here*, at the very top, before those widgets are rendered.
# if 'grid' not in st.session_state:
#     st.session_state.grid = [] # The 2D list representing the puzzle grid
# if 'words_to_find' not in st.session_state:
#     st.session_state.words_to_find = {} # Dictionary of {word: True/False} found status
# if 'placed_words_data' not in st.session_state:
#     st.session_state.placed_words_data = {} # Dictionary of {word: [(r,c), ...]} coordinates
# if 'found_words_coords' not in st.session_state:
#     st.session_state.found_words_coords = [] # Flat list of all (row, col) tuples for found words
# if 'message' not in st.session_state:
#     st.session_state.message = "" # Messages to display to the user

# # Initialize widget-linked session state keys with their default values
# # These defaults ensure the widgets have a value on the very first run.
# if 'genre_selector_key' not in st.session_state:
#     st.session_state.genre_selector_key = "Animals" # Default genre to start with
# if 'manual_words_input_key' not in st.session_state:
#     # Set default words based on the initial genre, this runs ONCE.
#     st.session_state.manual_words_input_key = GENRE_WORDS[st.session_state.genre_selector_key]
# if 'grid_rows_key' not in st.session_state:
#     st.session_state.grid_rows_key = 15 # Default value for rows slider
# if 'grid_cols_key' not in st.session_state:
#     st.session_state.grid_cols_key = 15 # Default value for cols slider
# if 'found_word_input_key' not in st.session_state:
#     st.session_state.found_word_input_key = "" # Default for the word input box


# # --- Helper Functions ---

# def is_valid_placement(grid, word, r, c, dr, dc):
#     """Checks if a word can be placed without conflicts or going out of bounds."""
#     rows, cols = len(grid), len(grid[0])
#     for i, char in enumerate(word):
#         nr, nc = r + i * dr, c + i * dc
#         if not (0 <= nr < rows and 0 <= nc < cols):
#             return False
#         if grid[nr][nc] != '' and grid[nr][nc] != char:
#             return False
#     return True

# def place_word(grid, word, r, c, dr, dc):
#     """Places a word on the grid and returns its coordinates."""
#     coords = []
#     for i, char in enumerate(word):
#         nr, nc = r + i * dr, c + i * dc
#         grid[nr][nc] = char
#         coords.append((nr, nc))
#     return coords

# def generate_word_search(words, rows, cols):
#     """Generates a word search grid, places words, and fills empty cells."""
#     grid = [['' for _ in range(cols)] for _ in range(rows)]
#     placed_words_data = {}
#     directions = [
#         (0, 1), (0, -1), (1, 0), (-1, 0),
#         (1, 1), (1, -1), (-1, 1), (-1, -1)
#     ]
#     words_to_place = sorted(words, key=len, reverse=True)

#     for word in words_to_place:
#         word = word.upper()
#         placed = False
#         attempts = 0
#         max_attempts = rows * cols * len(directions) * 2

#         while not placed and attempts < max_attempts:
#             dr, dc = random.choice(directions)
#             r = random.randint(0, rows - 1)
#             c = random.randint(0, cols - 1)
#             if is_valid_placement(grid, word, r, c, dr, dc):
#                 word_coords = place_word(grid, word, r, c, dr, dc)
#                 placed_words_data[word] = word_coords
#                 placed = True
#             attempts += 1
#         if not placed:
#             st.warning(f"Could not place word: '{word}'. Try a larger grid or fewer/shorter words.")

#     for r in range(rows):
#         for c in range(cols):
#             if grid[r][c] == '':
#                 grid[r][c] = random.choice(ALPHABET)
#     return grid, placed_words_data

# # --- render_grid function for Responsiveness ---
# def render_grid(grid, found_coords_list):
#     """Renders the word search grid using Streamlit's markdown and responsive CSS."""
#     rows = len(grid)
#     cols = len(grid[0])

#     st.markdown(f"""
#         <style>
#         body {{
#             font-family: 'Inter', sans-serif;
#             background-color: #f0f2f5;
#             color: #333;
#         }}
#         .grid-container {{
#             display: grid;
#             grid-template-columns: repeat({cols}, minmax(15px, 1fr));
#             max-width: 800px;
#             margin: auto;
#             border: 2px solid #a0a0a0;
#             padding: 5px;
#             background-color: #ffffff;
#             border-radius: 12px;
#             box-shadow: 0 8px 16px rgba(0,0,0,0.2);
#             gap: 1px;
#             user-select: none;
#             cursor: default;
#         }}
#         .grid-cell {{
#             width: 100%;
#             padding-top: 100%; /* Makes height equal to width */
#             position: relative;
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             font-weight: bold;
#             font-size: clamp(0.8em, 2vw, 1.2em);
#             border-radius: 6px;
#             background-color: #e0e0e0;
#             color: #333;
#             transition: background-color 0.1s ease, transform 0.1s ease;
#             box-sizing: border-box;
#         }}
#         .grid-cell-content {{
#             position: absolute;
#             top: 0;
#             left: 0;
#             width: 100%;
#             height: 100%;
#             display: flex;
#             justify-content: center;
#             align-items: center;
#         }}
#         .grid-cell-found {{
#             background-color: #4CAF50 !important;
#             color: white !important;
#             box-shadow: inset 0 0 8px rgba(0, 0, 0, 0.3);
#             transform: scale(1.05);
#         }}
#         @media (max-width: 768px) {{
#             /* Target Streamlit's internal column div for stacking on mobile */
#             /* This class might need verification by inspecting your app's HTML */
#             div[data-testid="stVerticalBlock"] > div > div.st-emotion-cache-1cypn85 {{
#                 flex-direction: column !important;
#             }}
#             .grid-container {{
#                 width: 95vw;
#                 max-width: none;
#             }}
#             .grid-cell {{
#                 font-size: clamp(0.7em, 3vw, 1.1em);
#             }}
#         }}
#         </style>
#     """, unsafe_allow_html=True)

#     grid_html = f"<div class='grid-container'>"
#     for r_idx in range(rows):
#         for c_idx in range(cols):
#             char = grid[r_idx][c_idx]
#             cell_class = "grid-cell"
#             if (r_idx, c_idx) in found_coords_list:
#                 cell_class += " grid-cell-found"
#             grid_html += f"<div class='{cell_class}'><div class='grid-cell-content'>{char}</div></div>"
#     grid_html += "</div>"
#     st.markdown(grid_html, unsafe_allow_html=True)



# # --- Callbacks ---
# def on_genre_change():
#     selected_genre = st.session_state.genre_selector_key
#     st.session_state.manual_words_input_key = GENRE_WORDS.get(selected_genre, "")

# def generate_puzzle_callback():
#     words_input = st.session_state.manual_words_input_key
#     rows = st.session_state.grid_rows_key
#     cols = st.session_state.grid_cols_key

#     words_list = [word.strip().upper() for word in words_input.split(',') if word.strip()]
#     if not words_list:
#         st.session_state.message = "Please enter some words or select a genre to generate the puzzle!"
#         return

#     st.session_state.grid, st.session_state.placed_words_data = generate_word_search(words_list, rows, cols)
#     st.session_state.words_to_find = {word: False for word in words_list}
#     st.session_state.found_words_coords = []
#     st.session_state.message = "Puzzle generated! Find the words."

# def check_found_word():
#     found_word_input = st.session_state.found_word_input_key.strip().upper()
#     words_to_find_dict = st.session_state.words_to_find
#     placed_words_data = st.session_state.placed_words_data

#     if not found_word_input:
#         st.session_state.message = "Please type a word to check."
#         return

#     if found_word_input in words_to_find_dict:
#         if not words_to_find_dict[found_word_input]:
#             st.session_state.words_to_find[found_word_input] = True
#             if found_word_input in placed_words_data:
#                 st.session_state.found_words_coords.extend(placed_words_data[found_word_input])
#             st.session_state.message = f"Congratulations! You found '{found_word_input}'!"
#         else:
#             st.session_state.message = f"You already found '{found_word_input}'."
#     else:
#         st.session_state.message = f"'{found_word_input}' is not in the list or not placed in the puzzle."

# # --- NEW Callback for Reset Button ---
# def reset_puzzle_callback():
#     st.session_state.grid = []
#     st.session_state.words_to_find = {}
#     st.session_state.placed_words_data = {}
#     st.session_state.found_words_coords = []
#     st.session_state.message = "Puzzle reset! Generate a new one."
#     # Reset widget-linked session state keys to their initial defaults
#     st.session_state.genre_selector_key = "Animals" # Set to default genre
#     st.session_state.manual_words_input_key = GENRE_WORDS["Animals"] # Reset words
#     st.session_state.grid_rows_key = 15 # Reset sliders
#     st.session_state.grid_cols_key = 15
#     st.session_state.found_word_input_key = "" # Clear text input
#     st.rerun() # Force a complete rerun from scratch

# # --- Streamlit App Layout ---
# st.set_page_config(layout="wide", page_title="Interactive Word Search")

# st.title("Word Search Puzzle Generator & Solver")

# # --- Sidebar for Settings and Words to Find ---
# with st.sidebar:
#     st.header("Puzzle Settings")

#     st.selectbox(
#         "Choose a Word Genre:",
#         options=list(GENRE_WORDS.keys()),
#         key="genre_selector_key",
#         on_change=on_genre_change,
#         help="Select a predefined category of words."
#     )

#     st.text_area(
#         "Or Enter Custom Words (comma-separated):",
#         key="manual_words_input_key",
#         height=150,
#         help="Enter your own words here. This will override words from genre selection."
#     )

#     st.subheader("Grid Dimensions")
#     st.slider("Grid Rows:", min_value=10, max_value=30, value=st.session_state.grid_rows_key, key="grid_rows_key")
#     st.slider("Grid Columns:", min_value=10, max_value=30, value=st.session_state.grid_cols_key, key="grid_cols_key")

#     st.button(
#         "Generate New Puzzle",
#         on_click=generate_puzzle_callback,
#         type="primary"
#     )

#     st.markdown("---")

#     st.header("Words to Find")
#     if st.session_state.words_to_find:
#         words_found_count = 0
#         for word, found in st.session_state.words_to_find.items():
#             if found:
#                 st.markdown(f"<span style='text-decoration: line-through; color: green;'>{word}</span>", unsafe_allow_html=True)
#                 words_found_count += 1
#             else:
#                 st.write(word)
#         st.write(f"Words Found: {words_found_count} / {len(st.session_state.words_to_find)}")
#     else:
#         st.info("No words to find yet. Generate a puzzle!")

#     st.subheader("Check Your Word")
#     st.text_input(
#         "Type a word you found:",
#         key="found_word_input_key"
#     )
#     st.button(
#         "Check Word",
#         on_click=check_found_word
#     )

#     st.markdown("---")
#     # Call the new reset_puzzle_callback function on button click
#     st.button("Reset Puzzle", on_click=reset_puzzle_callback, help="Clears the current puzzle and found words.")


# # Display messages to the user (main content area)
# if st.session_state.message:
#     st.info(st.session_state.message)

# # Main content area for the puzzle itself
# st.subheader("The Puzzle")
# if st.session_state.grid:
#     render_grid(st.session_state.grid, st.session_state.found_words_coords)
# else:
#     st.info("Choose words/genre and click 'Generate New Puzzle' to start!")

# # --- Initial Puzzle Generation on First Load ---
# if not st.session_state.grid:
#     # Trigger the generation callback (it reads values from session state, which are already initialized)
#     generate_puzzle_callback()
#     st.rerun() # Force a rerun to display the generated grid immediately


# # --- Check if all words are found (after all other logic) ---
# if st.session_state.words_to_find and all(st.session_state.words_to_find.values()):
#     st.balloons()
#     st.success("Congratulations! You found all the words!")

import streamlit as st
import random
import string
import os

# --- Constants ---
ALPHABET = string.ascii_uppercase # All uppercase letters for the puzzle

# --- Define Genres and their Words ---
GENRE_WORDS = {
    "Select a Genre": "", # Default empty option for selectbox
    "Animals": "LION,TIGER,BEAR,ELEPHANT,MONKEY,ZEBRA,GIRAFFE,SNAKE,WOLF,FOX,EAGLE,OWL,PANDA,KOALA,FROG,SHARK,DOLPHIN,WHALE,OCTOPUS",
    "Fruits": "APPLE,BANANA,CHERRY,DATES,GRAPE,LEMON,MANGO,ORANGE,PEAR,PLUM,BERRY,KIWI,LIME,PEACH,MELON,AVOCADO,PINEAPPLE",
    "Sports": "SOCCER,BASKETBALL,TENNIS,GOLF,SWIMMING,RUNNING,CYCLING,VOLLEYBALL,BASEBALL,HOCKEY,FOOTBALL,BADMINTON,BOXING,CRICKET",
    "Technology": "PYTHON,STREAMLIT,CODING,COMPUTER,NETWORK,SOFTWARE,HARDWARE,PROGRAMMING,ALGORITHM,DATA,INTERNET,WEBSITE,MOBILE,CLOUD,SECURITY",
    "Countries": "INDIA,USA,CANADA,BRAZIL,GERMANY,FRANCE,JAPAN,CHINA,AUSTRALIA,EGYPT,UK,MEXICO,ITALY,SPAIN,RUSSIA,SOUTHAFRICA,NIGERIA",
    "Food": "PIZZA,BURGER,PASTA,SUSHI,SALAD,SOUP,BREAD,CHEESE,CHOCOLATE,COFFEE,TEA,WATER,JUICE,COOKIE,CAKE,RICE,CHICKEN,FISH"
}

# --- Session State Initialization ---
# Initialize session state variables.
# IMPORTANT: All session state variables linked to widgets (via `key=`)
# MUST be initialized *here*, at the very top, before those widgets are rendered.
if 'grid' not in st.session_state:
    st.session_state.grid = [] # The 2D list representing the puzzle grid
if 'words_to_find' not in st.session_state:
    st.session_state.words_to_find = {} # Dictionary of {word: True/False} found status
if 'placed_words_data' not in st.session_state:
    st.session_state.placed_words_data = {} # Dictionary of {word: [(r,c), ...]} coordinates
if 'found_words_coords' not in st.session_state:
    st.session_state.found_words_coords = [] # Flat list of all (row, col) tuples for found words
if 'message' not in st.session_state:
    st.session_state.message = "" # Messages to display to the user

# Initialize widget-linked session state keys with their default values
if 'genre_selector_key' not in st.session_state:
    st.session_state.genre_selector_key = "Animals" # Default genre to start with
if 'manual_words_input_key' not in st.session_state:
    # Set default words based on the initial genre.
    st.session_state.manual_words_input_key = GENRE_WORDS[st.session_state.genre_selector_key]
if 'grid_rows_key' not in st.session_state:
    st.session_state.grid_rows_key = 15 # Default value for rows slider
if 'grid_cols_key' not in st.session_state:
    st.session_state.grid_cols_key = 15 # Default value for cols slider
if 'found_word_input_key' not in st.session_state:
    st.session_state.found_word_input_key = "" # Default for the word input box


# --- Helper Functions ---

def is_valid_placement(grid, word, r, c, dr, dc):
    """Checks if a word can be placed without conflicts or going out of bounds."""
    rows, cols = len(grid), len(grid[0])
    for i, char in enumerate(word):
        nr, nc = r + i * dr, c + i * dc
        if not (0 <= nr < rows and 0 <= nc < cols):
            return False
        if grid[nr][nc] != '' and grid[nr][nc] != char:
            return False
    return True

def place_word(grid, word, r, c, dr, dc):
    """Places a word on the grid and returns its coordinates."""
    coords = []
    for i, char in enumerate(word):
        nr, nc = r + i * dr, c + i * dc
        grid[nr][nc] = char
        coords.append((nr, nc))
    return coords

def generate_word_search(words, rows, cols):
    """Generates a word search grid, places words, and fills empty cells."""
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    placed_words_data = {}
    directions = [
        (0, 1), (0, -1), (1, 0), (-1, 0),
        (1, 1), (1, -1), (-1, 1), (-1, -1)
    ]
    words_to_place = sorted(words, key=len, reverse=True)

    for word in words_to_place:
        word = word.upper()
        placed = False
        attempts = 0
        max_attempts = rows * cols * len(directions) * 2

        while not placed and attempts < max_attempts:
            dr, dc = random.choice(directions)
            r = random.randint(0, rows - 1)
            c = random.randint(0, cols - 1)
            if is_valid_placement(grid, word, r, c, dr, dc):
                word_coords = place_word(grid, word, r, c, dr, dc)
                placed_words_data[word] = word_coords
                placed = True
            attempts += 1
        if not placed:
            st.warning(f"Could not place word: '{word}'. Try a larger grid or fewer/shorter words.")

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '':
                grid[r][c] = random.choice(ALPHABET)
    return grid, placed_words_data

# --- render_grid function for Responsiveness ---
def render_grid(grid, found_coords_list):
    """Renders the word search grid using Streamlit's markdown and responsive CSS."""
    rows = len(grid)
    cols = len(grid[0])

    st.markdown(f"""
        <style>
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #f0f2f5;
            color: #333;
        }}
        .grid-container {{
            display: grid;
            grid-template-columns: repeat({cols}, minmax(15px, 1fr));
            max-width: 800px; /* Limits max width on large screens */
            margin: auto; /* Centers the grid */
            border: 2px solid #a0a0a0;
            padding: 5px;
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            gap: 1px;
            user-select: none;
            cursor: default;
        }}
        .grid-cell {{
            width: 100%;
            padding-top: 100%; /* Makes height equal to width */
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
            font-weight: bold;
            font-size: clamp(0.8em, 2vw, 1.2em); /* Responsive font size */
            border-radius: 6px;
            background-color: #e0e0e0;
            color: #333;
            transition: background-color 0.1s ease, transform 0.1s ease;
            box-sizing: border-box; /* Include padding and border in the element's total size */
        }}
        .grid-cell-content {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .grid-cell-found {{
            background-color: #4CAF50 !important;
            color: white !important;
            box-shadow: inset 0 0 8px rgba(0, 0, 0, 0.3);
            transform: scale(1.05);
        }}
        /* Media query for small screens (e.g., mobile phones) */
        @media (max-width: 768px) {{
            /* Target Streamlit's internal column div for stacking on mobile */
            /* This class might need verification by inspecting your app's HTML in dev tools */
            div[data-testid="stVerticalBlock"] > div > div.st-emotion-cache-1cypn85 {{ /* Common class */
                flex-direction: column !important;
            }}
            .grid-container {{
                width: 95vw; /* Take almost full viewport width on mobile */
                max-width: none; /* No max-width restriction on small screens */
            }}
            .grid-cell {{
                font-size: clamp(0.7em, 3vw, 1.1em); /* Adjust font size for smaller screens */
            }}
        }}
        </style>
    """, unsafe_allow_html=True)

    grid_html = f"<div class='grid-container'>"
    for r_idx in range(rows):
        for c_idx in range(cols):
            char = grid[r_idx][c_idx]
            cell_class = "grid-cell"
            if (r_idx, c_idx) in found_coords_list:
                cell_class += " grid-cell-found"
            grid_html += f"<div class='{cell_class}'><div class='grid-cell-content'>{char}</div></div>"
    grid_html += "</div>"
    st.markdown(grid_html, unsafe_allow_html=True)


# --- Callbacks ---

def on_genre_change():
    """Callback when genre changes. Updates manual_words_input_key with genre words."""
    selected_genre = st.session_state.genre_selector_key
    st.session_state.manual_words_input_key = GENRE_WORDS.get(selected_genre, "")

def generate_puzzle_callback():
    """Generates the puzzle using words from selected genre or manual input."""
    words_input = st.session_state.manual_words_input_key
    rows = st.session_state.grid_rows_key
    cols = st.session_state.grid_cols_key

    words_list = [word.strip().upper() for word in words_input.split(',') if word.strip()]
    if not words_list:
        st.session_state.message = "Please enter some words or select a genre to generate the puzzle!"
        return

    st.session_state.grid, st.session_state.placed_words_data = generate_word_search(words_list, rows, cols)
    st.session_state.words_to_find = {word: False for word in words_list}
    st.session_state.found_words_coords = []
    st.session_state.message = "Puzzle generated! Find the words."

def check_found_word():
    """Checks the typed word against the puzzle's word list."""
    found_word_input = st.session_state.found_word_input_key.strip().upper()
    words_to_find_dict = st.session_state.words_to_find
    placed_words_data = st.session_state.placed_words_data

    if not found_word_input:
        st.session_state.message = "Please type a word to check."
        return

    if found_word_input in words_to_find_dict:
        if not words_to_find_dict[found_word_input]:
            st.session_state.words_to_find[found_word_input] = True
            if found_word_input in placed_words_data:
                st.session_state.found_words_coords.extend(placed_words_data[found_word_input])
            st.session_state.message = f"Congratulations! You found '{found_word_input}'!"
        else:
            st.session_state.message = f"You already found '{found_word_input}'."
    else:
        st.session_state.message = f"'{found_word_input}' is not in the list or not placed in the puzzle."

# --- NEW Callback for Reset Button (to handle widget state resets) ---
def reset_puzzle_callback():
    st.session_state.grid = []
    st.session_state.words_to_find = {}
    st.session_state.placed_words_data = {}
    st.session_state.found_words_coords = []
    st.session_state.message = "Puzzle reset! Generate a new one."
    # Reset widget-linked session state keys to their initial defaults
    st.session_state.genre_selector_key = "Animals" # Reset genre selector to default
    st.session_state.manual_words_input_key = GENRE_WORDS["Animals"] # Reset words to default genre's words
    st.session_state.grid_rows_key = 15 # Reset sliders to default
    st.session_state.grid_cols_key = 15
    st.session_state.found_word_input_key = "" # Clear text input
    st.rerun() # Force a complete rerun from scratch


# --- Streamlit App Layout ---
st.set_page_config(layout="wide", page_title="Interactive Word Search")

st.title("Word Search Puzzle Generator & Solver")

# --- Sidebar for Puzzle Settings ---
with st.sidebar:
    st.header("Puzzle Settings")

    st.selectbox(
        "Choose a Word Genre:",
        options=list(GENRE_WORDS.keys()),
        key="genre_selector_key",
        on_change=on_genre_change,
        help="Select a predefined category of words."
    )

    st.text_area(
        "Or Enter Custom Words (comma-separated):",
        key="manual_words_input_key",
        height=150,
        help="Enter your own words here. This will override words from genre selection."
    )

    st.subheader("Grid Dimensions")
    st.slider("Grid Rows:", min_value=10, max_value=30, value=st.session_state.grid_rows_key, key="grid_rows_key")
    st.slider("Grid Columns:", min_value=10, max_value=30, value=st.session_state.grid_cols_key, key="grid_cols_key")

    st.button(
        "Generate New Puzzle",
        on_click=generate_puzzle_callback,
        type="primary"
    )

    st.markdown("---") # Separator in sidebar for reset button
    # Reset button remains in sidebar
    st.button("Reset Puzzle", on_click=reset_puzzle_callback, help="Clears the current puzzle and found words.")


# Display messages to the user (main content area)
if st.session_state.message:
    st.info(st.session_state.message)

# --- Main content area with two columns ---
# Puzzle on left (3 parts), Words to Find on right (1 part)
col1, col2 = st.columns([3, 1])

with col1: # Left column for the puzzle
    st.subheader("The Puzzle")
    if st.session_state.grid:
        render_grid(st.session_state.grid, st.session_state.found_words_coords)
    else:
        st.info("Choose words/genre and click 'Generate New Puzzle' to start!")

with col2: # Right column for Words to Find and Check Word input
    st.subheader("Words to Find")
    if st.session_state.words_to_find:
        words_found_count = 0
        for word, found in st.session_state.words_to_find.items():
            if found:
                st.markdown(f"<span style='text-decoration: line-through; color: green;'>{word}</span>", unsafe_allow_html=True)
                words_found_count += 1
            else:
                st.write(word)
        st.write(f"Words Found: {words_found_count} / {len(st.session_state.words_to_find)}")
    else:
        st.info("No words to find yet. Generate a puzzle!")

    st.subheader("Check Your Word")
    st.text_input(
        "Type a word you found:",
        key="found_word_input_key"
    )
    st.button(
        "Check Word",
        on_click=check_found_word
    )


# --- Initial Puzzle Generation on First Load ---
# This block runs only once when the app is first loaded and `st.session_state.grid` is empty.
# It relies on the default values for widget-linked session state already set at the top.
if not st.session_state.grid:
    generate_puzzle_callback() # Call the generation callback (it reads values from session state)
    st.rerun() # Force a rerun to display the generated grid immediately


# --- Check if all words are found (after all other logic) ---
# This check will run on every rerun, displaying congratulations if all words are found.
if st.session_state.words_to_find and all(st.session_state.words_to_find.values()):
    st.balloons()
    st.success("Congratulations! You found all the words!")