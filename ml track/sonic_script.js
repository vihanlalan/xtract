/* ==========================================================================
   The Arena Awaits — Quiz & Jigsaw Puzzle Engine
   Plain JS (ES6+), No Frameworks, No Build Step
   ========================================================================== */

/**
 * MAIN CONFIGURATION BLOCK
 */
const CONFIG = {
  GRID_SIZE: 4,                  // 4x4 Grid = 16 pieces total
  HINT_LIMIT: 3,                // Maximum hint uses (3 seconds each)
  HINT_DURATION_MS: 3000,      // Hint preview length in ms
  FLIP_DURATION_MS: 1600,      // 3D Card flip animation duration
  SOUND_ENABLED_DEFAULT: false,// Sound start muted by default

  // SHUFFLED QUESTION-TO-PIECE MAPPING
  // Question Index (0..15) -> Unlocks Piece Index (0..15)
  QUESTION_PIECE_MAP: [6, 11, 2, 14, 8, 0, 13, 4, 10, 1, 15, 7, 3, 12, 9, 5],

};


/* ==========================================================================
   STATE & PERSISTENCE
   ========================================================================== */

const STORAGE_KEY = "hunger_games_square_jigsaw_progress_v4";

const state = {
  solvedQuestionIds: [],       // Array of solved question IDs (1..16)
  unlockedPieceIndices: [],    // Array of unlocked piece indices (0..15)
  boardOccupancy: Array(16).fill(null), // Array of length 16: cellIdx -> pieceIdx
  trayPositions: {},           // { pieceIdx: { xRatio, yRatio } }
  wrongAttempts: {},           // { questionId: count }
  cooldownTimestamps: {},      // { questionId: timestamp }
  hintsLeft: CONFIG.HINT_LIMIT,
  soundEnabled: CONFIG.SOUND_ENABLED_DEFAULT,
  completed: false,
  flipped: false
};

// DOM References
const boardEl = document.getElementById("puzzle-board");
const trayEl = document.getElementById("piece-tray");
const gridOverlayEl = document.getElementById("grid-overlay");
const hintPreviewEl = document.getElementById("hint-preview");
const goldSweepEl = document.getElementById("gold-sweep");
const solvedCountEl = document.getElementById("solved-count");
const placedCountEl = document.getElementById("placed-count");
const flipCardEl = document.getElementById("flip-card");
const backTitleEl = document.getElementById("back-title");
const backSubtitleEl = document.getElementById("back-subtitle");
const revealContainerEl = document.getElementById("reveal-container");
const tapRevealBtn = document.getElementById("tap-reveal-btn");
const flipBackBtn = document.getElementById("flip-back-btn");
const hintBtn = document.getElementById("hint-btn");
const hintCountEl = document.getElementById("hint-count");
const resetBtn = document.getElementById("reset-btn");
const soundToggleBtn = document.getElementById("sound-toggle-btn");
const soundIconOff = document.getElementById("sound-icon-off");
const soundIconOn = document.getElementById("sound-icon-on");
const appContainerEl = document.getElementById("app-container");
const resetModalEl = document.getElementById("reset-modal");
const modalCancelBtn = document.getElementById("modal-cancel-btn");
const modalConfirmBtn = document.getElementById("modal-confirm-btn");
const questionsGridEl = document.getElementById("questions-grid");

// Quiz Modal DOM
const quizModalEl = document.getElementById("quiz-modal");
const quizModalTitleEl = document.getElementById("quiz-modal-title");
const quizQuestionBodyEl = document.getElementById("quiz-question-body");
const quizAnswerInputEl = document.getElementById("quiz-answer-input");
const quizSubmitBtnEl = document.getElementById("quiz-submit-btn");
const quizCloseBtnEl = document.getElementById("quiz-close-btn");
const quizModalCancelBtnEl = document.getElementById("quiz-modal-cancel-btn");
const quizStatusMsgEl = document.getElementById("quiz-status-msg");



let audioCtx = null;
let currentQuestionObj = null;
let activeDragPiece = null;
let dragOffset = { x: 0, y: 0 };
let dragStartSourceCell = null;
let dragStartTime = 0;
let dragStartX = 0;
let dragStartY = 0;
let pieceElements = [];
let cooldownTimerInterval = null;


/* ==========================================================================
   AUDIO SYSTEM
   ========================================================================== */

function initAudio() {
  if (!audioCtx) {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (AudioContextClass) audioCtx = new AudioContextClass();
  }
  if (audioCtx && audioCtx.state === "suspended") audioCtx.resume();
}

