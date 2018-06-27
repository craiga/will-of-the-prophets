$(function() {
    // Extract colours and sizes from document.
    // Assumes something in the document has already got the required classes attached to something.
    var orange = $(".text-orange").css('color');
    var blue = $(".text-blue").css('color');
    var borderWidth = parseInt($('.border').css('border-width'));

    $('[data-buttholes-start-at]').each(function(i, endEle) {
        var startIds = $(endEle).data('buttholes-start-at');
        $(startIds).each(function(i , startId) {
            // Calculate start and end positions
            var startEle = document.getElementById(startId);
            var startPosA = $(startEle).offset();
            var startPosB = $(startEle).offset();
            startPosA.top = startPosA.top + ($(startEle).outerHeight() / 2);
            startPosA.left = startPosA.left + borderWidth;
            startPosB.top = startPosB.top + ($(startEle).outerHeight() / 2);
            startPosB.left = startPosB.left + $(startEle).outerWidth() - borderWidth;
            var endPos = $(endEle).offset();
            endPos.top = endPos.top + ($(endEle).outerHeight() / 4);
            endPos.left = endPos.left + ($(endEle).outerWidth() / 2);

            // Calculate size of the canvas
            var top = Math.min(startPosA.top, startPosB.top, endPos.top);
            var left = Math.min(startPosA.left, startPosB.left, endPos.left);
            var height = Math.max(startPosA.top, startPosB.top, endPos.top) - top;
            var width = Math.max(startPosA.left, startPosB.left, endPos.left) - left;

            // Ensure start of butthole will be on top of canvas.
            $(startEle).css('z-index', 20);

            // Create and inject canvas
            var canvas = document.createElement('canvas');
            $(canvas).css({
                position: 'absolute',
                top: top,
                left: left,
                'z-index': 10,
            });
            $(canvas).attr('height', height);
            $(canvas).attr('width', width);
            $('.container').append(canvas);

            // Set up canvas for drawing
            var ctx = canvas.getContext('2d');

            // Create gradient
            var gradient = ctx.createLinearGradient(0, 0, 0, endPos.top - top);
            gradient.addColorStop(0, blue);
            gradient.addColorStop(1, orange);
            
            // Draw sides
            ctx.strokeStyle = gradient;
            ctx.lineWidth = borderWidth;
            ctx.beginPath();
            ctx.moveTo(startPosA.left - left, startPosA.top - top);
            ctx.lineTo(endPos.left - left, endPos.top - top);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(startPosB.left - left, startPosB.top - top);
            ctx.lineTo(endPos.left - left, endPos.top - top);
            ctx.stroke();

            // Draw background
            ctx.beginPath();
            ctx.globalAlpha = 0.75;
            ctx.fillStyle = gradient;
            ctx.moveTo(startPosA.left - left, startPosA.top - top);
            ctx.lineTo(startPosB.left - left, startPosB.top - top);
            ctx.lineTo(endPos.left - left, endPos.top - top);
            ctx.lineTo(startPosA.left - left, startPosA.top - top);
            ctx.fill();
        });
    });
});
