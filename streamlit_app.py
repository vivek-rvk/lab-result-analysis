import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import math

st.set_page_config(page_title="Lab Result Analysis", layout="centered")

st.title("📊 Laboratory Result Analysis Tool")

st.write(
    "Upload the formatted Excel file to generate "
    "**Marks Distribution** and **Grade Distribution** plots."
)

uploaded_file = st.file_uploader(
    "Upload Lab Results Excel File",
    type=["xlsx"]
)

if uploaded_file is not None:

    # -----------------------------
    # Read Excel sheets
    # -----------------------------
    course_info_df = pd.read_excel(uploaded_file, sheet_name="Course_Info")
    marks_df = pd.read_excel(uploaded_file, sheet_name="Marks")

    course_info = dict(zip(course_info_df["Field"], course_info_df["Value"]))

    # -----------------------------
    # Grade assignment
    # -----------------------------
    def assign_grade(marks):
        if pd.isna(marks):
            return "F"
        elif marks >= 80:
            return "O"
        elif marks >= 70:
            return "A+"
        elif marks >= 60:
            return "A"
        elif marks >= 55:
            return "B+"
        elif marks >= 50:
            return "B"
        elif marks >= 45:
            return "C"
        elif marks >= 40:
            return "P"
        else:
            return "F"

    marks_df["Grade"] = marks_df["Total"].apply(assign_grade)

    grade_order = ["O", "A+", "A", "B+", "B", "C", "P", "F"]
    grade_counts = marks_df["Grade"].value_counts().reindex(grade_order, fill_value=0)

    # -----------------------------
    # Plot setup
    # -----------------------------
    fig, axes = plt.subplots(2, 1, figsize=(8, 10))
    y_major = 5

    # -----------------------------
    # Fig (a): Marks Distribution
    # -----------------------------
    bins = list(range(0, 101, 10))  # 0–10, 10–20, ..., 90–100

    counts, _, _ = axes[0].hist(
        marks_df["Total"],
        bins=bins,
        align="left",        # 🔴 critical
        rwidth=1.0,          # 🔴 critical
        color="tab:blue",
        edgecolor="black"
    )

    axes[0].set_xlim(0, 100)
    axes[0].set_xticks(bins)        # 🔴 critical
    axes[0].set_xlabel("Marks Secured")
    axes[0].set_ylabel("Number of Students")
    axes[0].set_title("(a) Marks Distribution (10-mark intervals)")


    ymax_a = math.ceil(max(counts) / y_major) * y_major
    axes[0].set_ylim(0, ymax_a)

    axes[0].xaxis.set_major_locator(MultipleLocator(10))
    axes[0].xaxis.set_minor_locator(MultipleLocator(10))
    axes[0].yaxis.set_major_locator(MultipleLocator(y_major))
    axes[0].yaxis.set_minor_locator(MultipleLocator(y_major / 2))

    axes[0].grid(which="major", linestyle="--", alpha=0.7)
    axes[0].grid(which="minor", linestyle=":", alpha=0.4)

    # -----------------------------
    # Fig (b): Grade Distribution
    # -----------------------------
    axes[1].bar(grade_counts.index, grade_counts.values, color="tab:blue")

    axes[1].set_xlabel("Grade")
    axes[1].set_ylabel("Number of Students")
    axes[1].set_title("(b) Grade Distribution")

    ymax_b = math.ceil(max(grade_counts.values) / y_major) * y_major
    axes[1].set_ylim(0, ymax_b)

    axes[1].yaxis.set_major_locator(MultipleLocator(y_major))
    axes[1].yaxis.set_minor_locator(MultipleLocator(y_major / 2))

    axes[1].grid(which="major", linestyle="--", alpha=0.7)
    axes[1].grid(which="minor", linestyle=":", alpha=0.4)

    # -----------------------------
    # Overall title
    # -----------------------------
    fig.suptitle(
        f"Result Analysis – {course_info['Course Code and Name']}\n"
        f"Academic Year: {course_info['Academic Year']} | "
        f"Program: {course_info['Program']} | "
        f"Batch: {course_info['Batch']}",
        fontsize=12
    )

    plt.tight_layout(rect=[0, 0, 1, 0.93])

    st.pyplot(fig)

    with st.expander("📄 View Student Marks & Grades"):
        st.dataframe(marks_df)

else:
    st.info("Please upload the Excel file to proceed.")
