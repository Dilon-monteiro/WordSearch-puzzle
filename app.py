import streamlit as st
import random
import string
import os

# --- Constants ---
ALPHABET = string.ascii_uppercase # All uppercase letters for the puzzle

# Common English letter frequencies (simplified for demonstration)
# This will be used for 'smart' filler letters
COMMON_LETTER_FREQUENCIES = {
    'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7, 'S': 6.3, 'H': 6.1, 'R': 6.0,
    'D': 4.3, 'L': 4.0, 'U': 2.8, 'C': 2.8, 'M': 2.4, 'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0,
    'P': 1.9, 'B': 1.5, 'V': 1.0, 'K': 0.8, 'J': 0.2, 'X': 0.1, 'Q': 0.1, 'Z': 0.1
}
# Create a list of letters weighted by frequency for random choice
WEIGHTED_ALPHABET = [letter for letter, freq in COMMON_LETTER_FREQUENCIES.items() for _ in range(int(freq * 10))]
if not WEIGHTED_ALPHABET: # Fallback in case calculation is off
    WEIGHTED_ALPHABET = list(ALPHABET)


# --- Define Genres and their Words ---
GENRE_WORDS = {
    "Select a Genre": "",
    "Animals": "LION,TIGER,BEAR,ELEPHANT,MONKEY,ZEBRA,GIRAFFE,SNAKE,WOLF,FOX,EAGLE,OWL,PANDA,KOALA,FROG,SHARK,DOLPHIN,WHALE,OCTOPUS",
    "Fruits": "APPLE,BANANA,CHERRY,DATES,GRAPE,LEMON,MANGO,ORANGE,PEAR,PLUM,BERRY,KIWI,LIME,PEACH,MELON,AVOCADO,PINEAPPLE",
    "Sports": "SOCCER,BASKETBALL,TENNIS,GOLF,SWIMMING,RUNNING,CYCLING,VOLLEYBALL,BASEBALL,HOCKEY,FOOTBALL,BADMINTON,BOXING,CRICKET",
    "Technology": "PYTHON,STREAMLIT,CODING,COMPUTER,NETWORK,SOFTWARE,HARDWARE,PROGRAMMING,ALGORITHM,DATA,INTERNET,WEBSITE,MOBILE,CLOUD,SECURITY",
    "Countries": "INDIA,USA,CANADA,BRAZIL,GERMANY,FRANCE,JAPAN,CHINA,AUSTRALIA,EGYPT,UK,MEXICO,ITALY,SPAIN,RUSSIA,SOUTHAFRICA,NIGERIA",
    "Food": "PIZZA,BURGER,PASTA,SUSHI,SALAD,SOUP,BREAD,CHEESE,CHOCOLATE,COFFEE,TEA,WATER,JUICE,COOKIE,CAKE,RICE,CHICKEN,FISH"
}

# --- Session State Initialization ---
if 'grid' not in st.session_state:
    st.session_state.grid = []
if 'words_to_find' not in st.session_state:
    st.session_state.words_to_find = {}
if 'placed_words_data' not in st.session_state:
    st.session_state.placed_words_data = {}
if 'found_words_coords' not in st.session_state:
    st.session_state.found_words_coords = []
if 'message' not in st.session_state:
    st.session_state.message = ""

# Initialize widget-linked session state keys with their default values
if 'genre_selector_key' not in st.session_state:
    st.session_state.genre_selector_key = "Animals"
if 'manual_words_input_key' not in st.session_state:
    st.session_state.manual_words_input_key = GENRE_WORDS[st.session_state.genre_selector_key]
if 'grid_rows_key' not in st.session_state:
    st.session_state.grid_rows_key = 15
if 'grid_cols_key' not in st.session_state:
    st.session_state.grid_cols_key = 15
if 'found_word_input_key' not in st.session_state:
    st.session_state.found_word_input_key = ""
# AI feature specific session state initializations
if 'difficulty_key' not in st.session_state:
    st.session_state.difficulty_key = "Medium"
if 'filler_mode_key' not in st.session_state:
    st.session_state.filler_mode_key = "Smart Fillers (Frequency)"


# --- Helper Functions (Updated for AI features) ---

def is_valid_placement(grid, word, r, c, dr, dc):
    """
    Checks if a word can be placed at (r, c) with direction (dr, dc) without conflicts.
    A conflict occurs if the placement goes out of bounds or overwrites an existing
    letter that is different from the current character of the word.
    """
    rows, cols = len(grid), len(grid[0])
    for i, char in enumerate(word):
        nr, nc = r + i * dr, c + i * dc
        if not (0 <= nr < rows and 0 <= nc < cols):
            return False
        if grid[nr][nc] != '' and grid[nr][nc] != char:
            return False
    return True

