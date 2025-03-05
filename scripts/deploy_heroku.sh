#! /bin/bash

echo "Deploying to Heroku with NLTK data setup..."

# First, make sure NLTK setup script is executable
chmod +x /home/edz/code/gdanalystv2/nltk_setup.py

# Ensure the necessary files are committed
git add nltk_setup.py Procfile app.json
git commit -m "Add NLTK setup for Heroku deployment"

# Push to Heroku
git push heroku main

# Run the NLTK setup script on Heroku immediately
echo "Running NLTK setup on Heroku..."
heroku run python nltk_setup.py

# Restart the dynos to ensure they use the new NLTK data
echo "Restarting Heroku dynos..."
heroku restart

echo "Deployment complete!"
