from enum import Enum
import json
from json import JSONDecodeError
import html
import os
import random
import requests


URL = "https://opentdb.com/api.php"
URL_CATEGORY = "https://opentdb.com/api_category.php"
FILENAME_CATEGORY = "category.json"
FILENAME_QUESTIONS = "questions.json"


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


class Difficulty(Enum):
    easy = 1
    medium = 2
    hard = 3


class Question:
    question = []

    def create_questions(self, question_json: json = None) -> list:
        if question_json:
            self.question_json = question_json
            for question in question_json:
                if 'question' in question and 'correct_answer' in question \
                        and 'incorrect_answers' in question:
                    self.question.append(self.transform_question(question))
            return self.question

    def print_question(self, index: int) -> dict:
        if len(self.question) > index and 'question' in self.question[index] \
                and 'answers' in self.question[index]:
            print(f"{self.question[index]['question']}")
            for i, answer in enumerate(self.question[index]['answers']):
                print(f'{i + 1} - {answer}')
            print()
            return self.question[index]

    def transform_question(self, question: dict) -> dict:
        transformed_question = {}
        if 'question' in question \
                and 'correct_answer' in question \
                and 'incorrect_answers' in question:
            transformed_question['question'] = \
                html.unescape(question['question'])
            all_answers = question['incorrect_answers']
            all_answers.append(question['correct_answer'])
            random.shuffle(all_answers)
            transformed_question['answers'] = []
            for index, answer in enumerate(all_answers):
                transformed_question['answers'].append(html.unescape(answer))
                if answer == question['correct_answer']:
                    transformed_question['index_correct_answer'] = index
            return transformed_question

    def is_correct_answer(self, question: dict, index: int) -> bool:
        if 'index_correct_answer' in question and \
                index == question['index_correct_answer']:
            return True
        return False

    def print_questions(self) -> None:
        for q in range(len(self.question)):
            self.print_question(q)


class Score:
    def __init__(self):
        self._point = 0
        self._name = ""

    @property
    def point(self) -> int:
        return self._point

    @point.setter
    def point(self, point: int) -> int:
        if not isinstance(point, int):
            raise ValueError("Value point must be an integer!")
        if point < 0:
            raise ValueError("Value point must be positive!")
        self._point = point
        return self._point

    def point_add(self, point: int) -> int:
        self.point += point
        return self.point

    @property
    def name(self) -> int:
        return self._name

    @name.setter
    def name(self, name: int) -> int:
        self._name = name
        return self._name

    def __str__(self) -> str:
        return f'{self.name}: {self.point}'


class FileManager:
    @staticmethod
    def save_json_to_file(filename: str, data: dict | list) -> dict | list:
        with open(filename, "w", encoding="UTF-8") as file:
            json.dump(data, file)
            return data

    @staticmethod
    def load_json_from_file(filename: str) -> dict | list:
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                return data
        except JSONDecodeError:
            pass


class Quiz:
    def __init__(
            self,
            filename_questions=FILENAME_QUESTIONS,
            filename_category=FILENAME_CATEGORY
            ):
        self.filename_questions = filename_questions
        self.filename_category = filename_category

    def get_questions(self) -> json:
        url = f'{URL}?amount=10&'\
              + f'category={self.category_number}&difficulty={self.difficutly}'
        response = requests.get(url)
        if response.status_code:
            if response.json()['response_code'] == 0:
                self.questions = response.json()['results']
                FileManager().save_json_to_file(
                    self.filename_questions,
                    self.questions
                    )
                return self.questions
            else:
                print("Something went wrong. Please, try again!")
                input("Press any key to continue")
        else:
            print("Something went wrong. Please, try again!")
            input("Press any key to continue")

    def get_category_from_api(self):
        response = requests.get(URL_CATEGORY)
        if response.status_code:
            if "trivia_categories" in response.json():
                FileManager().save_json_to_file(
                        self.filename_category,
                        response.json()["trivia_categories"]
                        )

    def get_category_from_file(self, filename: str) -> json:
        if os.path.exists(filename):
            self.category = FileManager().load_json_from_file(filename)
            return self.category

    def print_category(self) -> None:
        for cat in self.category:
            print(f'{cat["id"]} - {cat["name"]}')

    def is_category_number_correct(
            self,
            category_number: int,
            ) -> bool:
        for cat in self.category:
            if "id" in cat and cat["id"] == category_number:
                return True
        return False

    def choose_difficulty(self) -> int | None:
        while True:
            text_input = "Please, choose difficulty level: "
            text_input += "1- Easy, 2- Medium, 3-Hard, 4-Exit: "
            difficutly = input(text_input)
            try:
                if int(difficutly) in [1, 2, 3]:
                    self.difficutly = Difficulty(int(difficutly)).name
                    return self.difficutly
                elif difficutly == "4":
                    exit()
            except ValueError:
                print("Wrong difficutly. Please, try again!")
                input("Press any key to continue")

    def choose_category(self) -> int | None:
        while True:
            try:
                self.print_category()
                print("Please, choose the category number: ")
                category_number = int(input())
                if not self.is_category_number_correct(category_number):
                    print("Wrong category. Please, try again!")
                    input("Press any key to continue")
                else:
                    self.category_number = category_number
                    return category_number
            except ValueError:
                print("Wrong category. Please, try again!")
                input("Press any key to continue")


def main():
    clear_console()
    print("Hello, welcome to our online quiz consisting of 10 questions!")
    score = Score()
    score.name = input("Your name: ")
    print(f'Hello {score.name}!')
    quiz = Quiz()
    category = quiz.get_category_from_file(FILENAME_CATEGORY)
    if category:
        quiz.choose_difficulty()
        quiz.choose_category()
        question_json = quiz.get_questions()
        question = Question()
        question.create_questions(question_json)
        for i in range(len(question.question)):
            clear_console()
            current_question = question.print_question(i)
            while True:
                answer = input("Your answer: ")
                try:
                    number_answer = int(answer)
                    if question.is_correct_answer(
                        current_question,
                        number_answer - 1
                            ):
                        score.point_add(10)
                        print("Correct answer!")
                        print(f"Your points: {score.point}\n")
                        input("Press any key to continue")

                    else:
                        print(f"Wrong answer! The correct answer is {current_question['answers'][int(current_question['index_correct_answer'])]}")
                        input("Press any key to continue")
                    break
                except ValueError:
                    print("Please choose an integer!")
                    input("Press any key to continue")

        print(f"Congratulations {score.name}! Your points: {score.point}")

    else:
        print("Something went wrong. No file with categories.")


if __name__ == "__main__":
    main()
