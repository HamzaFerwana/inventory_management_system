const MAX_ROWS = 6, COLS = 5;
const boardEl = document.getElementById("board");
const keyboardEl = document.getElementById("keyboard");
const toast = document.getElementById("toast");


let validWordsCache = new Set();
let ANSWER = "";
let grid = Array.from({ length: MAX_ROWS }, () => Array(COLS).fill(""));
let row = 0, col = 0, isGameOver = false;

function toastShow(msg) {
    toast.innerText = msg;
    toast.style.display = "block";
    setTimeout(() => toast.style.display = "none", 1500);
}

function toggleShakeRow() {
    const currentRow = document.querySelectorAll(".row")[row];
    if (!currentRow) return;
    const tiles = currentRow.querySelectorAll(".tile");

    tiles.forEach(tile => {
        tile.classList.add("shake");
        tile.dataset.oldClass = tile.className;
        tile.style.backgroundColor = "#dc2626"; 
        tile.style.border = "2px solid black";

        setTimeout(() => {
            tile.classList.remove("shake");
            tile.className = tile.dataset.oldClass;
            tile.style.backgroundColor = "";
            tile.style.border = "";
        }, 500);
    });
}

function buildBoard() {
    boardEl.innerHTML = "";
    for (let r = 0; r < MAX_ROWS; r++) {
        const rowEl = document.createElement("div");
        rowEl.className = "row";
        if (r === 0) rowEl.classList.add("active");
        for (let c = 0; c < COLS; c++) {
            const tile = document.createElement("div");
            tile.className = "tile";
            tile.id = `tile-${r}-${c}`;
            rowEl.appendChild(tile);
        }
        boardEl.appendChild(rowEl);
    }
}

function buildKeyboard() {
    keyboardEl.innerHTML = "";
    const keys = "QWERTYUIOPASDFGHJKLZXCVBNM".split("");
    keys.forEach(k => {
        const btn = document.createElement("button");
        btn.className = "key";
        btn.textContent = k;
        btn.onclick = () => handleKey(k);
        keyboardEl.appendChild(btn);
    });
    const enter = document.createElement("button");
    enter.className = "key";
    enter.textContent = "ENTER";
    enter.onclick = () => handleKey("Enter");
    keyboardEl.appendChild(enter);

    const back = document.createElement("button");
    back.className = "key";
    back.textContent = "⌫";
    back.onclick = () => handleKey("Backspace");
    keyboardEl.appendChild(back);
}

function updateTiles() {
    for (let r = 0; r < MAX_ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            document.getElementById(`tile-${r}-${c}`).textContent = grid[r][c];
        }
    }
}

async function handleKey(key) {
    if (isGameOver) return;
    if (key === "Backspace") {
        if (col > 0) { 
            col--; 
            grid[row][col] = ""; 
            updateTiles(); 
        }
        return;
    }
    if (key === "Enter") { 
        await validatedSubmit(); 
        return; 
    }
    if (key.length === 1 && col < COLS) {
        grid[row][col] = key.toUpperCase();
        col++;
        updateTiles();
    }
}


async function fetchValidWords(count = 5000000,word) {
    try {
        const res = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${word}`);
        if (!res.ok) throw new Error("Failed to fetch words");
        const words = await res.json();
        words.forEach(word => validWordsCache.add(word.toLowerCase()));
        console.log(`Loaded ${validWordsCache.size} words into cache`);
        return words;
    } catch (error) {
        console.error("Error fetching words:", error);
        return [];
    }
}


function isValidWord(word) {
    word = word.toLowerCase();
    return validWordsCache.has(word);
}
async function apiIsRealWord(word) {
    try {
        const res = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${word}`);
        return res.ok;   // true = valid English word
    } catch (e) {
        return false;
    }
}


async function validatedSubmit() {
    if (col < COLS) {
        toastShow("Word is incomplete");
        toggleShakeRow();
        return;
    }

    const guess = grid[row].join("").toLowerCase();


    if (/^([a-zA-Z])\1{4}$/.test(guess)) {
        toastShow("Invalid word!");
        toggleShakeRow();
        return;
    }


    const isReal = await apiIsRealWord(guess);

    if (!isReal) {
        toastShow("Word not in dictionary!");
        toggleShakeRow();
        return;
    }

    checkGuess(guess.toUpperCase());
}

