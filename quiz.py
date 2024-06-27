import streamlit as st
import os, random
from typing import List
from utils import read_file
from session_state import States

from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field, validator

loader = CSVLoader(file_path=f"{os.getcwd()}/resources/words.csv")
data = loader.load()

api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    api_key=api_key,
    temperature=States.get("temperature"),
    top_p=States.get("top_p"),
    frequency_penalty=States.get("frequency_penalty"),
    presence_penalty=States.get("presence_penalty"),
)

class QuizInfo(BaseModel):
    quiz_answer : str = Field(description="퀴즈 정답")
    quiz_hint : List[str] = Field(description="퀴즈 힌트")

    @validator("quiz_hint", allow_reuse=True)
    def check_contains_answer(cls, v, values):
        if values['quiz_answer'] in v:
            raise ValueError("퀴즈 정답은 퀴즈 힌트에 포함될 수 없습니다.")
        return v

def get_word():
    choosen_word = random.choice(data)
    return choosen_word.page_content.split(" ")[1]

def generate_quiz_info() -> QuizInfo:
    answer = get_word()
    prompt_source = read_file(f"{os.getcwd()}/resources/prompts/generate_hint.md")
    output_parser = PydanticOutputParser(pydantic_object=QuizInfo)
    prompt = PromptTemplate(
        template=prompt_source,
        input_variables=["give me 20 hints for the following word"],
        partial_variables={"format_instructions" : output_parser.get_format_instructions()}
    )
    chain = prompt | llm | output_parser
    return chain.invoke({"quiz_answer" : answer})

def validate_answer(answer : str, user_sentence : str):
    return True if answer in user_sentence else False

def response_for_wrong_answer(quiz_info : QuizInfo, user_input : str):
    picked_hint = rand_pick(quiz_info.quiz_hint)
    answer = quiz_info.quiz_answer
    prompt_source = read_file(f"{os.getcwd()}/resources/prompts/response_wrong.md")
    prompt = PromptTemplate(
        template=prompt_source,
        input_variables=["quiz_answer", "user_input", "rand_pick_hint"]
    )
    chain = prompt | llm
    return chain.invoke({"quiz_answer" : answer, "user_input" : user_input, "rand_pick_hint" : picked_hint})

welcome_messages = [
    "Hello there! Welcome to the ultimate Guessing Game! Ready to test your guessing skills?",
    "Welcome, adventurer! Dare to join me in a game of guesses? Let's see how sharp you are!",
    "Hi! I'm your friendly guessing game bot. Think you can outsmart me? Let’s find out!",
    "Greetings! Fancy a challenge? Let's play the Guessing Game. I bet you can't beat me!",
    "Welcome aboard! If you're up for some fun, let's dive into a guessing game together.",
    "Hey there! Welcome to our guessing arena. Ready to put your intuition to the test?",
    "Hello and welcome! Join me for a fun round of Guessing Game and let's see who wins!",
    "Hi! Looking for something exciting? Let’s play the Guessing Game. It’s time to guess!",
    "Welcome, new friend! Let's make your visit thrilling with a cool Guessing Game. Ready?",
    "Greetings! I challenge you to a Guessing Game. Think you have what it takes? Let’s play!"
]

correct_guess_messages = [
    "Congratulations! You got it right. The answer was indeed {quiz_answer}.",
    "Spot on! {quiz_answer} is the correct answer. Well done!",
    "You nailed it! The answer is {quiz_answer}. You're really good at this!",
    "Absolutely right! The correct answer is {quiz_answer}. Impressive!",
    "That’s correct! {quiz_answer} was exactly what I was thinking of. Great guessing!",
    "You guessed it! {quiz_answer} is right. You must be a mind reader!",
    "Correct! The answer is {quiz_answer}. Let’s see if you can get the next one too!",
    "Yes! {quiz_answer} is the right answer. You're on a roll!",
    "Right on target! {quiz_answer} is correct. Keep up the great work!",
    "Exactly right! {quiz_answer} was the answer I was looking for. You did it!"
]

def rand_pick(params : List[str]) -> str:
    return random.choice(params)

__all__ = ["generate_quiz_info", "validate_answer", "response_for_wrong_answer", "welcome_messages", "correct_guess_messages", "rand_pick"]