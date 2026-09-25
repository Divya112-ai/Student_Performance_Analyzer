# ============================================================
# STUDENT PERFORMANCE & ATTENDANCE ANALYZER
# Python for Data Science - GTU PBL Micro Project
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# 1. PROJECT TITLE
# ============================================================

print("=" * 70)
print("        STUDENT PERFORMANCE & ATTENDANCE ANALYZER")
print("        Python for Data Science - GTU PBL")
print("=" * 70)


# ============================================================
# 2. LOAD DATASET
# ============================================================

file_path = "student_performance.csv"

try:
    df = pd.read_csv(file_path)
    print("\nDataset loaded successfully!")

except FileNotFoundError:
    print("\nERROR: student_performance.csv was not found.")
    print("Please keep the CSV file in the same folder as this Python file.")
    exit()


# ============================================================
# 3. DISPLAY FIRST FEW RECORDS
# ============================================================

print("\nFirst 5 Records:")
print(df.head())


# ============================================================
# 4. BASIC DATASET INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("DATASET INFORMATION")
print("=" * 70)

print("\nNumber of Students:", len(df))

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)


# ============================================================
# 5. DATA CLEANING
# ============================================================

print("\n" + "=" * 70)
print("DATA CLEANING")
print("=" * 70)


# Check missing values
print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())


# Check duplicate records
print("\nNumber of Duplicate Records:")
print(df.duplicated().sum())


# Remove duplicate records
df = df.drop_duplicates()


# Numerical columns
numeric_columns = [
    "Attendance",
    "Assignment",
    "Midterm",
    "Final",
    "Practical"
]


# Convert numerical columns to numeric
for column in numeric_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# Fill missing numerical values using median
for column in numeric_columns:

    df[column] = df[column].fillna(
        df[column].median()
    )


print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

print("\nData cleaning completed successfully!")


# ============================================================
# 6. DATA VALIDATION
# ============================================================

# Attendance must be between 0 and 100

df["Attendance"] = df[
    "Attendance"
].clip(0, 100)


# Marks cannot be negative

for column in [
    "Assignment",
    "Midterm",
    "Final",
    "Practical"
]:

    df[column] = df[
        column
    ].clip(lower=0)


# ============================================================
# 7. MAXIMUM MARKS
# ============================================================

# Maximum marks for each component

ASSIGNMENT_MAX = 20
MIDTERM_MAX = 50
FINAL_MAX = 100
PRACTICAL_MAX = 20


# Total maximum marks

TOTAL_MAX = (
    ASSIGNMENT_MAX
    + MIDTERM_MAX
    + FINAL_MAX
    + PRACTICAL_MAX
)


# ============================================================
# 8. CALCULATE TOTAL MARKS
# ============================================================

df["Total_Marks"] = (
    df["Assignment"]
    + df["Midterm"]
    + df["Final"]
    + df["Practical"]
)


# ============================================================
# 9. CALCULATE OVERALL PERFORMANCE PERCENTAGE
# ============================================================

# Correct calculation:
#
# Total obtained marks / Total maximum marks * 100
#
# Example:
# 18 + 42 + 78 + 18 = 156
#
# 156 / 190 * 100 = 82.11%

df["Average_Marks"] = (
    df["Total_Marks"]
    / TOTAL_MAX
) * 100


# Round to 2 decimal places

df["Average_Marks"] = df[
    "Average_Marks"
].round(2)


# ============================================================
# 10. PERFORMANCE CLASSIFICATION
# ============================================================

def classify_performance(percentage):

    if percentage >= 80:
        return "Excellent"

    elif percentage >= 70:
        return "Very Good"

    elif percentage >= 60:
        return "Good"

    elif percentage >= 50:
        return "Average"

    else:
        return "Needs Improvement"


df["Performance"] = df[
    "Average_Marks"
].apply(classify_performance)


# ============================================================
# 11. PASS / FAIL STATUS
# ============================================================

# Student is considered passed if overall percentage >= 40%

df["Result"] = np.where(
    df["Average_Marks"] >= 40,
    "Pass",
    "Fail"
)


# ============================================================
# 12. ATTENDANCE CLASSIFICATION
# ============================================================

def classify_attendance(attendance):

    if attendance >= 85:
        return "Good"

    elif attendance >= 75:
        return "Satisfactory"

    else:
        return "Low Attendance"


df["Attendance_Status"] = df[
    "Attendance"
].apply(classify_attendance)


# ============================================================
# 13. STUDENTS REQUIRING ATTENTION
# ============================================================

# A student requires attention if:
#
# Attendance < 75%
# OR
# Performance < 50%

df["Requires_Attention"] = np.where(
    (df["Attendance"] < 75)
    |
    (df["Average_Marks"] < 50),
    "Yes",
    "No"
)


