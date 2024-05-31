import json

def test_get_movies(client):
    response = client.get('/movies')
    assert response.status_code == 200

def test_add_movie(client):
    new_movie = {'title': 'Inception', 'genre': 'Sci-Fi'}
    response = client.post('/movies', data=json.dumps(new_movie), content_type='application/json')
    assert response.status_code == 201
