from flask import Flask,session,g,request
import config
from exts import db,mail
from blueprints import qa_bp,user_bp,mine_bp,collect_bp,admin_bp
from flask_migrate import Migrate
from models import UserModel
from flask_cors import CORS
from flask_avatars import Avatars
from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
avatars = Avatars(app) # automatically generate avatars
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)

#处理跨域请求
CORS(app, supports_credentials=True)

migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)
app.register_blueprint(mine_bp)
app.register_blueprint(collect_bp)
app.register_blueprint(admin_bp)

@app.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # 给g绑定一个叫做user的变量，他的值是user这个变量
            # setattr(g,"user",user)
            g.user = user
        except:
            g.user = None

# 请求来了 -> before_request -> 视图函数 -> 视图函数中返回模板 -> context_processor

@app.context_processor
def context_processor():
    if hasattr(g,"user"):
        return {"user": g.user}
    else:
        return {}


if __name__ == '__main__':
    app.run()

