# Posit Interview Test Solution

## Requirements

- Python 3.11 or higher
- Chrome installed on your machine

## User Guide

### 1. Install the required packages

```bash
pip install -r requirements.txt
```

### 2. Setup your .env file

Copy the file `.env.template` to `.env` and fill in the required values.

```bash
cp .env.template .env
```

The `.env` file should look like this:

```sh
POSIT_TEST_FULLNAME=
POSIT_TEST_USERNAME=
POSIT_TEST_PASSWORD=
```

### 3. Run the script

```bash
pytest test_posit.py
```

## Notes

- The script will automatically download the latest version of ChromeDriver for your OS.
- The script will try to create a test space for each run and clean it up afterwards.
- Free accounts can only have 1 test space beyond the default "Your Workspace".
- The script will refuse to clean up any workspace not named "Test Space X" to prevent accidental deletion of important data.
- If you do not have room to creata a new space, the script will fail.
