from flask import (
    Blueprint,
    render_template,
    request,
    session,
    flash,
    redirect,
    jsonify
)
import json
from flask import session as S
from exts import db,session
from models import FavoriteModel,QuestionModel,UserModel,UserFavoriteQuestionModel,AnswerModel
from decorators import login_required
from werkzeug.security import generate_password_hash,check_password_hash

bp = Blueprint("mine",__name__,url_prefix="/mine")


@bp.route("/mine/see_my_collection")
@login_required
def see_my_collection():
    user_id = S.get("user_id")
    favorite = db.session.query(FavoriteModel).filter(FavoriteModel.author_id == user_id).all()

    return render_template("mine.html",favorite=favorite)

@bp.route("/mine/see_my_collection_item/<int:id>")
@login_required
def see_my_collection_item(id):
    user_id = S.get("user_id")
    favorites = db.session.query(FavoriteModel).filter(FavoriteModel.id ==id).first()
    q_fav = favorites.qs
    print(q_fav)
    return render_template("favorite_item.html",qs=q_fav,favorites = favorites)

@bp.route("/mine/see_my_info")
@login_required
def see_my_info():
    user_id = S.get("user_id")
    info = db.session.query(UserModel).filter(UserModel.id == user_id).first()
    return render_template("personal_info.html",info=info)

@bp.route("/mine/see_my_question")
@login_required
def see_my_question():
    user_id = S.get("user_id")
    questions = db.session.query(QuestionModel).filter(QuestionModel.author_id == user_id).all()
    return render_template("my_question.html",questions=questions)

@bp.route("/mine/delete_q",methods=["POST"])
@login_required
def delete_q():
    data = json.loads(request.form.get('data'))
    q_id = data['q_id']
    db.session.query(AnswerModel).filter(AnswerModel.question_id == q_id).delete()
    db.session.query(UserFavoriteQuestionModel).filter(UserFavoriteQuestionModel.question_id == q_id).delete()
    db.session.query(QuestionModel).filter(QuestionModel.id == q_id).delete()
    db.session.commit()

    user_id = S.get("user_id")
    questions = db.session.query(QuestionModel).filter(QuestionModel.author_id == user_id).all()
    return render_template("my_question.html", questions=questions)

@bp.route("/change_password/", methods=["POST"])
@login_required
def change_password(): # add assessment
    user_id = S.get("user_id")
    user = db.session.query(UserModel).filter(UserModel.id == user_id).first()
    form_results = request.form # get data from form
    initial_password = form_results.get("initial_password")
    new_password = form_results.get("new_password")
    # check if all imformation is filled
    if check_password_hash(user.password,initial_password):
        flash("Wrong password!")
        info = db.session.query(UserModel).filter(UserModel.id == user_id).first()
        return render_template("personal_info.html",info=info)
    hash_password = generate_password_hash(new_password)
    db.session.query(UserModel).filter(UserModel.id == user_id).update({'password': hash_password})
    db.session.commit()
    info = db.session.query(UserModel).filter(UserModel.id == user_id).first()
    return render_template("personal_info.html",info=info)