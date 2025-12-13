# Fraud Detection Django App (skeleton)
This project contains a Django web application skeleton integrating a machine learning model,
M-Pesa Daraja (STK Push) and Gava Connect (SMS) placeholders. It is intended for academic/demo use.
Thew model is trained using XGBoost algorithm and Random Forest Regressor using Jupyter notebook then imported as a .pkl file

## Setup
1. Create and activate a python virtualenv (Python 3.8+)
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Populate `.env` from `.env.example` and set correct values (DARJA keys, GAVA URL, MODEL_PATH)
3. Run migrations and create superuser:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
4. Run server:
   ```bash
   python manage.py runserver
   ```
5. For Daraja callbacks use a public URL (ngrok) and set DARJA_CALLBACK_URL in .env.

## Notes
- This is a skeleton and placeholders must be adapted to your model's feature expectations.
- Place your trained model .pkl at the path defined in MODEL_PATH in the .env file.
