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


function drawButthole(coordinates, canvas) {
    // Set up canvas for drawing
    var ctx = canvas.getContext('2d');

    // Create gradient
    var gradient = ctx.createLinearGradient(0, 0, 0, coordinates[5]);
    gradient.addColorStop(0, getBlue());
    gradient.addColorStop(1, getOrange());
    
    // Draw sides
    ctx.strokeStyle = gradient;
    ctx.lineWidth = getBorderWidth();
    ctx.beginPath();
    ctx.moveTo(coordinates[0], coordinates[1]);
    ctx.lineTo(coordinates[4], coordinates[5]);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(coordinates[2], coordinates[3]);
    ctx.lineTo(coordinates[4], coordinates[5]);
    ctx.stroke();

    // Draw background
    ctx.beginPath();
    ctx.globalAlpha = 0.75;
    ctx.fillStyle = gradient;
    ctx.moveTo(coordinates[0], coordinates[1]);
    ctx.lineTo(coordinates[2], coordinates[3]);
    ctx.lineTo(coordinates[4], coordinates[5]);
    ctx.lineTo(coordinates[0], coordinates[1]);
    ctx.fill();
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
