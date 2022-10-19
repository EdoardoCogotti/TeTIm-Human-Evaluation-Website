from flask import render_template, url_for, flash, redirect, request, session
from flask_tetim.form import AnswerForm, ChooseModelPlayForm, ChooseModelShowForm, SaveScoreForm
from flask_tetim.models import Question, Answer, Score
from flask_tetim import app, db
from sqlalchemy.sql.expression import func, select
from datetime import datetime
from random import sample
import uuid
import socket
import time
import random

num_images = 20
models = ['DALLE2', 'Latent Diffusion', 'Stable Diffusion', 'Craiyon', 'GLIDE']
questions = []
# mask_map = {'Craiyon': 1, 'DALLE2': 2, 'GLIDE': 3, 'Latent Diffusion': 4, 'Stable Diffusion': 5, 'real': 6}
mask_map = {'Craiyon': ["17654", "13496", "10935"], 'DALLE2': ["25498", "29160", "20375"],
            'GLIDE': ["30473", "34267", "38752"], 'Latent Diffusion': ["43658", "45954", "44217"],
            'Stable Diffusion': ["54785", "52387", "51067"], 'real': ["66478", "61951", "60146"]}
model_map = {'Woody': "Craiyon", "Paradise": "Latent Diffusion", "Igloo": "Stable Diffusion",
             "Eva": "DALLE2", "Braid": "GLIDE"}

@app.route('/', methods=['GET', 'POST'])
# @app.route('/home', methods=['GET', 'POST']) # cause issue of back button
def home():
    form = ChooseModelPlayForm()
    if form.validate_on_submit():
        session["counter"] = 0
        session["score"] = 0
        session["start_time"] = time.time()
        if form.model.data == "Random":
            session["model"] = random.choice(models)
        else:
            session["model"] = model_map[form.model.data]
        session["language"] = form.language.data
        session["round_images"] = [random.choice(range(2)) for _ in range(num_images)]
        session["start_game"] = True
        return redirect(url_for("play"))
    # print(f"home {session}")
    return render_template("choose.html", title="Choose", form=form)


@app.route('/play', methods=['GET', 'POST'])
def play():
    global questions

    # print(len(session.keys()))
    if len(session.keys()) == 0:
        return render_template("session_expired.html")

    if "ip" not in session:
        session["ip"] = request.headers.get("X-Real-Ip")  # request.remote_addr
        session["uuid"] = uuid.uuid4()
        session.permanent = False

    counter = session["counter"]
    ip = session["ip"]
    rand_uuid = session["uuid"]
    score = session["score"]
    model = session["model"]
    if session["start_game"]:
        session["start_game"] = False
        questions = Question.query.order_by(func.random()).limit(num_images).all()
    # print(model)
    # print(f"Request cookies {request.cookies}")
    real = session["round_images"][counter] == 0
    form = AnswerForm()
    if form.validate_on_submit():
        answer = Answer(ip=ip, uuid=rand_uuid, real_answer=real, user_answer=form.real_button.data,
                        model=model, question_id=questions[counter].id, timestamp=datetime.utcnow())
        if (real and form.real_button.data) or (not real and form.fake_button.data):
            score += 1
            session["score"] = score
            flash("Correct answer", 'success')
        else:
            flash("Wrong answer", 'danger')
        counter += 1
        session["counter"] = counter
        db.session.add(answer)
        db.session.commit()
        if counter == len(questions):
            session["end_time"] = time.time()
            session["end_flag"] = True
            return redirect(url_for("result"))
        return redirect(url_for("play"))

    # get imagefile
    image_tuple = session["round_images"][counter]
    model_name = "real" if image_tuple == 0 else session["model"]
    # random_folder = "%05d" % random.randint(0, 99999)
    # model_folder = model_name
    # model_folder = str(mask_map[model_name]) + random_folder[1:]
    model_folder = sample(mask_map[model_name], 1)[0]
    category_folder = questions[counter].category
    sub_folder = "images/" if image_tuple == 0 else ""
    id_name = str(questions[counter].image_file)
    extension = ".png" # ".jpg" if image_tuple == 0 else ".png"
    filename = "tetim/" + model_folder + "/" + category_folder + "/" + sub_folder + id_name + extension
    image_file = url_for('static', filename=filename)
    # print(image_file)
    return render_template("home.html", question=questions[counter], form=form, image_file=image_file, score=score,
                           counter=counter, lang=session["language"], socket=socket.gethostname(), model=model)


@app.route('/score', methods=['GET', 'POST'])
def highscore():
    form = ChooseModelShowForm()
    if form.validate_on_submit():
        choice = form.model.data
        return redirect(url_for("highscore", choice=choice))
    model_alias = request.args.get("choice")
    # print(model_alias)
    choice = None
    if model_alias in model_map:
        choice = model_map[model_alias]
    best_scores = []
    if choice:
        # get highscore
        best_scores = Score.query.filter(Score.model == choice).order_by(Score.score.desc(), Score.seconds.asc()).limit(10).all()
    return render_template("highscores.html", title="Highscore", form=form, best_scores=best_scores, choice=model_alias)


@app.route('/result', methods=['GET', 'POST'])
def result():
    if not session["end_flag"] or not "end_flag" in session:
        return redirect(url_for("home"))
    else:
        form = SaveScoreForm()
        user_score = session["score"]
        user_time = round(session["end_time"] - session["start_time"], 2)
        best_scores = Score.query.filter(Score.model == session["model"]).order_by(Score.score.desc(), Score.seconds.asc()).limit(10).all()
        if len(best_scores) != 0:
            min_best_score = best_scores[-1]
        else:
            min_best_score = Score(score=-1, seconds=-1)
        if form.validate_on_submit():
            score = Score(model=session["model"], username=form.name.data, score=user_score, seconds=user_time)
            db.session.add(score)
            db.session.commit()
            session["end_flag"] = False
            return redirect(url_for("highscore"))
        return render_template("save_score.html", title="Result", form=form, user_score=user_score,
                               user_time=user_time, min_best_score=min_best_score, num_best=len(best_scores))


@app.route('/about')
def about():
    return render_template("about.html", title="About")


@app.route('/contacts')
def contacts():
    return render_template("contacts.html", title="Contacts")


def cookies_check():
    value = request.cookies.get('cookie_consent')
    return value == 'true'


@app.context_processor
def inject_template_scope():
    injections = dict()
    injections.update(cookies_check=cookies_check)
    return injections