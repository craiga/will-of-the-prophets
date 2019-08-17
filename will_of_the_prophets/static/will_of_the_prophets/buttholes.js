/**
 * Helper Point class for simple vector manipulation. All instance methods
 * should return new instances to allow safe chaining.
 */
function Point(x, y) {
  this.x = x || 0;
  this.y = y || 0;
}

/**
 * Returns an SVG quad string.
 *
 * See https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths for
 * more details.
 */
Point.toQuadCurveString = function(controlPoint, endPoint) {
  return "Q" + [controlPoint.toString(), endPoint.toString()].join(",");
};

/**
 * Returns the midpoint between two Points.
 */
Point.getMidPoint = function(startPoint, endPoint) {
  return endPoint
    .subtract(startPoint)
    .scale(0.5)
    .add(startPoint);
};

Point.prototype.ortho = function() {
  return new Point(this.y, -this.x);
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

Point.prototype.toString = function() {
  return this.x + " " + this.y;
};

function renderButtholes() {
  var NS = "http://www.w3.org/2000/svg";
  var container = document.querySelector(".board__buttholes");
  if (!container) return;

  /**
   * Returns the center point of the provided element relative to the container
   * as a unit value ([0, 1]);
   *
   * @param {Element} el The element whose center we would like to find.
   *
   * @returns {Point} The center point of the provided element.
   */
  function getRelativeCenterAsPoint(el) {
    var containerRect = container.getBoundingClientRect();
    var rect = el.getBoundingClientRect();
    var x = (rect.x - containerRect.x + rect.width / 2) / containerRect.width;
    var y = (rect.y - containerRect.y + rect.height / 2) / containerRect.height;

    return new Point(x, y);
  }

  /**
   * Calculates a control point for quadratic curve based on the provided
   * start and end points.
   *
   * @param {Point} startPoint The start point of the curve.
   * @param {Point} endPoint The end point of the curve.
   * @param {number} rotationDirection The direction for which the orthogonal
   *    should be calculated. 1 = clockwise, -1 = counterclockwise.
   *
   * @returns {Point}
   */
  function getControlPoint(startPoint, endPoint, rotationDirection) {
    var midPoint = Point.getMidPoint(startPoint, endPoint);

    // Calculate the control point by finding and scaling the orthogonal, then
    // shifting it to the midPoint.
    return endPoint
      .subtract(startPoint)
      .ortho()
      .scale(rotationDirection * 0.2)
      .add(midPoint);
  }

  /**
   * Creates an SVG path element starting at the provide point using the
   * provided curves.
   *
   * @param {Point} startPoint The start point of the path.
   * @param {string[]} curves An array of quad curve strings.
   *
   * @return {SVGPathElement}
   */
  function createPathElement(startPoint, curves) {
    var path = document.createElementNS(NS, "path");
    path.setAttribute("d", "M " + startPoint.toString() + curves.join(" "));
    return path;
  }

  /**
   * Renders an SVG path between the provided start element and end element.
   *
   * @param {Element} startEl
   * @param {Element} endEl
   */
  function renderPath(startEl, endEl) {
    var startPoint = getRelativeCenterAsPoint(startEl);
    var endPoint = getRelativeCenterAsPoint(endEl);
    var midPoint = Point.getMidPoint(startPoint, endPoint);

    // If the end point is to the left of the start point, we want the line to
    // curve left first. Otherwise curve to the right first. Doing this is
    // creates a more natural looking curve.
    var rotationDirection = startPoint.x > endPoint.x ? 1 : -1;

    var controlPoint1 = getControlPoint(
      startPoint,
      midPoint,
      rotationDirection
    );
    var controlPoint2 = getControlPoint(midPoint, endPoint, -rotationDirection);

    var path = createPathElement(startPoint, [
      Point.toQuadCurveString(controlPoint1, midPoint),
      Point.toQuadCurveString(controlPoint2, endPoint)
    ]);
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
}

renderButtholes();