def calculate_placement_score(grid, word, r, c, dr, dc):
    """
    Calculates a score for a potential word placement.
    Higher score for more intersections with existing words.
    """
    score = 0
    rows, cols = len(grid), len(grid[0])
    for i, char in enumerate(word):
        nr, nc = r + i * dr, c + i * dc
        if 0 <= nr < rows and 0 <= nc < cols: # Check bounds (already done by is_valid_placement, but good for scoring too)
            if grid[nr][nc] == char: # Intersection with a matching letter
                score += 1
            # Could add scores for being near other words, etc.
    return score

def get_filler_letter(mode):
    """Returns a random filler letter based on the selected mode."""
    if mode == "Smart Fillers (Frequency)":
        return random.choice(WEIGHTED_ALPHABET)
    else: # "Random" or any other mode
        return random.choice(ALPHABET)


def place_word(grid, word, r, c, dr, dc):
    """Places a word on the grid and returns the list of coordinates."""
    coords = []
    for i, char in enumerate(word):
        nr, nc = r + i * dr, c + i * dc
        grid[nr][nc] = char
        coords.append((nr, nc))
    return coords

def generate_word_search(words, rows, cols, difficulty_level, filler_mode):
    """
    Generates a word search grid given a list of words and grid dimensions,
    with AI enhancements for placement and fillers.
    """
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    placed_words_data = {}

    # Define all 8 possible directions
    all_directions = [
        (0, 1), (0, -1),   # Horizontal
        (1, 0), (-1, 0),   # Vertical
        (1, 1), (1, -1),   # Diagonal
        (-1, 1), (-1, -1)  # Anti-diagonal
    ]

    # Adjust directions based on difficulty
    if difficulty_level == "Easy":
        # Prioritize horizontal and vertical
        placement_directions = [(0, 1), (1, 0)] * 4 + [(0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    elif difficulty_level == "Medium":
        placement_directions = all_directions
    elif difficulty_level == "Hard":
        # Prioritize diagonals and reverse words
        placement_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)] * 4 + [(0, 1), (0, -1), (1, 0), (-1, 0)]
    else: # Fallback
        placement_directions = all_directions


    words_to_place = sorted(words, key=len, reverse=True) # Prioritize longer words

    for word in words_to_place:
        word = word.upper()
        best_score = -1
        best_attempt = None # (r, c, dr, dc)
        attempts_made = 0
        max_placement_attempts = rows * cols * len(placement_directions) # Increased attempts for better placement

        # Try to find the best placement
        while attempts_made < max_placement_attempts:
            r = random.randint(0, rows - 1)
            c = random.randint(0, cols - 1)
            dr, dc = random.choice(placement_directions) # Use difficulty-adjusted directions

            if is_valid_placement(grid, word, r, c, dr, dc):
                current_score = calculate_placement_score(grid, word, r, c, dr, dc)
                # For hard difficulty, we actively seek high scores (intersections)
                # For easy, we might care less about high scores, or even prefer low scores
                if difficulty_level == "Hard" and current_score > best_score:
                    best_score = current_score
                    best_attempt = (r, c, dr, dc)
                elif difficulty_level == "Easy" and (best_attempt is None or current_score < best_score):
                    # For easy, prefer less intersections (or simply first valid for speed)
                    best_score = current_score
                    best_attempt = (r, c, dr, dc)
                    if best_attempt and current_score == 0: # Found a non-overlapping spot
                        break
                elif difficulty_level == "Medium" and (best_attempt is None or current_score >= best_score):
                    best_score = current_score
                    best_attempt = (r, c, dr, dc)

            attempts_made += 1

        if best_attempt:
            r, c, dr, dc = best_attempt
            word_coords = place_word(grid, word, r, c, dr, dc)
            placed_words_data[word] = word_coords
        else:
            st.warning(f"Could not optimally place word: '{word}'. Placing randomly as fallback.")
            # Fallback to random placement if optimal not found within attempts
            for _ in range(rows * cols * len(all_directions)): # Simple brute-force fallback
                r = random.randint(0, rows - 1)
                c = random.randint(0, cols - 1)
                dr, dc = random.choice(all_directions)
                if is_valid_placement(grid, word, r, c, dr, dc):
                    word_coords = place_word(grid, word, r, c, dr, dc)
                    placed_words_data[word] = word_coords
                    break

    # Fill any remaining empty spaces in the grid with smart/random letters
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '':
                grid[r][c] = get_filler_letter(filler_mode)

    return grid, placed_words_data

