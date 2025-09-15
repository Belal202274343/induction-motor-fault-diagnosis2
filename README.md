# Induction Motor Fault Diagnosis

An AI project to classify induction motor condition (Healthy or Faulty) using manually entered operational data.

## Team Information

| AC.NO | Name | Role | Contributions |
|------|------|------|---------------|
| 1 | Student 1 | Data Collection & Preprocessing | Designed CSV schema, cleaned data |
| 2 | Student 2 | ML Engineer | Feature engineering, model training |
| 3 | Student 3 | QA & Documentation | Testing, report writing |

## Project Setup Instructions

```bash
git clone <repository-url>
cd induction-motor-fault-diagnosis
uv sync
uv run python main.py
```

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

- Follow feature-branch workflow
- Submit pull requests for review
- Keep commits focused and atomic
- Use descriptive commit messages
- Update documentation as needed
# induction-motor-fault-diagnosis