function playSnapSound() {
  if (!state.soundEnabled) return;
  initAudio();
  if (!audioCtx) return;

  try {
    const now = audioCtx.currentTime;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();

    osc.type = "sine";
    osc.frequency.setValueAtTime(440, now);
    osc.frequency.exponentialRampToValueAtTime(880, now + 0.08);

    gain.gain.setValueAtTime(0.3, now);
    gain.gain.exponentialRampToValueAtTime(0.01, now + 0.12);

    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start(now);
    osc.stop(now + 0.13);
  } catch (e) { }
}

function playCannonBoom() {
  if (!state.soundEnabled) return;
  initAudio();
  if (!audioCtx) return;

  try {
    const now = audioCtx.currentTime;

    const subOsc = audioCtx.createOscillator();
    const subGain = audioCtx.createGain();
    subOsc.type = "sine";
    subOsc.frequency.setValueAtTime(80, now);
    subOsc.frequency.exponentialRampToValueAtTime(25, now + 1.2);

    subGain.gain.setValueAtTime(0.8, now);
    subGain.gain.exponentialRampToValueAtTime(0.001, now + 1.4);

    subOsc.connect(subGain);
    subGain.connect(audioCtx.destination);
    subOsc.start(now);
    subOsc.stop(now + 1.45);

    const bufferSize = audioCtx.sampleRate * 1.0;
    const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) output[i] = Math.random() * 2 - 1;

    const whiteNoise = audioCtx.createBufferSource();
    whiteNoise.buffer = noiseBuffer;

    const filter = audioCtx.createBiquadFilter();
    filter.type = "lowpass";
    filter.frequency.setValueAtTime(400, now);
    filter.frequency.exponentialRampToValueAtTime(60, now + 0.8);

    const noiseGain = audioCtx.createGain();
    noiseGain.gain.setValueAtTime(0.5, now);
    noiseGain.gain.exponentialRampToValueAtTime(0.001, now + 0.9);

    whiteNoise.connect(filter);
    filter.connect(noiseGain);
    noiseGain.connect(audioCtx.destination);

    whiteNoise.start(now);
    whiteNoise.stop(now + 0.95);
  } catch (e) { }
}


/* ==========================================================================
   STORAGE
   ========================================================================== */

function saveState() {
  try {
    const dataToSave = {
      solvedQuestionIds: state.solvedQuestionIds,
      unlockedPieceIndices: state.unlockedPieceIndices,
      boardOccupancy: state.boardOccupancy,
      trayPositions: state.trayPositions,
      wrongAttempts: state.wrongAttempts,
      cooldownTimestamps: state.cooldownTimestamps,
      hintsLeft: state.hintsLeft,
      soundEnabled: state.soundEnabled
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(dataToSave));
  } catch (e) {
    console.warn("LocalStorage save error:", e);
  }
}

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed.solvedQuestionIds)) state.solvedQuestionIds = parsed.solvedQuestionIds;
      if (Array.isArray(parsed.unlockedPieceIndices)) state.unlockedPieceIndices = parsed.unlockedPieceIndices;
      if (Array.isArray(parsed.boardOccupancy) && parsed.boardOccupancy.length === 16) state.boardOccupancy = parsed.boardOccupancy;
      if (parsed.trayPositions) state.trayPositions = parsed.trayPositions;
      if (parsed.wrongAttempts) state.wrongAttempts = parsed.wrongAttempts;
      if (parsed.cooldownTimestamps) state.cooldownTimestamps = parsed.cooldownTimestamps;
      if (typeof parsed.hintsLeft === "number") state.hintsLeft = parsed.hintsLeft;
      if (typeof parsed.soundEnabled === "boolean") state.soundEnabled = parsed.soundEnabled;
    }
  } catch (e) {
    console.warn("LocalStorage load error:", e);
  }
}


/* ==========================================================================
   QUESTIONS GRID PANEL
   ========================================================================== */

function renderQuestionsGrid() {
  questionsGridEl.innerHTML = "";
  const now = Date.now();

  QUESTIONS.forEach(q => {
    const btn = document.createElement("button");
    btn.className = "q-btn";
    btn.dataset.id = q.id;

    const isSolved = state.solvedQuestionIds.includes(q.id);
    const cooldownTime = state.cooldownTimestamps[q.id] || 0;
    const isCooldown = !isSolved && cooldownTime > now;

    if (isSolved) {
      btn.classList.add("solved");
      btn.innerHTML = `✓ Q${q.id}`;
      btn.disabled = true;
    } else if (isCooldown) {
      btn.classList.add("cooldown");
      const remainingSec = Math.ceil((cooldownTime - now) / 1000);
      btn.innerHTML = `⏳ ${remainingSec}s`;
      btn.disabled = true;
    } else {
      btn.innerHTML = `Q${q.id}`;
      btn.addEventListener("click", () => openQuizModal(q));
    }

    questionsGridEl.appendChild(btn);
  });

  if (!cooldownTimerInterval) {
    cooldownTimerInterval = setInterval(updateCooldownTimers, 1000);
  }
}

