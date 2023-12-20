# Installation du projet Huggy CamemBERT

1. git clone
```git clone git@bitbucket.org:insignagency/camembert.git```
2. Install rust for MacOS ```brew install rust```
3. Update pip ```pip install --upgrade pip```
4. Install the python lib with pip ```pip install -r requirements.txt```

---

## Build de l'application

### Steps:

1. **Docker Compose**

    Lancer le container mysql défini dans `docker-compose.yml`

    ```bash
    docker-compose up -d
    ```

2. **MySQL**

   Importer les données dans mysql

    ```bash
    mysql -h 127.0.0.1 -u root -p website < huggy.sql
    ```

    This command connects to the MySQL server running on localhost with the username 'root'. It will prompt you for the password. The `< huggy.sql` part of the command tells MySQL to execute the SQL commands from the `huggy.sql` file.

3. **Flask Server**

  Lancer le serveur http

   ```bash
   ./web/server.py
   ```
   L'url d'accès sera affichée lorsque le serveur sera prêt, url du type http://localhost:3006.

## Utilisation
Se rendre sur l'url fournie dans l'étape précédente.

## Built With

* [Docker](https://docker.com/)
* [MySQL](https://www.mysql.com/)
* [mysql-connector-python](https://pypi.org/project/mysql-connector-python/)
* [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
* [Transformers by Hugging Face](https://pypi.org/project/transformers/)
* [NumPy](https://pypi.org/project/numpy/)
* [SciPy](https://pypi.org/project/scipy/)
* [Scikit-Learn](https://pypi.org/project/scikit-learn/)
* [Sentence Transformers](https://pypi.org/project/sentence-transformers/)
* [Flask](https://flask.palletsprojects.com/en/2.3.x/)

## Google doc

   [gdoc](https://docs.google.com/document/d/1tfg18eZCPDAX9bsQqZ7joLcF_9x77NS-53cOqs48bOg/edit?usp=drive_link)

## Author

* **Cyprien Diederichs**