# ============================================================
# 14. DISPLAY CALCULATED DATA
# ============================================================

print("\n" + "=" * 70)
print("CALCULATED STUDENT PERFORMANCE")
print("=" * 70)

print(
    df[
        [
            "Student_ID",
            "Name",
            "Attendance",
            "Total_Marks",
            "Average_Marks",
            "Performance",
            "Result"
        ]
    ].to_string(index=False)
)


# ============================================================
# 15. DESCRIPTIVE STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("DESCRIPTIVE STATISTICS")
print("=" * 70)


statistics = df[
    [
        "Attendance",
        "Assignment",
        "Midterm",
        "Final",
        "Practical",
        "Total_Marks",
        "Average_Marks"
    ]
].describe()


print(statistics)


# ============================================================
# 16. CLASS PERFORMANCE SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("CLASS PERFORMANCE SUMMARY")
print("=" * 70)


class_average = df[
    "Average_Marks"
].mean()


average_attendance = df[
    "Attendance"
].mean()


highest_percentage = df[
    "Average_Marks"
].max()


lowest_percentage = df[
    "Average_Marks"
].min()


print(
    f"\nTotal Students       : {len(df)}"
)

print(
    f"Class Average        : {class_average:.2f}%"
)

print(
    f"Average Attendance   : {average_attendance:.2f}%"
)

print(
    f"Highest Performance  : {highest_percentage:.2f}%"
)

print(
    f"Lowest Performance   : {lowest_percentage:.2f}%"
)


# ============================================================
# 17. PASS / FAIL ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("PASS / FAIL ANALYSIS")
print("=" * 70)


pass_count = (
    df["Result"] == "Pass"
).sum()


fail_count = (
    df["Result"] == "Fail"
).sum()


pass_percentage = (
    pass_count / len(df)
) * 100


fail_percentage = (
    fail_count / len(df)
) * 100


print(
    f"\nPassed Students : {pass_count}"
)

print(
    f"Failed Students : {fail_count}"
)

print(
    f"Pass Percentage  : {pass_percentage:.2f}%"
)

print(
    f"Fail Percentage  : {fail_percentage:.2f}%"
)


# ============================================================
# 18. PERFORMANCE DISTRIBUTION
# ============================================================

print("\n" + "=" * 70)
print("PERFORMANCE DISTRIBUTION")
print("=" * 70)


performance_count = df[
    "Performance"
].value_counts()


print(performance_count)


# ============================================================
# 19. ATTENDANCE DISTRIBUTION
# ============================================================

print("\n" + "=" * 70)
print("ATTENDANCE DISTRIBUTION")
print("=" * 70)


attendance_count = df[
    "Attendance_Status"
].value_counts()


print(attendance_count)


# ============================================================
# 20. TOP 10 STUDENTS
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 STUDENTS")
print("=" * 70)


top_10 = df.sort_values(
    "Average_Marks",
    ascending=False
).head(10)


print(
    top_10[
        [
            "Student_ID",
            "Name",
            "Attendance",
            "Average_Marks",
            "Performance"
        ]
    ].to_string(index=False)
)


# ============================================================
# 21. STUDENTS REQUIRING ATTENTION
# ============================================================

print("\n" + "=" * 70)
print("STUDENTS REQUIRING ATTENTION")
print("=" * 70)


attention_students = df[
    df["Requires_Attention"] == "Yes"
]


if len(attention_students) == 0:

    print("\nNo students require attention.")

else:

    print(
        attention_students[
            [
                "Student_ID",
                "Name",
                "Attendance",
                "Average_Marks",
                "Performance",
                "Result"
            ]
        ].to_string(index=False)
    )


# ============================================================
# 22. COMPONENT-WISE PERFORMANCE
# ============================================================

print("\n" + "=" * 70)
print("COMPONENT-WISE PERFORMANCE")
print("=" * 70)


# Convert every component into percentage
# so that different maximum marks can be compared.

component_averages = pd.Series({

    "Assignment": (
        df["Assignment"].mean()
        / ASSIGNMENT_MAX
    ) * 100,

    "Midterm": (
        df["Midterm"].mean()
        / MIDTERM_MAX
    ) * 100,

    "Final": (
        df["Final"].mean()
        / FINAL_MAX
    ) * 100,

    "Practical": (
        df["Practical"].mean()
        / PRACTICAL_MAX
    ) * 100
})


component_averages = (
    component_averages.round(2)
)


print(
    component_averages
)


# ============================================================
# 23. ATTENDANCE VS PERFORMANCE
# ============================================================

correlation = df[
    [
        "Attendance",
        "Average_Marks"
    ]
].corr().iloc[0, 1]