function updateCooldownTimers() {
  const now = Date.now();
  let needReRender = false;

  QUESTIONS.forEach(q => {
    const cooldownTime = state.cooldownTimestamps[q.id] || 0;
    if (cooldownTime > 0 && cooldownTime <= now) {
      delete state.cooldownTimestamps[q.id];
      delete state.wrongAttempts[q.id];
      needReRender = true;
    }
  });

  if (needReRender) {
    saveState();
  }
  renderQuestionsGrid();
}


/* ==========================================================================
   QUIZ QUESTION MODAL
   ========================================================================== */

function openQuizModal(qObj) {
  currentQuestionObj = qObj;
  quizModalTitleEl.textContent = qObj.title;

  quizQuestionBodyEl.innerHTML = "";
  if (qObj.isCode) {
    const pre = document.createElement("pre");
    const code = document.createElement("code");
    code.textContent = qObj.text;
    pre.appendChild(code);
    quizQuestionBodyEl.appendChild(pre);
  } else {
    quizQuestionBodyEl.textContent = qObj.text;
  }

  quizAnswerInputEl.value = "";
  quizStatusMsgEl.className = "quiz-status-msg hidden";
  quizStatusMsgEl.textContent = "";

  const cooldownTime = state.cooldownTimestamps[qObj.id] || 0;
  const now = Date.now();
  if (cooldownTime > now) {
    const remSec = Math.ceil((cooldownTime - now) / 1000);
    showQuizStatus(`Gamemaker Lockout: Cooldown active (${remSec}s remaining).`, "cooldown");
    quizAnswerInputEl.disabled = true;
    quizSubmitBtnEl.disabled = true;
  } else {
    quizAnswerInputEl.disabled = false;
    quizSubmitBtnEl.disabled = false;
  }

  quizModalEl.classList.remove("hidden");
  setTimeout(() => quizAnswerInputEl.focus(), 100);
}

function closeQuizModal() {
  quizModalEl.classList.add("hidden");
  currentQuestionObj = null;
}

function showQuizStatus(msg, type) {
  quizStatusMsgEl.textContent = msg;
  quizStatusMsgEl.className = `quiz-status-msg ${type}`;
}

function normalizeInput(str) {
  return str.toString().trim().toLowerCase().replace(/[\s\W_]+/g, "");
}

async function sha256Hex(str) {
  const bytes = new TextEncoder().encode(str);
  const hashBuf = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(hashBuf)).map(b => b.toString(16).padStart(2, "0")).join("");
}


const LOCAL_ANSWER_HASHES = {
  1: ["535fa30d7e25dd8a49f1536779734ec8286108d115da5045d77f3b4185d8f790"],
  2: ["dc9f28b12dd1818ee42ffc92ecb940386214598837348d30d3c6c0b7b57e34c9"],
  3: ["aea92132c4cbeb263e6ac2bf6c183b5d81737f179f21efdc5863739672f0f470"],
  4: [
    "a438450d6ba8f12daa4f1f7ee389bd1b945a812336ab79a86f41bacb6c790bbe",
    "af8a09d60a71002f2c5c207a32a8b8bfdd5816c67c6e84bafc9363458b446bac",
    "999cabe45a6571053ef91e48522239e73b703d3064ca5a3d0e49f86acf55120e"
  ],
  5: ["b89a199ea81b6a925de700d15ccecdd9a0d7b9df2643a65f1b6f59af57a2c99d"],
  6: ["70edfd75bd0267f3653bbb18ae13a4b92e0f66120abb4419ecf7607189df5125"],
  7: ["59e19706d51d39f66711c2653cd7eb1291c94d9b55eb14bda74ce4dc636d015a"],
  8: [
    "2f1987bf98c09d2f5d2a23a6ae29fa53b9aec8f07ed1330bd439122f5a1a2c2c",
    "4b98886cc264ec45ddc1b54503ff3827e6b9d4a5fb58d03f00dc8258d0b25080"
  ],
  9: ["2132beb96348cdb5944f252db6d2c667edaf7bad53fe17fa51aee50b0987d737"],
  10: ["6b51d431df5d7f141cbececcf79edf3dd861c3b4069f0b11661a3eefacbba918"],
  11: ["e7f6c011776e8db7cd330b54174fd76f7d0216b612387a5ffcfb81e6f0919683"],
  12: ["a649dab5b07b10053b7ba7fb00dfe00083c70b345df188a8975819fd446e1da0"],
  13: ["3be24e5f7650d4c778b2359130d1854741a2ef1b488bcdcf8800c102cc47b118"],
  14: ["73475cb40a568e8da8a045ced110137e159f890ac4da883b6b17dc651b3a8049"],
  15: ["4c470b026027fa6e3a0f45c5437240f21ec77960d8475b5cc99c97bbd1a14879"],
  16: ["19581e27de7ced00ff1ce50b2047e7a567c76b1cbaebabe5ef03f7c3017bb5b7"]
};

