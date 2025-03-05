import os
import sys
import subprocess

def setup_heroku():
    """Set up NLTK data for Heroku deployment."""
    # Run NLTK downloader
    try:
        from download_nltk_data import download_nltk_data
        download_nltk_data()
        print("NLTK data downloaded successfully.")
    except Exception as e:
        print(f"Failed to download NLTK data: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    setup_heroku()