function updateKeyboard(guess, status) {
    for (let i = 0; i < COLS; i++) {
        const letter = guess[i].toUpperCase();
        const btn = Array.from(keyboardEl.children).find(b => b.textContent === letter);
        if (!btn) continue;
        
        const currentBg = btn.style.backgroundColor;
        if (status[i] === "correct") {
            btn.style.backgroundColor = "#16a34a";
        } else if (status[i] === "present" && currentBg !== "rgb(22, 163, 74)") {
            btn.style.backgroundColor = "#f59e0b";
        } else if (status[i] === "absent" && !["rgb(22, 163, 74)", "rgb(245, 158, 11)"].includes(currentBg)) {
            btn.style.backgroundColor = "#334155";
        }
    }
}

function checkGuess(guess) {
    const answerChars = ANSWER.split("");
    let status = Array(COLS).fill("absent");
    let taken = Array(COLS).fill(false);

    for (let i = 0; i < COLS; i++) {
        if (guess[i] === answerChars[i]) { 
            status[i] = "correct"; 
            taken[i] = true; 
        }
    }
    

    for (let i = 0; i < COLS; i++) {
        if (status[i] !== "correct") {
            for (let j = 0; j < COLS; j++) {
                if (!taken[j] && guess[i] === answerChars[j]) { 
                    status[i] = "present"; 
                    taken[j] = true; 
                    break; 
                }
            }
        }
    }


    for (let i = 0; i < COLS; i++) {
        document.getElementById(`tile-${row}-${i}`).classList.add(status[i]);
    }
    
    updateKeyboard(guess, status);

    if (guess.toUpperCase() === ANSWER.toUpperCase()) {
        toastShow("Great Job!");
        isGameOver = true;
        setTimeout(resetGame, 2000);
        return;
    }
    
    row++;
    col = 0;
    
    if (row >= MAX_ROWS) {
        toastShow(`OOPs! You Lost. The word was: ${ANSWER}`);
        isGameOver = true;
        setTimeout(resetGame, 2000);
    }

    document.querySelectorAll(".row").forEach(r => r.classList.remove("active"));
    if (!isGameOver) document.querySelectorAll(".row")[row].classList.add("active");
}

document.addEventListener("keydown", (e) => {
    if (e.key === "Enter") handleKey("Enter");
    else if (e.key === "Backspace") handleKey("Backspace");
    else if (/^[a-zA-Z]$/.test(e.key)) handleKey(e.key.toUpperCase());
});

document.getElementById("btn-reset").onclick = () => resetGame();
document.getElementById("btn-reveal").onclick = () => toastShow(`Word: ${ANSWER}`);

function resetGame() {
    grid = Array.from({ length: MAX_ROWS }, () => Array(COLS).fill(""));
    row = 0; 
    col = 0; 
    isGameOver = false;
    
    document.querySelectorAll(".tile").forEach(t => { 
        t.textContent = ""; 
        t.className = "tile"; 
    });
    
    Array.from(keyboardEl.children).forEach(btn => {
        btn.style.backgroundColor = "";
    });
    
    document.querySelectorAll(".row").forEach(r => r.classList.remove("active"));
    document.querySelectorAll(".row")[0]?.classList.add("active");
    
    fetchNewWord();
}

async function fetchNewWord() {
    try {
        let validWord = false;
        let word = "";

        while (!validWord) {
            const res = await fetch("https://random-word-api.herokuapp.com/word?length=5&number=1");
            const data = await res.json();
            word = data[0].toLowerCase();

            // Check if the word exists in the dictionary API
            const apiRes = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${word}`);
            if (apiRes.ok) {
                validWord = true;
            }
        }

        ANSWER = word.toUpperCase();
        validWordsCache.add(word); // optional: add to cache
        console.log("New Answer:", ANSWER);
    } catch (error) {
        console.error(error);
        toastShow("Error fetching word!");
    }
}


async function initGame() {
    buildBoard(); 
    buildKeyboard(); 
    updateTiles(); 
    
    toastShow("Loading word dictionary...");
    await Promise.all([
        fetchValidWords(500),
        fetchValidWords(500),
        fetchValidWords(500)
    ]);
    
    await fetchNewWord();
    toastShow("Game ready!");
}

initGame();