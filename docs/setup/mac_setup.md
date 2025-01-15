# Mac Setup (M3)

## Setting up the environment

### Install Homebrew

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Install Pyenv

```
brew install pyenv
```

### Install Python 3.10 using Pyenv

1. Make sure to run your terminal with Rosetta.
    - Open Finder > Applications.
    - Right click on Terminal.
    - Click Get Info.
    - Check "Open using Rosetta"
    - Click "Open"
2. Install Python 3.10 using Pyenv
    ```
    pyenv install 3.10.12
    pyenv global 3.10.12
    ```
    ```
    echo 'export PATH="/opt/homebrew/Cellar/python@3.10/3.10.12/bin:$PATH"' >> ~/.zshrc
    ```
3. Install poppler
    ```
    brew install poppler
    ```
4. Install virtualenv
    ```
    pip install virtualenv
    which virtualenv
    ```

## Add SSH key to Github (if not already added)

Purpose: To allow you to push to Github without having to enter your password every time.

1. Generate SSH key
    ```
    ssh-keygen -t ed25519 -C "your_email@example.com"
    ```
2. View SSH key (copy the output)
    ```
    cat ~/.ssh/id_ed25519.pub
    ```
3. Add SSH key to Github
    - Go to Github settings
    - Click on SSH and GPG keys
    - Click on New SSH key
    - Paste your SSH key into the text box
    - Click Add SSH key
4. Test SSH connection
    ```
    ssh -T git@github.com
    ```

## Setting up the project

### Clone the repository

```
git clone git@github.com:cup-noodlehS/haircat-backend.git
cd haircat-backend
```

### Setup virtual environment

```
python3.10 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```
pip install -r requirements.txt
```

## Setup PostgreSQL

1. Install PostgreSQL
    ```
    brew install postgresql@14
    ```
2. Start PostgreSQL
    ```
    brew services start postgresql@14
    ```
3. Run psql
    ```
    psql postgres
    ```
4. Create user
    ```
    CREATE ROLE haircatuser WITH PASSWORD 'password' SUPERUSER CREATEROLE CREATEDB LOGIN;
    ```
5. Create database
    ```
    CREATE DATABASE haircat OWNER haircatuser;
    ```
6. Exit psql with CTRL + D
7. Restart PostgreSQL
    ```
    brew services restart postgresql@14
    ```
8. Run migrations `python haircat/manage.py migrate`

## Running the server

1. Activate virtual environment (once per session)
    ```
    source .venv/bin/activate
    ```
    > to deactivate, run `deactivate`
2. Run server
    ```
    python haircat/manage.py runserver
    ```

<p align="right">Last updated by <a href="https://github.com/cup-noodlehS"><b>Sheldon Arthur</b></a></p>
