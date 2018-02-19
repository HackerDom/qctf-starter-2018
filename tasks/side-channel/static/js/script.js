function initCanvas(canvas) {
    canvas[0].width = canvas.width();
    canvas[0].height = canvas.height();

    var context = canvas[0].getContext('2d');
    context.strokeStyle = '#df4b26';
    context.lineJoin = 'round';
    context.lineWidth = 20;
    return context;
}

function redraw(context, strokes, start) {
    for (var i = start; i < strokes.length; i++) {
        var stroke = strokes[i];
        context.beginPath();

        if (stroke.dragged) {
            var prevStroke = strokes[i - 1];
            context.moveTo(prevStroke.x, prevStroke.y);
        } else
            context.moveTo(stroke.x - 1, stroke.y);
        context.lineTo(stroke.x, stroke.y);

        context.closePath();
        context.stroke();
    }
}

function submitImage(canvas) {
    $('#status-text').text('Проверка пароля...');
    canvas[0].toBlob(function (blob) {
        var formData = new FormData();
        formData.append('image', blob);
        $.ajax({
            type: 'POST',
            url: '/api/submit_image',
            data: formData,
            processData: false,
            contentType: false
        })
            .done(function (response) {
                $('#status-text').html(response.status);
            })
            .fail(function () {
                $('#status-text').text('Не удалось подключиться к серверу');
            });
    });
}

$(function () {
    var canvas = $('#main-canvas');
    var context = initCanvas(canvas);
    var strokes = [];
    $(window).resize(function () {
        context = initCanvas(canvas);
        redraw(context, strokes, 0);
    });

    var painting = false;
    canvas.mousedown(function (e) {
        strokes.push({
            x: e.pageX - this.offsetLeft,
            y: e.pageY - this.offsetTop,
            dragged: false
        });
        redraw(context, strokes, strokes.length - 1);
        painting = true;
    });
    canvas.mousemove(function (e) {
        if (painting) {
            strokes.push({
                x: e.pageX - this.offsetLeft,
                y: e.pageY - this.offsetTop,
                dragged: true
            });
            redraw(context, strokes, strokes.length - 1);
        }
    });

    function stopPainting() {
        painting = false;
    }

    canvas.mouseup(stopPainting);
    canvas.mouseleave(stopPainting);

    $('#clear-btn').click(function () {
        context.clearRect(0, 0, context.canvas.width, context.canvas.height);
        strokes = [];
    });
    $('#enter-btn').click(function () {
        submitImage(canvas);
    });
});
