#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors
import bcrypt
#for uploading photo:
from app import app
#from flask import Flask, flash, request, redirect, render_template
import time
import os
import calendar
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


##Initialize the app from Flask
#app = Flask(__name__)
#app.secret_key = "secret key"

# Configure MySQL
conn = pymysql.connect(host='localhost',
                       port = 8889,
                       user='root',
                       password='root',
                       db='ProjectTest',
                       charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)


# def allowed_image(filename):

#     if not "." in filename:
#         return False

#     ext = filename.rsplit(".", 1)[1]

#     if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
#         return True
#     else:
#         return False


# def allowed_image_filesize(filesize):

#     if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
#         return True
#     else:
#         return False


# #Define a route to hello function
# @app.route('/')
# def hello():
#     return render_template('index.html')

# #Define route for login
# @app.route('/login')
# def login():
#     return render_template('login.html')

# #Define route for register
# @app.route('/register')
# def register():
#     return render_template('register.html')

# #Authenticates the login
# @app.route('/loginAuth', methods=['GET', 'POST'])
# def loginAuth():
#     #grabs information from the forms
#     username = request.form['username']
#     password = request.form['password']

#     #cursor used to send queries
#     cursor = conn.cursor()
#     #executes query
#     query = 'SELECT * FROM user WHERE username = %s and password = %s'
#     cursor.execute(query, (username, password))
#     #stores the results in a variable
#     data = cursor.fetchone()
#     #use fetchall() if you are expecting more than 1 data row
#     cursor.close()
#     error = None
#     if(data):
#         #creates a session for the the user
#         #session is a built in
#         session['username'] = username
#         return redirect(url_for('home'))
#     else:
#         #returns an error message to the html page
#         error = 'Invalid login or username'
#         return render_template('login.html', error=error)

# #Authenticates the register
# @app.route('/registerAuth', methods=['GET', 'POST'])
# def registerAuth():
#     #grabs information from the forms
#     username = request.form['username']
#     password = request.form['password']

#     #cursor used to send queries
#     cursor = conn.cursor()
#     #executes query
#     query = 'SELECT * FROM user WHERE username = %s'
#     cursor.execute(query, (username))
#     #stores the results in a variable
#     data = cursor.fetchone()
#     #use fetchall() if you are expecting more than 1 data row
#     error = None
#     if(data):
#         #If the previous query returns data, then user exists
#         error = "This user already exists"
#         return render_template('register.html', error = error)
#     else:
#         ins = 'INSERT INTO user VALUES(%s, %s)'
#         cursor.execute(ins, (username, password))
#         conn.commit()
#         cursor.close()
#         return render_template('index.html')


# @app.route('/home')
# def home():
#     user = session['username']
#     cursor = conn.cursor();
#     query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
#     cursor.execute(query, (user))
#     data = cursor.fetchall()
#     cursor.close()
#     return render_template('home.html', username=user, posts=data)

        
# @app.route('/post', methods=['GET', 'POST'])
# def post():
#     username = session['username']
#     cursor = conn.cursor();
#     blog = request.form['blog']
#     query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
#     cursor.execute(query, (blog, username))
#     conn.commit()
#     cursor.close()
#     return redirect(url_for('home'))

# @app.route('/select_blogger')
# def select_blogger():
#     #check that user is logged in
#     #username = session['username']
#     #should throw exception if username not found
    
#     cursor = conn.cursor();
#     query = 'SELECT DISTINCT username FROM blog'
#     cursor.execute(query)
#     data = cursor.fetchall()
#     cursor.close()
#     return render_template('select_blogger.html', user_list=data)

# @app.route('/show_posts', methods=["GET", "POST"])
# def show_posts():
#     poster = request.args['poster']
#     cursor = conn.cursor();
#     query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
#     cursor.execute(query, poster)
#     data = cursor.fetchall()
#     cursor.close()
#     return render_template('show_posts.html', poster_name=poster, posts=data)


# def allowed_file(filename):
# 	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
# @app.route('/upload_image_pages')
# def upload_image_page():
# 	return render_template('upload1.html')

