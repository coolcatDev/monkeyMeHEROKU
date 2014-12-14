from flask import Flask, render_template, redirect, \
	url_for, request, session, flash

from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

#local
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///monkeyDB.db'


#heroku
import os
#app.config.from_object('config.BaseConfig')

app.config.from_object(os.environ['APP_SETTINGS'])



db = SQLAlchemy(app)

from models import *



@app.route('/')
def index():
 
  if not session.get('logged_in'):
                return render_template('login.html')
       
  else:
                return redirect(url_for('friendList'))



@app.route('/friends')
def friendList():
  if not session.get('logged_in'):
                
                return render_template('login.html')
       
  else:
                
                userID = session['user_id']
              
                userList = db.session.query(friendships).filter((friendships.userIdA == userID) | (friendships.userIdB == userID)) 
              
                bestFriend = db.session.query(bestFriends).filter((bestFriends.userIdA == userID) | (bestFriends.userIdB == userID)) 
              
                return render_template('friends.html', userList=userList, bestFriend=bestFriend)


@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':

          userCheck = request.form['username']
          userCheck2 = request.form['password']
          userName = users.query.filter_by(userName=userCheck, userPass=userCheck2).first()

          if userName:
                      session['logged_in'] = True
                      session['user_id'] = userName.id
                  
                      return redirect(url_for('friendList'))
          else:
                      return render_template('login.html')           
    else:
          return render_template('login.html')



     
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return render_template('login.html')



@app.route('/users')
def allList():

  if not session.get('logged_in'):
        return render_template('login.html')
   
  else:
        userList = users.query.all()
        return render_template('users.html', userList=userList)
        #query = session.query(users, friendships).join(friendships).filter(....)



@app.route('/profile<profileId>')
def profile(profileId):
  if not session.get('logged_in'):
        return render_template('login.html')
  else: 
        profileID = profileId
        
        bestFriend = db.session.query(bestFriends).filter((bestFriends.userIdA == profileID) | (bestFriends.userIdB == profileID)) 

        userList = users.query.filter_by(id=profileID).all()
        
        return render_template('profile.html', userList=userList, bestFriend=bestFriend)



@app.route('/myProfile')
def myProfile():
  
  if not session.get('logged_in'):
        
        return render_template('login.html')
  
  else: 
        profileID = session['user_id']
        
        userList = users.query.filter_by(id=profileID).all()
        
        return render_template('myProfile.html', userList=userList)



@app.route('/addFriend/<userToAdd>')
def addFriend(userToAdd):
    #get loged in user id and username
    profileID = session['user_id']
    profileNameSearch = users.query.filter_by(id=profileID).first()
    profileName = profileNameSearch.userName
    #get new friends id and username
    userToAddNameSearch = users.query.filter_by(id=userToAdd).first()
    userToAddName = userToAddNameSearch.userName

    #check friendship doesnt exist to avoid duplication

    frienshipCheck = friendships.query.filter_by(userNameA=profileName, userNameB=userToAddName).first()

    if frienshipCheck:
          return redirect(url_for('friendList'))

    frienshipCheck2 = friendships.query.filter_by(userNameA=userToAddName, userNameB=profileName).first()
    if frienshipCheck2:
          return redirect(url_for('friendList'))

    else:  
          newFriend = friendships(profileID, userToAdd, profileName, userToAddName)


          db.session.add(newFriend)
          db.session.commit()
          return redirect(url_for('friendList'))



@app.route('/removeFriend/<friendshipToRemove>/<userToRemove>')
def removeFriend(friendshipToRemove,userToRemove):

    profileID = session['user_id']

    #remove friendship
    oldFriend = friendships.query.filter_by(id=friendshipToRemove).first()
    db.session.delete(oldFriend)
    db.session.commit()

    #remove BFF if exists
    oldBFFCheck = bestFriends.query.filter_by(userIdA=profileID, userIdB=userToRemove).first()

    if oldBFFCheck:
          db.session.delete(oldBFFCheck)
          db.session.commit()

    oldBFFCheck = bestFriends.query.filter_by(userIdA=userToRemove, userIdB=profileID).first()
      
    if oldBFFCheck:
          db.session.delete(oldBFFCheck)
          db.session.commit()


    return redirect(url_for('friendList'))





