# Brokeman's Game Station
HTML5 game hosting & sharing site


## Tools

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)


## Getting Started

### Requirements:

- Python version 3.11+

- Python libraries:
  - Django
  - django-environ
  - psycopg2
  - boto3

A .env file should be located at `bgs/.env` containing
the following:

| Key        | Description                                                                                                     |
|------------|-----------------------------------------------------------------------------------------------------------------|
| SECRET_KEY | Arbitrary string for Django hashing & cryptographic signing.                                                    |
| DEBUG      | "True": Debug mode "False": Production                                                                          |
| DB_NAME    | Name for main postgresql database. Locally hosted for now. Make sure to create this db prior to running server. |
| PORT       | Server port number. Left unspecified, it will default to 3000.                                                  |

Migrate database changes to your local database
```shell
python manage.py migrate
```

Run server
```shell
python manage.py runserver
```

Optional: Use `do` script shortcut to run commands. Unix-only.
- Make `do` script executable `chmod +x ./do`
- Run python manage.py commands `./do <command>`
