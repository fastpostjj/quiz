# The quiz


The program implements a quiz. It gets questions from API 'https://opentdb.com'.

At the beginning the program prompts the user for their name.

    Hello, welcome to our online quiz consisting of 10 questions!
    Your name:

Next the program prompts the user to choose difficulty level or exit:

    1- Easy, 2- Medium, 3-Hard, 4-Exit:

Then the program prompts the user to choose the category of questions:

    9 - General Knowledge
    10 - Entertainment: Books
    11 - Entertainment: Film
    12 - Entertainment: Music
    ...

After that the program will ask 10 questions and prompt the user to choose right answer. If user choose correct answer the programs will print

    Your answer: [answer]
    Correct answer!
    Your points: [points earned]

If user choose incorrect answer the programs will print

    Your answer: [answer]
    Wrong answer! The correct answer is [answer]

If user enter not digit the program will reprompt:

    Please choose an integer!

At the end the program prints:

    Congratulations [user's name]! Your points: [points earned].

## Running the program

To run the program first execute

    python -m venv venv

Then execute

    -for Linux or MacOs:
    source venv/bin/activate

    or

    -for Windows:
    venv/Scripts/activate

Now execute

    python -m pip install -r requirements.txt

 Finally, execute

    python project.py

To test the program execute

    pytest

## The structure of the project

The file "project.py" contains the main  program. The files "category.json" and "questions.json" create while the program is working and contain all the categories, that are available and questions, that were received from API. The file "test_project.py" contains tests.
