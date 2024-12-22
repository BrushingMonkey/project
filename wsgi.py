from app import app  # Import your Flask app instance

# Expose the application as the WSGI callable
if __name__ == "__main__":
    app.run()
