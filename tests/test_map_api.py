import os
import tempfile
import json
import pytest

from map_api import create_app


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({'TESTING': True, 'DATABASE': db_path})

    with app.test_client() as client:
        with app.app_context():
            pass
        yield client

    os.close(db_fd)
    os.unlink(db_path)

def test_index(client):
    """Testing index."""

    rv = client.get('/')
    assert b'helloy' in rv.data

@pytest.mark.parametrize(
    "x,y", 
    [
        (10,8), 
        (4,6)
    ]
)
def test_createLayout(client,x,y):
    """Testing createLayout."""

    rv = client.get(f'/createLayout?x={x}&y={y}')
    assert json.loads(rv.data.decode('utf-8'))

    data = json.loads(rv.data.decode('utf-8'))
    assert isinstance(data['table_id'],int)

def test_getLayouts(client):
    """Testing getLayout."""


    rv = client.get('/getLayouts')
    assert json.loads(rv.data.decode('utf-8'))

@pytest.mark.parametrize(
    "table_id,x,y", [
        (1,0, 0), 
        (1,1, 2)
    ])
def test_getValueOf(client,table_id,x,y):
    """Testing getValueOf."""

    rv = client.get(f'/getValueOf?table_id={table_id}&x={x}&y={y}')

    data = json.loads(rv.data.decode('utf-8'))
    assert isinstance(data['value'],int)