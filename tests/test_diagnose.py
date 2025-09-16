import pytest


def test_diagnose_endpoint():
    # Import the loader from main to get the Flask app object without running the server
    from main import load_flask_app

    app = load_flask_app()
    client = app.test_client()

    data = {
        "current": "5.0",
        "voltage": "220.0",
        "power": "1000.0",
        "rpm": "1450",
        "vibration_level": "0.2",
        "visual_damage": "0",
        "noise_level": "Low",
        "operating_condition": "Normal",
        "maintenance_status": "none",
    }

    resp = client.post("/diagnose", data=data, follow_redirects=True)
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    # Expect either a prediction shown or an error message rendered
    assert ("Prediction:" in html) or ("Error:" in html)
