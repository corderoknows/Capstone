from contextlib import AbstractContextManager
import os
from typing import Any
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import Movie, setup_db, Actor, db




class CastingTestCase(unittest.TestCase):
    def setUp(self):
        self.CASTING_ASSISTANT = os.environ['CASTING_ASSISTANT']
        self.CASTING_DIRECTOR =  os.environ['CASTING_DIRECTOR']
        self.EXECUTIVE_PRODUCER = os.environ['EXECUTIVE_PRODUCER']

        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        self.new_actor = {
            "name": "Boseman",
            "age": 43,
            "gender": "male"
        }

        self.new_movie = {
            "title": "Black Panther",
            "duration": 3,
            "release_year": 2018
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self_app)

            
            self.db.create_all()

    def tearDown(self):
        pass

    def test_health(self):
        res = self.client().get('/')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], 'Healthy!')

    def test_get_actors_without_token(self):
        res = self.client().get('actors')
        self.assertEqual(res.status_code, 401)

    def test_get_actors_with_valid_token(self):
        res = self.client().get(
            '/actors',
            headers={
                "Authorization": f"Beareer {self.EXECUTIVE_PRODUCER}"})
        self.assertEqual(res.status_code, 200)

    def test_get_specific_actor_without_token(self):
        res = self.client().get('actors/8')
        self.assertEqual(res.status_code, 401)

    def test_get_actors_with_valid_token(self):
        res = self.client().get(
            'actors/8',
            headers={
                "Authorizations": f"Bearer {self.EXECUTIVE_PRODUCER}"},
            json=self.new_actor)
        self.assertEqual(res.status_code, 401)


        
    def test_create_actor_without_token(self):
        res = self.client().post('actors', json=self.new_actor)
        self.assertEqual(res.status_code, 401)

    def test_create_actor_without_valid_token():
        res = self.client().post(
            'actors',
            headers={
                "Authorization": f"Bearer {self.EXECUTIVE_PRODUCER}"},
            json=self.new_actor)
        self.assertEqual(res.status_code, 200)

    def test_delete_actor_without_token(self):
        res = self.client().delete('/actors/10')
        self.assertEqual(res.status_code, 401)

    def test_delete_actor_with_valid_token(self):
        res = self.client().delete('/actors/10',
                                   headers={"Authorization": f"Bearer {self.EXECUTIVE_PRODUCER}"})
        self.assertEqual(res.status_code, 200)

    def test_get_movies_without_token(self):
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 401)

    def test_get_movies_with_valid_token(self):
        res = self.client().get(
            '/movies',
            headers={
                "Authorization": f"Bearer {self.EXECUTIVE_PRODUCER}"})
        self.assertEqual(res.status_code, 200)

    def test_get_specific_movie_without_token(self):
        res = self.client().get('/movies/6')
        self.assertEqual(res.status_code, 401)

    def test_get_specific_movie_with_valid_token(self):
        res = self.client().get(
            '/movies/6',
            headers={
                "Authorization": f"Bearer {self.EXECUTIVE_PRODUCER}"})
        self.assertEqual(res.status_code, 200)

    def test_create_movie_without_token(self):
        res = self.client().post('/movies', json=self.new_movie)
        self.assertEqual(res.status_code, 401)

    def test_create_movie_with_valid_token(self):
        res = self.client().post(
            '/movies',
            headers={
                "Authorization": f"Bearer {self.EXECUTIVE_PRODUCER}"},
            json=self.new_movie)
        self.assertEqual(res.status_code, 200)

    def test_patch_movie_without_token(self):
        res = self.client().patch('/movies/6', json=self.new_movie)
        self.assertEqual(res.status_code, 401)

    def test_patch_movie_with_valid_token(self):
        res = self.client().patch(
            '/movies/6',
            headers={
                "Authorization": f"Bearer {self.EXECUTIVE_PRODUCER}"},
            json=self.new_movie)
        self.assertEqual(res.status_code, 200)

    def test_delete_movie_without_token(self):
        res = self.client().delete('/movies/8')
        self.assertEqual(res.status_code, 401)

    def test_delete_movie_with_valid_token(self):
        res = self.client().delete('/movies/8',
                                   headers={"Authorization": f"Bearer {self.EXECUTIVE_PRODUCER}"})
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()



