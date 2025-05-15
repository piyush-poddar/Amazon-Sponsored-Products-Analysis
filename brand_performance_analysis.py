import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("cleaned_sponsored_soft_toys.csv")

if not os.path.isdir("Brand Performance Plots"):
    os.mkdir("Brand Performance Plots")

# Top 5 brands by frequency
brand_counts = df['Brand'].value_counts().head(5)

plt.figure(figsize=(8, 5))
bars = plt.bar(brand_counts.index, brand_counts.values, color='skyblue')
plt.title("Top 5 Brands by Frequency (Sponsored Soft Toys)")
plt.xlabel("Brand")
plt.ylabel("Number of Products")
plt.xticks(rotation=45)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height - 1, str(int(height)), ha='center', va='bottom')
plt.tight_layout()
plt.savefig("Brand Performance Plots/top_brands_by_freq.png")
# plt.show()


# Pie chart showing percentage share of top brands by frequency
# Get full brand counts
all_brand_counts = df['Brand'].value_counts()

# Take top 5
top_5_brands = all_brand_counts.head(5)

# Sum the rest into 'Others'
others_sum = all_brand_counts.iloc[5:].sum()

# Add "Others" to the top 5
final_counts = top_5_brands.copy()
final_counts['Others'] = others_sum

# Plotting the pie chart
plt.figure(figsize=(7, 7))
plt.pie(
    final_counts.values,
    labels=final_counts.index,
    autopct='%1.1f%%',
    startangle=140,
    colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0', '#d3d3d3']
)
plt.title("Market Share of Top Brands (by Frequency) with Others")
plt.axis('equal')
plt.tight_layout()
plt.savefig("Brand Performance Plots/top_brands_by_freq_market_share.png")
# plt.show()


# Average rating by brand
rated_df = df[df['Rating'].notna()]
brand_avg_rating = rated_df.groupby('Brand')['Rating'].mean().sort_values(ascending=False).head(5)

plt.figure(figsize=(8, 5))
bars = plt.bar(brand_avg_rating.index, brand_avg_rating.values, color='salmon')
plt.title("Top 5 Brands by Average Rating")
plt.xlabel("Brand")
plt.ylabel("Average Rating")
plt.ylim(0, 5)
plt.xticks(rotation=45)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height - 0.5, f"{height:.2f}", ha='center', va='bottom')
plt.tight_layout()
plt.savefig("Brand Performance Plots/top_brands_by_avg_rating.png")
# plt.show()


# Pie chart showing percentage share of top brands by average rating
top_rated_brands = brand_avg_rating.index.tolist()

# Step 2: Get frequency of these top-rated brands
top_brand_counts = rated_df[rated_df['Brand'].isin(top_rated_brands)]['Brand'].value_counts()

# Step 3: Count "Others"
others_count = rated_df[~rated_df['Brand'].isin(top_rated_brands)].shape[0]

# Add "Others" to the top brand counts
final_counts = top_brand_counts.copy()
final_counts['Others'] = others_count

plt.figure(figsize=(7, 7))
plt.pie(
    final_counts.values,
    labels=final_counts.index,
    autopct='%1.1f%%',
    startangle=140,
    colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0', '#d3d3d3']
)
plt.title("Frequency Share of Top 5 Brands (by Avg Rating) in Rated Products")
plt.axis('equal')
plt.tight_layout()
plt.savefig("Brand Performance Plots/top_brands_by_avg_rating_market_share.png")
# plt.show()