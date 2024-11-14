# ECE461L-Team-Repo

this will be a place for our ECE 461L Software team to collaborate on the semester project and add/change files accordingly.

## Getting Started

### 1. Set Up a Virtual Environment

To ensure consistency in development, it's important to create a virtual environment. Follow these steps:

```bash
# Create a virtual environment (for Python 3)
python3 -m venv myvenv

# Activate the virtual environment:
# On macOS/Linux:
source myvenv/bin/activate
# On Windows:
myvenv\Scripts\activate
```

### 2. Install Dependencies

Once your virtual environment is set up and activated, install the required packages from the requirements.txt file:

```bash
#Install dependencies from requirements.txt
pip install -r requirements.txt
```

### 3. Update .gitignore
Before making any commits, make sure you add the virtual environment folder to the .gitignore file to avoid pushing it to the repository. Add the following line to **.gitignore**:
```bash 
myvenv/
```

### 4. Create a Branch for Your Changes
When working on a new feature or bug fix, always create a new branch before making any changes:

```bash
git checkout <your-branch-name>
```

Once you've made your changes, push your branch and create a pull request for review.

# Stage changes
```bash
git add .
```
# Commit changes
```bash
git commit -m "Add a description of your changes"
```
# Push branch to remote
```bash
git push origin <your-branch-name>
```