async function handleQuizSubmit() {
  if (!currentQuestionObj) return;

  const rawInput = quizAnswerInputEl.value;
  if (!rawInput.trim()) return;

  quizSubmitBtnEl.disabled = true;

  const qId = currentQuestionObj.id;
  let isCorrect = false;
  let validated = false;

  // Attempt backend API if served via HTTP/HTTPS
  if (window.location.protocol.startsWith("http")) {
    try {
      const response = await fetch("/api/answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          questionId: qId,
          answer: rawInput
        })
      });

      if (response.ok) {
        const result = await response.json();
        if (typeof result.correct === "boolean") {
          isCorrect = result.correct;
          validated = true;
        }
      }
    } catch (e) {
      // Backend not reached; fall back to client-side hash check
    }
  }

  // Fallback for file:// or static hosts like GitHub Pages
  if (!validated) {
    const norm = normalizeInput(rawInput);
    const hash = await sha256Hex(norm);
    const accepted = LOCAL_ANSWER_HASHES[qId] || [];
    isCorrect = accepted.includes(hash);
  }

  if (isCorrect) {
    const qIndex = qId - 1;
    const targetPieceIdx = CONFIG.QUESTION_PIECE_MAP[qIndex];

    if (!state.solvedQuestionIds.includes(qId)) {
      state.solvedQuestionIds.push(qId);
    }

    if (!state.unlockedPieceIndices.includes(targetPieceIdx)) {
      state.unlockedPieceIndices.push(targetPieceIdx);
    }

    delete state.wrongAttempts[qId];
    delete state.cooldownTimestamps[qId];

    playCannonBoom();
    showQuizStatus(
      "CORRECT! Question solved & Piece unlocked!",
      "success"
    );

    saveState();
    unlockPieceDOM(targetPieceIdx);

    setTimeout(() => {
      closeQuizModal();
      renderQuestionsGrid();
      updateProgress();
    }, 900);

  } else {
    const attempts = (state.wrongAttempts[qId] || 0) + 1;
    state.wrongAttempts[qId] = attempts;

    const modalBox = quizModalEl.querySelector(".modal-box");
    modalBox.classList.add("shake");
    setTimeout(() => modalBox.classList.remove("shake"), 450);

    if (attempts >= 3) {
      state.cooldownTimestamps[qId] = Date.now() + 60000;

      showQuizStatus(
        "The Gamemakers are not impressed. 3 wrong attempts! Lockout active for 60 seconds.",
        "cooldown"
      );

      quizAnswerInputEl.disabled = true;
      quizSubmitBtnEl.disabled = true;
    } else {
      const rem = 3 - attempts;

      showQuizStatus(
        `The Gamemakers are not impressed. Incorrect answer. (${rem} attempt(s) remaining)`,
        "error"
      );

      quizSubmitBtnEl.disabled = false;
    }

    saveState();
    renderQuestionsGrid();
  }
}

function unlockPieceDOM(pieceIdx) {
  const piece = pieceElements[pieceIdx];
  if (!piece) return;

  piece.classList.remove("quiz-locked");
  const lockOverlay = piece.querySelector(".piece-lock-overlay");
  if (lockOverlay) lockOverlay.remove();

  piece.classList.add("just-unlocked");
  setTimeout(() => piece.classList.remove("just-unlocked"), 600);
}

function setupGridGuide() {
  gridOverlayEl.innerHTML = "";
  const N = CONFIG.GRID_SIZE;
  for (let i = 0; i < N * N; i++) {
    const cell = document.createElement("div");
    cell.className = "grid-cell-guide";
    cell.textContent = i + 1;
    gridOverlayEl.appendChild(cell);
  }
}