@app.route('/upload_image', methods=['GET','POST'])
def upload_image():
    try:
        session['username']
    except:
        return redirect('/')
    picurl=request.form['picurl']
    cursor = conn.cursor()
    query = 'INSERT INTO RecipePicture VALUES(%s, %s)'
    cursor.execute(query, (session['recipeID'],picurl))
    conn.commit()
    cursor.close()
    return render_template('upload.html')
	
@app.route('/')
def hello():
    return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
    return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
        #grabs information from the forms
    username = request.form['username']
    password = request.form['password'].encode('utf-8')
    
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    profile = request.form['profile']
    hashedpassword = bcrypt.hashpw(password, bcrypt.gensalt())
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM person WHERE userName = %s'
    cursor.execute(query, (username))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error = error)
    else:
        ins = 'INSERT INTO person VALUES(%s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, hashedpassword,fname,lname,email,profile))
        conn.commit()
        cursor.close()
        return render_template('index.html')
    # return render_template('index.html')

@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():

    #grabs information from the forms
    username = request.form['username']
    password = request.form['password'].encode('utf-8')
    
    # hashedpassword = bcrypt.hashpw(password, bcrypt.gensalt())
    # print(hashedpassword)
    
    # passwordMatches = bcrypt.checkpw(password, hashedPWInBytes)
    # if(passwordMatches):
        # print("trueee")
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM person WHERE userName = %s'
    cursor.execute(query, (username))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        user = data
      
        hashedPWInBytes = user['password'].encode('utf-8')
        passwordMatches = bcrypt.checkpw(password, hashedPWInBytes)
        if(passwordMatches):
            session['username'] = username
            session['recipeID']=''
            return redirect(url_for('home'))
        else:
        #returns an error message to the html page
            error = 'Invalid login or username'
            return render_template('login.html', error=error)
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)
    # return render_template('home.html')

@app.route('/post_recipe_page',methods=['GET','POST'])
def post_recipe_page():
    try:
        session['username']
    except:
        return redirect('/')
    return render_template('post_recipe.html')

@app.route('/post_recipe',methods=['GET','POST'])
def post_recipe():
    try:
        session['username']
    except:
        return redirect('/')
    title=request.form['title']
    numofservings=request.form['numofservings']
    if(int(numofservings)<0):
        error='Please enter number of servings more than 0'
        return render_template('post_recipe.html',error=error)
    cursor = conn.cursor()
    query = 'INSERT INTO Recipe (title,numServings,postedBy) VALUES(%s, %s, %s)'
    cursor.execute(query, (title,numofservings,session['username']))
    conn.commit()
    query2 = 'SELECT recipeID FROM recipe ORDER BY recipeID DESC'
    cursor.execute(query2)
    data = cursor.fetchone()
    
    session['recipeID']=data['recipeID']
    # print(session['recipeID'])
    cursor.close()
    return render_template('post_steps.html')

@app.route('/postSteps', methods=['GET', 'POST'])
def postSteps():
    try:
        session['username']
    except:
        return redirect('/')
    # print(session['username'])
    stepno=request.form['stepno']
    stepdesc=request.form['stepdesc']
    cursor = conn.cursor()
    query = 'INSERT INTO step  VALUES(%s, %s, %s)'
    cursor.execute(query, (stepno,session['recipeID'],stepdesc))
    conn.commit()
    cursor.close()
    return render_template('post_steps.html')

@app.route('/postIngredientsPage', methods=['GET', 'POST'])
def postIngredientsPage():
    try:
        session['username']
    except:
        return redirect('/')
    return render_template('post_ingredients.html')

