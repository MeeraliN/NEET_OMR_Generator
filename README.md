# NEET OMR Generator

Do you have your siblings preparing for NEET exam?

If yes, then this repo is for you!

## What it does?

It will give you the OMR sheet marked with the correct answers!

## How it works?

### 1. Install Python

Install Python 3.14 or later from [Python.org](https://www.python.org/downloads/)
- Verify installation: `python --version`
- Ensure pip is installed: `pip --version`

### 2. Run the below commands in your Command Prompt

```bash
pip install pillow
```

### 3. Download all the files from this repo and paste them in the same place, where the Python is installed

It may look something like

`C:\Users\<User_Name>\AppData\Local\Programs\Python\Python314`

### 4. Click the pic of Answer key

### 5. Paste the pic in ChatGPT/Gemini/Copilot, along with the text written inside the file [Prompt to get CSV Answer key for OMR Marking NEET](./Prompt_to_get_CSV_Answer_key_for_OMR_Marking_NEET.txt)

### 6. In response, you will get the answer key, paste it in the [answers.csv file](./answers.csv)

### 7. Make sure the format of [answers.csv file](./answers.csv) looks like below:

```bash
<Chapter/Topic Name>
Question,Answer
<Question_number, Correct_Option in alphabet (a/b/c/d)>
```
Example
```bash
Coordination Compounds
Question,Answer
1,a
2,b
3,c
4,d
```

### 8. Open the [Marked_OMR_Creation](./Marked_OMR_Creation.py)

Press F5 from your keyboard to run it.

### 9. The marked OMR sheet with the chapter title is ready!

Print the generated OMR(titled as your chapter/topic name), and print the blank OMR

### 10. Place the carbon paper between the Blank OMR and Marked OMR

This will speed up the process of checking the answers!

Yes! It's super time saver!

2 circles marked in 1 row means the answer is wrong! See the explanations, prepare that topic well!

# Best of Luck for NEET Exams :)




