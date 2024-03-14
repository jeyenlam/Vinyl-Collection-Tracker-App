from website import create_app

# Create the Flask application instance
app = create_app()

if __name__ == '__main__':
  # Run the Flask application in debug mode if the script is run directly
  app.run(debug=True)