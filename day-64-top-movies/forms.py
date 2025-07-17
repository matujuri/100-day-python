from wtforms import StringField, FloatField, SubmitField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange

class RateForm(FlaskForm):
    rating = FloatField(validators=[DataRequired(), NumberRange(min=0, max=10)], label="10点満点での評価（例：7.5）")
    review = StringField(validators=[DataRequired()], label="レビュー")
    submit = SubmitField("送信")
    
class SearchForm(FlaskForm):
    title = StringField("タイトル", validators=[DataRequired()])
    submit = SubmitField("検索")
    
class LoginForm(FlaskForm):
    email = StringField("メールアドレス", validators=[DataRequired()])
    password = PasswordField("パスワード", validators=[DataRequired()])
    submit = SubmitField("ログイン")
    
class RegisterForm(FlaskForm):
    email = StringField("メールアドレス", validators=[DataRequired()])
    password = PasswordField("パスワード", validators=[DataRequired()])
    name = StringField("名前", validators=[DataRequired()])
    submit = SubmitField("登録")