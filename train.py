import pandas as pd
import pickle

from sklearn.linear_model import LinearRegression

# Load dataset
df = pd.read_csv("dataset/house_data.csv")

# Convert city names into numbers
df = pd.get_dummies(df, columns=["city"])

# Features
X = df.drop("price", axis=1)

# Target
y = df["price"]

# Train model
model = LinearRegression()

model.fit(X, y)

# Save model
with open("model.pkl", "wb") as file:
    pickle.dump(model, file)

# Save column names
with open("columns.pkl", "wb") as file:
    pickle.dump(X.columns.tolist(), file)

print("Model trained successfully!")
print("Model saved successfully!")

