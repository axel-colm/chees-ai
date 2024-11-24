import os
from flask import Flask, request, jsonify, session, send_from_directory
from flask_session import Session
from chess import Chess
from chess.alphabeta import AlphaBeta
import random

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
    session['board'] = Chess()
    return jsonify({'message': 'New game started'})

@app.route('/api/chess/move', methods=['POST'])
def apply_move():
    chess: Chess = session.get('board')
    move = request.json.get('move')
    ok = chess.move(move)
    response = {'board': chess.board.board, 'turn': chess.turn, 'isCheck': {'white': chess.board.is_check(1), 'black': chess.board.is_check(-1)}}
    if not ok:
        response['error'] = 'Invalid move'
        return jsonify(response), 400
    
    return jsonify(response), 200


@app.route('/api/chess/moves', methods=['GET'])
def get_moves():
    row = request.args.get('row')
    col = request.args.get('col')
    if row.isdigit() and col.isdigit():
        row, col = int(row), int(col)
    else:
        return jsonify({'error': 'Invalid row or col'}), 400
    
    chess = session.get('board')
    if not chess:
        return jsonify({'error': 'No game in progress'}), 400
    
    piece = chess.board.get_piece(col, row)
    if piece == 0:
        return jsonify({'moves': []})
    moves = chess.board.get_legal_moves(col, row)
    moves = [{'row': move[1], 'col': move[0]} for move in moves]
    return jsonify({'moves': moves})


@app.route('/api/chess/random-move', methods=['POST'])
def random_move():
    chess: Chess = session.get('board')
    color = chess.turn
    pieces = chess.board.get_pieces_of(color)
    moves = []
    src = None
    while len(moves) == 0:
        src = random.choice(pieces)
        moves = chess.board.get_legal_moves(src[0], src[1])
    dest = random.choice(moves)
    src = chess.board.convert_coord_inv(*src)
    dst = chess.board.convert_coord_inv(*dest)
    move = f"{src}-{dst}"
    ok = chess.move(move)
    response = {'board': chess.board.board, 'turn': chess.turn, 'isCheck': {'white': chess.board.is_check(1), 'black': chess.board.is_check(-1)}}
    if not ok:
        response['error'] = 'Invalid move'
        return jsonify(response), 400
    return jsonify(response), 200

@app.route('/api/chess/alphabeta-move', methods=['POST'])
def alphabeta_move():
    depth = request.json.get('depth', 3)
    chess: Chess = session.get('board')
    move = AlphaBeta.get_best_move(chess.board, depth, chess.turn)
    src = move[0]
    dest = move[1]
    src = chess.board.convert_coord_inv(*src)
    dst = chess.board.convert_coord_inv(*dest)
    move = f"{src}-{dst}"
    print(move)
    ok = chess.move(move)
    result = {'board': chess.board.board, 'turn': chess.turn, 'isCheck': {'white': chess.board.is_check(1), 'black': chess.board.is_check(-1)}}
    if not ok:
        result['error'] = 'Invalid move'
        return jsonify(result), 400
    return jsonify(result), 200
    
    
if __name__ == '__main__':
    app.run(debug=True)