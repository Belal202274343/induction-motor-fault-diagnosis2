# Induction Motor Fault Diagnosis

An AI project to classify induction motor condition (Healthy or Faulty) using manually entered operational data and interactive GUI.

## Team Information

| AC.NO | Name | Role | Contributions |
|------|------|------|---------------|
| 1 | Student 1 | Data Collection & Preprocessing | Designed CSV schema, cleaned data |
| 2 | Student 2 | ML Engineer | Feature engineering, model training |
| 3 | Student 3 | QA & Documentation | Testing, report writing |

## Project Setup Instructions

### Requirements
- Python 3.9 (recommended for full compatibility)
- All dependencies listed in `pyproject.toml` (see below)

### Environment Setup
```bash
git clone <repository-url>
cd induction-motor-fault-diagnosis
# Create Python 3.9 environment
python3.9 -m venv .venv-py39
.\.venv-py39\Scripts\activate
pip install --upgrade pip
pip install numpy pandas scikit-learn matplotlib jupyter seaborn fpdf openpyxl lime shap flask-login tk
uv sync  # (optional, if using uv)
uv run python main.py
```

### Known Issues
- Library `shap` requires Python <3.10 due to `llvmlite` limitation. Use Python 3.9 for full feature support.

## Project Structure

```
induction-motor-fault-diagnosis/
├── README.md
├── pyproject.toml
├── .python-version
├── main.py
├── src/
│   ├── data/        # Data preprocessing modules
│   ├── models/      # ML model definitions & training scripts
│   └── utils/       # Helper functions (feature engineering, encoding)
├── notebooks/       # Jupyter notebooks for EDA & experiments
├── data/            # CSV data (manual input + sample datasets)
└── docs/           # Documentation & diagrams
```

## Usage Examples

```python
from src.models import train_model
model = train_model("data/motor_fault_data.csv")
```

## Results & Performance

```markdown
## Results
- Accuracy: 92%
- F1-score for BearingFault: 0.90
- Key Insight: Temperature + vibration level were most important features.
```

## Contributing

## Features

- Graphical User Interface (Tkinter) for easy data entry and diagnosis
- Upload new CSV data and update the model instantly
- Export diagnosis results to PDF
- Model evaluation and confusion matrix visualization
- Data distribution plots (seaborn)
- Test model on live or simulated data
- Online learning: add manual diagnosis to training data

## How to Use

1. Run `main.py` to launch the GUI
2. Enter motor data manually or upload a CSV
3. Diagnose faults, view model evaluation, and export results
4. Use the simulation feature to test the model on random data

## Environment Notes

- For full compatibility, use Python 3.9 and install all dependencies as listed above.
- If you encounter issues with `shap` or `llvmlite`, downgrade Python or remove SHAP-dependent features.

- Follow feature-branch workflow
- Submit pull requests for review
- Keep commits focused and atomic
- Use descriptive commit messages
- Update documentation as needed
# induction-motor-fault-diagnosis
