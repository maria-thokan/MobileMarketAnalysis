import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class DataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Cleaning, Analysis & Visualization")
        self.df = None

        # Buttons
        tk.Button(root, text="Clean Data", command=self.clean_data, width=30).pack(pady=5)
        tk.Button(root, text="Run Analysis", command=self.run_analysis, width=30).pack(pady=5)
        tk.Button(root, text="Show Visualizations", command=self.show_visuals, width=30).pack(pady=5)
        tk.Button(root, text="Exit", command=root.quit, width=30).pack(pady=5)

    def clean_data(self):
        try:
            self.df = pd.read_excel("analysis_report.xlsx", sheet_name="Sheet1")

            # Fill missing, drop duplicates, format text
            self.df = self.df.fillna("unknown").drop_duplicates()
            for col in self.df.select_dtypes(include=["object"]).columns:
                self.df[col] = (
                    self.df[col]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    .str.replace(r"\s+", " ", regex=True)
                )

            # Rename columns
            self.df.columns = self.df.columns.str.strip().str.lower().str.replace(" ", "_")

            # Convert datatypes
            if "price" in self.df.columns:
                self.df["price"] = pd.to_numeric(self.df["price"], errors="coerce").astype("Int64")
            if "rating" in self.df.columns:
                self.df["rating"] = pd.to_numeric(self.df["rating"], errors="coerce").astype(float) / 10
            if "ram_capacity" in self.df.columns:
                self.df["ram_capacity"] = pd.to_numeric(self.df["ram_capacity"], errors="coerce").astype("Int64")
            if "battery_capacity" in self.df.columns:
                self.df["battery_capacity"] = pd.to_numeric(self.df["battery_capacity"], errors="coerce").astype("Int64")

            # Save cleaned file
            self.df.to_excel("data_analysis_cleaned.xlsx", index=False)
            messagebox.showinfo("Data Cleaned", "Data cleaned and saved as data_analysis_cleaned.xlsx")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to clean data:\n{e}")

    def run_analysis(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Please clean data first.")
            return

        try:
            avg_price = self.df["price"].mean() if "price" in self.df.columns else None
            max_rating = self.df["rating"].max() if "rating" in self.df.columns else None
            min_rating = self.df["rating"].min() if "rating" in self.df.columns else None

            msg = "Analysis Results:\n\n"
            if avg_price: msg += f"Average Price: {avg_price:.2f}\n"
            if max_rating: msg += f"Max Rating: {max_rating:.1f}\n"
            if min_rating: msg += f"Min Rating: {min_rating:.1f}\n"

            messagebox.showinfo("Analysis", msg)

        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed:\n{e}")

    def show_visuals(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Please clean data first.")
            return

        try:
            # 1. Bar chart of brand counts
            self.df['brand_name'].value_counts().plot(kind='bar', figsize=(8,5))
            plt.title("Brand Distribution")
            plt.show()

            # 2. Pie chart of rating
            self.df['rating'].value_counts().plot(kind='pie', autopct='%1.1f%%', figsize=(6,6))
            plt.title("Rating Distribution")
            plt.ylabel("")
            plt.show()

            # 3. Scatter plot
            sns.scatterplot(x='price', y='battery_capacity', data=self.df, hue='brand_name', palette='tab10')
            plt.title("Price vs Battery (by Brand)")
            plt.show()

            # 4. Histogram of price
            self.df['price'].plot(kind='hist', bins=20, edgecolor='black', figsize=(8,5))
            plt.title("Price Distribution Histogram")
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"Visualization failed:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DataApp(root)
    root.mainloop()
