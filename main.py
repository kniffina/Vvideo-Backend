from google.appengine.ext import ndb
from google.net.proto.ProtocolBuffer import ProtocolBufferDecodeError
import logging
import webapp2
import json
import datetime

class Video(ndb.Model):
    video_id = ndb.StringProperty()
    user_id = ndb.StringProperty()
    video_title = ndb.StringProperty()
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    votes_received = ndb.IntegerProperty()

class VideoHandler(webapp2.RequestHandler):
    def post(self, user=None, user_id=None):
        if(user_id):
            parent_key = ndb.Key(Video, "parent_video")
            user = ndb.Key(urlsafe=user_id).get()
            video_data = json.loads(self.request.body)
            
            new_video = Video(video_id=None, user_id=user.user_id, video_title=video_data["video_title"], 
                created_date=None, votes_received=0)
            
            #create a dict of the new video
            new_video.put()
            new_video.video_id = new_video.key.urlsafe()
            new_video.put()
            video_dict = new_video.to_dict()

            #put the video inside of the user
            user.put()
            user.videos_created.append(video_dict)
            user.put()

            self.response.headers['Content-Type'] = 'text/plain'
            self.response.headers["Status"] = "201 Created"
            self.response.write(json.dumps(video_dict))             

    def get(self, user=None, user_id=None, video=None, video_id=None):
        if(user_id and video_id):
            video = ndb.Key(urlsafe=video_id).get()
            user = ndb.Key(urlsafe=user_id).get()
        
            self.response.write(video.video_id)
            

            for vid in user.videos_created:
                
                self.response.write(vid)

               
            


            
    def delete(self, user=None, user_id=None, video_id=None):
        if(user_id and video_id):
            user = ndb.Key(urlsafe=user_id).get()
            video = ndb.Key(urlsafe=video_id).get()

            for vid in user.videos_created:
                if vid.video_id == video.video_id:
                    user.videos_created.remove(vid)
                    video.key.delete()
            
                    self.response.headers['Content-Type'] = 'text/plain'
                    self.response.headers["Status"] = "204 No Content"
                    self.response.write(json.dumps("Video deleted"))

                else:
                    self.response.headers['Content-Type'] = 'text/plain'
                    self.response.headers["Status"] = "404 Not Found"
                    self.response.write(json.dumps("Not deleted"))


class User(ndb.Model):
    user_id = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    contacts = ndb.JsonProperty()
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    birthday = ndb.StringProperty()
    videos_created = ndb.JsonProperty()
    phone_number = ndb.StringProperty()

class UserHandler(webapp2.RequestHandler):
    def post(self):
        parent_key = ndb.Key(User, "parent_user")
        user_data = json.loads(self.request.body)

        new_user = User(user_id=None, first_name=user_data["first_name"], last_name=user_data["last_name"],
            email = user_data["email"], username=user_data["username"], password=user_data["password"], 
            birthday=user_data["birthday"], phone_number=user_data["phone_number"], contacts=[], videos_created=[])
        
        new_user.put()
        new_user.user_id = new_user.key.urlsafe()
        new_user.put()
        user_dict = new_user.to_dict()

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.headers["Status"] = "201 Created"
        self.response.write(json.dumps(user_dict))
    
    def get(self, user_id=None):
        if user_id:
            user = ndb.Key(urlsafe=user_id).get()
            user_dict = user.to_dict()

            self.response.headers['Content-Type'] = 'text/plain'
            self.response.headers["Status"] = "200 OK"
            self.response.write(json.dumps(user_dict))
    
    def delete(self, user_id=None):
        if(user_id):
            user = ndb.Key(urlsafe=user_id).get()
            user.key.delete()

            self.response.headers['Content-Type'] = 'text/plain'
            self.response.headers["Status"] = "204 No Content"
            self.response.write("User deleted.")

    def patch(self, user_id=None):
        if(user_id):
            user = ndb.Key(urlsafe=user_id).get()
            user_data = json.loads(self.request.body)

          # user data will be an array of objects
            if "first_name" in user_data:
                user.first_name = user_data["first_name"]
          
            if "last_name" in user_data:  
                user.last_name = user_data["last_name"]
            
            if "email" in user_data:
                user.email = user_data["email"]

            if "username" in user_data:
                user.username = user_data["username"]
            
            if "password" in user_data:
                user.password = user_data["password"]
            
            if "birthday" in user_data:
                user.birthday = user_data["birthday"]
            
            if "phone_number" in user_data:
                user.phone_number = user_data["phone_number"]

            if "contacts" in user_data:
                #add to the contacts list
                for contact in user_data["contacts"]:
                    user.contacts.append(contact)
            
            if "videos_created" in user_data:
                for video in user_data["videos_created"]:
                    user.videos_created.append(video)
                 
            user.put()
            user_dict = user.to_dict()
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.headers["Status"] = "200 OK"
            self.response.write(json.dumps(user_dict))
    
    # used for completely resetting the contacts list, and adding new data while doing it
    def put(self, user_id=None):
        if(user_id):
            user = ndb.Key(urlsafe=user_id).get()
            user_data = json.loads(self.request.body)

            # user data will be an array of objects
            if "first_name" in user_data:
                user.first_name = user_data["first_name"]
            
            if "last_name" in user_data:
                user.last_name = user_data["last_name"]
            
            if "email" in user_data:
                user.email = user_data["email"]
            
            if "username" in user_data:
                user.username = user_data["username"]
            
            if "password" in user_data:
                user.password = user_data["password"]
            
            if "birthday" in user_data:
                user.birthday = user_data["birthday"]
                
            if "phone_number" in user_data:
                user.phone_number = user_data["phone_number"]
            
            if "contacts" in user_data:
                user.contacts = [] #reset contacts
                for contact in user_data["contacts"]:
                    user.contacts.append(contact)
            
            if "videos_created" in user_data:
                for video in user_data["videos_created"]:
                    user.videos_created.append(video)
    
            user.put()
            user_dict = user.to_dict()
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.headers["Status"] = "200 OK"
            self.response.write(json.dumps(user_dict))
                           