function createPuzzlePieces() {
  trayEl.innerHTML = "";
  boardEl.querySelectorAll(".puzzle-piece").forEach(el => el.remove());
  pieceElements = [];

  const N = CONFIG.GRID_SIZE;
  const boardRect = boardEl.getBoundingClientRect();
  const cellW = boardRect.width / N;
  const cellH = boardRect.height / N;

  for (let r = 0; r < N; r++) {
    for (let c = 0; c < N; c++) {
      const idx = r * N + c;
      const isUnlockedByQuiz = state.unlockedPieceIndices.includes(idx);
      const placedCellIdx = state.boardOccupancy.indexOf(idx);

      const piece = document.createElement("div");
      piece.className = "puzzle-piece";
      piece.dataset.index = idx;
      piece.dataset.row = r;
      piece.dataset.col = c;
      piece.setAttribute("role", "button");
      piece.setAttribute("aria-label", `Puzzle piece ${idx + 1}`);

      // Size & Background Slicing for Square Pieces
      piece.style.width = `${cellW}px`;
      piece.style.height = `${cellH}px`;
      piece.style.backgroundSize = "400% 400%";
      const posX = (c / (N - 1)) * 100;
      const posY = (r / (N - 1)) * 100;
      piece.style.backgroundPosition = `${posX}% ${posY}%`;

      if (!isUnlockedByQuiz) {
        piece.classList.add("quiz-locked");
        const lockOverlay = document.createElement("div");
        lockOverlay.className = "piece-lock-overlay";
        lockOverlay.innerHTML = `🔒`;
        piece.appendChild(lockOverlay);
      }

      attachPiecePointerEvents(piece, idx);
      pieceElements[idx] = piece;

      if (placedCellIdx !== -1) {
        piece.classList.add("on-board");
        boardEl.appendChild(piece);
        positionPieceInBoardCell(piece, placedCellIdx);
      } else {
        trayEl.appendChild(piece);
        positionPieceInTray(piece, idx);
      }
    }
  }

  updateProgress();
}

function positionPieceInBoardCell(piece, cellIdx) {
  const N = CONFIG.GRID_SIZE;
  const boardRect = boardEl.getBoundingClientRect();
  const cellW = boardRect.width / N;
  const cellH = boardRect.height / N;

  const r = Math.floor(cellIdx / N);
  const c = cellIdx % N;

  piece.style.left = `${c * cellW}px`;
  piece.style.top = `${r * cellH}px`;
  piece.style.transform = "rotate(0deg)";
}

function positionPieceInTray(piece, idx) {
  const trayRect = trayEl.getBoundingClientRect();
  const pieceRect = piece.getBoundingClientRect();

  let pos = state.trayPositions[idx];
  if (!pos) {
    const maxLeft = Math.max(10, trayRect.width - pieceRect.width - 10);
    const maxTop = Math.max(10, trayRect.height - pieceRect.height - 10);
    const xRatio = Math.random() * (maxLeft / (trayRect.width || 1));
    const yRatio = Math.random() * (maxTop / (trayRect.height || 1));

    pos = { xRatio, yRatio };
    state.trayPositions[idx] = pos;
    saveState();
  }

  const left = pos.xRatio * trayRect.width;
  const top = pos.yRatio * trayRect.height;

  piece.style.left = `${left}px`;
  piece.style.top = `${top}px`;
  piece.style.transform = "rotate(0deg)";
}

function handleResize() {
  const N = CONFIG.GRID_SIZE;
  const boardRect = boardEl.getBoundingClientRect();
  const cellW = boardRect.width / N;
  const cellH = boardRect.height / N;

  for (let idx = 0; idx < N * N; idx++) {
    const piece = pieceElements[idx];
    if (!piece) continue;

    piece.style.width = `${cellW}px`;
    piece.style.height = `${cellH}px`;

    const placedCellIdx = state.boardOccupancy.indexOf(idx);
    if (placedCellIdx !== -1) {
      positionPieceInBoardCell(piece, placedCellIdx);
    } else {
      positionPieceInTray(piece, idx);
    }
  }
}


/* ==========================================================================
   MOVABLE GRID PIECE POINTER DRAG & DROP
   ========================================================================== */

