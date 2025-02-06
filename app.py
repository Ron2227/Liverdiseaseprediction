from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

def check_liver_disease(age, gender, total_bilirubin, direct_bilirubin, alkaline_phosphotase,
                        alamine_aminotransferase, aspartate_aminotransferase, albumin):
    reasons = []
    if total_bilirubin > 1.2:
        reasons.append("Total Bilirubin is high (>1.2)")
    if direct_bilirubin > 0.4:
        reasons.append("Direct Bilirubin is high (>0.4)")
    if alkaline_phosphotase > 120:
        reasons.append("Alkaline Phosphatase is high (>120)")
    if alamine_aminotransferase > 40:
        reasons.append("Alamine Aminotransferase is high (>40)")
    if aspartate_aminotransferase > 40:
        reasons.append("Aspartate Aminotransferase is high (>40)")
    if albumin < 3.5:
        reasons.append("Albumin is low (<3.5)")

    if reasons:
        return "Liver Disease Detected", reasons
    else:
        return "No Liver Disease", ["All values are within normal ranges."]

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        result, reasons = check_liver_disease(
            data['age'], data['gender'], data['total_bilirubin'],
            data['direct_bilirubin'], data['alkaline_phosphotase'],
            data['alamine_aminotransferase'], data['aspartate_aminotransferase'],
            data['albumin']
        )
        return jsonify({
            'status': result,
            'reasons': reasons
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
