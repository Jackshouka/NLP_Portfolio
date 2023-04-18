To run, set up a python venv and install the following in a terminal window:
venv setup:
    pip install virtualenv
    virtualenv botenv
    (For linux/mac - venv activation): source botenv/bin/activate
    (For Windows) - botenv\Scripts\activate

Required Packages:
    pip install tensorflow spacy
    python -m spacy download en_core_web_sm
    pip install scikit-learn
    pip install nltk

And you're all set! To run the chatbot, enter 'python3 driver_bot.py' for linx/mac (I don't know windows sorry.)