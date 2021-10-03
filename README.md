# Full Stack API Final Project


## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter) and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.
>Once you're ready, you can submit your project on the last page.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend
The [./backend](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter/backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


### Frontend

The [./frontend](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter/frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads? 

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. *./frontend/src/components/QuestionView.js*
2. *./frontend/src/components/FormView.js*
3. *./frontend/src/components/QuizView.js*


By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API. 



>View the [README within ./frontend for more details.](./frontend/README.md)

## Setup

For pop-os 18.04

### Set Up Python Virtual Environment

Create a new virtual environment:
```
python3 -m virtualenv fsndp2
```

Activate the environment:
```
source fsndp2/bin/activate
```

Install the pip dependencies
```
pip install -r requirements.txt
```

### Set Up the `trivia` and `trivia_test` Database

Start postgres:
```
sudo -u postgres -i
```

Create both databases:
```
createdb trivia
psql trivia < /home/xinlee/Documents/fsnd_p2/backend/trivia.psql
psql trivia_test < /home/xinlee/Documents/fsnd_p2/backend/trivia.psql
```

### Run Flask App

```
export FLASK_APP=flaskr
export FLASK_ENV=development # enables debug mode
flask run
```

### If needed, grant privileges on all tables to user `myuser`
```
sudo -u postgres -i
psql trivia
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO myuser;
```

### Alternatively, grant ownership of tables to user `myuser`
```
alter table categories owner to myuser;
alter table questions owner to myuser;
```

### Run tests

```
python -m test_flaskr
```


### Sample Curl Tests

```
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "country"}'
```

```
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "Test question", "answer": "Test answer", "category": 1, "difficulty": 1}'
```