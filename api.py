import os
from flask import Flask, request, jsonify, session, send_from_directory
from flask_session import Session
from chess import Board

app = Flask(__name__)
app.config['SECRET_KEY'] =  os.environ.get('SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


@app.route('/api/chess/new', methods=['GET'])
def new_game():
    session['board'] = Board()
    return jsonify({'message': f'New game started\n{session["board"].display()}'})

@app.route('/api/chess/move', methods=['POST'])
def apply_move():
    board = session.get('board')
    if not board:
        return jsonify({'error': 'No game in progress'}), 400
    move = request.json.get('move')
    success = board.apply_move(move)
    session['board'] = board  # Update the session with the new board state
    return jsonify({'success': success, 'board': board.board})

@app.route('/api/chess/moves', methods=['GET'])
def get_moves():
    board = session.get('board')
    if not board:
        return jsonify({'error': 'No game in progress'}), 400
    row = request.args.get('row')
    col = request.args.get('col')
    print(f'Row: {row}, Col: {col}')
    if row is None or col is None:
        return jsonify({'error': 'Row and column must be provided'}), 400
    try:
        row = int(row)
        col = int(col)
    except ValueError:
        return jsonify({'error': 'Row and column must be integers'}), 400
    coord_str = board.convert_coord_inv(row, col)
    print(f'Getting moves for {coord_str}')
    print(f'Board state:\n{board.display()}')
    moves = board.get_legal_moves(row, col)
    return jsonify({'moves': moves})

@app.route('/api/chess/undo', methods=['POST'])
def undo_move():
    board = session.get('board')
    if not board:
        return jsonify({'error': 'No game in progress'}), 400
    board.undo_move()
    session['board'] = board
    
    return jsonify({'message': 'Move undone'})

@app.route('/api/chess/reset', methods=['POST'])
def reset_game():
    session.pop('board', None)
    return jsonify({'message': 'Game reset'})



if __name__ == '__main__':
    app.run(debug=True)