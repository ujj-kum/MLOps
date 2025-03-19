from flask import Flask, render_template, jsonify, request
from src.pipeline.prediction_pipeline import PredictionPipeline, CustomData

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method=="GET":
        return render_template('form.html')
    else:
        # Use Custom Data class from prediction_pipeline.py
        data = CustomData(
            carat = float(request.form.get("carat")),
            depth = float(request.form.get("depth")),
            table = float(request.form.get("table")),
            x = float(request.form.get("x")),
            y = float(request.form.get("y")),
            z = float(request.form.get("z")),
            cut = request.form.get("cut"),
            color = request.form.get("color"),
            clarity = request.form.get("clarity")
        )
        final_data = data.get_data_as_dataframe()
        # Use PredictionPipeline class from prediction_pipeline.py
        pipeline = PredictionPipeline()
        prediction = pipeline.predict(features=final_data)
        return render_template('result.html', prediction=round(prediction[0], 3))
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)