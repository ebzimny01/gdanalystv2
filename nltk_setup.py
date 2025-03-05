#! /usr/bin/env python3
"""
NLTK Setup Script for Heroku
This script properly downloads all required NLTK data packages for the application.
"""
import os
import sys
import nltk
import ssl

def setup_nltk_data():
    """Download required NLTK data packages and configure paths."""
    print("Setting up NLTK data...")
    
    # Define the directory where NLTK data will be stored
    nltk_data_dir = os.environ.get('NLTK_DATA', os.path.join(os.getcwd(), 'nltk_data'))
    os.makedirs(nltk_data_dir, exist_ok=True)
    
    # Add the NLTK data directory to the search path
    nltk.data.path.insert(0, nltk_data_dir)
    
    print(f"NLTK data directory: {nltk_data_dir}")
    print(f"NLTK search paths: {nltk.data.path}")
    
    # Handle SSL certificate issues that might occur on some platforms
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    
    # List of required NLTK packages
    required_packages = [
        'punkt',            # Standard tokenizer
        'punkt_tab',        # Specifically needed by the error message
        'averaged_perceptron_tagger',
        'wordnet',
        'stopwords',
        'omw-1.4'           # Open Multilingual WordNet
    ]
    
    # Download each package
    for package in required_packages:
        try:
            print(f"Downloading {package}...")
            nltk.download(package, download_dir=nltk_data_dir, quiet=False)
        except Exception as e:
            print(f"Error downloading {package}: {str(e)}")
            
            # For punkt_tab specifically, which might be part of punkt
            if package == 'punkt_tab':
                print("Note: punkt_tab is part of the punkt package. Creating a symbolic link...")
                try:
                    # Create tokenizers/punkt_tab if it doesn't exist
                    punkt_tab_dir = os.path.join(nltk_data_dir, 'tokenizers', 'punkt_tab')
                    os.makedirs(punkt_tab_dir, exist_ok=True)
                    
                    # Create english directory inside punkt_tab
                    os.makedirs(os.path.join(punkt_tab_dir, 'english'), exist_ok=True)
                    
                    # Link punkt files to punkt_tab - important for some NLTK versions
                    punkt_dir = os.path.join(nltk_data_dir, 'tokenizers', 'punkt')
                    if os.path.exists(punkt_dir):
                        for lang_dir in os.listdir(punkt_dir):
                            lang_path = os.path.join(punkt_dir, lang_dir)
                            if os.path.isdir(lang_path):
                                target_dir = os.path.join(punkt_tab_dir, lang_dir)
                                os.makedirs(target_dir, exist_ok=True)
                                for file in os.listdir(lang_path):
                                    src_file = os.path.join(lang_path, file)
                                    dst_file = os.path.join(target_dir, file)
                                    if os.path.isfile(src_file) and not os.path.exists(dst_file):
                                        with open(src_file, 'rb') as f_in:
                                            with open(dst_file, 'wb') as f_out:
                                                f_out.write(f_in.read())
                                        print(f"Copied {src_file} to {dst_file}")
                except Exception as e:
                    print(f"Error creating punkt_tab link: {str(e)}")

    # Verify the downloads
    print("\nVerifying NLTK data:")
    for package in required_packages:
        try:
            # For punkt_tab, check the directory structure
            if package == 'punkt_tab':
                tab_path = os.path.join(nltk_data_dir, 'tokenizers', 'punkt_tab')
                if os.path.exists(tab_path) and os.path.isdir(tab_path):
                    print(f"✓ {package} directory exists")
                else:
                    print(f"✗ {package} directory missing!")
            else:
                nltk.data.find(f'tokenizers/{package}')
                print(f"✓ {package} successfully installed")
        except LookupError:
            print(f"✗ {package} not found after download attempt!")

    print("\nNLTK setup complete!")

if __name__ == "__main__":
    setup_nltk_data()
