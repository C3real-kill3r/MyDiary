import unittest
import json
from diary import *

class Test_Diary(unittest.TestCase):
    
    def test_home(self):
        with app.test_client() as h:
            response = h.get('/api/v1/')
            self.assertEqual(response.status_code, 200)
        with app.test_client() as h:
        	response = h.get('/ap1/v1/')
        	self.assertEqual(response.status_code, 404)
   
    def test_comment(self):
    	with app.test_client() as c:
    		response= c.get('/api/v1/get_all',)
    		self.assertEqual(response.status_code, 200)

    def test_comment_single(self):
    	with app.test_client() as cs:
    		response= cs.get('/api/v1/get_one/1',)
    		self.assertEqual(response.status_code, 200)

    def test_logout(self):
    	with app.test_client() as lo:
    		response= lo.get('/api/v1/logout',)
    		self.assertEqual(response.status_code, 200)

    def test_register(self):
        with app.test_client() as r:
            response=r.get('/api/v1/register',)
            self.assertEqual(response.status_code, 405)
            self.assertEqual(r.post('/api/v1/login', json={"username":"brybz","password":"1234","email":"brybzi@gmail.com","name":"brian ryb"}).status_code, 200)

    def test_login(self):
        with app.test_client() as l:
            response=l.get('/api/v1/login',)
            self.assertEqual(response.status_code, 405)
            self.assertEqual(l.post('/api/v1/login', json={"username":"brybz","password":"1234"}).status_code, 200)

    def test_make_entry(self):
        with app.test_client() as m:
            response=m.get('/api/v1/login',)
            self.assertEqual(response.status_code, 405)    
            self.assertEqual(m.post('/api/v1/login', json={"entry":"lets try something out"}).status_code, 500)