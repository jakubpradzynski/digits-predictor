$(document).ready(function () {

    var canvasWidth = '560';
    var canvasHeight = '560';
    var canvasDiv = document.getElementById('canvasDiv');
    canvas = document.createElement('canvas');
    canvas.setAttribute('width', canvasWidth);
    canvas.setAttribute('height', canvasHeight);
    canvas.setAttribute('id', 'canvas');
    canvasDiv.appendChild(canvas);
    if (typeof G_vmlCanvasManager != 'undefined') {
        canvas = G_vmlCanvasManager.initElement(canvas);
    }
    context = canvas.getContext("2d");
    context.fillStyle = 'black';
    context.fillRect(0, 0, canvas.width, canvas.height);

    $('#canvas').mousedown(function (e) {
        var mouseX = e.pageX - this.offsetLeft;
        var mouseY = e.pageY - this.offsetTop;

        paint = true;
        addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop);
        redraw();
    });

    $('#canvas').mousemove(function (e) {
        if (paint) {
            addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop, true);
            redraw();
        }
    });

    $('#canvas').mouseup(function (e) {
        paint = false;
    });

    $('#canvas').mouseleave(function (e) {
        paint = false;
    });

    var clickX = [];
    var clickY = [];
    var clickDrag = [];
    var paint;

    function addClick(x, y, dragging) {
        clickX.push(x);
        clickY.push(y);
        clickDrag.push(dragging);
    }

    function redraw() {
        context.clearRect(0, 0, context.canvas.width, context.canvas.height); // Clears the canvas
        context.fillRect(0, 0, canvas.width, canvas.height);

        context.strokeStyle = "#FFFFFF";
        context.lineJoin = "round";
        context.lineWidth = 15;

        for (var i = 0; i < clickX.length; i++) {
            context.beginPath();
            if (clickDrag[i] && i) {
                context.moveTo(clickX[i - 1], clickY[i - 1]);
            } else {
                context.moveTo(clickX[i] - 1, clickY[i]);
            }
            context.lineTo(clickX[i], clickY[i]);
            context.closePath();
            context.stroke();
        }
    }

    var button = document.getElementById('btn-predict');
    button.addEventListener('click', function (e) {
        var spinner = document.getElementById("spinner");
        var body = document.getElementById("body");
        var container = document.getElementById("container");
        spinner.style.display = "block";
        body.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
        container.style.opacity = 0.1;
        var dataURL = canvas.toDataURL('image/png');
        var requestUrl = window.location.origin + '/predict';
        $.post(requestUrl, dataURL, function (data, status) {
            var html = "<table class='table-fill'>";
            html += "<thead>\n" +
                "<tr>\n" +
                "<th class=\"text-left\">Photo</th>\n" +
                "<th class=\"text-left\">SVN predict</th>\n" +
                "<th class=\"text-left\">SVN probability</th>\n" +
                "<th class=\"text-left\">CNN predict</th>\n" +
                "<th class=\"text-left\">CNN probability</th>\n" +
                "</tr>\n" +
                "</thead>" +
                "<tbody class=\"table-hover\">\n"
            for (var i = data.length - 1; i >= 0; i--) {
                html += "<tr>";
                html += "<td>" + "<img src='" + data[i].decodedUrl + "' width='112px' height='112px' class='digit-image' alt='Digit'/>" + "</td>";
                html += "<td>" + data[i].svmPredict + "</td>";
                html += "<td>" + data[i].svmProbability + "</td>";
                html += "<td>" + data[i].cnnPredict + "</td>";
                html += "<td>" + data[i].cnnProbability + "</td>";
                html += "</tr>";

            }
            html += "</tbody>";
            html += "</table>";
            document.getElementById('predicts').innerHTML = html;
            spinner.style.display = "none";
            body.style.backgroundColor = "#FFFFFF";
            container.style.opacity = 1;
        })
    });

    var buttonClear = document.getElementById('btn-clear');
    buttonClear.addEventListener('click', function (e) {
        context.clearRect(0, 0, context.canvas.width, context.canvas.height);
        context.fillRect(0, 0, canvas.width, canvas.height);
        clickX = [];
        clickY = [];
        clickDrag = [];
    });

    var buttonClearHistory = document.getElementById('btn-clear-history');
    buttonClearHistory.addEventListener('click', function (e) {
        var requestUrl = window.location.origin + '/clearHistory';
        $.get(requestUrl, function (data, status) {
            document.getElementById('predicts').innerHTML = "";
        })
    });

});
