var $SCRIPT_ROOT = "/" //"{{ request.script_root|tojson|safe }}";
var statusEl = $('#status'), fenEl = $('#fen'), pgnEl = $('#pgn');
var board;
var chess = new Chess()

var onDragStart = function(source, piece, position, orientation){
  if (chess.game_over() === true ||
      (chess.turn() === 'w' && piece.search(/^b/) !== -1) ||
      (chess.turn() === 'b' && piece.search(/^w/) !== -1)) {
    return false;
  }
};

// odpala sie za kazdym ruchem
var onDrop = function(source, target){
  var move = chess.move({
    from: source,
    to: target,
    promotion: 'n' // TODO: funkcja na wybor promocji
  });
  if (move === null) return 'snapback';

  updateStatus();
  getResponseMove();
};

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
  getLastCapture();
  //createTable();
  //upadteScroll();

  statusEl.html(status);
  fenEl.html(chess.fen());
  pgnEl.html(chess.pgn());
};

var config = {
  draggable: true,
  position: 'start',
  onDragStart: onDragStart,
  onDrop: onDrop,
  onSnapEnd: onSnapEnd
};

var randomResponse = function(){
  fen = chess.fen()
  $.get($SCRIPT_ROOT + "/move/" + fen, function(data){
    chess.move(data, {sloppy:true});
    upadteStatus();
  })
}

var getResponseMove = function(){
  var e = document.getElementById("sel1");
  var depth = e.options[e.selectedIndex].value;
  fen = chess.fen()
  $.get($SCRIPT_ROOT + "/move/" + depth + "/" + fen, function(data){
    chess.move(data, {sloppy:true});
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
}

var newGame = function(){
  chess.reset();
  board.start();
  updateStatus();
}

var getCapturedPieces = function(){
  var history = chess.history({verbose:true});
  for (var i = 0; i < history.length; i++){
    if ("captured" in history[i]){
      console.log(history[i]["captured"]);
    }
  }  
}

var getLastCapture = function(){
  var history = chess.history({verbose:true});
  var index = history.length-1;

  if (history[index] != undefined && "captured" in history[index]){
    console.log(history[index]["captured"]);
  }
}

const fs = require('fs')
var getPGN = function(){
  let pgn = chess.pgn({max_width: 5, newline_char: '<br />'});
  fs.writeFile('pgn.txt', pgn, (err) => {
    if (err) throw err;
  })
}
