import os
import zipfile

def create_deployment_package():
    """
    Creates a simple lambda deployment package.
    Note: For a real production build, dependencies from requirements.txt
    must be installed in a build directory before packaging, or ideally
    an AWS Lambda Container Image should be built for heavy ML dependencies.
    """
    print("Preparing Lambda deployment package...")
    
    # We create a lambda handler file for Mangum
    with open("lambda_handler.py", "w") as f:
        f.write("from mangum import Mangum\n")
        f.write("from app import app\n\n")
        f.write("handler = Mangum(app)\n")
        
    # Zip essential files
    files_to_zip = ["app.py", "ai_models.py", "automated_workflow.py", "lambda_handler.py", "requirements.txt"]
    zip_filename = "deployment_package.zip"
    
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in files_to_zip:
            if os.path.exists(file):
                zipf.write(file)
                print(f"Added {file} to {zip_filename}")
            else:
                print(f"Warning: {file} not found.")
                
    print(f"\nDeployment package created: {zip_filename}")
    print("Next steps:")
    print("1. Upload this ZIP to AWS Lambda and set the execution handler to 'lambda_handler.handler'.")
    print("2. Remember to package required libraries (fastapi, mangum, scikit-learn, etc.) as Lambda Layers, or use a Docker container image for deployment which is recommended for ML libraries.")

if __name__ == "__main__":
    create_deployment_package()
