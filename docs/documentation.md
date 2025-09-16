# Induction Motor Fault Diagnosis - Documentation

## Overview
This project provides an AI-powered system for diagnosing faults in induction motors using operational data. It features a graphical user interface (GUI) for easy data entry, model evaluation, and result export.

## Detailed Project Explanation

### Project Idea
This project aims to automate the diagnosis of faults in induction motors using artificial intelligence. The system collects operational data (such as current, voltage, vibration, temperature, etc.) and uses machine learning models to classify the motor status (Healthy, Faulty, and fault type).

### Main Components
- **Graphical User Interface (GUI):** Built with Tkinter, allows users to enter data manually, upload CSV files, and interact with the model easily.
- **Data Preprocessing:** Cleans and encodes input data, handles missing values, and prepares features for modeling.
- **Machine Learning Model:** Trained using scikit-learn, supports online learning (model updates with new data), and provides predictions for new inputs.
- **Visualization:** Uses matplotlib and seaborn to plot data distributions, feature correlations, and model evaluation metrics.
- **PDF Export:** Generates a PDF report for each diagnosis, including input data and prediction results.
- **Live/Simulated Data Testing:** Users can test the model on real-time entered data or generate random simulated data for robustness checks.

### Workflow
1. **Data Entry:** User enters motor data manually or uploads a CSV file containing multiple records.
2. **Preprocessing:** The system cleans and encodes the data, handling categorical and numerical features.
3. **Model Training:** The model is trained (or updated) using the available data. Online learning allows the model to improve as new data is added.
4. **Diagnosis:** The user can diagnose faults for new data, view the result instantly, and add the result to the training set for future improvement.
5. **Visualization:** The user can view data distribution, feature importance, and confusion matrix to understand model performance.
6. **Export:** The user can export the diagnosis result and input data to a PDF report for documentation or sharing.

### Example Scenarios
- **Manual Diagnosis:** Enter operational values (current, voltage, vibration, etc.) and get instant fault prediction.
- **Batch Diagnosis:** Upload a CSV file with multiple motor records and diagnose all at once.
- **Model Evaluation:** View accuracy, confusion matrix, and feature importance to assess model reliability.
- **Simulated Testing:** Generate random data within logical ranges and test the model's robustness.
- **Online Learning:** Add new diagnosis results to the training data and update the model for better future predictions.

### Usage Example
1. Run `main.py` to launch the GUI.
2. Enter or upload motor data.
3. Click "Diagnose" to get results.
4. View model evaluation and plots.
5. Export results to PDF if needed.

### Technologies Used
- Python 3.9
- Tkinter (GUI)
- pandas, numpy (data handling)
- scikit-learn (ML)
- matplotlib, seaborn (visualization)
- fpdf (PDF export)
- openpyxl (Excel support)
- lime, shap (model explanation)

### Notes
- For full functionality, use Python 3.9 due to SHAP/llvmlite compatibility.
- All features are modular and can be extended for more advanced diagnostics or integration with IoT sensors.

## Features
- **Graphical User Interface (Tkinter):** Enter data manually, upload CSV files, and interact with the model.
- **Live/Simulated Data Testing:** Test the model on real or randomly generated data.
- **Online Learning:** Add manual diagnosis to training data and update the model instantly.
- **Export to PDF:** Save diagnosis results and inputs as a PDF report.
- **Model Evaluation:** View accuracy, confusion matrix, and feature importance.
- **Data Visualization:** Plot data distributions and feature correlations using matplotlib/seaborn.

## Project Structure
```
induction-motor-fault-diagnosis/
├── main.py
├── src/
│   ├── data/
│   ├── models/
│   └── utils/
├── data/
├── docs/
│   └── documentation.md
├── notebooks/
└── README.md
```

## Environment Setup
- **Recommended Python Version:** 3.9
- **Dependencies:**
  - numpy, pandas, scikit-learn, matplotlib, seaborn, fpdf, openpyxl, lime, shap, flask-login, tk
- **Setup Steps:**
  1. Create a Python 3.9 virtual environment
  2. Install dependencies from `pyproject.toml` or manually
  3. Run `main.py` to launch the GUI

## Usage
1. Launch the GUI with `python main.py`
2. Enter motor data manually or upload a CSV file
3. Diagnose faults and view results
4. Export results to PDF or visualize data
5. Test model on live or simulated data

## Known Issues
- Library `shap` requires Python <3.10 due to `llvmlite` limitation. Use Python 3.9 for full feature support.

## Contributing
- Fork the repository and create a feature branch
- Commit changes with clear messages
- Submit pull requests for review

## Contact
For questions or support, open an issue on GitHub or contact the project owner.
