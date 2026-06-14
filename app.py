from flask import Flask, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

# Load columns
with open("columns.pkl", "rb") as file:
    columns = pickle.load(file)

cities = [
    "Mumbai", "Pune", "Delhi", "Bangalore", "Hyderabad",
    "Chennai", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow",
    "Nagpur", "Nashik", "Surat", "Indore", "Chandigarh",
    "Kochi", "Bhopal"
]

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        city = request.form["city"]
        area = float(request.form["area"])
        bedrooms = int(request.form["bedrooms"])
        bathrooms = int(request.form["bathrooms"])

        data = {col: 0 for col in columns}

        data["area"] = area
        data["bedrooms"] = bedrooms
        data["bathrooms"] = bathrooms

        city_column = f"city_{city}"

        if city_column in data:
            data[city_column] = 1

        prediction = model.predict(pd.DataFrame([data]))

        result = f"Estimated House Price: ₹{prediction[0]:,.0f}"

    city_options = "".join(
        [f"<option value='{city}'>{city}</option>" for city in cities]
    )

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>House Price Predictor</title>

        <style>

        body {{
            background: #f4f6f9;
            font-family: Arial;
        }}

        .container {{
            width: 500px;
            margin: 50px auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 0 15px rgba(0,0,0,0.15);
            text-align: center;
        }}

        h1 {{
            color: #333;
        }}

        input, select {{
            width: 90%;
            padding: 12px;
            margin: 10px;
            border: 1px solid #ccc;
            border-radius: 8px;
        }}

        button {{
            background: #007bff;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
        }}

        button:hover {{
            background: #0056b3;
        }}

        h2 {{
            color: green;
        }}

        </style>
    </head>

    <body>

        <div class="container">

            <h1>🏠 House Price Predictor</h1>

            <form method="POST">

                <select name="city" required>
                    {city_options}
                </select>

                <input type="number" name="area" placeholder="Area (sq ft)" required>

                <input type="number" name="bedrooms" placeholder="Bedrooms" required>

                <input type="number" name="bathrooms" placeholder="Bathrooms" required>

                <button type="submit">Predict Price</button>

            </form>

            <h2>{result}</h2>

        </div>

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True, port=5001)