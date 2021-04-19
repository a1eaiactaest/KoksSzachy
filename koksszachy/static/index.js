var $SCRIPT_ROOT = "" //"{{ request.script_root|tojson|safe }}";
var statusEl = $('#status'), fenEl = $('#fen'), pgnEl = $('#pgn');
var board;
var chess = new Chess()
var whiteSquareGrey = '#a9a9a9'
var blackSquareGrey = '#696969'

// move highlighting
// https://chessboardjs.com/examples#5003
var removeGreySquares = function(){
  $('#board .square-55d63').css('background', '');
}

var greySquare = function(square){
  var $square = $('#board .square-' + square);

  var background = whiteSquareGrey;
  if ($square.hasClass('black-3c85d')){
    background = blackSquareGrey;
  }

  $square.css('background', background);
}

var onDragStart = function(source, piece){
  if (chess.game_over() === true ||
      (chess.turn() === 'w' && piece.search(/^b/) !== -1) ||
      (chess.turn() === 'b' && piece.search(/^w/) !== -1)) {
    return false;
  }
};

var onDrop = function(source, target){
  removeGreySquares();
  
  var move = chess.move({
    from: source,
    to: target,
    promotion: 'q' // TODO: funkcja na wybor promocji
  });
  if (move === null) return 'snapback';

  updateStatus();
  getResponseMove();
  console.log(chess.fen());
};

var onMouseoverSquare = function(square, piece){
  var moves = chess.moves({
    square: square,
    verbose: true
  });

  if (moves.length === 0) return;

  greySquare(square);

  for (var i = 0; i < moves.length; i++){
    greySquare(moves[i].to);
  }
}

var onMouseoutSquare = function(square, piece){
  removeGreySquares();
}


// odpala sie za kazdym ruchem

var onSnapEnd = function(){
  board.position(chess.fen());
};

var updateStatus = function(){
  var status = '';

  var moveColor = 'White';
  if (chess.turn() === 'b'){
    moveColor = 'Black';
  }

  // check for checkmate
  if (chess.in_checkmate() === true){
    status = 'Game over, ' + moveColor + ' is in checkm8.';
  }

  // check for draw
  else if (chess.in_draw() === true){
    status = 'Game over, draw';
  }

  // nothing of above
  else{
    status = moveColor + ' to move';

    // check whether it's check
    if (chess.in_check() === true){
      status += ', ' + moveColor + ' is getting checked :0';
    }
  }

  setStatus(status);
  updatePGN();

  statusEl.html(status);
  fenEl.html(chess.fen());
  pgnEl.html(chess.pgn());
};

var config = {
  draggable: true,
  position: 'start',
  onDragStart: onDragStart,
  onDrop: onDrop,
  onMouseoutSquare: onMouseoutSquare,
  onMouseoverSquare: onMouseoverSquare,
  onSnapEnd: onSnapEnd
};

var getResponseMove = function(){
  var e = document.getElementById("sel1");
  var depth = e.options[e.selectedIndex].value;
  fen = chess.fen()
  $.get($SCRIPT_ROOT + "/info/" + depth + "/" + fen, function(data){
    chess.move(data, {sloppy:true}); // wykonaj ruch ściągnięty z url
    updateStatus();

    setTimeout(function(){ board.position(chess.fen()); }, 100);
  })
}

setTimeout(function(){
  board = ChessBoard('board', config);
}, 0);
  
setStatus = function(status){
  document.getElementById("status").innerHTML = status;
}

var takeBack = function(){
  chess.undo(); //dla bialyhc
  if (chess.turn() != 'w'){ //czarnych
    chess.undo();
  }
  board.position(chess.fen());
  updateStatus();
  console.log('Piece taken back');
}

var newGame = function(){
  chess.reset();
  board.start();
  updateStatus();
  console.log('New game');
  document.getElementById('pgnview').innerHTML = "";
}

var analysis = function(){
  var content = [chess.pgn()];  
	console.log(content);
  $.ajax({
    type: "POST",
    contentType: "application/json;charset=utf-8",
    url: "/analysis",
    traditional: "true",
    data: JSON.stringify({content}),
    dataType: "json"
  });
}

var acc = 1;
var num = 1;
var updatePGN = function(){
  document.getElementById('pgnview').innerHTML = chess.pgn({ max_width: 5, newline_char: '\n' });
}

