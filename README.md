# Cloning and using

```bash
git@github.com:kapiosk/SimplzDND.git
cd SimplzDND
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
gunicorn --bind 0.0.0.0:5000 wsgi:app
```