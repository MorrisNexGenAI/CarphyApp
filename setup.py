# setup.py
import os

# Define the structure
structure = {
    "main.py": "",
    "carphy.kv": "",
    "database.py": "",
    "buildozer.spec": "",
    "README.md": "",
    "screens": {
        "__init__.py": "",
        "login_screen.py": "",
        "signup_screen.py": "",
        "home_screen.py": "",
        "course_screen.py": "",
        "pamphlet_screen.py": "",
        "cart_screen.py": "",
        "order_screen.py": "",
        "admin_screen.py": ""
    },
    "assets": {
        "icon.png": ""
    }
}

# Create directories and files
def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w") as f:
                f.write(content)

# Run the setup
if __name__ == "__main__":
    create_structure(".", structure)
    print("File structure created successfully!")