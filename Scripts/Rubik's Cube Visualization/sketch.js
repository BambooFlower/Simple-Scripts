let cam;

// UP, DOWN, RIGHT, LEFT, FRONT, BACK
const UPP = 0;
const DWN = 1;
const RGT = 2;
const LFT = 3;
const FRT = 4;
const BCK = 5;

const colors = [
  '#FFFFFF',
  '#FFFF00',
  '#FFA500',
  '#FF0000',
  '#00FF00',
  '#0000FF'
];

const dim = 3;
const cube = []; // Cubie[dim][dim][dim]; initialized in setup()

function setup() {
  // Disable the context menu on the canvas so the camera can use the right mouse button
  createCanvas(600, 600, WEBGL).elt.oncontextmenu = () => false;

  cam = createEasyCam({ distance: 400 });

  for (let i = 0; i < dim; i++) {
    cube[i] = [];
    for (let j = 0; j < dim; j++) {
      cube[i][j] = [];
      for (let k = 0; k < dim; k++) {
        const len = 50;
        const offset = (dim - 1) * len * 0.5;
        const x = len * i - offset;
        const y = len * j - offset;
        const z = len * k - offset;
        cube[i][j][k] = new Cubie(x, y, z, len);
      }
    }
  }
}

function draw() {
  background(51);
  for (let i = 0; i < dim; i++) {
    for (let j = 0; j < dim; j++) {
      for (let k = 0; k < dim; k++) {
        cube[i][j][k].show();
      }
    }
  }
}
