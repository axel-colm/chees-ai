document.addEventListener('DOMContentLoaded', function () {
    const boardElement = document.getElementById('board');
    const initialBoard = [
        [-2, -3, -4, -5, -6, -4, -3, -2],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [2, 3, 4, 5, 6, 4, 3, 2]
    ];

    const color = -1; // -1 for white, 1 for black
    var listMoves = null;
    var selectedSquare = null;
    var board = initialBoard;
    var turn = -1;

    const pieceImages = {
        '-1': '/images/Pw.png',
        '-2': '/images/Rw.png',
        '-3': '/images/Knw.png',
        '-4': '/images/Bw.png',
        '-5': '/images/Qw.png',
        '-6': '/images/Kw.png',
        '1': '/images/Pb.png',
        '2': '/images/Rb.png',
        '3': '/images/Knb.png',
        '4': '/images/Bb.png',
        '5': '/images/Qb.png',
        '6': '/images/Kb.png'
    };

    const overlay = document.getElementById('overlay');
    displayBoard();
    overlay.style.display = 'flex';

    function displayBoard() {
        boardElement.innerHTML = '';
        const rows = color === -1 ? [...Array(8).keys()].reverse() : [...Array(8).keys()];
        for (let row of rows) {
            for (let col = 0; col < 8; col++) {
                const square = document.createElement('div');
                square.classList.add('square');
                square.classList.add((row + col) % 2 === 0 ? 'white' : 'black');
                square.dataset.row = color === -1 ? 7 - row : row;
                square.dataset.col = col;
                square.addEventListener('click', () => onCaseClick(row, col));
                // Number on the first column
                if (col === 0) {
                    const number = document.createElement('div');
                    number.classList.add('number');
                    number.textContent = color === 1 ? 8 - row : row + 1;
                    square.appendChild(number);
                }

                // Letter on the last row
                if (row === (color === 1 ? 7 : 0)) {
                    const letter = document.createElement('div');
                    letter.classList.add('letter');
                    letter.textContent = String.fromCharCode(97 + col);
                    square.appendChild(letter);
                }

                const piece = board[row][col];

                // if the piece is user piece
                const piece_color = piece / Math.abs(piece);
                if (piece_color === color) {
                    square.classList.add('user-piece');
                }
                if (piece !== 0) {
                    const img = document.createElement('img');
                    img.src = pieceImages[piece];
                    img.alt = piece;
                    img.classList.add('piece');
                    square.appendChild(img);
                }
                boardElement.appendChild(square);
            }


        }
        overlay.style.display = 'none';

    }

    function onCaseClick(row, col) {
        const p = board[row][col];
        const p_color = p / Math.abs(p);
        const square = boardElement.querySelector(`.square[data-row='${color === -1 ? 7 - row : row}'][data-col='${col}']`);

        if (selectedSquare) {
            const selectedRow = color === -1 ? 7 - parseInt(selectedSquare.dataset.row) : parseInt(selectedSquare.dataset.row);
            const selectedCol = parseInt(selectedSquare.dataset.col);
            const isMoveValid = listMoves && listMoves.some(move => move.row === row && move.col === col);

            if (isMoveValid) {
                movePiece(selectedRow, selectedCol, row, col);
                setListMoves(null);
                displayBoard();
                return;
            } else {
                selectedSquare.classList.remove('selected');
                selectedSquare = null;
                setListMoves(null);
            }
        }

        if (p_color === color) {
            selectedSquare = square;
            square.classList.add('selected');
            requestListMoves(row, col);
        }
    }


    function setListMoves(moves) {
        // Remove move points
        if (listMoves) {
            const movePoints = document.querySelectorAll('.move-point');
            movePoints.forEach(point => point.remove());
            const attackPoints = document.querySelectorAll('.attack-point');
            attackPoints.forEach(point => point.remove());
        }
        listMoves = moves;
        // Display move points
        if (listMoves && selectedSquare && turn === color) {
            listMoves.forEach(move => {
                const moveSquare = boardElement.querySelector(`.square[data-row='${color === -1 ? 7 - move.row : move.row}'][data-col='${move.col}']`);

                if (moveSquare) {
                    // si il y a une piece sur la case, on ajoute un cercle rouge
                    const point = document.createElement('div');
                    if (board[move.row][move.col] !== 0) {
                        point.classList.add('attack-point');
                    } else {
                        point.classList.add('move-point');
                    }
                    moveSquare.appendChild(point);
                }
            });
        }
    }

    function requestListMoves(row, col) {
        fetch(`/api/chess/moves?row=${row}&col=${col}`)
            .then(response => response.json())
            .then(data => {
                setListMoves(data.moves);
            });
    }


    document.getElementById('new-game-button').addEventListener('click', function () {
        fetch('/api/chess/new')
            .then(response => response.json())
            .then(data => {
                overlay.style.display = 'none';
                displayBoard(initialBoard); // Reset the board to the starting position
            });
    });


    function movePiece(fromRow, fromCol, toRow, toCol) {
        // make a post on /api/chess/move
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8'];
        from = letters[fromCol] + numbers[fromRow];
        to = letters[toCol] + numbers[toRow];

        fetch('/api/chess/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                move: `${from}-${to}`
            })
        })
            .then(response => response.json())
            .then(data => {
                board = data.board;
                turn = data.turn;
                displayBoard();
                setCheck(data.isCheck);
                if (turn !== color) {
                    requestAiMove();
                }
            });
    }

    function setCheck(isCheck) {
        let blackKing = null;
        let whiteKing = null;

        for (let row = 0; row < 8; row++) {
            for (let col = 0; col < 8; col++) {
                if (board[row][col] === 6) {
                    whiteKing = { row, col };
                } else if (board[row][col] === -6) {
                    blackKing = { row, col };
                }
            }
        }

        const whiteKingSquare = boardElement.querySelector(`.square[data-row='${color === -1 ? 7 - whiteKing.row : whiteKing.row}'][data-col='${whiteKing.col}']`);
        const blackKingSquare = boardElement.querySelector(`.square[data-row='${color === -1 ? 7 - blackKing.row : blackKing.row}'][data-col='${blackKing.col}']`);
        whiteKingSquare.classList.remove('ischeck');
        blackKingSquare.classList.remove('ischeck');
        if (isCheck.black) {
            blackKingSquare.classList.add('ischeck');
        }
        if (isCheck.white) {
            whiteKingSquare.classList.add('ischeck');
        }
    }

    function requestAiMove() {
        fetch('/api/chess/alphabeta-move', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({ depth: 3 })
        })
            .then(response => response.json())
            .then(data => {
            board = data.board;
            turn = data.turn;
            displayBoard();
            setCheck(data.isCheck);
            });
    }




});