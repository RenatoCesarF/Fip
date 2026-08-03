<img width="1440" height="323" alt="Fip banner" src="https://github.com/user-attachments/assets/dae7dd95-3e8e-4244-9cd3-d77f5bb0b29c" />

# Fip

### A fast and simple app to filter pictures by favoriting or deleting them

The initial idea was to use this app to review photographs taken during a photoshoot session, but you can use it however you want.

## Features

* Import pictures from a folder
* Manipulate each picture:

  * Rotate
  * Zoom in
  * Zoom out
* Favorite pictures and save them inside a `/favs` folder
* Mark unwanted pictures using `X` and delete them at the end of the filtering process

## Requirements

* Python 3
* pip

## Installation

Clone the repository:

```bash
git clone https://github.com/RenatoCesarF/Fip
cd fip
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

### macOS and Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

## How to use

1. Open the application
2. Select the folder containing your pictures
3. Review and manipulate each picture
4. Favorite the pictures you want to keep
5. Mark unwanted pictures for deletion
6. Finish the filtering process to save favorites and delete marked pictures

## Screens

### Filter

<img width="1121" height="746" alt="Filter screen" src="https://github.com/user-attachments/assets/2cda3b9b-6610-40b5-b94d-791e3f99785c" />

### Home

<img width="1121" height="746" alt="Home screen" src="https://github.com/user-attachments/assets/2193ff5e-d559-4a73-afbe-8aa7449184f1" />
