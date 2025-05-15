import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("cleaned_sponsored_soft_toys.csv")

if not os.path.isdir("Price vs Rating Plots"):
    os.mkdir("Price vs Rating Plots")

# Drop rows with missing rating or price
filtered_df = df[df['Rating'].notna() & df['Selling Price'].notna()]

# Price vs Rating scatter plot
plt.figure(figsize=(8, 5))
plt.scatter(filtered_df['Rating'], filtered_df['Selling Price'], alpha=0.6, color='purple')
plt.title('Price vs. Rating of Sponsored Soft Toys', pad=20)
plt.xlabel('Rating')
plt.ylabel('Selling Price (₹)')
plt.grid(True)
plt.tight_layout()
plt.savefig("Price vs Rating Plots/price_vs_rating_scatter.png")
# plt.show()

# Average price by rating range
# Create rating bins
bins = [0, 2, 3, 4, 4.5, 5]
labels = ['1-2', '2-3', '3-4', '4-4.5', '4.5-5']
filtered_df['Rating Range'] = pd.cut(filtered_df['Rating'], bins=bins, labels=labels)

# Compute average price for each rating range
avg_price_by_rating = filtered_df.groupby('Rating Range')['Selling Price'].mean()

# Plotting
plt.figure(figsize=(8, 5))
bars = plt.bar(avg_price_by_rating.index.astype(str), avg_price_by_rating.values, color='mediumseagreen')
plt.title('Average Price by Rating Range', pad=20)
plt.xlabel('Rating Range')
plt.ylabel('Average Price (₹)')

# Add labels on top
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 5, f"{height:.0f}", ha='center', va='bottom')

plt.tight_layout()
plt.savefig("Price vs Rating Plots/avg_price_by_rating_range.png")
# plt.show()
