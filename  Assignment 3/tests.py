import pytest
from app import app, db, DataPoint

@pytest.fixture
def test_app():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_data_points.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(test_app):
    return test_app.test_client()

@pytest.fixture
def sample_data():
    data_points = [
        DataPoint(feature1=1.0, feature2=2.0, category=1),
        DataPoint(feature1=3.0, feature2=4.0, category=2),
    ]
    db.session.add_all(data_points)
    db.session.commit()
    return data_points

def test_api_get_data(client, sample_data):
    response = client.get('/api/data')
    assert response.status_code == 200
    data = response.get_json()

    assert len(data) == 2
    assert data[0]['feature1'] == 1.0
    assert data[0]['feature2'] == 2.0
    assert data[0]['category'] == 1

def test_api_add_data(client):
    new_data = {
        'feature1': 5.0,
        'feature2': 6.0,
        'category': 3
    }
    response = client.post('/api/data', json=new_data)
    assert response.status_code == 201

    created_data = db.session.get(DataPoint, response.json['id'])
    assert created_data is not None
    assert created_data.feature1 == 5.0
    assert created_data.feature2 == 6.0
    assert created_data.category == 3

def test_api_delete_data(client, sample_data):
    record_id = sample_data[0].id
    response = client.delete(f'/api/data/{record_id}')
    assert response.status_code == 200

    deleted_data = db.session.get(DataPoint, record_id)
    assert deleted_data is None

def test_api_delete_nonexistent_data(client):
    response = client.delete('/api/data/123')
    assert response.status_code == 404
    assert response.get_json() == {"error": "Record not found"}

def test_api_add_invalid_data(client):
    invalid_data = {
        'feature1': 'X',
        'feature2': 6.0,
        'category': 3
    }
    response = client.post('/api/data', json=invalid_data)
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid data"}