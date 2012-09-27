#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# NOTE:  This is a modified version of the 'chat' demo application included in
# the Tornado framework tarball.

"""
@author: Rahul Gautam
@author: Mahipal Chaudhary
@note: Puzzel > Shaddy Puzzel
"""

import logging
import time
import json
import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import uuid
from shady_puzzle import RandomCube

from tornado.options import define, options

define("port", default=8000, help="Run on the given port", type=int)

global play_dict

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", CubeHome),
			(r"/index", MainHandler),
            (r"/auth/login", AuthLoginHandler),
            (r"/auth/logout", AuthLogoutHandler),
            (r"/a/message/new", MessageNewHandler),
            (r"/a/message/updates", MessageUpdatesHandler),
            (r"/game/cube/getarray", GetArray),
            (r"/game/cube/getsolution", GetSolution),
            (r"/game/cube/checksolution", CheckSolution),
            (r"/game/cube/play",Play),
            (r"/game/cube/random",GetRandom),
            (r"/cube",GameHome)
        ]
        settings = dict(
            cookie_secret="MjkwYzc3MDI2MjhhNGZkNDg1MjJkODgyYjBmN2MyMTM4M",
            login_url="/auth/login",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            debug=True,
            autoescape="xhtml_escape"
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json: return None
        return tornado.escape.json_decode(user_json)
        

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        global play_dict
        user = self.get_current_user()
        api_key = self.settings['cookie_secret']
        upn = user['email']
        # Make a note that this is a quick way to generate a JS-style epoch:
        timestamp = str(int(time.time()) * 1000)
        auth_obj = {
            'api_key': api_key, # Whatever is in server.conf
            'upn': upn, # e.g. user@gmail.com
            'timestamp': timestamp,
            #'signature': <gibberish>, # We update the sig below
            'signature_method': 'HMAC-SHA1', # Won't change (for now)
            'api_version': '1.0' # Won't change (for now)
        }
        secret = 'secret' # Whatever is in server.conf for our API key
        # For this app I'm using the convenient _create_signature() method but
        # it is trivial to implement the same exact thing in just about any
        # language. Here's the function (so you don't have to look it up =):
        #
        # def _create_signature(secret, *parts):
        #    hash = hmac.new(utf8(secret), digestmod=hashlib.sha1)
        #    for part in parts: hash.update(utf8(part))
        #    return utf8(hash.hexdigest())
        #
        # Real simple: HMAC-SHA1 hash the three parts using 'secret'.  The utf8
        # function just ensures that the encoding is UTF-8.  In most cases you
        # won't have to worry about stuff like that since these values will most
        # likely just be ASCII.
        signature = tornado.web._create_signature(
            secret,
            api_key,
            upn,
            timestamp
        )
        auth_obj.update({'signature': signature})
        auth = json.dumps(auth_obj)
        self.render(
            "index.html",
            messages=MessageMixin.cache,
            auth=auth,
            game_type=play_dict.get(user.get(u'email'),"single")
        )

class Play(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        global play_dict
        email = self.get_current_user().get(u'email')
        gametype = self.get_argument("gametype", None)
        play_dict[email] = gametype
        return

class CubeHome(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render(
            "home.html"
        )		

class GameHome(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render(
            "game.html"
        )		
        
class MessageMixin(object):
    waiters = set()
    cache = []
    cache_size = 200

    def wait_for_messages(self, callback, cursor=None):
        cls = MessageMixin
        if cursor:
            index = 0
            for i in xrange(len(cls.cache)):
                index = len(cls.cache) - i - 1
                if cls.cache[index]["id"] == cursor: break
            recent = cls.cache[index + 1:]
            if recent:
                callback(recent)
                return
        cls.waiters.add(callback)

    def cancel_wait(self, callback):
        cls = MessageMixin
        cls.waiters.remove(callback)

    def new_messages(self, messages):
        cls = MessageMixin
        logging.info("Sending new message to %r listeners", len(cls.waiters))
        for callback in cls.waiters:
            try:
                callback(messages)
            except:
                logging.error("Error in waiter callback", exc_info=True)
        cls.waiters = set()
#        logging.info(" cache : "+ str(cls.cache))
#        logging.info(" cache : "+ str(messages))
        key= messages[0].get('from')
        flag = 1
        for i in cls.cache:
			if i['from'] == key:
				flag = 0
				i['body'] = messages[0].get('body')
				i['html'] = messages[0].get('html')
				i['id'] = messages[0].get('id')        
        if flag:
			cls.cache.extend(messages)
        if len(cls.cache) > self.cache_size:
            cls.cache = cls.cache[-self.cache_size:]
            
    def modify_messages(self, from_user, color='black'):
        cls = MessageMixin
        cls.waiters = set()
        logging.info(" cachedsfas : "+ str(cls.cache))
        logging.info("user"+from_user)
        for i in cls.cache:
			logging.info(str(i['from']))
			if str(i['from']) == from_user:
				loc = i['html'].find('>')
				loc2 = 1
				if i['html'].find("style='color:") != -1:
					loc = i['html'].find("style='color:")
					loc2 = i['html'].find(";",loc)+1
					loc2 = loc2-loc
				red_class = " style='color:%s'; "%color
				i['html'] = i['html'][:loc-1] + red_class + i['html'][loc+loc2:]
				
				logging.info(" cache : "+ str(cls.cache))
        
        if len(cls.cache) > self.cache_size:
            cls.cache = cls.cache[-self.cache_size:]



class GenerateArray(object):
	puzzle_dict = {}
	solution_dict = {}
	rc = RandomCube()
	
	def __init__(self):
		pass
		
	@staticmethod
	def get_array(key):
		if GenerateArray.puzzle_dict.has_key(key):
			pass
		else:
			result_dict = GenerateArray.rc.get_random_cube()
			GenerateArray.solution_dict[key] = result_dict.pop('solution')
			GenerateArray.puzzle_dict[key] = result_dict
		return GenerateArray.puzzle_dict.get(key)
	
	@staticmethod
	def get_solution(key):		
		return GenerateArray.solution_dict.get(key, "Error_No_Solution_Found")
	
	@staticmethod
	def get_cells(key):
		if GenerateArray.puzzle_dict.has_key(key):
			return GenerateArray.puzzle_dict[key].get('cells')
		else:
			return 

	@staticmethod
	def get_xaxis(key):
		if GenerateArray.puzzle_dict.has_key(key):
			return GenerateArray.puzzle_dict[key].get('x_axis')
		else:
			return
			
	@staticmethod
	def get_yaxis(key):
		if GenerateArray.puzzle_dict.has_key(key):
			return GenerateArray.puzzle_dict[key].get('y_axis')
		else:
			return
					
	@staticmethod
	def del_tournament(key):
		if GenerateArray.puzzle_dict.has_key(key):		
			del GenerateArray.puzzle_dict[key]
			
		if GenerateArray.solution_dict.has_key(key):		
			del GenerateArray.solution_dict[key]

	@staticmethod
	def get_random(key):
	    GenerateArray.del_tournament(key)
	    return GenerateArray.get_array(key)

	@staticmethod
	def check_solution(key, solution_li):
		if GenerateArray.solution_dict.has_key(key):
			cells = GenerateArray.get_cells(key)
			x_axis = GenerateArray.get_xaxis(key)
			y_axis = GenerateArray.get_yaxis(key)
			logging.info(" solution_string "+str(solution_li))
			solution_li = map(str,solution_li.split(','))
			solution_array = []
			k=0
			
			for i in range(cells+1):
				temp = []
				for j in range(cells+1):
					temp.append(solution_li[k])
					k+=1					
				solution_array.append(temp)
			
			#GenerateArray.solution_dict[key])			
			del solution_array[0]
			for i in solution_array:
				del i[0]
			info_x_axis=[]
			info_y_axis=[]
			flag=0
			for i in range(len(solution_array)):
				count=0
				tmp=[]
				for j in range(len(solution_array[i])):
					if solution_array[j][i] =='1':
						count+=1
						flag=1
					else:
						if count!=0:
						  tmp.append(count)
						  count=0
						  flag=0
				if flag:
					tmp.append(count)
				info_x_axis.append(tmp)

			for i in range(len(solution_array)):
				count=0
				tmp=[]
				for j in range(len(solution_array[i])):
					if solution_array[i][j] =='1':
						count+=1
						flag=1
					else:
						if count!=0:
						  tmp.append(count)
						  count=0
						  flag=0
				if flag:
					tmp.append(count)
				info_y_axis.append(tmp)
				
			if x_axis == info_x_axis and y_axis == info_y_axis:
				return True
			else:
				return False
		else:
			return False

	

class GetArray(BaseHandler):	
    @tornado.web.authenticated
    def post(self):
        gametype = self.get_argument("gametype", None)
        tournament = self.get_argument("tournament", None)
        from_user = self.get_current_user().get(u'name')
        key = None
        if from_user is not None and gametype == 'single':
            from_user = from_user.replace(' ','_')
            key	= from_user	
        elif tournament is not None:
            key = tournament		
        else:
            game_array = {
				"success" : 1,
				"result" : ' Parameters not found ',
			}
		
        if key:
            game_array = GenerateArray.get_array(key)
            game_array['success'] = 0	
		
        self.write(game_array)
        

class GetRandom(BaseHandler):	
    @tornado.web.authenticated
    def post(self):
        gametype = self.get_argument("gametype", None)
        tournament = self.get_argument("tournament", None)
        from_user = self.get_current_user().get(u'name')
        key = None
        if from_user is not None and gametype == 'single':
			from_user = from_user.replace(' ','_')
			key	= from_user	
        elif tournament is not None:
		    key = tournament		
        else:
			game_array = {
				"success" : 1,
				"result" : ' Parameters not found ',
			}
		
        if key:
			game_array = GenerateArray.get_random(key)
			game_array['success'] = 0	
		
        self.write(game_array)        
			

class GetSolution(BaseHandler,MessageMixin):
    @tornado.web.authenticated
    def post(self):
        gametype = self.get_argument("gametype", None)
        tournament = self.get_argument("tournament", None)
        from_user = self.get_current_user().get(u'name')
        key = None
        game_array = {}
        if from_user is not None and gametype == 'single':
			from_user = from_user.replace(' ','_')
			key	= from_user	
        elif tournament is not None:
		    key = tournament		
        else:
			game_array = {
				"success" : 1,
				"result" : ' Tournament not found ',
			}

			#self.modify_messages(from_user,'red')
        if key:
			game_array['result'] = GenerateArray.get_solution(key)
			game_array['success'] = 0		
        self.write(game_array)
		

class CheckSolution(BaseHandler, MessageMixin):
    @tornado.web.authenticated
    def post(self):
        gametype = self.get_argument("gametype", None)
        tournament = self.get_argument("tournament", None)
        from_user = self.get_current_user().get(u'name')
        solution_li = self.get_argument("solution", None)
        game_array = {}
        key = None
        if from_user is not None and gametype == 'single':
			from_user = from_user.replace(' ','_')
			key	= from_user	
        elif tournament is not None:
		    key = tournament			
		
        if key is not None and solution_li is not None:
			if GenerateArray.check_solution(key,solution_li):
				game_array['result'] = '1'
			else:
				game_array['result'] = '0'
				
			game_array['success'] = 0
			
        else:
			game_array = {
				"success" : 1,
				"result" : ' Tournament not found ',
			}
		#self.modify_messages(from_user,'blue')
        self.write(game_array)	
             

class MessageNewHandler(BaseHandler, MessageMixin):
    @tornado.web.authenticated
    def post(self):
        message = {
            "id": str(uuid.uuid4()),
            "from": self.current_user["name"].replace(' ','_'),
            "body": self.get_argument("body"),
        }
        #logging.info(" dict : "+ str(self.current_user))
        message["html"] = self.render_string("message.html", message=message)
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(message)
        self.new_messages([message])


class MessageUpdatesHandler(BaseHandler, MessageMixin):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    def post(self):
        cursor = self.get_argument("cursor", None)
        self.wait_for_messages(self.on_new_messages,
                               cursor=cursor)

    def on_new_messages(self, messages):
        # Closed client connection
        if self.request.connection.stream.closed():
            return
        self.finish(dict(messages=messages))

    def on_connection_close(self):
        self.cancel_wait(self.on_new_messages)


class AuthLoginHandler(BaseHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect(ax_attrs=["name","email"])

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")
        self.set_secure_cookie("user", tornado.escape.json_encode(user))
        self.redirect("/cube")


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.write("You are now logged out")
        self.redirect("/")

def main():
    global play_dict
    play_dict = {} 
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port, ssl_options={
        "certfile": os.path.join(os.getcwd(), "certificate.pem"),
        "keyfile": os.path.join(os.getcwd(), "keyfile.pem"),
    })
    print("For this to work you must add the following to Cube's "
          "server.conf:\n")
    # Using the cookie_secret as the API key here:
    print('api_keys = "MjkwYzc3MDI2MjhhNGZkNDg1MjJkODgyYjBmN2MyMTM4M:secret"')
    print("\n...and restart Cube for the change to take effect.")
    print("Listening on 0.0.0.0:%s" % options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
