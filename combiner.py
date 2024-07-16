import pandas as pd

# File paths
file1 = "product.xlsx"
file2 = "product_reviews_all_star_levels.xlsx"

# Read both Excel files
df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)

# Concatenate both dataframes vertically (union)
combined_df = pd.concat([df1, df2], ignore_index=True)

# Output filename for combined file
output_filename = "combined.xlsx"

# Save combined dataframe to Excel
combined_df.to_excel(output_filename, index=False)

print(f"Combined data saved to {output_filename}")