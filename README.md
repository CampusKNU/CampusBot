### How to copy project to your directory


--- Windows tutorial --- 

1. Create new folder
```
mkdir StudmistoBot
git clone https://github.com/CampusKNU/CampusBot
```
2. create a [virtual enviromental](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)
```
python -m venv env 
```
3. Activate virtual enviromental
```
.\env\Scripts\activate
```
4. Install libraries
```
pip install -r requirements.txt
```


Structure of project: 

CampusBOT/
│
├── src/
│   ├── __init__.py
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── bot.py          # Main bot logic
│   │   ├── admin.py        # Admin commands and logic
│   │   └── user.py         # User commands and logic
│   │
│   └── database/
│       ├── __init__.py
│       └── db_manager.py   # Database manager/helper functions
│
├── tests/
│   ├── __init__.py
│   ├── test_bot.py     # Tests for bot functionality
│   └── test_db.py      # Tests for database functions
│
├── .env                # Configuration file (e.g., API keys, database connection info)
│
└── requirements.txt    # Dependencies