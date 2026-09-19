const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreEl = document.getElementById('score');
const livesEl = document.getElementById('lives');
const controlButtons = document.querySelectorAll('[data-direction]');
const restartButton = document.getElementById('restartButton');

const SCREEN_WIDTH = 600;
const SCREEN_HEIGHT = 650;
const CELL_SIZE = 30;
const FPS = 60;
const BLACK = '#000';
const WHITE = '#fff';
const BLUE = '#1d4ed8';
const YELLOW = '#facc15';
const RED = '#ef4444';
const PINK = '#f472b6';
const CYAN = '#22d3ee';
const ORANGE = '#f59e0b';

const MAZE = [
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,1],
  [1,3,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,1,3,1],
  [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
  [1,2,1,1,2,1,2,1,1,1,1,1,2,1,2,1,1,2,1,1],
  [1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,1],
  [1,1,1,1,2,1,1,1,0,1,0,1,1,1,2,1,1,1,1],
  [0,0,0,1,2,1,0,0,0,0,0,0,0,1,2,1,0,0,0],
  [1,1,1,1,2,1,0,1,1,0,1,1,0,1,2,1,1,1,1],
  [0,0,0,0,2,0,0,1,0,0,0,1,0,0,2,0,0,0,0],
  [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
  [0,0,0,1,2,1,0,0,0,0,0,0,0,1,2,1,0,0,0],
  [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
  [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
  [1,2,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,2,1],
  [1,3,2,1,2,2,2,2,2,0,2,2,2,2,2,1,2,3,1],
  [1,1,2,1,2,1,2,1,1,1,1,1,2,1,2,1,2,1,1],
  [1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,1],
  [1,2,1,1,1,1,1,1,2,1,2,1,1,1,1,1,1,2,1],
  [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
];

let score = 0;
let lives = 3;
let dots = [];
let powerPellets = [];
let gameOver = false;
let won = false;

const pacman = {
  x: CELL_SIZE,
  y: CELL_SIZE,
  direction: 'STOP',
  nextDirection: 'STOP',
  speed: 3,
  powerMode: false,
  powerTimer: 0,
};

const ghosts = [
  { color: RED, x: 9 * CELL_SIZE, y: 9 * CELL_SIZE, direction: 'UP', speed: 2, scared: false, spawnX: 9 * CELL_SIZE, spawnY: 9 * CELL_SIZE },
  { color: PINK, x: 8 * CELL_SIZE, y: 9 * CELL_SIZE, direction: 'DOWN', speed: 2, scared: false, spawnX: 8 * CELL_SIZE, spawnY: 9 * CELL_SIZE },
  { color: CYAN, x: 10 * CELL_SIZE, y: 9 * CELL_SIZE, direction: 'LEFT', speed: 2, scared: false, spawnX: 10 * CELL_SIZE, spawnY: 9 * CELL_SIZE },
  { color: ORANGE, x: 9 * CELL_SIZE, y: 10 * CELL_SIZE, direction: 'RIGHT', speed: 2, scared: false, spawnX: 9 * CELL_SIZE, spawnY: 10 * CELL_SIZE },
];

function buildMazeState() {
  dots = [];
  powerPellets = [];

  for (let row = 0; row < MAZE.length; row += 1) {
    for (let col = 0; col < MAZE[row].length; col += 1) {
      const value = MAZE[row][col];
      if (value === 2) {
        dots.push({ x: col * CELL_SIZE + CELL_SIZE / 2, y: row * CELL_SIZE + CELL_SIZE / 2 });
      } else if (value === 3) {
        powerPellets.push({ x: col * CELL_SIZE + CELL_SIZE / 2, y: row * CELL_SIZE + CELL_SIZE / 2 });
      }
    }
  }
}

function resetPositions() {
  pacman.x = CELL_SIZE;
  pacman.y = CELL_SIZE;
  pacman.direction = 'STOP';
  pacman.nextDirection = 'STOP';
  pacman.powerMode = false;
  pacman.powerTimer = 0;

  ghosts.forEach((ghost, index) => {
    ghost.x = ghost.spawnX;
    ghost.y = ghost.spawnY;
    ghost.direction = ['UP', 'DOWN', 'LEFT', 'RIGHT'][index % 4];
    ghost.scared = false;
  });
}

function canMove(entity, direction) {
  let newX = entity.x;
  let newY = entity.y;

  if (direction === 'UP') newY -= entity.speed;
  else if (direction === 'DOWN') newY += entity.speed;
  else if (direction === 'LEFT') newX -= entity.speed;
  else if (direction === 'RIGHT') newX += entity.speed;
  else return true;

  const corners = [
    [newX, newY],
    [newX + CELL_SIZE - 1, newY],
    [newX, newY + CELL_SIZE - 1],
    [newX + CELL_SIZE - 1, newY + CELL_SIZE - 1],
  ];

  for (const [cx, cy] of corners) {
    const col = Math.floor(cx / CELL_SIZE);
    const row = Math.floor(cy / CELL_SIZE);
    if (row >= 0 && row < MAZE.length && col >= 0 && col < MAZE[row].length && MAZE[row][col] === 1) {
      return false;
    }
  }
  return true;
}

function movePacman() {
  if (pacman.nextDirection !== 'STOP') {
    if (canMove(pacman, pacman.nextDirection)) {
      pacman.direction = pacman.nextDirection;
      pacman.nextDirection = 'STOP';
    }
  }

  if (canMove(pacman, pacman.direction)) {
    if (pacman.direction === 'UP') pacman.y -= pacman.speed;
    if (pacman.direction === 'DOWN') pacman.y += pacman.speed;
    if (pacman.direction === 'LEFT') pacman.x -= pacman.speed;
    if (pacman.direction === 'RIGHT') pacman.x += pacman.speed;
  }

  if (pacman.x < 0) pacman.x = SCREEN_WIDTH - CELL_SIZE;
  else if (pacman.x > SCREEN_WIDTH - CELL_SIZE) pacman.x = 0;
}

function getPossibleDirections(ghost) {
  const directions = ['UP', 'DOWN', 'LEFT', 'RIGHT'];
  const output = [];

  directions.forEach((direction) => {
    const reverse = (direction === 'UP' && ghost.direction === 'DOWN') ||
      (direction === 'DOWN' && ghost.direction === 'UP') ||
      (direction === 'LEFT' && ghost.direction === 'RIGHT') ||
      (direction === 'RIGHT' && ghost.direction === 'LEFT');

    if (!reverse && canMove(ghost, direction)) {
      output.push(direction);
    }
  });

  return output;
}

function moveGhost(ghost) {
  const possible = getPossibleDirections(ghost);
  if (!possible.length) return;

  let nextDir = ghost.direction;

  if (ghost.scared) {
    let maxDistance = -Infinity;
    for (const direction of possible) {
      const test = { x: ghost.x, y: ghost.y, speed: ghost.speed };
      if (direction === 'UP') test.y -= ghost.speed;
      if (direction === 'DOWN') test.y += ghost.speed;
      if (direction === 'LEFT') test.x -= ghost.speed;
      if (direction === 'RIGHT') test.x += ghost.speed;
      const dist = Math.hypot(test.x - pacman.x, test.y - pacman.y);
      if (dist > maxDistance) {
        maxDistance = dist;
        nextDir = direction;
      }
    }
  } else if (Math.random() < 0.7) {
    let minDistance = Infinity;
    for (const direction of possible) {
      const test = { x: ghost.x, y: ghost.y, speed: ghost.speed };
      if (direction === 'UP') test.y -= ghost.speed;
      if (direction === 'DOWN') test.y += ghost.speed;
      if (direction === 'LEFT') test.x -= ghost.speed;
      if (direction === 'RIGHT') test.x += ghost.speed;
      const dist = Math.hypot(test.x - pacman.x, test.y - pacman.y);
      if (dist < minDistance) {
        minDistance = dist;
        nextDir = direction;
      }
    }
  } else {
    nextDir = possible[Math.floor(Math.random() * possible.length)];
  }

  ghost.direction = nextDir;
  if (canMove(ghost, ghost.direction)) {
    if (ghost.direction === 'UP') ghost.y -= ghost.speed;
    if (ghost.direction === 'DOWN') ghost.y += ghost.speed;
    if (ghost.direction === 'LEFT') ghost.x -= ghost.speed;
    if (ghost.direction === 'RIGHT') ghost.x += ghost.speed;
  }

  if (ghost.x < 0) ghost.x = SCREEN_WIDTH - CELL_SIZE;
  else if (ghost.x > SCREEN_WIDTH - CELL_SIZE) ghost.x = 0;
}

function eatDotsAndPellets() {
  const centerX = pacman.x + CELL_SIZE / 2;
  const centerY = pacman.y + CELL_SIZE / 2;

  for (let i = dots.length - 1; i >= 0; i -= 1) {
    const dot = dots[i];
    if (Math.hypot(dot.x - centerX, dot.y - centerY) < CELL_SIZE / 2) {
      dots.splice(i, 1);
      score += 10;
    }
  }

  for (let i = powerPellets.length - 1; i >= 0; i -= 1) {
    const pellet = powerPellets[i];
    if (Math.hypot(pellet.x - centerX, pellet.y - centerY) < CELL_SIZE / 2) {
      powerPellets.splice(i, 1);
      score += 50;
      pacman.powerMode = true;
      pacman.powerTimer = 300;
      ghosts.forEach((ghost) => {
        ghost.scared = true;
      });
    }
  }
}

function handleCollisions() {
  for (const ghost of ghosts) {
    const dx = ghost.x - pacman.x;
    const dy = ghost.y - pacman.y;
    if (Math.hypot(dx, dy) < CELL_SIZE) {
      if (ghost.scared) {
        ghost.x = ghost.spawnX;
        ghost.y = ghost.spawnY;
        ghost.scared = false;
        score += 200;
      } else {
        lives -= 1;
        if (lives <= 0) {
          gameOver = true;
        } else {
          resetPositions();
        }
      }
    }
  }

  if (!dots.length && !powerPellets.length) {
    won = true;
  }
}

function update() {
  if (gameOver || won) return;

  movePacman();

  if (pacman.powerMode) {
    pacman.powerTimer -= 1;
    if (pacman.powerTimer <= 0) {
      pacman.powerMode = false;
      ghosts.forEach((ghost) => {
        ghost.scared = false;
      });
    }
  }

  ghosts.forEach((ghost) => moveGhost(ghost));
  eatDotsAndPellets();
  handleCollisions();
  updateHud();
}

function updateHud() {
  scoreEl.textContent = score;
  livesEl.textContent = lives;
}

function drawMaze() {
  for (let row = 0; row < MAZE.length; row += 1) {
    for (let col = 0; col < MAZE[row].length; col += 1) {
      if (MAZE[row][col] === 1) {
        ctx.fillStyle = BLUE;
        ctx.fillRect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE);
        ctx.fillStyle = BLACK;
        ctx.fillRect(col * CELL_SIZE + 2, row * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4);
      }
    }
  }
}

function drawDots() {
  ctx.fillStyle = WHITE;
  for (const dot of dots) {
    ctx.beginPath();
    ctx.arc(dot.x, dot.y, 3, 0, Math.PI * 2);
    ctx.fill();
  }

  ctx.fillStyle = WHITE;
  for (const pellet of powerPellets) {
    ctx.beginPath();
    ctx.arc(pellet.x, pellet.y, 8, 0, Math.PI * 2);
    ctx.fill();
  }
}

function drawPacman() {
  const centerX = pacman.x + CELL_SIZE / 2;
  const centerY = pacman.y + CELL_SIZE / 2;
  const radius = CELL_SIZE / 2 - 2;

  ctx.fillStyle = YELLOW;
  ctx.beginPath();
  ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
  ctx.fill();

  let mouthAngle = 0;
  if (pacman.direction === 'LEFT') mouthAngle = Math.PI;
  else if (pacman.direction === 'UP') mouthAngle = -Math.PI / 2;
  else if (pacman.direction === 'DOWN') mouthAngle = Math.PI / 2;

  ctx.fillStyle = BLACK;
  ctx.beginPath();
  ctx.moveTo(centerX, centerY);
  ctx.arc(centerX, centerY, radius, mouthAngle - Math.PI / 6, mouthAngle + Math.PI / 6);
  ctx.closePath();
  ctx.fill();
}

function drawGhost(ghost) {
  const centerX = ghost.x + CELL_SIZE / 2;
  const centerY = ghost.y + CELL_SIZE / 2;
  const bodyColor = ghost.scared ? '#4f46e5' : ghost.color;

  ctx.fillStyle = bodyColor;
  ctx.beginPath();
  ctx.arc(centerX, centerY - 2, CELL_SIZE / 2 - 2, Math.PI, 0);
  ctx.lineTo(centerX + CELL_SIZE / 2 - 2, centerY + CELL_SIZE / 2);
  ctx.lineTo(centerX + CELL_SIZE / 4, centerY + CELL_SIZE / 3);
  ctx.lineTo(centerX, centerY + CELL_SIZE / 2);
  ctx.lineTo(centerX - CELL_SIZE / 4, centerY + CELL_SIZE / 3);
  ctx.lineTo(centerX - CELL_SIZE / 2 + 2, centerY + CELL_SIZE / 2);
  ctx.closePath();
  ctx.fill();

  ctx.fillStyle = WHITE;
  ctx.beginPath();
  ctx.arc(centerX - 5, centerY - 3, 4, 0, Math.PI * 2);
  ctx.arc(centerX + 5, centerY - 3, 4, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = BLACK;
  ctx.beginPath();
  ctx.arc(centerX - 5, centerY - 3, 2, 0, Math.PI * 2);
  ctx.arc(centerX + 5, centerY - 3, 2, 0, Math.PI * 2);
  ctx.fill();
}

function drawText(message, color, size) {
  ctx.fillStyle = color;
  ctx.font = `bold ${size}px Arial`;
  ctx.textAlign = 'center';
  ctx.fillText(message, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 30);

  ctx.fillStyle = WHITE;
  ctx.font = '20px Arial';
  ctx.fillText('Press R to restart', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20);
}

function draw() {
  ctx.clearRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
  drawMaze();
  drawDots();
  drawPacman();
  ghosts.forEach(drawGhost);

  if (gameOver) {
    drawText('GAME OVER', RED, 52);
  } else if (won) {
    drawText('YOU WIN!', YELLOW, 52);
  }
}

function loop() {
  update();
  draw();
  requestAnimationFrame(loop);
}

function setDirection(direction) {
  pacman.nextDirection = direction;
}

function restartGame() {
  score = 0;
  lives = 3;
  gameOver = false;
  won = false;
  resetPositions();
  buildMazeState();
  updateHud();
}

window.addEventListener('keydown', (event) => {
  if (event.key === 'ArrowUp' || event.key.toLowerCase() === 'w') setDirection('UP');
  else if (event.key === 'ArrowDown' || event.key.toLowerCase() === 's') setDirection('DOWN');
  else if (event.key === 'ArrowLeft' || event.key.toLowerCase() === 'a') setDirection('LEFT');
  else if (event.key === 'ArrowRight' || event.key.toLowerCase() === 'd') setDirection('RIGHT');
  else if (event.key.toLowerCase() === 'r' && (gameOver || won)) restartGame();
});

controlButtons.forEach((button) => {
  button.addEventListener('pointerdown', (event) => {
    event.preventDefault();
    setDirection(button.dataset.direction);
  });
});

restartButton.addEventListener('click', restartGame);

buildMazeState();
updateHud();
requestAnimationFrame(loop);
