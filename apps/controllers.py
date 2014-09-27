# -*- coding: utf-8 -*-
from kstime import kstoday, ksyesterday, ksbmonth
from flask import render_template, request, redirect, url_for, g, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm.exc import NoResultFound
from apps import app, db
from models import User, Store, Stock, Category, History
from random import randint

#
# @ Before request
#
@app.before_request
def before_request():
	g.user_no = None

	if 'user_no' in session:
		g.user_no = session['user_no']
		g.user_name = session['user_name']


#
# @ Function Set
#
def makeStockList():
	stockList = []

	store = Store.query.filter_by(owner = g.user_no).first()
	stocks = Stock.query.filter_by(owner = store.no).all()

	categorys = Category.query.all()
	cateDict = {}
	for category in categorys:
		cateDict[category.no] = category.name

	for stock in stocks:
		yhistory = History.query.filter_by(owner = stock.no\
			).order_by(History.date_created.desc()).first()
		if yhistory:
			ystock = yhistory.totalstock
		else:
			ystock = 0

		bhistory = History.query.filter(History.owner == stock.no, History.date_created <= ksbmonth()).\
		order_by(History.date_created.desc()).first()
		if bhistory:
			bmstock = bhistory.totalstock
		else:
			bmstock = 0

		stockDict = {
			'no' : stock.no,
			'category': cateDict[stock.category],
			'name' : stock.name,
			'size' : stock.size,
			'stock' : stock.stock,
			'unitcost' : stock.unitcost,
			'ystock' : ystock,
			'bmstock' : bmstock,
			'memo' : stock.memo
		}

		stockList.append(stockDict)

	return stockList


@app.route('/')
def index():
	if 'user_no' in session:
		store = Store.query.filter_by(owner = g.user_no).first()
		stockList = makeStockList()

		return render_template("main.html", store=store, slist=stockList)
	return render_template('index.html')


#
# @ Sign-Up, Login, Logout
#
@app.route('/signup', methods=['POST'])
def signup():
	data = request.form
	useremail = data['useremail']
	username = data['username']
	storename = data['storename']
	userpw = data['password']
	
	user = User.query.filter_by(email = useremail).first()

	if user is None:
		user = User(
			email=useremail,
			password=generate_password_hash(userpw),
			name=username
			)

		db.session.add(user)
		db.session.commit()

		user = User.query.filter_by(email = useremail).first()

		store = Store(
			owner=user.no,
			name=storename
			)

		db.session.add(store)
		db.session.commit()
	else:
		# 중복유저
		return redirect(url_for('index'))

	session.permanent = True
	session['user_no'] = user.no
	session['user_name'] = user.name

	return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
	data = request.form
	userid = data['username']
	userpw = data['password']

	user = User.query.filter_by(email = userid).first()

	if user is None:
		# 실패 알림 창
		return redirect(url_for('index'))
	elif not check_password_hash(user.password, userpw):
		# 비밀번호 틀림 창
		return redirect(url_for('index'))

	session.permanent = True
	session['user_no'] = user.no
	session['user_name'] = user.name

	return redirect(url_for('index'))
	
@app.route('/logout', methods=['GET'])
def logout():
	session.clear()
	return redirect(url_for('index'))


#
# @ Create
#
@app.route('/create/store', methods=['GET'])
def create_store():
	pass
	
@app.route('/create/stock', methods=['POST'])
def create_stock():
	data = request.form

	name = data['name']
	store = int(data['store'])
	size = data['size']
	stock = int(data['stock'])
	cost = int(data['cost'])
	memo = data['memo']

	new_stock = Stock(
		owner=store,
		category=1,
		name=name,
		size=size,
		stock=stock,
		unitcost=cost,
		memo=memo
	)

	db.session.add(new_stock)
	db.session.commit()

	added_stock = Stock.query.filter_by(owner=store, name=name, size=size).first()

	return jsonify(stock_no=added_stock.no)


#
# @ Modify
#
@app.route('/modify/store', methods=['GET'])
def modify_store():
	pass
	
@app.route('/modify/stock', methods=['GET'])
def modify_stock():
	pass


#
# @ Delete
#
@app.route('/delete/store', methods=['GET'])
def delete_store():
	pass
	
@app.route('/delete/stock', methods=['GET'])
def delete_stock():
	pass


#
# @ Stock Management
#
@app.route('/stock/stocking', methods=['GET'])
def stock_stocking():
	pass

@app.route('/stock/releasing', methods=['GET'])
def stock_releasing():
	pass





