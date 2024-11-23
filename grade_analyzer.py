import pandas as pd
import textstat

# Read the CSV file
df = pd.read_csv('andmed ja analüüs/foxnews_h3_elements.csv'.encode('utf-8').decode('utf-8'))

# Calculate Flesch-Kincaid grade level for each headline
def calculate_grade(text):
    grade = textstat.flesch_kincaid_grade(text)
    return max(0, grade)  # Returns 0 if grade is negative, otherwise returns the grade

df['grade'] = df['headline'].apply(calculate_grade)

# Save to new CSV file
df.to_csv('Fox_News_headlines_with_grades.csv', index=False)