class Login(webapp2.RequestHandler):
    def post(self):
        user_data = json.loads(self.request.body)
        found = 0

        # if "username" in user_data:
        #     query = User.query(user_data["username"] == User.username)
        #     users = query.fetch(limit=100)

        #     for user in users:
        #         if user_data["password"] == user.password:
        #             user_dict = user.to_dict()
        #             found = 1
                
        
        if "email" in user_data:
            query = User.query(user_data["email"] == User.email)
            users = query.fetch(limit=100)

            for user in users:
                if user_data["password"] == user.password:
                    user_dict = user.to_dict()
                    found = 1
        
        if found == 1:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.headers["Status"] = "200 OK"
            self.response.write(json.dumps(user_dict))
        else:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.headers["Status"] = "404 Not Found"
            self.response.write("User not found")

                                        
class UserHasApp(webapp2.RequestHandler):
    def post(self):
        user_data = json.loads(self.request.body)
        found = 0

        # might be a better way to check.. might need one more field to ensure user is there.
        # if "phone_number" in user_data:
        #     query = User.query(user_data["phone_number"] == User.phone_number)
        #     users = query.fetch(limit=100)

        #     for user in users:
        #         if user_data["phone_number"] == user.phone_number:
        #             //do something
        #             found = 1
        
        # elif "email" in user_data:
        #     query = User.query(user_data["email"] == User.email)
        #     users = query.fetch(limit=100)

        #     for user in users:
        #         if user_data["email"] == user.email:
        #             found = 1
        
        # else:
        #     found = 0

        #check if email and phone number in user_data, otherwise
        # hard to verify that user is who they actually are
        if "email" and "phone_number" in user_data:
            query = User.query(user_data["email"] == User.email)
            users = query.fetch(limit=100)

            for user in users:
                if user_data["email"] == user.email and user_data["phone_number"] == user.phone_number:
                    user_dict = user.to_dict()
                    found = 1
        
        else:
            found = 0
        
        if found == 1:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.headers["Status"] = "200 OK"
            self.response.write(json.dumps(user_dict))
        else:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.headers["Status"] = "404 Not Found"
            self.response.write("User not found") 
                    

                
                




class CheckUsername(webapp2.RequestHandler):
    def post(self):
        username_data = json.loads(self.request.body)

        if "username" in username_data:
            query = User.query(username_data["username"] == User.username)
            usernames = query.fetch(limit=100)
            taken = 0

            for username in usernames:
                if username_data["username"] == username.username:
                    taken = 1
                    
        if taken == 1:
            self.response.write("taken")
        else:
            self.response.write("not")

       

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('This is the main page')

#used to allow 'patch' requests
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

app = webapp2.WSGIApplication([
    webapp2.Route('/', handler=MainPage, name="main-page"),
    webapp2.Route('/user', handler=UserHandler, name="user-handler"),
    webapp2.Route('/user/<user_id>', handler=UserHandler, name="user-handler"),
    webapp2.Route('/login', handler=Login, name="login"),
    webapp2.Route('/checkusername', handler=CheckUsername, name="check-username"),
    webapp2.Route('/userhasapp', handler=UserHasApp, name='user-has-app'),
    webapp2.Route('/user/<user_id>/video', handler=VideoHandler, name="video-handler"),
    webapp2.Route('/user/<user_id>/video/<video_id>', handler=VideoHandler, name="video-handler"),
], debug=True)

# C:\Users\a.kniffin.MORROW\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\dev_appserver.py
# In GitBash:
# "C:\Users\a.kniffin.MORROW\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\dev_appserver.py" "C:\documents\Vvideo"
