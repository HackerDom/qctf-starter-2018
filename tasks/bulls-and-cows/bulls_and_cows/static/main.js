function renderShortForm(props) {
    if (props.additionalFields === undefined) {
        props.additionalFields = '';
    }

    var textInput = '';
    var buttonStyleAttribute = '';
    if (props.name !== undefined) {
        textInput = (
            '<input type="text" name="' + props.name +
            '" placeholder="' + props.placeholder + '" class="form-control">');
        if (props.multiline) {
            textInput = '<div class="mb-2">' + textInput + '</div>'
        }
        if (!props.multiline) {
            buttonStyleAttribute = (
                ' style="border-top-left-radius: 0; border-bottom-left-radius: 0"');
        }
    }

    var idAttribute = '';
    if (props.id !== undefined) {
        idAttribute = ' id="' + props.id + '"';
    }

    var classAttribute = '';
    if (props.class !== undefined) {
        classAttribute = ' class="' + props.class + '"';
    }

    var submitInput = '';
    if (props.submitValue !== undefined) {
        submitInput = (
            '<span class="input-group-btn">' +
            '   <input type="submit" value="' + props.submitValue +
                            '"' + buttonStyleAttribute + ' class="btn btn-secondary">' +
            '</span>'
        );
    }

    return (
        '<form' + idAttribute + classAttribute + ' action="' + props.action + '" method="' + props.method + '">' +
        '   <div class="input-group' + (props.inlineBlock ? 'd-inline-block' : '') + '">' +
                textInput +
                props.additionalFields +
                submitInput +
        '   </div>' +
        '</form>'
    );
}

function renderMove(move) {
    return (
        '<div class="col-md-4 pl-0">' +
        '   <h4>' + move.guess + '</h4>' +
        '</div>' +
        '<div class="col-md-8">' +
        '   <h4>' + move.bulls + 'Б ' + move.cows + 'К' + '</h4>' +
        '</div>'
    );
}

function renderMoves(moves) {
    return (
        '<div class="container">' +
            moves.map(function(move) {
                return (
                    '<div class="row">' +
                        renderMove(move) +
                    '</div>'
                );
            }).join('') +
        '</div>'
    );
}

function renderNewMoveForm(game) {
    var lastMove = game.moves[game.moves.length - 1];
    var lastMoveNumber = lastMove === undefined ? 0 : lastMove.number;
    return renderShortForm({
        id: 'newMoveForm',
        class: 'mb-1 mt-1 mr-2',
        action: '/move',
        method: 'POST',
        name: 'guess',
        placeholder: 'Новая попытка',
        additionalFields: (
            '<input type="hidden" name="game_id" value="' + game.id + '">' +
            '<input type="hidden" name="number" value="' + (lastMoveNumber + 1) + '">')
    });
}

function renderEndGameForm(game) {
    return renderShortForm({
        id: 'endGameForm',
        class: 'mb-2 d-inline-block',
        action: '/end_game',
        method: 'POST',
        submitValue: 'Сдаться',
        additionalFields: '<input type="hidden" name="game_id" value="' + game.id + '">'
    });
}

function renderGameProgress(game) {
    return (
        '<div class="container">' +
        '   <div class="card"><div class="card-header p-0 pt-1">' +
        '       <div class="row">' +
        '           <div class="col-md-5 text-right">' +
        '               <h4>Казино загадало:</h4>' +
        '           </div>' +
        '           <div class="col-md-7">' +
        '               <h4>' + (game.secret_number || '????') + '</h4>' +
        '           </div>' +
        '       </div>' +
        '   </div>' +
        '   <div class="card-body py-2 px-0">' +
        '       <div class="row">' +
        '           <div class="col-md-5 text-right">' +
        '               <h4>Ваши попытки:</h4>' +
        '           </div>' +
        '           <div class="col-md-7">' +
                        renderMoves(game.moves) +
                        (game.has_ended ?
                            '<h4>Игра закончена</h4>' :
                            renderNewMoveForm(game)) +
        '           </div>' +
        '       </div>' +
        '   </div>' +
        '</div>'
    );
}