function attachPiecePointerEvents(piece, idx) {
  piece.addEventListener("pointerdown", (e) => {
    // Check if unlocked via Quiz
    if (!state.unlockedPieceIndices.includes(idx)) {
      const qIdx = CONFIG.QUESTION_PIECE_MAP.indexOf(idx);
      if (qIdx !== -1) {
        openQuizModal(QUESTIONS[qIdx]);
      }
      return;
    }

    e.preventDefault();
    initAudio();

    dragStartTime = Date.now();
    dragStartX = e.clientX;
    dragStartY = e.clientY;

    activeDragPiece = piece;
    piece.classList.add("dragging");

    // Track if piece came from a board cell
    dragStartSourceCell = state.boardOccupancy.indexOf(idx);

    // Append to board container during drag for unified coordinate space
    const initialRect = piece.getBoundingClientRect();
    if (piece.parentElement !== boardEl) {
      boardEl.appendChild(piece);
    }
    const boardRect = boardEl.getBoundingClientRect();

    dragOffset.x = e.clientX - initialRect.left;
    dragOffset.y = e.clientY - initialRect.top;

    const newLeft = e.clientX - boardRect.left - dragOffset.x;
    const newTop = e.clientY - boardRect.top - dragOffset.y;

    piece.style.left = `${newLeft}px`;
    piece.style.top = `${newTop}px`;
    piece.style.zIndex = "2000";

    try {
      piece.setPointerCapture(e.pointerId);
    } catch (err) { }
  });

  piece.addEventListener("pointermove", (e) => {
    if (activeDragPiece !== piece) return;
    e.preventDefault();

    const boardRect = boardEl.getBoundingClientRect();
    const newLeft = e.clientX - boardRect.left - dragOffset.x;
    const newTop = e.clientY - boardRect.top - dragOffset.y;

    piece.style.left = `${newLeft}px`;
    piece.style.top = `${newTop}px`;
  });

  const onPointerUpOrCancel = (e) => {
    if (activeDragPiece !== piece) return;
    e.preventDefault();
    piece.classList.remove("dragging");
    activeDragPiece = null;

    try {
      piece.releasePointerCapture(e.pointerId);
    } catch (err) { }

    handlePieceDrop(piece, idx);
  };

  piece.addEventListener("pointerup", onPointerUpOrCancel);
  piece.addEventListener("pointercancel", onPointerUpOrCancel);
}

function handlePieceDrop(piece, idx) {
  const N = CONFIG.GRID_SIZE;
  const boardRect = boardEl.getBoundingClientRect();
  const cellW = boardRect.width / N;
  const cellH = boardRect.height / N;

  const pieceRect = piece.getBoundingClientRect();
  const pieceCenterX = pieceRect.left + pieceRect.width / 2;
  const pieceCenterY = pieceRect.top + pieceRect.height / 2;

  // Check if dropped inside board bounds
  const droppedInsideBoard = (
    pieceCenterX >= boardRect.left - cellW * 0.2 &&
    pieceCenterX <= boardRect.right + cellW * 0.2 &&
    pieceCenterY >= boardRect.top - cellH * 0.2 &&
    pieceCenterY <= boardRect.bottom + cellH * 0.2
  );

  if (droppedInsideBoard) {
    // Determine closest cell index (0..15)
    const relX = Math.max(0, Math.min(boardRect.width - 1, pieceCenterX - boardRect.left));
    const relY = Math.max(0, Math.min(boardRect.height - 1, pieceCenterY - boardRect.top));

    const col = Math.floor(relX / cellW);
    const row = Math.floor(relY / cellH);
    const targetCellIdx = row * N + col;

    // Check if target cell already has another piece
    const existingPieceIdx = state.boardOccupancy[targetCellIdx];

    if (existingPieceIdx !== null && existingPieceIdx !== idx) {
      // SWAP OR displacement!
      if (dragStartSourceCell !== -1) {
        // Move existing piece into drag's source cell
        state.boardOccupancy[dragStartSourceCell] = existingPieceIdx;
        const existingPiece = pieceElements[existingPieceIdx];
        if (existingPiece) {
          positionPieceInBoardCell(existingPiece, dragStartSourceCell);
        }
      } else {
        // Came from tray -> Evict existing piece back to tray
        state.boardOccupancy[targetCellIdx] = null;
        const existingPiece = pieceElements[existingPieceIdx];
        if (existingPiece) {
          existingPiece.classList.remove("on-board");
          trayEl.appendChild(existingPiece);
          positionPieceInTray(existingPiece, existingPieceIdx);
        }
      }
    } else if (dragStartSourceCell !== -1 && dragStartSourceCell !== targetCellIdx) {
      // Clear old cell if moved to a different empty cell
      state.boardOccupancy[dragStartSourceCell] = null;
    }

    // Place piece in target cell
    state.boardOccupancy[targetCellIdx] = idx;
    piece.classList.add("on-board");
    if (piece.parentElement !== boardEl) boardEl.appendChild(piece);
    positionPieceInBoardCell(piece, targetCellIdx);

    piece.classList.add("snap-lock-anim");
    setTimeout(() => piece.classList.remove("snap-lock-anim"), 400);
    playSnapSound();
  } else {
    // Dropped outside board -> Remove from board cell and return to tray
    if (dragStartSourceCell !== -1) {
      state.boardOccupancy[dragStartSourceCell] = null;
    }

    piece.classList.remove("on-board");
    if (piece.parentElement !== trayEl) trayEl.appendChild(piece);

    const trayRect = trayEl.getBoundingClientRect();
    const currentPieceRect = piece.getBoundingClientRect();

    let left = currentPieceRect.left - trayRect.left;
    let top = currentPieceRect.top - trayRect.top;
    left = Math.max(0, Math.min(trayRect.width - currentPieceRect.width, left));
    top = Math.max(0, Math.min(trayRect.height - currentPieceRect.height, top));

    state.trayPositions[idx] = {
      xRatio: left / (trayRect.width || 1),
      yRatio: top / (trayRect.height || 1)
    };

    piece.style.left = `${left}px`;
    piece.style.top = `${top}px`;
    piece.style.zIndex = "10";
  }

  saveState();
  updateProgress();
}



