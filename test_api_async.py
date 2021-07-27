import pytest
import flask
import requests
import api_async

app = flask.Flask(__name__)

API_URL = 'http://127.0.0.1:5000/api/'
ping_url = API_URL + '/ping'
posts_url = API_URL + 'posts?'

# ______________________________________________________________________________
# Testing the url /api/ping
def test_1_api_ping():
    response = requests.get(ping_url)
    assert response.status_code == 200
    assert response.json() == {"success": True}


# Testing the url /api/posts without tags parameter
def test_2_api_posts():
    response = requests.get(posts_url)
    assert response.status_code == 400
    assert response.json() == {"error": "Tags parameter is required"}
# ______________________________________________________________________________

# Testing the url /api/posts/sortBy=id without tags parameter
def test_3_1_get_sort_by_without_tags():
    response = requests.get(posts_url + 'sortBy=id')
    assert response.status_code == 400
    assert response.json() == {"error": "Tags parameter is required"}


# Testing the url /api/posts/sortBy=likes without tags parameter
def test_3_2_get_sort_by_without_tags():
    response = requests.get(posts_url + 'sortBy=likes')
    assert response.status_code == 400
    assert response.json() == {"error": "Tags parameter is required"}


# Testing the url /api/posts/sortBy=reads without tags parameter
def test_3_3_get_sort_by_without_tags():
    response = requests.get(posts_url + 'sortBy=reads')
    assert response.status_code == 400
    assert response.json() == {"error": "Tags parameter is required"}


# Testing the url /api/posts/sortBy=popularity without tags parameter
def test_3_4_get_sort_by_without_tags():
    response = requests.get(posts_url + 'sortBy=popularity')
    assert response.status_code == 400
    assert response.json() == {"error": "Tags parameter is required"}


# Testing the url /api/posts?tags=tech&sortBy=id with tags parameter
def test_3_5_get_sort_by_with_tags():
    response = requests.get(posts_url + 'tags=tech&sortBy=id')
    assert response.status_code == 200


# Testing the url /api/posts?tags=tech&sortBy=likes  with tags parameter
def test_3_6_get_sort_by_with_tags():
    response = requests.get(posts_url + 'tags=tech&sortBy=likes')
    assert response.status_code == 200


# Testing the url /api/posts?tags=tech&sortBy=reads with tags parameter
def test_3_7_get_sort_by_with_tags():
    response = requests.get(posts_url + 'tags=tech&sortBy=reads')
    assert response.status_code == 200


# Testing the url /api/posts/tags=tech&sortBy=popularity with tags parameter
def test_3_8_get_sort_by_with_tags():
    response = requests.get(posts_url + 'tags=tech&sortBy=popularity')
    assert response.status_code == 200

# Testing the url /api/posts/tags=tech&sortBy=unknown_value with tags parameter
def test_3__9get_sort_by_with_tags():
    response = requests.get(posts_url + 'tags=tech&sortBy=unknown_value')
    assert response.status_code == 400
    assert response.json() == {"error":"sortBy parameter is invalid"}

# ______________________________________________________________________________
# Testing the url /api/posts/direction=asc without tags parameter
def test_4_1_get_direction_without_tags():
    response = requests.get(posts_url + 'direction=asc')
    assert response.json() == {"error": "Tags parameter is required"}
    assert response.status_code == 400


# Testing the url /api/posts/direction=desc without tags parameter
def test_4_2_get_direction_without_tags():
    response = requests.get(posts_url + 'direction=asc')
    assert response.json() == {"error": "Tags parameter is required"}
    assert response.status_code == 400


# Testing the url /api/posts/direction=asc with tags parameter
def test_4_3_get_direction_with_tags():
    response = requests.get(posts_url + 'tags=tech&direction=asc')
    assert response.status_code == 200


# Testing the url /api/posts/direction=desc with tags parameter
def test_4_4_get_direction_with_tags():
    response = requests.get(posts_url + 'tags=tech&direction=desc')
    assert response.status_code == 200

# Testing the url /api/posts/direction=unknown_value with tags parameter
def test_4_5_get_direction_with_tags():
    response = requests.get(posts_url + 'tags=tech&direction=unknown_value')
    assert response.status_code == 400
    assert response.json() == {"error": "direction Parameter is invalid"}
