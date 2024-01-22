from flask import Flask, redirect, request, abort, make_response, render_template, url_for, jsonify,session,flash
from database import redgister_db
import subprocess

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
r = redgister_db

app.secret_key = "secret"

# 用户登录
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_type = request.form.get('user_type')
        row = r.select("select * from users where username = '"+username+"' and password = '"+password+"' and  user_type = '"+user_type+"'")
        if row is not None:
            session['logged_in'] = True
            session['username'] = username
            session['password'] = password
            session['user_type'] = user_type
            flash('You were logged in')
            return redirect(url_for('home'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

# 主页
@app.route('/home')
def home():
    if 'logged_in' in session:
        if session['user_type'] == 'admin':
            # 管理员用户权限
            return render_template('header.html')
        else:
            # 普通用户权限
            return render_template('header_student.html')
    else:
        return redirect(url_for('login'))


# 添加学生信息
@app.route('/createS', methods=['GET', 'POST'])
def insert_S():
    if request.method == 'GET':
        return render_template('createS.html')
    if request.method == 'POST':
        Sno = request.form.get('sno')
        Sname = request.form.get('sname')
        Ssex = request.form.get('ssex')
        Sage = request.form.get('sage')
        Sdept = request.form.get('sdept')
        Sclass = request.form.get('sclass')
        r.exert("insert into S VALUES('" + Sno + " ',' " + Sname + " ',' " + Ssex + " ',' " + Sage + " ',' " + Sdept + " ',' " + Sclass + " ')")
        return render_template('success.html')


# 添加课程信息
@app.route('/createC', methods=['GET', 'POST'])
def insert_C():
    if request.method == 'GET':
        return render_template('createC.html')
    if request.method == 'POST':
        Cno = request.form.get('cno')
        Cname = request.form.get('cname')
        Cclassroom = request.form.get('cclassroom')
        Ccredit = request.form.get('ccredit')
        r.exert("insert into C VALUES('" + Cno + " ',' " + Cname + " ',' " + Cclassroom + " ',' " + Ccredit + " ')")
        return render_template('success.html')


# 添加选课信息
@app.route('/createSC', methods=['GET', 'POST'])
def insert_SC():
    if request.method == 'GET':
        return render_template('createSC.html')
    if request.method == 'POST':
        cno = request.form.get('cno')
        sno = request.form.get('sno')
        grade = request.form.get('grade')
        r.exert("insert into SC(sno,cno,grade) VALUES('" + sno + " ',' " + cno + " ',' " + grade + " ')")
        return render_template('success.html')


# 删除学生信息
@app.route('/deleteS', methods=['GET', 'POST'])
def delete_S():
    if request.method == 'GET':
        return render_template('deleteS.html')
    if request.method == 'POST':
        Sno = request.form.get('sno')
        print(Sno)
        r.exert("delete from S where sno = '" + Sno + "' ")
        return render_template('success.html')


# 删除课程信息
@app.route('/deleteC', methods=['GET', 'POST'])
def delete_C():
    if request.method == 'GET':
        return render_template('deleteC.html')
    if request.method == 'POST':
        Cno = request.form.get('cno')
        print(Cno)
        r.exert("delete from C where cno = '" + Cno + "' ")
        return render_template('success.html')


# 删除选课信息
@app.route('/deleteSC', methods=['GET', 'POST'])
def delete_SC():
    if request.method == 'GET':
        return render_template('deleteSC.html')
    if request.method == 'POST':
        Sno = request.form.get('sno')
        Cno = request.form.get('cno')
        print(Sno)
        print(Cno)
        r.exert("delete from SC where sno = '" + Sno + "' and cno = '" + Cno + "'")
        return render_template('success.html')


# 查找
@app.route('/query_1', methods=['GET', 'POST'])
def select_table():
    if request.method == 'GET':
        return render_template('query_1.html')
    if request.method == 'POST':
        Sno = request.form.get('sno')
        print(Sno)
        result = r.select(" select * from S,C,SC where SC.sno=S.sno and SC.cno=C.cno and SC.sno = '" + Sno + "'")
        print(result)
        return render_template('query_1son.html', result=result)


# 更新学生信息
@app.route('/updateS', methods=['GET', 'POST'])
def update_S():
    if request.method == 'GET':
        return render_template('updateS.html')
    if request.method == 'POST':
        Sno = request.form.get('sno')
        Sname = request.form.get('sname')
        Ssex = request.form.get('ssex')
        Sage = request.form.get('sage')
        Sdept = request.form.get('sdept')
        Sclass = request.form.get('sclass')
        r.exert("update S set sno='" + Sno + "', sname='" + Sname + "', ssex='" + Ssex + "', sage='" + Sage + "', sdept='" + Sdept + "', sclass='" + Sclass + "'")
        return render_template('success.html')


# 更新课程信息
@app.route('/updateC', methods=['GET', 'POST'])
def update_C():
    if request.method == 'GET':
        return render_template('updateC.html')
    if request.method == 'POST':
        Cno = request.form.get('cno')
        Cname = request.form.get('cname')
        Cclassroom = request.form.get('cclassroom')
        Ccredit = request.form.get('ccredit')
        r.exert("update C set cno='" + Cno + "', cname='" + Cname + "', cclassroom='" + Cclassroom + "', ccredit='" + Ccredit + "'")
        return render_template('success.html')


# 更新选课信息
@app.route('/updateSC', methods=['GET', 'POST'])
def update_SC():
    if request.method == 'GET':
        return render_template('updateSC.html')
    if request.method == 'POST':
        Sno = request.form.get('sno')
        Cno = request.form.get('cno')
        grade = request.form.get('grade')
        r.exert("update SC set sno='" + Sno + "', cno='" + Cno + "', grade='" + grade + "'")
        return render_template('success.html')


if __name__ == '__main__':
    app.run()
