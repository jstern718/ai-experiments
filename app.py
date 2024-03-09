''' To start:
        Start venv with "source venv/bin/activate"
        Enter "flask run" into console
        This will start a server and the webpage: "http://localhost:5000/chat"
'''


import os
from dotenv import load_dotenv
import json
from flask import Flask, render_template
from openai import OpenAI
from forms import MessageForm

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'very-secret'

client = OpenAI(api_key=os.environ.get("KEY"),)


@app.post('/chat')
def post_chat():

    question = "Send a message to the chat bot"
    form = MessageForm()

    if form.text.data != "":
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content":  form.text.data}])

        message = completion.choices[0].message.content

        return render_template('/base.html',
                               message=message,
                               question=question,
                               form=form)

    else:
        question = "Send a message to the chat bot"
        return render_template('/base.html',
                               message="No response yet",
                               question=question,
                               form=form)


@app.get('/chat')
def get_history():
    question = "Send a message to the chat bot"
    form = MessageForm()
    return render_template('/base.html',
                           question=question,
                           form=form)


@app.post('/history')
def post_history():
    print("run history post")
    question = """Please enter a history topic that you are interested in
                learning about"""
    form = MessageForm()

    counter = 0
    if form.text.data != "" and counter == 0:
        topic = form.text.data
        message = """ """
        prompt = f"""You are a historian specializing in {topic}.
        Create for me a list that contains 10 words that you think
        are important to know for a student who is trying to learn about
        {topic}. These words should be vocabulary that are specific to
        discussions of this historical period and topic, words that a professor
        might ask a student to define during an exam. With the 10 words,
        provide a one sentence definition or explanation of the
        term and its historical relevance, focusing on its relevance to
        {topic}. These sentences should assume a college level audience.
        Please list all of the words and their corresponding explanations
        as a dict in json, with the word as a key and the explanation as its
        value. """
        completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content":  prompt}])
        counter = counter + 1
        answer1 = json.loads(completion.choices[0].message.content)
        print("counter", counter, "message", message)

    if form.text.data != "" and counter == 1:
        topic = form.text.data
        message = message
        prompt2 = f"""I previously gave you the following prompt {prompt}.
        This was your response: {message}. Please find another 10 words
        (words not included in your previous response). Then respond with
        a dict in json of these new word/definition pairs."""
        completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content":  prompt2}])
        answer2 = json.loads(completion.choices[0].message.content)
        print("counter", counter, "message", message)

    if form.text.data == "":
        return render_template('/base.html',
                               message="No response yet",
                               question=question,
                               form=form)

    print("answer1", answer1)
    print("answer2", answer2)
    message = {**answer1, **answer2}
    print("message", message)
    return render_template('/base.html', message=message, question=question,
                           form=form)


@app.get('/history')
def get_chat():
    form = MessageForm()

    return render_template('/base.html',
                           question="""Please enter a history topic that
                                        you are interested in learning
                                        about""",
                           form=form)
