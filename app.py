from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load model and vectorizer
model = pickle.load(open("sentiment_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    user_input = request.form['review'].lower()
    transformed_input = vectorizer.transform([user_input])

    probabilities = model.predict_proba(transformed_input)[0]
    classes = model.classes_

    print("Probabilities:", dict(zip(classes, probabilities)))

    prediction = model.predict(transformed_input)[0]

    # --- Rule-Based Neutral Detection ---
    neutral_keywords = [
        "okay", "fine", "average", "not bad", 
        "not good", "normal", "so so", "alright"
    ]

    if any(word in user_input for word in neutral_keywords):
        result = "😐 Neutral Sentiment"
        confidence = 75.00
        color = "orange"

    else:
        max_prob = max(probabilities)
        confidence = round(max_prob * 100, 2)

        if prediction == "Positive":
            result = "😊 Positive Sentiment"
            color = "green"
        elif prediction == "Negative":
            result = "😔 Negative Sentiment"
            color = "red"
        else:
            result = "😐 Neutral Sentiment"
            color = "orange"

    return render_template(
        "index.html",
        prediction_text=result,
        confidence=confidence,
        color=color
    )
if __name__ == "__main__":
    app.run(debug=True)