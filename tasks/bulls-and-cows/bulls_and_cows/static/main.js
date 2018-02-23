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
        '<form id="newMoveForm" action="/move" method="POST">' +
        '   <input type="hidden" name="game_id" value="' + game.id + '">' +
        '   <input type="hidden" name="number" value="' + (lastMoveNumber + 1) + '">' +
        '   <input type="text" name="guess" placeholder="Guess">' +
        '   <input type="submit" value="Make a guess">' +
        '</form>'
    );
}

function renderEndGameForm(game) {
    return (
        '<form id="endGameForm" action="/end_game" method="POST">' +
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
        '<form id="newGameForm" action="/games" method="POST">' +
        '   <input type="text" name="bet" placeholder="Bet">' +
        '   <input type="submit" value="Start game">' +
        '</form>'
    );
}

function renderMainSection(lastGame) {
    var result = [];
    if (lastGame === undefined || lastGame.has_ended) {
        result.push(renderNewGameForm());
    }
    if (lastGame !== undefined) {
        result.push(renderLastGame(lastGame));
    }
    return result.join('');
}

function renderWithdrawMoneyForm() {
    return (
        '<form id="withdrawMoneyForm" action="/withdraw" method="POST">' +
        '   <input type="text" name="amount" placeholder="Amount">' +
        '   <input type="submit" value="Withdraw">' +
        '</form>'
    );
}

function renderCodes(codes) {
    return 'Your codes: ' + codes.join(', ');
}

function renderAccount(me) {
    return (
        'Balance: ' + me.balance +
        renderWithdrawMoneyForm() +
        renderCodes(me.codes)
    );
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

function updateLastGame(lastGame) {
    getElement('mainSection').innerHTML = renderMainSection(lastGame);
    subscribeToForm('newMoveForm');
    subscribeToForm('endGameForm');
    subscribeToForm('newGameForm');
}

function updateAll(me) {
    getElement('account').innerHTML = renderAccount(me);
    subscribeToForm('withdrawMoneyForm');
    getElement('gameSummaries').innerHTML = renderGameSummaries(me.games);
    var lastGame = me.games[me.games.length - 1];
    updateLastGame(lastGame);
}

function dispatchStateChange() {
    if (this.readyState === 4 && this.status === 200) {
        var response = JSON.parse(this.responseText);
        if (response.errors.length !== 0) {
            console.log(response.errors);
            return;
        }

        if ('me' in response) {
            updateAll.call(null, response.me);
        } else if ('game' in response) {
            updateLastGame.call(null, response.game);
        }
    }
}

function fetch(method, address, data) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = dispatchStateChange;
    xhttp.open(method, address, true);
    xhttp.send(data);
}

function subscribeToForm(formId) {
    var form = getElement(formId);
    if (form !== null) {
        form.addEventListener('submit', function (e) {
            var data = new FormData(form);
            fetch(form.method, form.action, data);
            e.preventDefault();
        })
    }
}


fetch('GET', '/me');