/* ==========================================================================
   PROGRESS & COMPLETION REVEAL FLOW
   ========================================================================== */

function updateProgress() {
  const solvedCount = state.solvedQuestionIds.length;
  // Placed count is total non-null entries on board
  const placedCount = state.boardOccupancy.filter(val => val !== null).length;

  solvedCountEl.textContent = solvedCount;
  placedCountEl.textContent = placedCount;

  // Check if puzzle is fully and CORRECTLY completed
  // All 16 questions solved AND boardOccupancy[i] === i for all i = 0..15
  const isCorrectlyAssembled = state.boardOccupancy.every((pieceIdx, cellIdx) => pieceIdx === cellIdx);

  if (solvedCount === CONFIG.GRID_SIZE * CONFIG.GRID_SIZE &&
    isCorrectlyAssembled &&
    !state.completed) {
    onPuzzleCompleted();
  }
}

async function onPuzzleCompleted() {
  state.completed = true;

  boardEl.classList.add("all-locked");
  goldSweepEl.classList.add("active");


  try {
    const response = await fetch("/api/reveal");

    if (!response.ok) {
      throw new Error("Reveal unavailable.");
    }

    const decryptedData = await response.json();

    backTitleEl.textContent = decryptedData.title;
    backSubtitleEl.textContent = decryptedData.subtitle;

  } catch (err) {
    backTitleEl.textContent = "BACK STAIRS LIFT";
    backSubtitleEl.textContent = "The Gamemakers await you there.";
  }


  setTimeout(() => {
    tapRevealBtn.classList.remove("hidden");
  }, 1500);
}

async function decryptRevealData(passphrase, encryptedObj) {
  const enc = new TextEncoder();
  const passphraseBytes = enc.encode(passphrase);

  const salt = new Uint8Array(atob(encryptedObj.salt).split("").map(c => c.charCodeAt(0)));
  const iv = new Uint8Array(atob(encryptedObj.iv).split("").map(c => c.charCodeAt(0)));
  const cipherBytes = new Uint8Array(atob(encryptedObj.ciphertext).split("").map(c => c.charCodeAt(0)));

  const baseKey = await crypto.subtle.importKey("raw", passphraseBytes, "PBKDF2", false, ["deriveKey"]);
  const derivedKey = await crypto.subtle.deriveKey(
    { name: "PBKDF2", salt: salt, iterations: 100000, hash: "SHA-256" },
    baseKey,
    { name: "AES-GCM", length: 256 },
    false,
    ["decrypt"]
  );

  const decryptedBuf = await crypto.subtle.decrypt({ name: "AES-GCM", iv: iv }, derivedKey, cipherBytes);
  return JSON.parse(new TextDecoder().decode(decryptedBuf));
}

function handleTapToReveal() {
  if (state.flipped) return;
  state.flipped = true;

  playCannonBoom();

  appContainerEl.classList.add("screen-shake");
  document.body.classList.add("flipping");
  setTimeout(() => appContainerEl.classList.remove("screen-shake"), 650);

  flipCardEl.classList.add("flipped");

  tapRevealBtn.classList.add("hidden");
  setTimeout(() => {
    flipBackBtn.classList.remove("hidden");
  }, CONFIG.FLIP_DURATION_MS);
}

function handleFlipBack() {
  state.flipped = false;
  flipCardEl.classList.remove("flipped");
  document.body.classList.remove("flipping");
  flipBackBtn.classList.add("hidden");
  tapRevealBtn.classList.remove("hidden");
}


/* ==========================================================================
   HINT & RESET CONTROLS
   ========================================================================== */