@app.route('/postIngredients', methods=['GET', 'POST'])
def postIngredients():
    try:
        session['username']
    except:
        return redirect('/')
    iname=request.form['iname']
    amount=request.form['amount']
    unit=request.form['unit']
    iurl=request.form['iurl']
    irestricdesc=request.form['irestricdesc']
    cursor = conn.cursor()
    query1='Select * from Ingredient where iName=%s'
    cursor.execute(query1,(iname))
    data=cursor.fetchall()
    if (data):

        if(iurl):
            error= "Purchase link already exists please enter ingredient without purchase link"
            return render_template('post_ingredients.html', error=error)
        else:
            query = 'INSERT INTO RecipeIngredient  VALUES(%s, %s, %s,%s)'
            cursor.execute(query, (session['recipeID'],iname,unit,amount))
            conn.commit()
    else:
        if(not iurl):
            error = 'Please enter a url for this ingredient'
            return render_template('post_ingredients.html', error=error)
        query='INSERT INTO Ingredient  VALUES(%s,%s)'
        cursor.execute(query,(iname,iurl))
        conn.commit()
        query2 = 'INSERT INTO RecipeIngredient  VALUES(%s, %s, %s,%s)'
        cursor.execute(query2, (session['recipeID'],iname,unit,amount))
        conn.commit()
    cursor.close()
    return render_template('post_ingredients.html')

@app.route('/postTagPage', methods=['GET', 'POST'])
def postTagPage():
    try:
        session['username']
    except:
        return redirect('/')
    return render_template('post_tag.html')

@app.route('/postTag', methods=['GET', 'POST'])
def postTag():
    try:
        session['username']
    except:
        return redirect('/')
    tag=request.form['tag']
    cursor = conn.cursor()
    query = 'INSERT INTO RecipeTag VALUES(%s, %s)'
    cursor.execute(query, (session['recipeID'],tag))
    conn.commit()
    cursor.close()
    return render_template('post_tag.html')

