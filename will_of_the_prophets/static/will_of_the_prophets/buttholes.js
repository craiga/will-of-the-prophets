function getOrange() {
    return $(".text-orange").css('color');
}


function getBlue() {
    return $(".text-blue").css('color');
}


function getBorderWidth() {
    return parseInt($('.border').css('border-width'));
}


/**
 * Calculate coordinates of buttholes.
 * Returns a list of six numbers:
 *  1 & 2: x and y coordinates of left side of start
 *  3 & 4: x and y coordinates of right side of start
 *  5 & 6: x and y coordinates of end
 */
function calculateCoordinates(startEle, endEle) {
    var startPos = $(startEle).offset();
    var endPos = $(endEle).offset();
    var squareWidth= $(startEle).outerWidth();
    var squareHeight= $(startEle).outerHeight();
    var borderWidth = getBorderWidth();
    return [
        startPos.left + borderWidth,
        startPos.top + (squareHeight / 2),
        startPos.left + squareWidth - borderWidth,
        startPos.top + (squareHeight / 2),
        endPos.left + (squareWidth / 2),
        endPos.top + (squareHeight / 4),
    ]
}


function createCanvas(coordinates) {
    var left = Math.min(coordinates[0], coordinates[2], coordinates[4]);
    var top = Math.min(coordinates[1], coordinates[3], coordinates[5]);
    var width = Math.max(coordinates[0], coordinates[2], coordinates[4]) - left;
    var height = Math.max(coordinates[1], coordinates[3], coordinates[5]) - top;
    var canvas = document.createElement('canvas');
    $(canvas).css({
        position: 'absolute',
        left: left,
        top: top,
    });
    $(canvas).attr('width', width);
    $(canvas).attr('height', height);
    $(canvas).addClass('butthole');
    $('.container').append(canvas);
    return canvas;
}


/** Transpose coordinates so that the upper-left corner is 0, 0. */
function transposeCoordinates(coordinates) {
    var minX = Math.min(coordinates[0], coordinates[2], coordinates[4]);
    var minY = Math.min(coordinates[1], coordinates[3], coordinates[5]);
    return [
        coordinates[0] - minX,
        coordinates[1] - minY,
        coordinates[2] - minX,
        coordinates[3] - minY,
        coordinates[4] - minX,
        coordinates[5] - minY,
    ];
}


function drawButtholeSides(coordinates, canvasContext) {
    canvasContext.lineWidth = getBorderWidth();
    canvasContext.beginPath();
    canvasContext.moveTo(coordinates[0], coordinates[1]);
    canvasContext.lineTo(coordinates[4], coordinates[5]);
    canvasContext.stroke();
    canvasContext.beginPath();
    canvasContext.moveTo(coordinates[2], coordinates[3]);
    canvasContext.lineTo(coordinates[4], coordinates[5]);
    canvasContext.stroke();
}


function drawButtholeBackground(coordinates, canvasContext) {
    canvasContext.beginPath();
    canvasContext.globalAlpha = 0.75;
    canvasContext.moveTo(coordinates[0], coordinates[1]);
    canvasContext.lineTo(coordinates[2], coordinates[3]);
    canvasContext.lineTo(coordinates[4], coordinates[5]);
    canvasContext.lineTo(coordinates[0], coordinates[1]);
    canvasContext.fill();
}


function drawButthole(coordinates, canvas) {
    var canvasContext = canvas.getContext('2d');

    // Create gradient
    var gradient = canvasContext.createLinearGradient(0, 0, 0, coordinates[5]);
    gradient.addColorStop(0, getBlue());
    gradient.addColorStop(1, getOrange());

    // Set up canvas context.
    canvasContext.strokeStyle = gradient;
    canvasContext.fillStyle = gradient;

    drawButtholeSides(coordinates, canvasContext);
    drawButtholeBackground(coordinates, canvasContext);
}


function drawButtholes() {
    $('[data-buttholes-start-at]').each(function(i, endEle) {
        var startIds = $(endEle).data('buttholes-start-at');
        $(startIds).each(function(i , startId) {
            // Calculate start and end positions
            var startEle = document.getElementById(startId);
            coordinates = calculateCoordinates(startEle, endEle);
            canvas = createCanvas(coordinates)
            coordinates = transposeCoordinates(coordinates);
            drawButthole(coordinates, canvas);
        });
    });
}


$(drawButtholes);
$(window).resize(function () {
    $('.butthole').remove();
    drawButtholes();
});