function renderNewGameForm() {
    return renderShortForm({
        id: 'newGameForm',
        class: 'mb-2 text-center',
        inlineBlock: true,
        multiline: true,
        action: '/games',
        method: 'POST',
        name: 'bet',
        placeholder: 'Ставка',
        submitValue: 'Начать игру'
    });
}

function renderGameMeta(game) {
    if (game === undefined || game.has_ended) {
        return renderNewGameForm();
    } else {
        return (
            '<div class="card mb-2 d-inline-block">' +
            '   <h6 class="card-header">Ставка: ' + game.bet + '</h6>' +
            '</div>' +
            renderEndGameForm(game)
        );
    }
}

function renderMainSection(lastGame) {
    var gameMetaHtml = renderGameMeta(lastGame);
    var gameProgressHtml = '';
    if (lastGame !== undefined) {
        gameProgressHtml = renderGameProgress(lastGame);
    }

    return (
        '<div class="container">' +
        '   <div class="row">' +
        '       <div class="col-md-3 text-center">' +
                    gameMetaHtml +
        '       </div>' +
        '       <div class="col-md-9">' +
                    gameProgressHtml +
        '       </div>' +
        '   </div>' +
        '</div>'
    );
}

function renderDepositMoneyForm() {
    return renderShortForm({
        id: 'depositMoneyForm',
        class: 'mb-2 mr-3',
        action: '/deposit',
        method: 'POST',
        name: 'amount',
        placeholder: 'Количество',
        submitValue: 'Внести деньги'
    });
}

function renderWithdrawMoneyForm() {
    return renderShortForm({
        id: 'withdrawMoneyForm',
        class: 'mb-2 mr-3',
        action: '/withdraw',
        method: 'POST',
        name: 'amount',
        placeholder: 'Количество',
        submitValue: 'Вывести деньги'
    });
}

function renderCodes(codes) {
    if (codes.length === 0) {
        return '';
    }
    return (
        '<p class="mb-0 ml-2">' +
        '   Деньги успешно выведены со счёта. Чтобы получить их,' +
        '   предъявите следующий код в ближайшем филиале нашего казино: ' +
            codes.map(function(code) {
                return '<strong>' + code + '</strong>';
            }).join(', ') +
        '</p>'
    );
}

function renderBalance(me) {
    return (
        '<p class="mb-2 ml-2">На счёте: <strong>' + me.balance + '</strong></p>' +
        renderDepositMoneyForm() +
        renderWithdrawMoneyForm() +
        renderCodes(me.codes)
    );
}

function renderNumberOfMoves(number) {
    var ending;
    if (11 <= number % 100 && number % 100 < 14) {
        ending = 'ок';
    } else if (number % 10 == 1) {
        ending = 'ка';
    } else if (2 <= number % 10 && number % 10 <= 4) {
        ending = 'ки';
    } else {
        ending = 'ок';
    }
    return number + ' попыт' + ending;
}

function colorMoneyDelta(number) {
    if (number > 0) {
        return '<span class="green">+' + number + '</span>';
    } else if (number < 0) {
        return '<span class="red">' + number + '</span>';
    } else {
        return number;
    }
}

function hasGivenUp(game) {
    var result = true;
    game.moves.forEach(function(move) {
        if (move.bulls === 4)
            result = false;
    });
    return result;
}

function payoffMultiplier(numberOfMoves) {
    if (numberOfMoves >= 9) {
        return 0;
    } else if (numberOfMoves === 8) {
        return 0.25;
    } else if (numberOfMoves === 7) {
        return 0.5;
    } else if (numberOfMoves === 6) {
        return 2;
    } else {
        return 3;
    }
}