@app.route('/pic_url', methods=['GET','POST'])
def pic_url():
    try:
        session['username']
    except:
        return redirect('/')
    return render_template('upload1.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    try:
        session['username']
    except:
        return redirect('/')
    session['recipeID']=None
    query='Select * from recipe where postedBy=%s'
    cursor=conn.cursor()
    cursor.execute(query,session['username'])
    data=cursor.fetchall()
    cursor.close()
    # if(session['recipeID']):
    #     session.pop('recipeID')
    return render_template('home.html',username=session['username'],recipe=data)

@app.route('/search_recipe', methods=['GET', 'POST'])
def search_recipe():
    try:
        session['username']
    except:
        return redirect('/')
    return render_template('search_recipe.html')
@app.route('/search_recipe_lo', methods=['GET', 'POST'])
def search_recipe_lo():
    return render_template('search_recipe_lo.html')

@app.route('/recipe_results', methods=['GET', 'POST'])
def recipe_results():
    tag=request.form['tag']
    stars=request.form['star']
    try:
        session['username']
    except:
        return redirect('/')
    if(stars):
        if(int(stars)>5 or int(stars)<0):
            error = "Please enter the value for stars between 0 and 5"
            return render_template("search_recipe.html",error=error)
    cursor=conn.cursor()
    print(tag,stars)
    cursor = conn.cursor()
    if(not tag and not stars):
        error = "Please enter the value for and/or stars"
        return render_template("search_recipe.html",error=error)
    elif(not stars):
        query = 'select recipeID,title from Recipe where recipeID in (Select recipeID from RecipeTag where tagText=%s)'
        cursor.execute(query,(tag))
        data=cursor.fetchall()
        print(data)
    elif(not tag):
        query = 'select recipeID,title from Recipe where recipeID in (Select recipeID from Review where stars=%s)'
        cursor.execute(query,(stars))
        data=cursor.fetchall()
        print(data)
    else:
        query ='select recipeID,title from Recipe where recipeID in (select recipeID from RecipeTag NATURAL JOIN Review where RecipeTag.tagText=%s and Review.stars=%s)'
        cursor.execute(query,(tag,stars))
        data=cursor.fetchall()
    cursor.close()
    if(data):
        return render_template('recipe_results.html',recipe_list=data)
    else:
        error='There were no results that matched your search, please try again.'
        return render_template('search_recipe.html',error=error)

@app.route('/all_recipes', methods=['GET','POST'])
def all_recipes():
    try:
        session['username']
    except:
        return redirect('/')
    cursor = conn.cursor()
    
    query = 'select * from Recipe'
    cursor.execute(query)
    data=cursor.fetchall()
    cursor.close()
    return render_template('all_recipes.html',recipe_list=data)

@app.route('/show_recipe', methods=['GET','POST'])
def show_recipe():
    try:
        session['username']
    except:
        return redirect('/')
    recipeID = request.args.get(('recipe'),default=None, type=None)
    if(not recipeID):
        error='You did not select a recipe to view, please try again'
        return render_template('search_recipe.html',error=error)
    session['recipeID']=recipeID
    cursor = conn.cursor();
    query1 = 'SELECT * FROM Recipe WHERE recipeID = %s'
    cursor.execute(query1, (recipeID))
    data1 = cursor.fetchall()
    # print(data1)
    query2 = 'SELECT * FROM step WHERE recipeID = %s ORDER BY stepNo'
    cursor.execute(query2, (recipeID))
    data2 = cursor.fetchall()
    # print(data2)
    query3 = 'SELECT * FROM RecipeIngredient Natural Join Ingredient WHERE recipeID = %s'
    cursor.execute(query3, (recipeID))
    data3 = cursor.fetchall()
    query4 = 'SELECT * FROM RecipePicture WHERE recipeID = %s'
    cursor.execute(query4, (recipeID))
    data4 = cursor.fetchall()
    # print(data1)
    # print(data2)
    # print(data3)
    
    query5='Select distinct unitName FROM RecipeIngredient Natural Join Ingredient WHERE recipeID = %s'
    cursor.execute(query5,(recipeID))
    data5=cursor.fetchall()
    query6='select* from review where recipeID=%s'
    cursor.execute(query6,recipeID)
    data6=cursor.fetchall()

    cursor.close()
    return render_template('show_recipe.html', details=data1, steps=data2,ingredients=data3,pictures=data4,units=data5,review=data6)

@app.route('/recipe_results_lo', methods=['GET', 'POST'])
def recipe_results_lo():
    tag=request.form['tag']
    stars=request.form['star']

    if(stars):
        if(int(stars)>5 or int(stars)<0):
            error = "Please enter the value for stars between 0 and 5"
            return render_template("search_recipe_lo.html",error=error)
    cursor=conn.cursor()
    print(tag,stars)
    cursor = conn.cursor()
    if(not tag and not stars):
        error = "Please enter the value for and/or stars"
        return render_template("search_recipe_lo.html",error=error)
    elif(not stars):
        query = 'select recipeID,title from Recipe where recipeID in (Select recipeID from RecipeTag where tagText=%s)'
        cursor.execute(query,(tag))
        data=cursor.fetchall()
        print(data)
    elif(not tag):
        query = 'select recipeID,title from Recipe where recipeID in (Select recipeID from Review where stars=%s)'
        cursor.execute(query,(stars))
        data=cursor.fetchall()
        print(data)
    else:
        query ='select recipeID,title from Recipe where recipeID in (select recipeID from RecipeTag NATURAL JOIN Review where RecipeTag.tagText=%s and Review.stars=%s)'
        cursor.execute(query,(tag,stars))
        data=cursor.fetchall()
    cursor.close()
    if(data):
        return render_template('recipe_results_lo.html',recipe_list=data)
    else:
        error='There were no results that matched your search, please try again.'
        return render_template('search_recipe_lo.html',error=error)

@app.route('/all_recipes_lo', methods=['GET','POST'])
def all_recipes_lo():
    cursor = conn.cursor()
    
    query = 'select * from Recipe'
    cursor.execute(query)
    data=cursor.fetchall()
    cursor.close()
    return render_template('all_recipes_lo.html',recipe_list=data)

@app.route('/show_recipe_lo', methods=['GET','POST'])
def show_recipe_lo():
    recipeID = request.args.get(('recipe'),default=None, type=None)
    if(not recipeID):
        error='You did not select a recipe to view, please try again'
        return render_template('search_recipe_lo.html',error=error)
    session['recipeID']=recipeID
    cursor = conn.cursor();
    query1 = 'SELECT * FROM Recipe WHERE recipeID = %s'
    cursor.execute(query1, (recipeID))
    data1 = cursor.fetchall()
    # print(data1)
    query2 = 'SELECT * FROM step WHERE recipeID = %s ORDER BY stepNo'
    cursor.execute(query2, (recipeID))
    data2 = cursor.fetchall()
    # print(data2)
    query3 = 'SELECT * FROM RecipeIngredient Natural Join Ingredient WHERE recipeID = %s'
    cursor.execute(query3, (recipeID))
    data3 = cursor.fetchall()
    query4 = 'SELECT * FROM RecipePicture WHERE recipeID = %s'
    cursor.execute(query4, (recipeID))
    data4 = cursor.fetchall()
    # print(data1)
    # print(data2)
    # print(data3)
    
    # query5='Select distinct unitName FROM RecipeIngredient Natural Join Ingredient WHERE recipeID = %s'
    # cursor.execute(query5,(recipeID))
    # data5=cursor.fetchall()
    query6='select* from review where recipeID=%s'
    cursor.execute(query6,recipeID)
    data6=cursor.fetchall()

    cursor.close()
    return render_template('show_recipe_lo.html', details=data1, steps=data2,ingredients=data3,pictures=data4,review=data6)

@app.route('/show_converted_recipe', methods=['GET','POST'])
def show_converted_recipe():
    try:
        session['username']
    except:
        return redirect('/')
    recipeID = session['recipeID']
    sunit=request.form['unit']
    dunit=request.form['unitd']
    print(sunit)
    print(dunit)
    cursor = conn.cursor();
    query1 = 'SELECT * FROM Recipe WHERE recipeID = %s'
    cursor.execute(query1, (recipeID))
    data1 = cursor.fetchall()
    # print(data1)
    query2 = 'SELECT * FROM step WHERE recipeID = %s ORDER BY stepNo'
    cursor.execute(query2, (recipeID))
    data2 = cursor.fetchall()
    # print(data2)
    session['ts']=str(calendar.timegm(time.gmtime()))
    query31='Create table t1'+session['ts']+' as (SELECT * FROM RecipeIngredient Natural Join Ingredient WHERE recipeID = %s);'
    print(query31)
    cursor.execute(query31,(recipeID))
    # data3 = cursor.fetchall()
    conn.commit()
    query32 = 'update t1'+session['ts']+' set unitName=%s, amount=(select ratio from UnitConversion WHERE sourceUnit=%s and destinationUnit=%s)*amount where unitName=%s;'
    cursor.execute(query32, (dunit,sunit,dunit,sunit))
    conn.commit()
    query3='select * from t1'+session['ts']
    cursor.execute(query3)
    data3 = cursor.fetchall()
    query4 = 'SELECT * FROM RecipePicture WHERE recipeID = %s'
    cursor.execute(query4, (recipeID))
    data4 = cursor.fetchall()
    # print(data1)
    # print(data2)
    # print(data3)
    
    query5='Select distinct unitName FROM t1'+session['ts']
    cursor.execute(query5)
    data5=cursor.fetchall()
    # query6='drop table t1'
    # cursor.execute(query6)
    query6='select* from review where recipeID=%s'
    cursor.execute(query6,recipeID)
    data6=cursor.fetchall()
    
    cursor.close()
    return render_template('show_converted_recipe.html', details=data1, steps=data2,ingredients=data3,pictures=data4,units=data5,review=data6)
@app.route('/finish_viewing',methods=['GET','POST'])
def finish_viewing():
    try:
        session['username']
    except:
        return redirect('/')
    cursor=conn.cursor()
    query='drop table t1'+session['ts']
    cursor.execute(query)
    query1='Select * from recipe where postedBy=%s'
    
    cursor.execute(query1,session['username'])
    data=cursor.fetchall()
    
    cursor.close()
    # if(session['recipeID']):
    #     session.pop('recipeID')
    return render_template('home.html',username=session['username'],recipe=data)
@app.route('/show_converted_recipe_2', methods=['GET','POST'])
def show_converted_recipe_2():
    try:
        session['username']
    except:
        return redirect('/')
    recipeID = session['recipeID']
    sunit=request.form['unit']
    dunit=request.form['unitd']
    print(sunit)
    print(dunit)
    cursor = conn.cursor();
    query1 = 'SELECT * FROM Recipe WHERE recipeID = %s'
    cursor.execute(query1, (recipeID))
    data1 = cursor.fetchall()
    # print(data1)
    query2 = 'SELECT * FROM step WHERE recipeID = %s ORDER BY stepNo'
    cursor.execute(query2, (recipeID))
    data2 = cursor.fetchall()
    # print(data2)
    # query31='Create table t1 as (SELECT * FROM RecipeIngredient Natural Join Ingredient WHERE recipeID = %s);'
    # cursor.execute(query31,(recipeID))
    # # data3 = cursor.fetchall()
    # conn.commit()
    query32 = 'update t1'+session['ts']+' set unitName=%s, amount=(select ratio from UnitConversion WHERE sourceUnit=%s and destinationUnit=%s)*amount where unitName=%s;'
    cursor.execute(query32, (dunit,sunit,dunit,sunit))
    conn.commit()
    query3='select * from t1'+session['ts']
    cursor.execute(query3)
    data3 = cursor.fetchall()
    query4 = 'SELECT * FROM RecipePicture WHERE recipeID = %s'
    cursor.execute(query4, (recipeID))
    data4 = cursor.fetchall()
    # print(data1)
    # print(data2)
    # print(data3)
    
    query5='Select distinct unitName FROM t1'+session['ts']
    cursor.execute(query5)
    data5=cursor.fetchall()
    # query6='drop table t1'
    # cursor.execute(query6)
    query6='select* from review where recipeID=%s'
    cursor.execute(query6,recipeID)
    data6=cursor.fetchall()
    cursor.close()
    return render_template('show_converted_recipe.html', details=data1, steps=data2,ingredients=data3,pictures=data4,units=data5,review=data6)
@app.route("/review", methods=['GET','POST'])
def review():
    try:
        session['username']
    except:
        return render_template('index.html')
    return redirect('/')

@app.route("/review_c", methods=['GET','POST'])
def review_c():

    try:
        session['username']
    except:
        return redirect('/')
    cursor=conn.cursor()
    query="drop table t1"+session['ts']
    cursor.execute(query)
    cursor.close()
    return render_template("/post_review.html")
@app.route("/post_review", methods=['GET','POST'])
def post_review():
    try:
        session['username']
    except:
        return redirect('/')
    recipeID=session['recipeID']
    username=session['username']
    revtitle=request.form['revtitle']
    revdesc=request.form['revdesc']
    stars=request.form['stars']
    if(int(stars)>5 or int(stars)<0):
        error = "Please enter the value for stars between 0 and 5"
        return render_template("post_review.html",error=error)
    cursor=conn.cursor()
    pre_query='select * from review where recipeID=%s and userName=%s'
    cursor.execute(pre_query,(recipeID,username))
    data=cursor.fetchall()
    if(data):
        error="You have already reviewed this recipe, please go back"
        return render_template('post_review.html',error=error)
    query="Insert into review values (%s,%s,%s,%s,%s)"
    cursor.execute(query,(username,recipeID,revtitle,revdesc,stars))
    conn.commit()
    cursor.close()
    return render_template("post_review_picture.html")
@app.route('/upload_review_picture', methods=['GET','POST'])
def upload_review_picture():
    try:
        session['username']
    except:
        # return render_template('index.html')
        return redirect('/')
    picurl=request.form['picurl']
    cursor = conn.cursor()
    recipeID=session['recipeID']
    username=session['username']
    query = 'INSERT INTO ReviewPicture VALUES(%s, %s,%s)'
    cursor.execute(query, (username,recipeID,picurl))
    conn.commit()
    cursor.close()
    return render_template('post_review_picture.html')
@app.route('/logout')
def logout():
    try:
        session.pop('username')
        return redirect('/')
    except:
        return redirect('/')
        
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)
