# Understanding app.json for Heroku Deployment

The `app.json` file in your project defines how your Django application gets deployed on Heroku. It's particularly useful for setting up consistent environments and enabling features like Review Apps, Button deployments, and Pipeline promotions.

## Key Components of app.json

### Basic Metadata
```json
{
  "name": "gdanalystv2",
  "description": "GD Analyst application",
  "repository": "https://github.com/ebzimny01/gdanalystv2",
  "keywords": ["python", "django", "nltk"]
}
```
- **name**: Identifies your application on Heroku
- **description**: A brief explanation of what your application does
- **repository**: The GitHub repository URL
- **keywords**: Tags that categorize your application (helps with discovery)

### Scripts
```json
"scripts": {
  "postdeploy": "python nltk_setup.py"
}
```
- **postdeploy**: Commands that run after your application is deployed but before it's available to users
- In this case, it runs your NLTK setup script to download required language data

### Environment Variables
```json
"env": {
  "NLTK_DATA": {
    "description": "Path where NLTK data will be stored",
    "value": "/app/nltk_data"
  }
}
```
- **env**: Defines environment variables for your application
- **NLTK_DATA**: Sets the path where NLTK will store and look for its data files
- Each variable can have a description and default value

### Buildpacks
```json
"buildpacks": [
  {
    "url": "heroku/python"
  }
]
```
- **buildpacks**: Lists the Heroku buildpacks required by your application
- **heroku/python**: The standard Python buildpack that handles dependencies in requirements.txt

### Formation (Dyno Configuration)
```json
"formation": {
  "web": {
    "quantity": 1,
    "size": "eco"
  },
  "worker": {
    "quantity": 1, 
    "size": "eco"
  }
}
```
- **formation**: Defines the dyno types and their configuration
- **web**: The web process that handles HTTP traffic (defined in your Procfile)
- **worker**: The background worker process (handles RQ jobs)
- **quantity**: Number of dynos of each type
- **size**: The dyno size ("eco" is Heroku's most affordable tier)

## How app.json Is Used

1. **Heroku Button Deployments**: Allows one-click deployment of your app
2. **Review Apps**: Enables automatic creation of temporary apps for pull requests
3. **Pipeline Promotions**: Helps maintain consistent configuration when promoting between environments
4. **Add-on Provisioning**: Can automatically provision required add-ons

## Benefits for Your Django App

- Ensures NLTK data is properly set up on deployment
- Maintains consistent dyno configuration
- Documents the application's requirements in a standardized format
- Makes it easier to set up development/staging environments that match production

## Common Customizations

- Add database add-ons
- Configure Redis for your Django RQ workers
- Set Django-specific environment variables
- Configure additional buildpacks (e.g., for static asset compilation)
