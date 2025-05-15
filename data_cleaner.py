import pandas as pd

# Load the data
df = pd.read_csv("data/sponsored_soft_toys.csv")

# Preview the data
print(df.head())

df.drop_duplicates(subset=["Image URL"], keep="first", inplace=True)

df["Selling Price"] = df["Selling Price"].astype(str).str.replace("₹", "").str.strip()
df["Selling Price"] = pd.to_numeric(df["Selling Price"], errors="coerce")

df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")

df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

df["Brand"] = df["Brand"].str.strip().str.lower()

# Create a new column 'Rated' that is True if 'Rating' is not null, otherwise False
df['Rated'] = df['Rating'].notna()

#df.dropna(subset=["Selling Price", "Rating", "Reviews"], inplace=True)
print(df.head())

# Save the cleaned data
df.to_csv("data/cleaned_sponsored_soft_toys.csv", index=False)
print("Data cleaning done. Cleaned data saved to cleaned_sponsored_soft_toys.csv")
