/**
 * Helper Point class for simple vector manipulation. All instance methods
 * should return new instances to allow safe chaining.
 */
function Point(x, y) {
  this.x = x || 0;
  this.y = y || 0;
}

Point.toQuadCurveString = function(control, end) {
  return "Q" + [control.toString(), end.toString()].join(",");
};

Point.prototype.rotate = function(deg) {
  var rad = (deg * Math.PI) / 180;
  var x = this.x;
  var y = this.y;

  var xp = x * Math.cos(rad) - y * Math.sin(rad);
  var yp = x * Math.sin(rad) + y * Math.cos(rad);

  return new Point(xp, yp);
};

Point.prototype.add = function(point) {
  return new Point(this.x + point.x, this.y + point.y);
};

Point.prototype.subtract = function(point) {
  return new Point(this.x - point.x, this.y - point.y);
};

Point.prototype.scale = function(scale) {
  return new Point(this.x * scale, this.y * scale);
};

Point.prototype.length = function() {
  return Math.sqrt(this.x * this.x + this.y * this.y);
};

Point.prototype.toString = function() {
  return this.x + " " + this.y;
};

Raven.context(function() {
  var NS = "http://www.w3.org/2000/svg";
  var container = document.querySelector(".board__buttholes");
  var containerRect = container.getBoundingClientRect();

  function getRelativeCenterAsPoint(el) {
    var rect = el.getBoundingClientRect();
    var x =
      (rect.left + rect.width / 2 - containerRect.left) / containerRect.width;
    var y =
      (rect.top + rect.height / 2 - containerRect.top) / containerRect.height;
    return new Point(x, y);
  }

  function renderPath(startEl, endEl) {
    var startPoint = getRelativeCenterAsPoint(startEl);
    var endPoint = getRelativeCenterAsPoint(endEl);
    var midPoint = endPoint
      .subtract(startPoint)
      .scale(0.5)
      .add(startPoint);

    // Longer buttholes should be curved more.
    var length = endPoint.subtract(startPoint).length();
    var rotationAngle = 40 * length;

    // If the end point is to the left of the start point, we want the line to
    // curve left first. Otherwise curve to the right first. This creates a
    // more natural looking curve.
    var rotationDirection = startPoint.x > endPoint.x ? -1 : 1;

    var controlPoint1 = midPoint
      .subtract(startPoint)
      .scale(0.5)
      .rotate(rotationDirection * rotationAngle)
      .add(startPoint);

    var controlPoint2 = endPoint
      .subtract(midPoint)
      .scale(0.5)
      .rotate(-rotationDirection * rotationAngle)
      .add(midPoint);

    var path = document.createElementNS(NS, "path");
    path.setAttribute(
      "d",
      "M " +
        startPoint.toString() +
        [
          Point.toQuadCurveString(controlPoint1, midPoint),
          Point.toQuadCurveString(controlPoint2, endPoint)
        ].join(" ")
    );

    container.appendChild(path);
  }

  var buttholeEnds = document.querySelectorAll("[data-butthole-starts]");
  [].forEach.call(buttholeEnds, function(endEl) {
    JSON.parse(endEl.dataset.buttholeStarts).forEach(function(startNumber) {
      renderPath(
        document.querySelector('[data-number="' + startNumber + '"]'),
        endEl
      );
    });
  });
});
