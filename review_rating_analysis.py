import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("cleaned_sponsored_soft_toys.csv")

if not os.path.isdir("Review and Rating Analysis Plots"):
    os.mkdir("Review and Rating Analysis Plots")

def shorten_title(title, max_words=4):
    return ' '.join(title.split()[:max_words]) + '...'

df['Short Title'] = df['Title'].apply(lambda x: shorten_title(x))

# Top 5 most reviewed products
# Filter out rows with missing reviews
top_reviewed = df[df['Reviews'].notna()].sort_values('Reviews', ascending=False).head(5)

plt.figure(figsize=(9, 5))
bars = plt.bar(top_reviewed['Short Title'], top_reviewed['Reviews'], color='skyblue')
plt.title('Top 5 Most Reviewed Sponsored Soft Toys', pad=20)
plt.xlabel('Product')
plt.ylabel('Number of Reviews')
plt.xticks(rotation=15, ha='right')

# Add review counts on top
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height - 5, f"{int(height)}", ha='center', va='bottom')

plt.tight_layout()
plt.savefig("Review and Rating Analysis Plots/top_reviewed_products.png")
# plt.show()

# Top 5 highest rated products
# Filter out missing ratings
top_rated = df[df['Rating'].notna()].sort_values('Rating', ascending=False).head(5)

plt.figure(figsize=(9, 5))
bars = plt.bar(top_rated['Short Title'], top_rated['Rating'], color='orange')
plt.title('Top 5 Highest Rated Sponsored Soft Toys', pad=20)
plt.xlabel('Product')
plt.ylabel('Rating (out of 5)')
plt.ylim(0, 5)  # Limit rating axis to 0–5
plt.xticks(rotation=15, ha='right')

# Add rating values on top
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 0.05, f"{height:.1f}", ha='center', va='bottom')

plt.tight_layout()
plt.savefig("Review and Rating Analysis Plots/top_rated_products.png")
# plt.show()

