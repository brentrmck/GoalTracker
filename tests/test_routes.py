def test_homepage_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Habit Tracker" in response.data

def test_add_habit(client):
    response = client.post('/', data={
        'name': 'Test Habit',
        'frequency': 'daily'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Test Habit' in response.data