print("\n" + "=" * 70)
print("ATTENDANCE VS ACADEMIC PERFORMANCE")
print("=" * 70)


print(
    f"\nCorrelation between Attendance "
    f"and Performance: {correlation:.2f}"
)


if correlation > 0:

    print(
        "The dataset shows a positive association "
        "between attendance and academic performance."
    )

elif correlation < 0:

    print(
        "The dataset shows a negative association "
        "between attendance and academic performance."
    )

else:

    print(
        "The dataset shows very little linear "
        "association between attendance and performance."
    )


# ============================================================
# 24. VISUALIZATION
# ============================================================

sns.set_theme(
    style="whitegrid"
)


# Create one figure with 6 graphs

fig, axes = plt.subplots(
    3,
    2,
    figsize=(16, 14)
)


# ============================================================
# GRAPH 1
# ATTENDANCE DISTRIBUTION
# ============================================================

sns.histplot(
    df["Attendance"],
    bins=8,
    kde=True,
    ax=axes[0, 0]
)


axes[0, 0].set_title(
    "Student Attendance Distribution",
    fontsize=13,
    fontweight="bold"
)


axes[0, 0].set_xlabel(
    "Attendance Percentage"
)


axes[0, 0].set_ylabel(
    "Number of Students"
)


# ============================================================
# GRAPH 2
# PERFORMANCE DISTRIBUTION
# ============================================================

sns.histplot(
    df["Average_Marks"],
    bins=8,
    kde=True,
    ax=axes[0, 1]
)


axes[0, 1].set_title(
    "Student Performance Distribution",
    fontsize=13,
    fontweight="bold"
)


axes[0, 1].set_xlabel(
    "Overall Performance (%)"
)


axes[0, 1].set_ylabel(
    "Number of Students"
)


# ============================================================
# GRAPH 3
# ATTENDANCE VS PERFORMANCE
# ============================================================

sns.scatterplot(
    data=df,
    x="Attendance",
    y="Average_Marks",
    hue="Performance",
    s=80,
    ax=axes[1, 0]
)


axes[1, 0].set_title(
    "Attendance vs Academic Performance",
    fontsize=13,
    fontweight="bold"
)


axes[1, 0].set_xlabel(
    "Attendance Percentage"
)


axes[1, 0].set_ylabel(
    "Overall Performance (%)"
)


# ============================================================
# GRAPH 4
# TOP 10 STUDENTS
# ============================================================

sns.barplot(
    data=top_10,
    x="Average_Marks",
    y="Name",
    ax=axes[1, 1]
)


axes[1, 1].set_title(
    "Top 10 Students by Overall Performance",
    fontsize=13,
    fontweight="bold"
)


axes[1, 1].set_xlabel(
    "Overall Performance (%)"
)


axes[1, 1].set_ylabel(
    "Student Name"
)


# ============================================================
# GRAPH 5
# COMPONENT-WISE PERFORMANCE
# ============================================================

component_averages.plot(
    kind="bar",
    ax=axes[2, 0]
)


axes[2, 0].set_title(
    "Component-wise Average Performance",
    fontsize=13,
    fontweight="bold"
)


axes[2, 0].set_xlabel(
    "Assessment Component"
)


axes[2, 0].set_ylabel(
    "Average Percentage"
)


axes[2, 0].set_ylim(
    0,
    100
)


axes[2, 0].tick_params(
    axis="x",
    rotation=0
)


# ============================================================
# GRAPH 6
# PERFORMANCE CATEGORY DISTRIBUTION
# ============================================================

performance_count.plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90,
    ax=axes[2, 1]
)


axes[2, 1].set_title(
    "Performance Category Distribution",
    fontsize=13,
    fontweight="bold"
)


axes[2, 1].set_ylabel("")


# ============================================================
# MAIN TITLE
# ============================================================

plt.suptitle(
    "Student Performance & Attendance Analysis",
    fontsize=20,
    fontweight="bold"
)


# ============================================================
# ADJUST LAYOUT
# ============================================================

plt.tight_layout(
    rect=[0, 0, 1, 0.96]
)


# ============================================================
# DISPLAY GRAPHS
# ============================================================

plt.show()


# ============================================================
# 25. SAVE ANALYZED DATA
# ============================================================

output_file = (
    "analyzed_student_performance.csv"
)


df.to_csv(
    output_file,
    index=False
)


# ============================================================
# 26. PROJECT COMPLETED
# ============================================================

print("\n" + "=" * 70)
print("PROJECT COMPLETED SUCCESSFULLY")
print("=" * 70)


print(
    f"\nAnalyzed dataset saved as:"
    f"\n{output_file}"
)


print("\nThank you!")