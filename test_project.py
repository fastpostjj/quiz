import json
import os
import pytest
from unittest.mock import patch
from project import Quiz, Question, Score


def test_print_question_empty():
    question = Question()
    test_json = [
        {"key1": "value1"},
        {"key2": "value2"},
        ]
    question.create_questions(test_json)
    print(question.question)
    assert question.print_question(0) is None


def test_print_question(capsys):
    question = Question()
    test_json = [
        {
            "question": "text_question1",
            "correct_answer": "text_answer",
            "incorrect_answers": [
                "text_answer",
                "text_answer"
                ]
        },
        {
            "question": "text_question2",
            "correct_answer": "text_answer",
            "incorrect_answers": [
                "text_answers",
                "text_answers"
                ]
        }
        ]
    question.create_questions(test_json)
    question.print_question(0)
    captured = capsys.readouterr()
    assert captured.out.strip() == "text_question1\n" \
        + "1 - text_answer\n" \
        + "2 - text_answer\n" \
        + "3 - text_answer"


def test_transform_question():
    question = Question()
    test_json = [
        {
            "question": "text_&quot;question1&quot;",
            "correct_answer": "text_&quot;answer&quot;",
            "incorrect_answers": [
                "text_&quot;answer&quot;",
                "text_&quot;answer&quot;"
                ]
        }
        ]
    res = question.transform_question(test_json[0])
    assert res["question"] == 'text_"question1"'
    assert res["answers"][0] == 'text_"answer"'


def test_is_correct_answer():
    question = Question()
    text_question = [
        {
            "question": "text_question1",
            "correct_answer": "text_answer1",
            "incorrect_answers": [
                "text_answer2",
                "text_answer3"
                ],
            "index_correct_answer": 1
        }
        ]
    result = question.is_correct_answer(text_question[0], 1)
    assert result
    result = question.is_correct_answer(text_question[0], 2)
    assert not result
    result = question.is_correct_answer(text_question[0], 5)
    assert not result


def test_score():
    score = Score()
    score.name = "test_name"
    assert score.name == "test_name"
    score.point = 5
    assert score.point == 5
    with pytest.raises(ValueError):
        score.point = 5.2
    with pytest.raises(ValueError):
        score.point = -3


def test_score_add_point():
    score = Score()
    score.point_add(10)
    assert score.point == 10


def test_choose_valid_category():
    quiz = Quiz()
    quiz.category = [
        {"id": 1, "name": "test_name1"},
        {"id": 2, "name": "test_name2"},
        {"id": 5, "name": "test_name5"}
        ]
    with patch('builtins.input', side_effect=['1', '2', '5']):
        chosen_category = quiz.choose_category()
        assert chosen_category == 1
        chosen_category = quiz.choose_category()
        assert chosen_category == 2
        chosen_category = quiz.choose_category()
        assert chosen_category == 5


def test_choose_difficulty_valid_input():
    quiz = Quiz()
    with patch('builtins.input', return_value='1'):
        chosen_difficulty = quiz.choose_difficulty()
        assert chosen_difficulty == "easy"
    with patch('builtins.input', return_value='2'):
        chosen_difficulty = quiz.choose_difficulty()
        assert chosen_difficulty == "medium"
    with patch('builtins.input', return_value='3'):
        chosen_difficulty = quiz.choose_difficulty()
        assert chosen_difficulty == "hard"


def test_is_category_number_correct():
    quiz = Quiz()
    quiz.category = [
        {"id": 1, "name": "test_name1"},
        {"id": 2, "name": "test_name2"},
        {"id": 5, "name": "test_name5"}
        ]
    assert quiz.is_category_number_correct(1)
    assert not quiz.is_category_number_correct(6)


def test_print_category(capsys):
    quiz = Quiz()
    quiz.category = [
        {"id": 1, "name": "test_name1"},
        {"id": 2, "name": "test_name2"},
        {"id": 5, "name": "test_name5"}
        ]
    quiz.print_category()
    captured = capsys.readouterr()
    assert captured.out.strip() == "1 - test_name1\n" \
        + "2 - test_name2\n" \
        + "5 - test_name5"


def test_get_category_from_file():
    quiz = Quiz()
    quiz_category = [
        {"id": 1, "name": "test_name1"},
        {"id": 2, "name": "test_name2"},
        {"id": 5, "name": "test_name5"}
        ]
    filename = "test.json"
    with open(filename, "w", encoding="UTF-8") as file:
        json.dump(quiz_category, file)
    result = quiz.get_category_from_file(filename)
    assert result == quiz_category
    if os.path.exists(filename):
        os.remove(filename)


def test_get_category_from_api():
    pass


def test_get_questions_valid():
    with patch('requests.get') as mock_get:
        mock_json = {
            'response_code': 0,
            'results': [{'question': 'Question 1', 'answer': 'Answer 1'}]
        }
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = mock_json
        filename = "test_question.json"
        quiz = Quiz(filename)
        quiz.category_number = 1
        quiz.difficutly = 'easy'
        questions = quiz.get_questions()

        assert questions == mock_json['results']
        mock_get.assert_called_once_with('https://opentdb.com/api.php?amount=10&category=1&difficulty=easy')
        if os.path.exists(filename):
            os.remove(filename)

