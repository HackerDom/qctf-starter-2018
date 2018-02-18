'use strict';

function mine() {
    checkResult(0);
}

function checkResult(result){
    const body = JSON.stringify({
        result: result
    });
    fetch('/task', {method: 'POST', credentials: 'include', body: body})
    .then(resp=>{
        if (!resp.ok){
            throw new Error(resp.statusText);
        }
        return resp.json();
    })
    .then(resp => {
        $('#success').show().fadeOut(2000);
        $('#balance').html(Number(resp['balance']));

        const miner = new PrimeFinder(resp['task']);
        $('.loading-cubes').show();
        miner.isPrime();
    })
    .catch(showError);
}

function showError(error){
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
            setTimeout(() => this.findNextPrime());
        }
        else if (this.currentDivider > Math.sqrt(this.currentNumber) + 1) {
            $('.loading-cubes').hide();
            checkResult(this.currentNumber);
            return true;
        }
        else {
            this.currentDivider++;
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