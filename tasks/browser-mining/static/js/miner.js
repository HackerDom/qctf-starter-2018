'use strict';

function mine() {
    STOP = false;
    checkResult(0);
}

function mineStop() {
    STOP = true;
}

function stopCheck() {
    if (STOP) {
        endFront();
    }
    return STOP;
}

function startFront() {
    $('.loading-cubes').show();
    $('#mining-start').hide();
    $('#mining-stop').show();
}

function endFront() {
    $('.loading-cubes').hide();
    $('#mining-stop').hide();
    $('#mining-start').show();
}

function checkResult(result) {
    const body = JSON.stringify({
        result: result
    });
    fetch('/task', {method: 'POST', credentials: 'include', body: body})
        .then(resp => {
            if (!resp.ok) {
                throw new Error(resp.statusText);
            }
            return resp.json();
        })
        .then(resp => {
            if (result !== 0) {
                $('#success').show().fadeOut(2000);
            }
            $('#balance').html(Number(resp['balance']));
            if (stopCheck()) {
                return;
            }
            const miner = new PrimeFinder(resp['task']);
            startFront();
            setTimeout(() => miner.isPrime());
        })
        .catch(showError);
}

function showError(error) {
    $('.error').html(`Произошла ошибка: ${error}`).show().fadeOut(2000);
}

class PrimeFinder {
    constructor(oldPrime) {
        this.currentNumber = oldPrime + 1;
        this.currentDivider = 2;
    }

    isDivisible() {
        return this.currentNumber % this.currentDivider === 0;
    }

    isPrime() {
        if (this.isDivisible()) {
            this.currentNumber++;
            this.currentDivider = 2;
            if (stopCheck()) {
                return;
            }
            setTimeout(() => this.findNextPrime());
        }
        else if (this.currentDivider > Math.sqrt(this.currentNumber) + 1) {
            $('.loading-cubes').hide();
            checkResult(this.currentNumber);
            return true;
        }
        else {
            this.currentDivider++;
            if (stopCheck()) {
                return;
            }
            setTimeout(() => this.isPrime(), 0);
        }
    }

    findNextPrime() {
        if (this.isPrime()) {
            return true;
        }
        else if (this.currentNumber > 100) {
            return false;
        }
    }

}

$(document).ready(() => {
    $('.loading-cubes').hide();
    $('#success').hide();
});
let STOP = false;