function makeReadable(number) {
    number = number.toString();
    var result = '';
    for (var i = 0; i < number.length; i++) {
        if (i >= 1 && (number.length - i) % 3 === 0)
            result += ' ';
        result += number[i];
    }
    return result;
}

$(function () {
    $('#credits-link').click(function () {
        event.preventDefault();
        $('#credit-page').show();
        $('#unavailable-page').hide();
    });
    $('#deposits-link, #support-link').click(function () {
        event.preventDefault();
        $('#credit-page').hide();
        $('#unavailable-page').show();
    });

    $('.amount-input')
        .keypress(function (event) {
            if (event.which !== 0 && event.which !== 8 &&
                !('0'.charCodeAt(0) <= event.which && event.which <= '9'.charCodeAt(0)))
                event.preventDefault();
        })
        .keyup(function (event) {
            var selStartOffset = $(this).val().length - $(this).prop('selectionStart');
            var selEndOffset = $(this).val().length - $(this).prop('selectionEnd');

            var value = makeReadable($(this).val().replace(/ /g, ''));
            $(this)
                .val(value)
                .prop('selectionStart', value.length - selStartOffset)
                .prop('selectionEnd', value.length - selEndOffset);
        });

    var FINAL_STEP = 5;
    var step = 1;

    function validateForm() {
        if (step === 1) {
            var creditAmountInput = $('#credit_amount');
            var creditAmount = parseInt(creditAmountInput.val().replace(/ /g, ''));
            if (1e5 <= creditAmount && creditAmount <= 3e6)
                creditAmountInput.removeClass('is-invalid');
            else {
                creditAmountInput.addClass('is-invalid');
                return false;
            }
        }
        return true;
    }

    function submitForm() {
        $('#result-loading').show();
        $('#result-negative, #result-positive, #result-error').hide();

        var form = $('#credit-page').find('form');
        form.find('.amount-input').each(function (_, item) {
            var el = $(item);
            el.val(el.val().replace(/ /g, ''));
        });

        $.post('/api/submit_credit_form', form.serialize())
            .done(function (response) {
                $('#result-loading').hide();
                if (response.result === 'positive') {
                    $('#result-positive').show();
                    $('#interest-rate').html(response.interest_rate + '%');
                    $('#monthly-payment').html(makeReadable(response.monthly_payment));
                    $('#bank-code').html(response.bank_code);
                } else
                if (response.result === 'negative') {
                    $('#result-negative').show();
                } else
                    $('#result-error').show();
            })
            .fail(function() {
                $('#result-loading').hide();
                $('#result-error').show();
            });

        form.find('.amount-input').each(function (_, item) {
            var el = $(item);
            el.val(makeReadable(el.val()));
        });
    }

    function changeStep(value) {
        if (!validateForm())
            return;
        if (value === FINAL_STEP)
            submitForm();

        $('#step' + step).hide();
        step = value;
        $('#step' + step).show();

        if (step === 1)
            $('#prev-page-btn').hide();
        else
            $('#prev-page-btn').show();
        if (step === FINAL_STEP)
            $('#next-page-btn').hide();
        else
            $('#next-page-btn').show();
    }

    $('#prev-page-btn').click(function (event) {
        event.preventDefault();
        changeStep(step - 1);
    });
    $('#next-page-btn').click(function (event) {
        event.preventDefault();
        changeStep(step + 1);
    });

    function changeHandler(list, select) {
        var newRow = list.find('.row:last-child').clone(true);
        list.append(newRow);
        newRow.find('.amount-input').val('0');

        select.off('change');
    }

    $('.extending-list').each(function (_, item) {
        var list = $(item);
        var select = list.find('.row:last-child select');
        select.change(function () {
            return changeHandler(list, $(this));
        });
    });
});
