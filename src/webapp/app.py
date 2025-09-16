from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import os
import pandas as pd
from io import BytesIO
from pathlib import Path
import logging

# Ensure src is in path for imports
import sys
sys.path.append(str(Path(__file__).parent.parent))

from models.model import train_model

app = Flask(__name__)
app.secret_key = "supersecretkey"

# configure simple logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_PATH = os.path.join(Path(__file__).parent.parent.parent, "data", "motor_fault_sample_ordered.csv")


def build_label_encoders(df, categorical_cols):
    """Return a dict of label encoders (mapping value->int) for each categorical column based on df."""
    encoders = {}
    for col in categorical_cols:
        uniques = pd.Series(df[col].astype(str).unique()).tolist()
        enc = {v: i for i, v in enumerate(uniques)}
        encoders[col] = enc
    return encoders


def preprocess_input(form, encoders=None):
    feature_cols = ["current", "voltage", "power", "rpm", "vibration_level", "visual_damage", "noise_level", "operating_condition", "maintenance_status"]
    X = []
    for col in feature_cols:
        val = form.get(col)
        if val is None or val == "":
            raise ValueError(f"Missing value for {col}")
        # numeric columns
        if col in ["current", "voltage", "power", "rpm", "vibration_level", "visual_damage"]:
            X.append(float(val))
        else:
            # categorical - attempt to encode using provided encoders if available
            if encoders and col in encoders:
                enc_map = encoders[col]
                if val in enc_map:
                    X.append(enc_map[val])
                else:
                    # unknown category: add as new index
                    new_idx = len(enc_map)
                    X.append(new_idx)
            else:
                # fallback: try numeric cast, otherwise keep string
                try:
                    X.append(int(val))
                except Exception:
                    X.append(val)
    return [X]


@app.route("/", methods=["GET"]) 
def index():
    return render_template("index.html")


@app.route("/diagnose", methods=["POST"])
def diagnose():
    # Solve: return a rendered page in all cases so the client doesn't receive redirects on error.
    try:
        df = pd.read_csv(DATA_PATH)
        categorical = ["noise_level", "operating_condition", "maintenance_status"]
        encoders = build_label_encoders(df, categorical)
        X_test = preprocess_input(request.form, encoders=encoders)
        feature_cols = ["current", "voltage", "power", "rpm", "vibration_level", "visual_damage", "noise_level", "operating_condition", "maintenance_status"]
        # Ensure numeric columns are numeric and categorical columns are encoded using the encoders
        numeric_cols = ["current", "voltage", "power", "rpm", "vibration_level", "visual_damage"]
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce').fillna(0.0)
        for col in categorical:
            # map known categories to integers, unknowns become -1
            df[col] = df[col].astype(str).map(encoders[col]).fillna(-1).astype(int)

        X_train = df[feature_cols].values.astype(float)
        y_train = df["fault_label"].values
        model = train_model(X_train, y_train)
        pred = model.predict(X_test)
        return render_template("result.html", prediction=pred[0], input=request.form, error=None)
    except Exception as e:
        # log the exception server-side for debugging
        logger.exception("Error during diagnosis")
        # render the result page with an error message so the client sees what happened
        return render_template("result.html", prediction=None, input=request.form, error=str(e))


@app.route("/upload", methods=["POST"])
def upload():
    # Upload functionality removed per user request.
    # If this route is reached somehow, inform the client that the feature is disabled.
    flash("Upload feature is disabled.")
    return redirect(url_for("index"))


@app.route("/export", methods=["POST"])
def export_pdf():
    # simple CSV export of last diagnosis (placeholder)
    output = BytesIO()
    df = pd.read_csv(DATA_PATH)
    df.tail(1).to_csv(output, index=False)
    output.seek(0)
    return send_file(output, mimetype='text/csv', download_name='diagnosis_export.csv')


if __name__ == "__main__":
    app.run(port=5000, debug=True)
