document.addEventListener('DOMContentLoaded', function() {
    const boardElement = document.getElementById('board');
    const initialBoard = [
        [2, 3, 4, 5, 6, 4, 3, 2],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-2, -3, -4, -5, -6, -4, -3, -2]
    ];

    const color = -1; // 1 for white, -1 for black
    var listMoves = null;
    var selectedSquare = null;

    const pieceImages = {  
        1: '/images/Pw.png',
        2: '/images/Rw.png',
        3: '/images/Knw.png',
        4: '/images/Bw.png',
        5: '/images/Qw.png',
        6: '/images/Kw.png',
        '-1': '/images/Pb.png',
        '-2': '/images/Rb.png',
        '-3': '/images/Knb.png',
        '-4': '/images/Bb.png',
        '-5': '/images/Qb.png',
        '-6': '/images/Kb.png'
    };

    const overlay = document.getElementById('overlay');
    
    function displayBoard(board) {
        boardElement.innerHTML = '';
        const rows = color === 1 ? [...Array(8).keys()].reverse() : [...Array(8).keys()];
        for (let row of rows) {
            for (let col = 0; col < 8; col++) {
            const square = document.createElement('div');
            square.classList.add('square');
            square.classList.add((row + col) % 2 === 0 ? 'white' : 'black');
            square.dataset.row = color === 1 ? 7 - row : row;
            square.dataset.col = col;
            square.addEventListener('click', function() {
                const p = board[row][col];
                const p_color = p / Math.abs(p);
                
                if (p_color === color) {
                    if (selectedSquare) {
                        selectedSquare.classList.remove('selected');
                        if (selectedSquare === square) {
                            selectedSquare = null;
                            return;
                        }
                    }
                    selectedSquare = square;
                    square.classList.add('selected');
                    requestListMoves(row, col);
                }
            });

            // Number on the first column
            if (col === 0) {
                const number = document.createElement('div');
                number.classList.add('number');
                number.textContent = color === -1 ? 8 - row : row + 1;
                square.appendChild(number);

            }
            // Letter on the last row
            console.log(row);
            if (row === (color === -1 ? 7 : 0)) {
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

    displayBoard(initialBoard);
    overlay.style.display = 'block';


    document.getElementById('new-game-button').addEventListener('click', function() {
        fetch('/api/chess/new')
        .then(response => response.json())
        .then(data => {
            overlay.style.display = 'none';
            displayBoard(initialBoard); // Reset the board to the starting position
        });
    });

    function requestListMoves(row, col) {
        fetch(`/api/chess/moves?row=${row}&col=${col}`)
        .then(response => response.json())
        .then(data => {
            listMoves = data;
            console.log(listMoves);
        });
    }


});