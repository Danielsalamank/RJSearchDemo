# pip install flask nltk numpy networkx

export FLASK_APP=index.py
export FLASK_ENV=development
python -m nltk.downloader punkt
flask run --debug