from PIL import Image, ImageDraw, ImageFont
import csv
import os

# ==============================================================================
# >> USER CONFIGURATION <<
# ==============================================================================
TOPIC_COORD_X = 210
TOPIC_COORD_Y = 1540
FONT_SIZE = 30
FONT_COLOR = "black"
FONT_PATH = "arial.ttf" 
BOLD_STRENGTH = 1
# ==============================================================================


def sanitize_filename(name):
    """Removes characters that are invalid in Windows filenames."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '')
    return name

def load_font(font_path, font_size):
    """Tries to load a specified font, falling back to a default if not found."""
    try:
        return ImageFont.truetype(font_path, font_size)
    except IOError:
        print(f"Warning: Font '{font_path}' not found. Using default font.")
        return ImageFont.load_default()

def read_csv_with_topic(csv_path):
    """Reads the topic from the first line and the answers from the rest of the CSV."""
    topic = "No Topic Found"
    answers = []
    try:
        print(f"1. Reading answers and topic from '{csv_path}'...")
        with open(csv_path, mode='r') as infile:
            topic = infile.readline().strip()
            reader = csv.DictReader(infile)
            for row in reader:
                answers.append({
                    'question': int(row['Question']),
                    'answer': row['Answer'].lower()
                })
        print(f"   - Topic found: '{topic}'")
        print(f"   - Successfully loaded {len(answers)} answers.")
        return topic, answers
    except FileNotFoundError:
        print(f"   - FATAL ERROR: The file '{csv_path}' was not found.")
        return None, None
    except Exception as e:
        print(f"   - FATAL ERROR: Could not read the CSV file. Error: {e}")
        return None, None

def mark_omr_and_create_pdf(topic, answers_data, omr_template_path):
    """Marks a blank OMR sheet and saves the final result directly as a PDF."""
    if not answers_data: return

    print(f"2. Marking OMR sheet...")
    try:
        omr_image = Image.open(omr_template_path)
    except FileNotFoundError:
        print(f"   - ERROR: The OMR template '{omr_template_path}' was not found.")
        return
        
    draw = ImageDraw.Draw(omr_image)
    
    # Write the bold topic name
    print("   - Writing bold topic name onto the sheet...")
    font = load_font(FONT_PATH, FONT_SIZE)
    x, y = TOPIC_COORD_X, TOPIC_COORD_Y
    draw.text((x + BOLD_STRENGTH, y), topic, font=font, fill=FONT_COLOR)
    draw.text((x, y + BOLD_STRENGTH), topic, font=font, fill=FONT_COLOR)
    draw.text((x + BOLD_STRENGTH, y + BOLD_STRENGTH), topic, font=font, fill=FONT_COLOR)
    draw.text((x, y), topic, font=font, fill=FONT_COLOR)
    
    # Mark the bubbles
    print("   - Marking answer bubbles...")
    radius, anchor_y_q1_o1, dx_option, dy_question, section_a_end_index, section_b_gap, column_starts_x = (
        9, 91, 27, 25.75, 34, 25, [533, 694, 859, 1025]
    )
    option_map = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    for item in answers_data:
        q_num, answer = item['question'], item['answer']
        if answer not in option_map: continue
        opt_num = option_map[answer]
        column_index = (q_num - 1) // 50
        row_index_in_column = (q_num - 1) % 50
        if column_index >= len(column_starts_x): continue
        current_x = column_starts_x[column_index] + ((opt_num - 1) * dx_option)
        current_y = anchor_y_q1_o1 + (row_index_in_column * dy_question)
        if row_index_in_column > section_a_end_index:
            current_y += section_b_gap
        bounding_box = [int(current_x - radius), int(current_y - radius), int(current_x + radius), int(current_y + radius)]
        draw.ellipse(bounding_box, fill="black")

    # --- NEW: PDF CONVERSION LOGIC ---
    print(f"3. Converting final image to PDF...")
    # Sanitize the topic to create a valid filename
    pdf_filename = sanitize_filename(topic) + ".pdf"
    
    # IMPORTANT: PDFs don't handle transparency (alpha channel) well.
    # We must convert the image to RGB mode before saving.
    rgb_image = omr_image.convert('RGB')
    
    # Save the RGB image as a high-quality PDF
    rgb_image.save(pdf_filename, "PDF", resolution=100.0)
    print(f"4. Success! Created PDF file: '{pdf_filename}'")
    
    # We can still show the image for a quick preview
    omr_image.show()

# --- Main Workflow ---
if __name__ == "__main__":
    answer_csv_path = "answers.csv"
    omr_template_path = "omr_sheet.jpg"

    topic, answers_data = read_csv_with_topic(answer_csv_path)
    if answers_data is not None:
        mark_omr_and_create_pdf(topic, answers_data, omr_template_path)
