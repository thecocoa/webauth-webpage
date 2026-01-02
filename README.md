Requirements:
**Supabase** https://supabase.com - create a user, free plan is perfect<br>
You'll need a .env file in the repo's root.<br>  
Never commit this file.  
It contains information that should not be public.  

Make sure it contains:

``DATABASE_URL=<your database url
SUPABASE=<your supabase anon>
SUPABASE_SERVICE_KEY=<you see where I'm going here>``

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






