"""
Setup script for development environment
Run this to set up the backend for development
"""
import os
import sys
from pathlib import Path


def create_env_file():
    """Create .env file from .env.example if it doesn't exist"""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if not env_file.exists() and env_example.exists():
        print("Creating .env file from .env.example...")
        env_file.write_text(env_example.read_text())
        print("✓ .env file created. Please edit it with your settings.")
    elif env_file.exists():
        print("✓ .env file already exists")
    else:
        print("⚠ Warning: .env.example not found")


def check_python_version():
    """Check if Python version is 3.11+"""
    if sys.version_info < (3, 11):
        print(f"⚠ Warning: Python 3.11+ recommended, you have {sys.version}")
        return False
    print(f"✓ Python version: {sys.version}")
    return True


def install_dependencies():
    """Install dependencies from requirements.txt"""
    import subprocess
    
    print("\nInstalling dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✓ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False


def run_tests():
    """Run tests to verify installation"""
    import subprocess
    
    print("\nRunning tests...")
    try:
        result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], check=False)
        if result.returncode == 0:
            print("✓ All tests passed")
            return True
        else:
            print("⚠ Some tests failed (this is expected if GraphDB is not running)")
            return False
    except Exception as e:
        print(f"⚠ Could not run tests: {e}")
        return False


def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "="*60)
    print("Setup Complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Edit .env file with your GraphDB settings")
    print("2. Start GraphDB: docker-compose up -d graphdb")
    print("3. Load RDF data into GraphDB repository 'knowledge-graph'")
    print("4. Run the development server:")
    print("   uvicorn app.main:app --reload --port 3000")
    print("\nAPI Documentation will be available at:")
    print("   http://localhost:3000/api/docs")
    print("\nTo run tests:")
    print("   pytest")
    print("\nTo run with coverage:")
    print("   pytest --cov=app")
    print("="*60)


def main():
    """Main setup function"""
    print("="*60)
    print("Knowledge Graph Backend - Development Setup")
    print("="*60)
    
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    # Run setup steps
    check_python_version()
    create_env_file()
    
    # Ask user if they want to install dependencies
    response = input("\nInstall dependencies now? (y/n): ").lower().strip()
    if response == 'y':
        install_dependencies()
        
        # Ask if they want to run tests
        response = input("\nRun tests? (y/n): ").lower().strip()
        if response == 'y':
            run_tests()
    
    print_next_steps()


if __name__ == "__main__":
    main()
