# LibraNet - Python Library Management System
**LibraNet** is a command-line library management system implemented in Python. It allows users to manage different types of library items, including:
- **Books** – track title, author, and page count.
- **Audiobooks** – track title, author, and duration; can be played.
- **E-Magazines** – track title, author, and issue number; can archive issues.
The system supports:
- Borrowing and returning items with automatic fine calculation for overdue returns.
- Searching items by title, type, or both.
- Persisting library data in a JSON file (`library.json`).
## Features
- List all items in the library.
- Borrow and return items with due date and fine calculation.
- Play audiobooks directly from the CLI.
- Search items by title, type, or title + type.
- Save and load library data automatically.
## Requirements
- Python 3.x
- Standard Python libraries: `json`, `os`, `datetime`, `abc`
## Setup
1. Clone the repository or download the project files.
2. Ensure the following files are present:
   - `libraNet.py` (main Python file)
   - `library.json` (optional; will be created automatically on first run)
3. Run the application:
```bash
python libraNet.py
