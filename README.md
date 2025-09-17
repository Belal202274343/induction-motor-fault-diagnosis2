````markdown
# Induction Motor Fault Diagnosis

An AI project to classify induction motor condition (Healthy or Faulty) using manually entered operational data.

# Induction Motor Fault Diagnosis

An AI project to classify induction motor condition (Healthy or Faulty) using manually entered operational data.

## Team Information

|   AC.NO   | Name                  | Role | Contributions |
|-----------|-----------------------|------|---------------|
| 202274343 | Belal Mohammed Modaes | Data Collection & Preprocessing | Designed CSV schema, cleaned data |
| 202073229 | Monawar Mashaal Ali   | ML Engineer | Feature engineering, model training |
| 202274130 | Kreem Abdul-Wahed     | QA & Documentation | Testing, report writing |

## Project Setup Instructions

```bash
git clone <repository-url>
cd induction-motor-fault-diagnosis
# create and activate a uv, then install dependencies
Initialize Project: uv init --python 3.12

Add Dependencies: uv add pandas scikit-learn matplotlib jupyter

Install Dependencies: uv sync

Run Scripts: uv run python main.py
```

## Recent changes (summary)

- Migrated the desktop GUI to a Flask-based web UI located in `src/webapp/`.
- Removed the CSV upload/merge feature by request; the app now uses the local dataset at `data/motor_fault_sample_ordered.csv` and will not accept uploaded CSVs.
- Preprocessing now builds categorical encoders from the dataset at runtime and uses them to encode categorical features before training/prediction.
- UI modernization: added updated CSS and a small JS file for micro-interactions (`src/webapp/static/style.css`, `src/webapp/static/script.js`).


## Project Structure

```
induction-motor-fault-diagnosis/
├── README.md
├── pyproject.toml
├── requirements.txt     # optional, minimal install list
├── main.py              # launcher that loads src/webapp/app.py
├── src/
│   ├── webapp/          # Flask app (templates + static)
│   │   ├── app.py
│   │   ├── templates/
│   │   │   ├── index.html
│   │   │   └── result.html
│   │   └── static/
│   │       ├── style.css
│   │       └── script.js
│   ├── data/            # Data preprocessing modules
│   └── models/          # ML model definitions & helpers
├── notebooks/           # Jupyter notebooks for EDA & experiments
├── data/                # CSV data (motor_fault_sample_ordered.csv)
├── tests/
│   └── test_diagnose.py # basic endpoint test using Flask test client
└── docs/                # Documentation & diagrams
```

## Usage Examples

```python
from src.models import train_model
model = train_model("data/motor_fault_sample_ordered.csv")
```

## Results & Performance

### Results

- Accuracy: 92%
- F1-score for BearingFault: 0.90
- Key Insight: Temperature + vibration level were most important features.

## Contributing

- Follow feature-branch workflow
- Submit pull requests for review
- Keep commits focused and atomic
- Use descriptive commit messages
- Update documentation as needed
