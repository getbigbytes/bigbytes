const HEIGHT = 14;
const WIDTH = 18.53;
const RATIO = WIDTH / HEIGHT;

type GradientLogoProps = {
  height?: number;
  width?: number;
}

function GradientLogo({
  height,
  width,
}: GradientLogoProps) {
  const h = height || (width ? (width * (1 / RATIO)) : HEIGHT);
  const w = width || (height ? (height * (RATIO)) : WIDTH);

  return (
      <svg width={w} height={h} xmlns:xlink="http://www.w3.org/1999/xlink" zoomAndPan="magnify"
           viewBox="0 0 150 149.999998" preserveAspectRatio="xMidYMid meet" version="1.0">


        <defs>
          <clipPath id="a680f83d17">
            <path
                d="M 20.597656 3.808594 L 129.347656 3.808594 L 129.347656 146.308594 L 20.597656 146.308594 Z M 20.597656 3.808594 "
                clip-rule="nonzero"/>
          </clipPath>
        </defs>


        <g clip-path="url(#a680f83d17)">
          <path fill="#00a99d"
                d="M 35.847656 99.382812 L 35.847656 19.820312 L 20.597656 28.636719 L 20.597656 108.171875 L 35.847656 116.960938 L 43.449219 121.378906 L 48.335938 124.171875 L 58.699219 130.167969 L 63.558594 132.988281 L 71.183594 137.382812 L 86.433594 146.167969 L 101.6875 137.382812 L 114.171875 130.167969 L 129.394531 121.378906 L 129.394531 89.433594 L 129.316406 89.40625 L 129.394531 89.355469 L 129.394531 71.828125 L 129.316406 71.804688 L 114.171875 63.039062 L 101.6875 55.828125 L 86.433594 47.039062 L 78.808594 42.621094 L 63.558594 51.433594 L 63.558594 3.820312 L 48.335938 12.609375 L 48.335938 106.59375 Z M 86.433594 128.59375 L 73.949219 121.378906 L 86.433594 114.167969 L 101.6875 105.355469 L 101.6875 73.429688 L 114.09375 80.589844 L 114.171875 80.539062 L 114.171875 112.566406 L 101.6875 119.777344 Z M 86.433594 96.566406 L 63.558594 109.75 L 63.558594 51.433594 L 86.433594 64.644531 Z M 86.433594 96.566406 "
                fill-opacity="1" fill-rule="evenodd"/>
        </g>
      </svg>


  );
}

export default GradientLogo;
