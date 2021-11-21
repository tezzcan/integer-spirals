from flask import Blueprint,Response, request, jsonify
from .models import Database
from .internal import prepare_table

api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/')
def index():
    return Response('helloy')

@api_bp.route('/createLayout', methods=['GET'])
def createLayout():
    try:
        db = Database()

        x = int(request.args.get('x'))
        y = int(request.args.get('y'))

        table = prepare_table(x, y)
        table_id = db.get_last_id() + 1

        for row_id, row in enumerate(table):
            for col_id, value in enumerate(row):
                data = [table_id, row_id, col_id, value]
                db.insert(data)

        db.set_last_id(table_id)
        db.close()
        return jsonify({
            'table_id': table_id
        })
    
    except Exception as e:
        return Response("Incorrect request.", status=400)

@api_bp.route('/getValueOf', methods=['GET'])
def getValueOf():
    try:
        db = Database()
        table_id = int(request.args.get('table_id'))
        x = int(request.args.get('x'))
        y = int(request.args.get('y'))

        value = db.get(table_id, x, y)
        
        db.close()
        return jsonify({
            'value': value[0]['value']
        })

    except Exception as e:
        return Response("Incorrect request.", status=400)
        #? customer is not always right :)
        
@api_bp.route('getLayouts', methods=['GET'])
def getLayouts():
    try: 
        db = Database()
        last_table_id = db.get_last_id()

        data = db.get_all()

        formatted_data = []
        for table_id in range(1, last_table_id+1):
            table_data = []
            for item in data:
                if item['table_id'] == table_id:
                    table_data.append({
                        'row_id': item['row_id'],
                        'col_id': item['col_id'],
                        'value': item['value']
                    })
            formatted_data.append({
                'table_id': table_id,
                'data': table_data
            })


        db.close()
        return jsonify(formatted_data)

    except Exception as e:
        return Response("Incorrect request.", status=400)