function renderMoneyDelta(game) {
    var multiplier = -1 + (hasGivenUp(game) ? 0 : payoffMultiplier(game.moves.length));
    var moneyDelta = Math.floor(multiplier * game.bet);
    return '<strong>' + colorMoneyDelta(moneyDelta) + '</strong>';
}

function renderGameSummaries(games) {
    if (games.length === 0) {
        return '<p class="mb-0">Вы пока не сыграли ни одной игры</p>';
    }

    var reversedGames = games.slice();
    reversedGames.reverse();
    return (
        '<div class="d-flex">' +
        '   <div>' +
                reversedGames.map(function(game) {
                    if (!game.has_ended) {
                        return '';
                    }
                    return (
                        '<p class="ml-2 mb-1">' +
                            '<strong>' + game.secret_number + '</strong>: ' +
                            renderNumberOfMoves(game.moves.length) + ',' +
                        '</p>'
                    )
                }).join('') +
        '   </div>' +
        '   <div>' +
                reversedGames.map(function(game) {
                    if (!game.has_ended) {
                        return '';
                    }
                    return (
                        '<p class="ml-2 mb-1">' +
                            renderMoneyDelta(game) +
                            (hasGivenUp(game) ? ' (сдался)' : '') +
                        '</p>'
                    )
                }).join('') +
        '   </div>' +
        '</div>'
    );
}


function displayModal(content) {
    $('#modal .modal-body').html(content);
    $('#modal').modal();
}

function modalCallback(content) {
    return function(e) {
        e.preventDefault();
        displayModal(content);
    };
}

function updateLastGame(lastGame) {
    $('#mainSection').html(renderMainSection(lastGame));
    subscribeToForm($('#newMoveForm'));
    subscribeToForm($('#endGameForm'));
    subscribeToForm($('#newGameForm'));
}

function updateAll(me) {
    $('#balance').html(renderBalance(me));
    subscribeToForm($('#withdrawMoneyForm'));
    $('#depositMoneyForm').submit(modalCallback(
        '<p>Функция ввода денег находится в разработке.</p>' +
        '<p class="mb-0">Приносим извинения за доставленные неудобства.</p>'
    ));
    $('#gameSummaries').html(renderGameSummaries(me.games));
    var lastGame = me.games[me.games.length - 1];
    updateLastGame(lastGame);
}

var errorMessageByFieldName = {
    bet: (
        '<p>Ставка должна быть целым числом от 1 до 100000.</p>' +
        '<p class="mb-0">Ставка не может превышать число денег на счёте.</p>'
    ),
    guess: (
        '<p class="mb-0">Некорректная попытка. Необходимо ввести четыре различные цифры.</p>'
    ),
    amount: (
        '<p class="mb-0">Вывести можно целую сумму не меньше <strong>1000000</strong> и не больше суммы на счёте.</p>'
    ),
    game_id: (
        '<p class="mb-0">Игра не найдена. Попробуйте перезагрузить страницу.</p>'
    ),
    number: (
        '<p class="mb-0">Не удалось отправить попытку. Попробуйте перезагрузить страницу.</p>'
    )
};

function dispatchStateChange() {
    if (this.readyState === 4) {
        var response = JSON.parse(this.responseText);

        if (this.status !== 200) {
            if (response.errors.length !== 0) {
                console.log(response.errors);
                var fieldName = Object.keys(response.errors)[0];
                var errorMessage = errorMessageByFieldName[fieldName];
                if (errorMessage !== undefined) {
                    displayModal(errorMessage);
                }
            }
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

function subscribeToForm(form) {
    if (form !== null) {
        form.submit(function (e) {
            var data = new FormData(form[0]);
            fetch(form.attr('method'), form.attr('action'), data);
            e.preventDefault();
        });
    }
}


fetch('GET', '/me');
$('.game-disabled').click(modalCallback(
    'Выбранная игра ещё в разработке. Поиграйте пока в «Быки и коровы»'
));