# --- render_grid function (No changes, already responsive) ---
def render_grid(grid, found_coords_list):
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
            max-width: 800px;
            margin: auto;
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
            padding-top: 100%;
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
            font-weight: bold;
            font-size: clamp(0.8em, 2vw, 1.2em);
            border-radius: 6px;
            background-color: #e0e0e0;
            color: #333;
            transition: background-color 0.1s ease, transform 0.1s ease;
            box-sizing: border-box;
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
        @media (max-width: 768px) {{
            /* Ensure columns stack on small screens */
            div[data-testid="stVerticalBlock"] > div > div.st-emotion-cache-1cypn85 {{
                flex-direction: column !important;
            }}
            /* Specific targeting for the columns that hold puzzle and words to find */
            div[data-testid="stHorizontalBlock"] {{
                flex-direction: column !important;
            }}

            .grid-container {{
                width: 95vw;
                max-width: none;
            }}
            .grid-cell {{
                font-size: clamp(0.7em, 3vw, 1.1em);
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


# --- Callbacks (Updated to pass AI parameters) ---

def on_genre_change():
    selected_genre = st.session_state.genre_selector_key
    st.session_state.manual_words_input_key = GENRE_WORDS.get(selected_genre, "")

def generate_puzzle_callback():
    words_input = st.session_state.manual_words_input_key
    rows = st.session_state.grid_rows_key
    cols = st.session_state.grid_cols_key
    # Get AI parameters from session state
    difficulty_level = st.session_state.difficulty_key
    filler_mode = st.session_state.filler_mode_key

    words_list = [word.strip().upper() for word in words_input.split(',') if word.strip()]
    if not words_list:
        st.session_state.message = "Please enter some words or select a genre to generate the puzzle!"
        return

    # Pass AI parameters to the generation function
    st.session_state.grid, st.session_state.placed_words_data = \
        generate_word_search(words_list, rows, cols, difficulty_level, filler_mode)
    st.session_state.words_to_find = {word: False for word in words_list}
    st.session_state.found_words_coords = []
    st.session_state.message = "Puzzle generated! Find the words."

def check_found_word():
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

def reset_puzzle_callback():
    st.session_state.grid = []
    st.session_state.words_to_find = {}
    st.session_state.placed_words_data = {}
    st.session_state.found_words_coords = []
    st.session_state.message = "Puzzle reset! Generate a new one."
    # Reset widget-linked session state keys to their initial defaults
    st.session_state.genre_selector_key = "Animals"
    st.session_state.manual_words_input_key = GENRE_WORDS["Animals"]
    st.session_state.grid_rows_key = 15
    st.session_state.grid_cols_key = 15
    st.session_state.found_word_input_key = ""
    st.session_state.difficulty_key = "Medium"
    st.session_state.filler_mode_key = "Smart Fillers (Frequency)"
    st.rerun()


# --- Streamlit App Layout ---
st.set_page_config(layout="wide", page_title="AI WordSearch")

st.title("WordSearch") # Updated title!

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

    # --- AI Specific Controls ---
    st.subheader("Generation Options")
    st.selectbox(
        "Difficulty:",
        options=["Easy", "Medium", "Hard"],
        key="difficulty_key",
        help="Easy: Prioritizes straight lines, less overlaps. Hard: More diagonals, more intersections."
    )
    st.selectbox(
        "Filler Letters:",
        options=["Smart Fillers (Frequency)", "Random"],
        key="filler_mode_key",
        help="Smart: Uses common letter frequencies. Random: Purely random letters."
    )

    st.button(
        "Generate New Puzzle",
        on_click=generate_puzzle_callback,
        type="primary"
    )

    st.markdown("---")
    st.button("Reset Puzzle", on_click=reset_puzzle_callback, help="Clears the current puzzle and found words.")


# Display messages to the user (main content area)
if st.session_state.message:
    st.info(st.session_state.message)

# --- Main content area with two columns: Puzzle (left) and Words to Find (right) ---
col1, col2 = st.columns([3, 1]) # 3 parts for puzzle, 1 part for words to find

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
    generate_puzzle_callback() # Call the generation callback to generate the first puzzle
    st.rerun() # Force a rerun to display the generated grid immediately


# --- Check if all words are found (after all other logic) ---
if st.session_state.words_to_find and all(st.session_state.words_to_find.values()):
    st.balloons()
    st.success("Congratulations! You found all the words!")