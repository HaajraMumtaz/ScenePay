import os
from dotenv import load_dotenv
from PIL import Image
import pytesseract
import pandas as pd
import cv2

def image_to_string_with_conf(image_path):
    image = Image.open(image_path)
    df = pytesseract.image_to_data(image, output_type=pytesseract.Output.DATAFRAME)

    df = df[df['text'].notnull() & (df['conf'] != -1)]  # filter empty/invalid

    lines = []
    word_confidences = []

    # Group by line structure
    for (par_num, line_num), line_df in df.groupby(['par_num', 'line_num']):
        line_words = line_df.sort_values('word_num')
        for _, word in line_words.iterrows():
            if int(word['conf']) > 60:
                words = line_words['text'].tolist()

        line_text = ' '.join(words)
        lines.append(line_text)

    full_text = '\n'.join(lines)
    return full_text, word_confidences
load_dotenv()  # at top of your app
pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD", "tesseract")

text, word_confs = image_to_string_with_conf(r"C:\Users\DELL\Downloads\s.jpeg")

print("Full OCR Text:\n", text)

text=pytesseract.image_to_string(r"C:\Users\DELL\Downloads\s.jpeg")

print("\n\n\n\nyour new data:",text)


