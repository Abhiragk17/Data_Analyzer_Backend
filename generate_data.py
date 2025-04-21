import pandas as pd
import numpy as np

# Create sample data
np.random.seed(42)  # For reproducibility

# Generate 15 students' data
n_students = 15

data = {
    'student_id': range(1, n_students + 1),
    'cgpa': np.random.uniform(6.0, 10.0, n_students),
    'attendance_percentage': np.random.uniform(60, 100, n_students),
    'study_hours': np.random.randint(2, 8, n_students),
    'previous_semester_gpa': np.random.uniform(6.0, 10.0, n_students),
    'extracurricular_activities': np.random.randint(0, 5, n_students),
    'pass_fail': np.random.choice(['Pass', 'Fail'], n_students, p=[0.7, 0.3])
}

# Create DataFrame
df = pd.DataFrame(data)

# Round numeric columns to 2 decimal places
df['cgpa'] = df['cgpa'].round(2)
df['attendance_percentage'] = df['attendance_percentage'].round(2)
df['previous_semester_gpa'] = df['previous_semester_gpa'].round(2)

# Save to Excel
df.to_excel('student_performance.xlsx', index=False)

# Display the data
print("Sample Dataset:")
print(df)

# Display basic statistics
print("\nBasic Statistics:")
print(df.describe())