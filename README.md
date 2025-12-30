Requirements:
**Supabase** https://supabase.com - create a user, free plan is perfect

**Update OS**
- example Ubuntu

``sudo apt update
sudo apt install -y   build-essential   libssl-dev   zlib1g-dev   libbz2-dev\
libreadline-dev   libsqlite3-dev   libncursesw5-dev   libffi-dev   liblzma-dev\
tk-dev   uuid-dev   libgdbm-dev   libnss3-dev   libedit-dev   libexpat1-dev
``

Optional but highly recommended:
**pyenv** https://github.com/pyenv/pyenv

``curl -fsSL https://pyenv.run | bash``

Setup:
Create a virtualenv with pyenv

``pyenv virtualenv webauth-webpage
cd ~/projects/webauth-webpage
pyenv local webauth-webpage``

Clone the repo:

``git clone https://github.com/thecocoa/webauth-webpage.git``

Install the requirements:
``pip install -r requirements.txt``

Run the example:
``flask run``