function handleHint() {
  if (state.hintsLeft <= 0) return;

  state.hintsLeft--;
  hintCountEl.textContent = state.hintsLeft;
  if (state.hintsLeft === 0) hintBtn.disabled = true;
  saveState();

  hintPreviewEl.classList.add("active");
  setTimeout(() => {
    hintPreviewEl.classList.remove("active");
  }, CONFIG.HINT_DURATION_MS);
}

function openResetModal() {
  resetModalEl.classList.remove("hidden");
}

function closeResetModal() {
  resetModalEl.classList.add("hidden");
}

function confirmReset() {
  closeResetModal();
  state.solvedQuestionIds = [];
  state.unlockedPieceIndices = [];
  state.boardOccupancy = Array(16).fill(null);
  state.trayPositions = {};
  state.wrongAttempts = {};
  state.cooldownTimestamps = {};
  state.completed = false;
  state.flipped = false;
  state.hintsLeft = CONFIG.HINT_LIMIT;
  hintCountEl.textContent = state.hintsLeft;
  hintBtn.disabled = false;

  boardEl.classList.remove("all-locked");
  goldSweepEl.classList.remove("active");
  flipCardEl.classList.remove("flipped");
  tapRevealBtn.classList.add("hidden");
  flipBackBtn.classList.add("hidden");
  document.body.classList.remove("flipping");

  saveState();
  renderQuestionsGrid();
  createPuzzlePieces();
}


/* ==========================================================================
   AUDIO TOGGLE & PARTICLE CANVAS
   ========================================================================== */

function toggleSound() {
  state.soundEnabled = !state.soundEnabled;
  if (state.soundEnabled) {
    soundIconOff.classList.add("hidden");
    soundIconOn.classList.remove("hidden");
    initAudio();
  } else {
    soundIconOn.classList.add("hidden");
    soundIconOff.classList.remove("hidden");
  }
  saveState();
}

function initParticleCanvas() {
  const canvas = document.getElementById("bg-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  let width = (canvas.width = window.innerWidth);
  let height = (canvas.height = window.innerHeight);

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  const particleCount = 45;
  const particles = [];

  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      r: Math.random() * 2 + 0.8,
      speedY: Math.random() * 0.4 + 0.15,
      oscAmp: Math.random() * 1.5 + 0.5,
      oscSpeed: Math.random() * 0.02 + 0.005,
      angle: Math.random() * Math.PI * 2,
      opacity: Math.random() * 0.6 + 0.2
    });
  }

  function render() {
    ctx.clearRect(0, 0, width, height);
    for (let p of particles) {
      p.y -= p.speedY;
      p.angle += p.oscSpeed;
      p.x += Math.sin(p.angle) * p.oscAmp * 0.2;

      if (p.y < -10) {
        p.y = height + 10;
        p.x = Math.random() * width;
      }

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(241, 213, 122, ${p.opacity})`;
      ctx.shadowBlur = 8;
      ctx.shadowColor = "#d4af37";
      ctx.fill();
    }
    requestAnimationFrame(render);
  }

  window.addEventListener("resize", () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  });

  render();
}


/* ==========================================================================
   INITIALIZATION
   ========================================================================== */

function initApp() {
  loadState();

  if (state.soundEnabled) {
    soundIconOff.classList.add("hidden");
    soundIconOn.classList.remove("hidden");
  } else {
    soundIconOn.classList.add("hidden");
    soundIconOff.classList.remove("hidden");
  }

  hintCountEl.textContent = state.hintsLeft;
  if (state.hintsLeft === 0) hintBtn.disabled = true;

  setupGridGuide();
  renderQuestionsGrid();
  createPuzzlePieces();

  // Control Listeners
  hintBtn.addEventListener("click", handleHint);
  resetBtn.addEventListener("click", openResetModal);
  modalCancelBtn.addEventListener("click", closeResetModal);
  modalConfirmBtn.addEventListener("click", confirmReset);
  tapRevealBtn.addEventListener("click", handleTapToReveal);
  flipBackBtn.addEventListener("click", handleFlipBack);
  soundToggleBtn.addEventListener("click", toggleSound);

  // Quiz Modal Listeners
  quizCloseBtnEl.addEventListener("click", closeQuizModal);
  quizModalCancelBtnEl.addEventListener("click", closeQuizModal);
  quizSubmitBtnEl.addEventListener("click", handleQuizSubmit);
  quizAnswerInputEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter") handleQuizSubmit();
  });



  window.addEventListener("resize", handleResize);
  initParticleCanvas();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initApp);
} else {
  initApp();
}
