import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
car_data = pd.read_csv('Cleaned_Car_data.csv')

# Display the first few rows to understand the data
print(car_data.head())

# Count the number of cars by company
# company_counts = car_data['company'].value_counts()

# # Plot the bar chart
# plt.figure(figsize=(10, 6))
# company_counts.plot(kind='bar', color='skyblue')
# plt.title('Number of Cars by Company', fontsize=16)
# plt.xlabel('Company', fontsize=12)
# plt.ylabel('Number of Cars', fontsize=12)
# plt.xticks(rotation=45)
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.tight_layout()
# plt.show()

# Calculate the average price by company
# average_price = car_data.groupby('company')['Price'].mean().sort_values(ascending=False)

# # Plot the bar chart
# plt.figure(figsize=(10, 6))
# average_price.plot(kind='bar', color='orange')
# plt.title('Average Car Price by Company', fontsize=16)
# plt.xlabel('Company', fontsize=12)
# plt.ylabel('Average Price (₹)', fontsize=12)
# plt.xticks(rotation=45)
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.tight_layout()
# plt.show()


# plt.figure(figsize=(10, 6))
# plt.scatter(car_data['kms_driven'], car_data['Price'], alpha=0.5, color='green')
# plt.title('Price vs. Kilometers Driven')
# plt.xlabel('Kilometers Driven')
# plt.ylabel('Price (₹)')
# plt.grid()
# plt.show()


# Count the percentage of cars by fuel type
# fuel_counts = car_data['fuel_type'].value_counts()

# # Plot the pie chart
# plt.figure(figsize=(8, 8))
# fuel_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['lightblue', 'orange', 'lightgreen'])
# plt.title('Percentage Distribution of Fuel Types', fontsize=16)
# plt.ylabel('')  # Remove default ylabel
# plt.show()


# Plot car prices distribution
# plt.figure(figsize=(10, 6))
# sns.histplot(car_data['Price'], kde=True, color='purple', bins=30)
# plt.title('Distribution of Car Prices', fontsize=16)
# plt.xlabel('Price (₹)', fontsize=12)
# plt.ylabel('Frequency', fontsize=12)
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.show()


# avg_price_by_year = car_data.groupby('year')['Price'].mean()
# avg_price_by_year.plot(kind='line', marker='o', color='orange', figsize=(10, 6))
# plt.title('Average Car Price by Year')
# plt.xlabel('Year')
# plt.ylabel('Average Price (₹)')
# plt.grid()
# plt.show()


# import matplotlib.pyplot as plt
# import numpy as np

# # Example data
# actual_prices = [250000, 300000, 350000, 400000, 450000]
# predicted_prices = [245000, 310000, 340000, 380000, 460000]
# car_models = ['Model A', 'Model B', 'Model C', 'Model D', 'Model E']

# x = np.arange(len(car_models))

# # Plotting
# plt.figure(figsize=(10, 6))
# plt.bar(x - 0.2, actual_prices, 0.4, label='Actual Price', color='blue')
# plt.bar(x + 0.2, predicted_prices, 0.4, label='Predicted Price', color='orange')

# plt.xticks(x, car_models)
# plt.xlabel('Car Models')
# plt.ylabel('Price in ₹')
# plt.title('Predicted vs Actual Car Prices')
# plt.legend()

# plt.show()


# # Example data
# predicted_prices = [245000, 310000, 340000, 380000, 460000, 280000, 390000, 420000, 370000, 290000]

# # Plotting Histogram
# plt.figure(figsize=(10, 6))
# plt.hist(predicted_prices, bins=10, color='blue', edgecolor='black')
# plt.title('Distribution of Predicted Car Prices')
# plt.xlabel('Price in ₹')
# plt.ylabel('Frequency')
# plt.show()

# # Example data
# car_models = ['Model A', 'Model B', 'Model C', 'Model D', 'Model E']
# predictions_count = [12, 8, 15, 10, 5]

# # Plotting Bar Chart
# plt.figure(figsize=(10, 6))
# plt.bar(car_models, predictions_count, color='green')
# plt.title('Car Model Popularity')
# plt.xlabel('Car Models')
# plt.ylabel('Number of Predictions')
# plt.show()


# import seaborn as sns
# import pandas as pd

# # Example data
# data = pd.DataFrame({
#     'year': [2010, 2015, 2020, 2020, 2022],
#     'km_driven': [50000, 30000, 15000, 20000, 10000],
#     'fuel_type': [1, 0, 1, 0, 1],  # 1 for Petrol, 0 for Diesel
#     'predicted_price': [250000, 300000, 350000, 400000, 450000]
# })

# # Correlation Heatmap
# plt.figure(figsize=(8, 6))
# sns.heatmap(data.corr(), annot=True, cmap='coolwarm', linewidths=0.5)
# plt.title('Feature Correlation Heatmap')
# plt.show()


# import matplotlib.pyplot as plt

# car_counts = car_data['company'].value_counts()
# car_counts.plot(kind='bar', figsize=(10, 6), color='skyblue')
# plt.title('Number of Cars by Company')
# plt.xlabel('Company')
# plt.ylabel('Count')
# plt.xticks(rotation=45)
# plt.show()


