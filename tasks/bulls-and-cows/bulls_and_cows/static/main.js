function getElement(id) {
    return document.getElementById(id);
}

function renderMove(move) {
    return (
        '<div class="move">' +
        '   Guess: ' + move.guess + ', result: ' + move.bulls + ' ' + move.cows +
        '</div>'
    );
}

function renderMoves(moves) {
    return (
        '<ul class="moves">' +
        moves.map(function(move) {
            return (
                '<li>' +
                    renderMove(move) +
                '</li>'
            )
        }).join('') +
        '</ul>'
    );
}

function renderNewMoveForm(game) {
    var lastMove = game.moves[game.moves.length - 1];
    var lastMoveNumber = lastMove === undefined ? 0 : lastMove.number;
    return (
        '<form action="/move" method="POST">' +
        '   <input type="hidden" name="game_id" value="' + game.id + '">' +
        '   <input type="hidden" name="number" value="' + (lastMoveNumber + 1) + '">' +
        '   <input type="text" name="guess" placeholder="Guess">' +
        '   <input type="submit" value="Make a guess">' +
        '</form>'
    );
}

function renderEndGameForm(game) {
    return (
        '<form action="/end_game" method="POST">' +
        '   <input type="hidden" name="game_id" value="' + game.id + '">' +
        '   <input type="submit" value="End this game">' +
        '</form>'
    );
}

function renderLastGame(game) {
    return (
        '<div class="game">' +
        '   Bet: ' + game.bet +
            renderMoves(game.moves) +
            (game.has_ended ?
                'The game has ended' :
                renderNewMoveForm(game) + renderEndGameForm(game)) +
        '</div>'
    );
}

function renderNewGameForm() {
    return (
        '<form action="/games" method="POST">' +
        '   <input type="text" name="bet" placeholder="Bet">' +
        '   <input type="submit" value="Start game">' +
        '</form>'
    );
}

function renderMainSection(me) {
    var result = [];
    var lastGame = me.games[me.games.length - 1];
    if (lastGame === undefined || lastGame.has_ended) {
        result.push(renderNewGameForm());
    }
    if (lastGame !== undefined) {
        result.push(renderLastGame(lastGame));
    }
    return result.join('');
}

function renderAccountInfo(me) {
    return 'Balance: ' + me.balance;
}

function renderGameSummary(game) {
    return 'Bet: ' + game.bet + ', number of moves: ' + game.moves.length + (game.has_ended ? '' : ' (active)');
}

function renderGameSummaries(games) {
    return (
        '<p>Games:</p>' +
        '<div class="game_summaries"><ul>' +
        games.map(function(game) {
            return (
                '<li>' +
                    renderGameSummary(game) +
                '</li>'
            )
        }).join('') +
        '</ul></div>'
    );
}

function renderAll(me) {
    getElement('accountInfo').innerHTML = renderAccountInfo(me);
    getElement('gameSummaries').innerHTML = renderGameSummaries(me.games);
    getElement('mainSection').innerHTML = renderMainSection(me);
}


function fetchAll() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            var me = JSON.parse(this.responseText);
            renderAll.call(undefined, me);
        }
    };
    xhttp.open('GET', '/me', true);
    xhttp.send();
}


fetchAll();