@app.route('/addBestFriend/<userToRequest>/<userToRequestName>')
def addBestFriend(userToRequest,userToRequestName):
          
  profileID = session['user_id']
  profileNameSearch = users.query.filter_by(id=profileID).first()
  profileName = profileNameSearch.userName

  #remove existing BFF from both parts col a or b
  oldBestFriend = bestFriends.query.filter_by(userIdA=userToRequest).first()
  if oldBestFriend:
      db.session.delete(oldBestFriend)
      db.session.commit()
  else:
      oldBestFriend = bestFriends.query.filter_by(userIdB=userToRequest).first()
      if oldBestFriend:
          db.session.delete(oldBestFriend)
          db.session.commit()        

  oldBestFriend = bestFriends.query.filter_by(userIdA=profileID).first()
  if oldBestFriend:
      db.session.delete(oldBestFriend)
      db.session.commit()
  else:
      oldBestFriend = bestFriends.query.filter_by(userIdB=profileID).first()
      if oldBestFriend:
          db.session.delete(oldBestFriend)
          db.session.commit()  

  #add the new friend
  newBFF = bestFriends(profileID, userToRequest, profileName, userToRequestName)
  db.session.add(newBFF)
  db.session.commit()
  return redirect(url_for('friendList'))




@app.route('/register')
def register():
 
  if session.get('logged_in'):
                return redirect(url_for('friendList'))
       
  else:
                return render_template('register.html')


@app.route('/registeringUser', methods=['GET', 'POST'])
def registering():

      if request.method == 'POST':

          userCheck = request.form['username']
          userCheck2 = request.form['email']
          userCheck3= request.form['password']
          userCheck4 = request.form['passwordCheck']
          userCheck5 = request.form['phone']
          userName = users.query.filter_by(userName=userCheck).first()


          if userName:
                      return render_template('register.html')
          if userCheck2 == "":
                      return render_template('register.html')  
          if userCheck3 == "":
                      return render_template('register.html')  
          if userCheck5 == "":
                      return render_template('register.html')    

          else:
                      if userCheck3 == userCheck4:
                                       newUser = users(userCheck, userCheck2, userCheck5, userCheck3)
                                       db.session.add(newUser)
                                       db.session.commit()
                                       userName = users.query.filter_by(userName=userCheck, userPass=userCheck3).first()
                                       session['logged_in'] = True
                                       session['user_id'] = userName.id
                                       return redirect(url_for('friendList'))

                      else:
                                       return render_template('register.html')           
      else:
          return render_template('register.html')



@app.route('/deleteAccount/<userToDelete>')
def deleteAccount(userToDelete):

    #User
    oldAccountUser = users.query.filter_by(id=userToDelete).first()
    
    db.session.delete(oldAccountUser)
    
    db.session.commit()

    #Friendships
    oldAccountFriendshipsA = friendships.query.filter_by(userIdA=userToDelete).all()
    
    for row in oldAccountFriendshipsA:
        db.session.delete(row)
        db.session.commit()
        

    oldAccountFriendshipsB = friendships.query.filter_by(userIdB=userToDelete).all()
    
    for row in oldAccountFriendshipsB:
        db.session.delete(row)
        db.session.commit()

    #BFF
    oldAccountBFFA = bestFriends.query.filter_by(userIdA=userToDelete).first()
   
    if oldAccountBFFA:
        db.session.delete(oldAccountBFFA)
        db.session.commit()


    oldAccountBFFB = bestFriends.query.filter_by(userIdB=userToDelete).first()

    if oldAccountBFFB:   
        db.session.delete(oldAccountBFFB)
        db.session.commit()


    return redirect(url_for('logout'))





if __name__ == '__main__':
    app.run(debug=True)


