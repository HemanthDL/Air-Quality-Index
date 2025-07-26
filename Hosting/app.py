from app.app import app  # Import the Flask app object from app/app.py

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