'''
#
# @index & article list
#
@app.route('/', methods=['GET'])
def article_list():
	# html 파일에 전달할 데이터 Context
	context = {}

	# Article 데이터 전부를 받아와서 최신글 순서대로 정렬하여 'article_list' 라는 key값으로 context에 저장한다.
	context['article_list'] = Article.query.order_by(desc(Article.date_created)).all()

	return render_template('home.html', context=context, active_tab='timeline')

#
# @article controllers
#
@app.route('/article/create/', methods=['GET', 'POST'])
def article_create():
	form = ArticleForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			# 사용자가 입력한 글 데이터로 Article 모델 인스턴스를 생성한다.
			article = Article(
				title=form.title.data,
				author=form.author.data,
				category=form.category.data,
				content=form.content.data,
				date_created = kstime(9)
			)

			# 데이터베이스에 데이터를 저장할 준비를 한다. (게시글)
			db.session.add(article)
			# 데이터베이스에 저장하라는 명령을 한다.
			db.session.commit()

			flash(u'게시글을 작성하였습니다.', 'success')
			return redirect(url_for('article_list'))

	return render_template('article/create.html', form=form, active_tab='article_create')


@app.route('/article/detail/<int:id>', methods=['GET'])
def article_detail(id):
	article = Article.query.get(id)
	comments = Comment.query.order_by(desc(Comment.date_created)).filter_by(article_id=article.id)

	return render_template('article/detail.html', article=article, comments=comments)


@app.route('/article/update/<int:id>', methods=['GET', 'POST'])
def article_update(id):
	article = Article.query.get(id)
	form = ArticleForm(request.form, obj=article)
	if request.method == 'POST':
		if form.validate_on_submit():
			form.populate_obj(article)
			db.session.commit()
		return redirect(url_for('article_detail', id=id))

	return render_template('article/update.html', form=form)


@app.route('/article/delete/<int:id>', methods=['GET', 'POST'])
def article_delete(id):
	if request.method == 'GET':
		return render_template('article/delete.html', article_id=id)
	elif request.method == 'POST':
		article_id = request.form['article_id']
		article = Article.query.get(article_id)
		db.session.delete(article)
		db.session.commit()

		flash(u'게시글을 삭제하였습니다.', 'success')
		return redirect(url_for('article_list'))


@app.route('/article/like/<int:id>', methods=['GET'])
def article_like(id):
	article = Article.query.get(id)
	article.like += 1

	db.session.commit()

	return redirect(url_for('article_detail', id=id))


#
# @comment controllers
#
@app.route('/comment/create/<int:article_id>', methods=['GET', 'POST'])
def comment_create(article_id):
	form = CommentForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			comment = Comment(
				author=form.author.data,
				email=form.email.data,
				content=form.content.data,
				password=form.password.data,
				date_created = kstime(9),
				article=Article.query.get(article_id)
			)

			db.session.add(comment)
			db.session.commit()

			flash(u'댓글을 작성하였습니다.', 'success')
		return redirect(url_for('article_detail', id=article_id))
	return render_template('comment/create.html', form=form)


@app.route('/comment/delete/<int:id>', methods=['GET', 'POST'])
def comment_delete(id):
	if request.method == 'POST':
		comment = Comment.query.get(request.form['comment_id'])

		if request.form['password'] == comment.password:
			article_id = comment.article_id
			db.session.delete(comment)
			db.session.commit()

			flash(u'댓글을 삭제하였습니다.', 'success')
			return redirect(url_for('article_detail', id=article_id))
		else:
			flash(u'비밀번호가 일치하지 않습니다. 다시 한번 입력해주세요.', 'danger')
			return render_template('comment/delete.html', comment_id=request.form['comment_id'])

	elif request.method == 'GET':
		flash(u'경고! 댓글이 완전히 삭제되니, 다시 한번 확인하시기 바랍니다.', 'warning')
		return render_template('comment/delete.html', comment_id=id)

		
@app.route('/comment/like/<int:id>', methods=['GET'])
def comment_like(id):
	comment = Comment.query.get(id)
	article_id = comment.article_id
	comment.like += 1

	db.session.commit()

	return redirect(url_for('article_detail', id=article_id))


#
# @Join controllers
#
@app.route('/user/join/', methods=['GET', 'POST'])
def user_join():
	form = JoinForm()

	if request.method == 'POST':
		if form.validate_on_submit():
			user = User(
				email=form.email.data,
				password=generate_password_hash(form.password.data),
				name=form.name.data,
				join_date = kstime(9)
			)

			db.session.add(user)
			db.session.commit()

			flash(u'가입이 완료 되었습니다.', 'success')
			return redirect(url_for('article_list'))
	#if GET
	return render_template('user/join.html', form=form, active_tab='user_join')

#
# @Login controllers
#
@app.route('/login', methods=['GET','POST'])
def log_in():
	form = LoginForm()

	if request.method == 'POST':
	   if form.validate_on_submit():
			email = form.email.data
			password = form.password.data

			try: 
				user = db.session.query(User).filter(User.email==email).one() 
				if not check_password_hash(user.password, password): 
					flash(u'이메일 혹은 비밀번호가 올바르지 않습니다.', 'danger') 
					return render_template('user/login.html', form=form, active_tab='log_in') 
				else: 
					session.permanent = True 
					session['user_email'] = user.email 
					session['user_name'] = user.name 
					session['user_id'] = user.id

					flash(u'로그인 되었습니다.', 'success')
					return redirect(url_for('article_list')) 
			except NoResultFound, e: 
				flash(u'이메일 혹은 비밀번호가 올바르지 않습니다.', 'danger') 
				return render_template('user/login.html', form=form, active_tab='log_in') 

	#if GET
	return render_template('user/login.html', form = form, active_tab='log_in')


@app.route('/logout')
def log_out():
	session.clear()
	#if GET
	return redirect(url_for('article_list'))
#
# @error Handlers
#
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
	return render_template('500.html'), 500'''