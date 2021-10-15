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

The following setup was tested on pop-os 18.04 .

### 1. Set Up Python Virtual Environment

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

### 2. Set Up the `trivia` and `trivia_test` Database

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

### 3.1. (Optional) If needed, grant ownership of tables to user `myuser`
```
alter table categories owner to myuser;
alter table questions owner to myuser;
```

### 3.2. (Optional) Alternatively, grant privileges on all tables to user `myuser`
```
sudo -u postgres -i
psql trivia
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO myuser;
```

### 4. Create `.env` file with POSTGRES credentials
Create an `.env` in `backend` folder with your POSTGRES username and password:
```
POSTGRES_USER=replace with your username
POSTGRES_PASSWORD=replace with your password
```

e.g.)
```
POSTGRES_USER=myuser
POSTGRES_PASSWORD=password
```

### 5. Run Flask App Development Server
In a terminal from the `backend` directory, run:
```
export FLASK_APP=flaskr
export FLASK_ENV=development # enables debug mode
flask run
```

### 6. Run tests
In a terminal from the `backend` directory, run:
```
python -m test_flaskr
```

### 7. Run React Frontend

In a terminal from the `frontend` directory, install the node packages. You only need to perform this once:
```
npm install
```

In a terminal from the `frontend` directory, start the frontend app:
```
npm start
```

## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable

### Endpoints

---

#### GET /categories
- General:
  - Returns a list of questions categories.
- Request Parameters: **None**
- Request Headers: **None**
- Sample: `curl http://127.0.0.1:5000/categories`

```
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "success": true
}
```

---

#### GET /questions
- General:
  - Returns a list of questions, number of total questions, current category, categories.
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Request Parameters:
  - **`page`** Integer
- Request Headers: **None**
- Sample: 
  - `curl http://127.0.0.1:5000/questions`
  - `curl http://127.0.0.1:5000/questions?page=2`
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "currentCategory": null, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "totalQuestions": 21
}
```

---

#### DELETE /questions/{question_id}
- General
  - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value.
- Request Parameters: **None**
- Request Headers: **None**
- Sample: `curl http://127.0.0.1:5000/questions/27 -X DELETE`

```
{
  "questionID": 27, 
  "success": true
}
```

---

#### POST /questions
- General
 - If the new question and answer text, difficulty and category score are provided, a new question will be created.
 - If a search term is given instead, it will return any questions for whom the search term is a substring of the question.
- Request Parameters (For Creating Question): **None**
- Request Headers (For Creating Question):
  - **`question`** String
  - **`answer`** String
  - **`category`** Integer
  - **`difficulty`** Integer
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "Test question", "answer": "Test answer", "category": 1, "difficulty": 1}'`

```
{
  "created": 28, 
  "success": true
}
```
- Request Parameters (For Searching): **None**
- Request Headers (For Searching):
  - **`searchTerm`** String
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "country"}'`

```
{
  "currentCategory": null, 
  "questions": [
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ], 
  "success": true, 
  "totalQuestions": 1
}
```

---

#### GET /categories/{category_id}/questions
- General
  - Retrieves questions based on the given category id.
- Request Parameters (For Creating Question):
  - **`category_id`** Integer
- Request Headers (For Creating Question):
  - **None**
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`

```
{
  "currentCategory": "Science", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Test answer", 
      "category": 1, 
      "difficulty": 1, 
      "id": 26, 
      "question": "Test question"
    }
  ], 
  "success": true, 
  "totalQuestions": 4
}
```

---

#### POST /quizzes
- General
  - Play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
- Request Parameters (For Creating Question): **None**
- Request Headers (For Creating Question):
  - **`previous_questions`** Array of Integers
  - **`quiz_category`** JSON
    - **`type`** String
    - **`id`** Integer
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [1,2,3,4,5,20], "quiz_category" : {"type" : "Science", "id" : 1}}'`

```
{
  "question": {
    "answer": "Mona Lisa", 
    "category": 2, 
    "difficulty": 3, 
    "id": 17, 
    "question": "La Giaconda is better known as what?"
  }, 
  "success": true
}
```