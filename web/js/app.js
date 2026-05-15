/**
 * MNIST Digit Classifier - JavaScript Application
 * Updated for Obsidian Theme
 */

// Constants
const CANVAS_SIZE = 280;
const MODEL_SIZE = 28;
const DRAW_COLOR = '#ffffff'; // White ink for dark theme
const BG_COLOR = '#000000';   // Pure black for better MNIST compatibility
const AUTO_PREDICT_DELAY = 500;

// State
let canvas, ctx;
let isDrawing = false;
let session = null;
let lastPredictionTime = 0;
let drawingHistory = [];
let predictions = [];
let autoPredict = true;

// UI Elements
const drawingCanvas = document.getElementById('drawingCanvas');
const clearBtn = document.getElementById('clearBtn');
const undoBtn = document.getElementById('undoBtn');
const predictBtn = document.getElementById('predictBtn');
const predictionDigit = document.getElementById('predictionDigit');
const predictionConfidence = document.getElementById('predictionConfidence');
const probabilitiesGrid = document.getElementById('probabilitiesGrid');
const statusText = document.getElementById('status');
const inferenceTimeText = document.getElementById('inferenceTime');
const loadingOverlay = document.getElementById('loadingOverlay');

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    await init();
});

/**
 * Initialize the application
 */
async function init() {
    console.log('🚀 Initializing MNIST Digit Classifier (Obsidian Edition)...');
    
    // Setup canvas
    setupCanvas();
    
    // Load ONNX model
    await loadModel();
    
    // Setup event listeners
    setupEventListeners();
    
    // Initialize probability display
    initProbabilities();
    
    // Hide loading overlay
    if (loadingOverlay) {
        loadingOverlay.classList.add('hidden');
    }
    
    console.log('✅ Application initialized successfully!');
}

/**
 * Setup canvas properties and context
 */
function setupCanvas() {
    canvas = drawingCanvas;
    if (!canvas) return;

    ctx = canvas.getContext('2d', { willReadFrequently: true });
    
    // Set dimensions based on CSS or default
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width || CANVAS_SIZE;
    canvas.height = canvas.width;
    
    // Configure canvas context
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.lineWidth = 20; // Thicker stroke for better digit recognition
    ctx.fillStyle = BG_COLOR;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

/**
 * Load ONNX model
 */
async function loadModel() {
    console.log('🤖 Loading ONNX model...');
    try {
        // Modern ONNX Runtime configuration
        const ortConfig = {
            executionProviders: ['wasm'], // Use 'wasm' for best cross-browser support
            graphOptimizationLevel: 'all',
        };
        
        // Set WASM paths explicitly to the same CDN version as index.html
        // This ensures the wasm files are found even if not in the local folder
        if (typeof ort !== 'undefined' && ort.env && ort.env.wasm) {
            ort.env.wasm.wasmPaths = 'https://cdn.jsdelivr.net/npm/onnxruntime-web/dist/';
        }
        
        // Model path relative to index.html
        const modelPath = 'models/mnist_cnn.onnx';
        
        console.log(`📡 Fetching model from: ${modelPath}`);
        
        // Load the session
        session = await ort.InferenceSession.create(modelPath, ortConfig);
        
        console.log('✅ ONNX Model Loaded Successfully');
        console.log('Input names:', session.inputNames);
        console.log('Output names:', session.outputNames);
        
        if (statusText) statusText.textContent = 'Modelo ONNX Ativo';
    } catch (error) {
        console.error('❌ CRITICAL: Failed to load ONNX model:', error);
        session = null;
        if (statusText) statusText.textContent = 'Erro ao carregar modelo';
        
        // Detailed error for the user
        const errorMsg = error.message || 'Unknown error';
        alert(`Falha ao carregar o modelo de IA: ${errorMsg}\n\nVerifique se o arquivo 'web/models/mnist_cnn.onnx' existe e se você está usando um servidor local (http://localhost).`);
    }
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Canvas events
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);
    
    // Touch events
    canvas.addEventListener('touchstart', (e) => { e.preventDefault(); handleTouch(e); });
    canvas.addEventListener('touchmove', (e) => { e.preventDefault(); handleTouch(e); });
    canvas.addEventListener('touchend', stopDrawing);
    
    // Button events
    clearBtn.addEventListener('click', clearCanvas);
    undoBtn.addEventListener('click', undoDrawing);
    predictBtn.addEventListener('click', predict);
}

/**
 * Initialize probability display
 */
function initProbabilities() {
    probabilitiesGrid.innerHTML = '';
    
    for (let i = 0; i < 10; i++) {
        const div = document.createElement('div');
        div.className = 'probability-item';
        div.setAttribute('data-digit', i);
        div.innerHTML = `
            <div class="probability-bar" style="height: 0px;"></div>
            <div class="probability-digit">${i}</div>
        `;
        probabilitiesGrid.appendChild(div);
    }
}

/**
 * Start drawing
 */
function startDrawing(e) {
    isDrawing = true;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    drawingHistory.push(canvas.toDataURL());
    
    ctx.beginPath();
    ctx.moveTo(x, y);
    
    // Hide instruction text on first stroke
    const instruction = document.querySelector('.instruction');
    if (instruction) instruction.style.opacity = '0';
}

/**
 * Draw on canvas
 */
function draw(e) {
    if (!isDrawing) return;
    
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    ctx.strokeStyle = DRAW_COLOR;
    ctx.lineTo(x, y);
    ctx.stroke();
    
    // Auto-predict after delay
    if (autoPredict && Date.now() - lastPredictionTime > AUTO_PREDICT_DELAY) {
        predict();
        lastPredictionTime = Date.now();
    }
}

/**
 * Handle touch events
 */
function handleTouch(e) {
    const touch = e.touches[0];
    const rect = canvas.getBoundingClientRect();
    const mouseEvent = new MouseEvent(e.type === 'touchstart' ? 'mousedown' : 'mousemove', {
        clientX: touch.clientX,
        clientY: touch.clientY,
    });
    canvas.dispatchEvent(mouseEvent);
}

/**
 * Stop drawing
 */
function stopDrawing() {
    if (isDrawing) {
        isDrawing = false;
        ctx.closePath();
    }
}

/**
 * Clear canvas
 */
function clearCanvas() {
    ctx.fillStyle = BG_COLOR;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    drawingHistory = [];
    
    // Reset UI
    predictionDigit.textContent = '?';
    predictionConfidence.textContent = '0%';
    const instruction = document.querySelector('.instruction');
    if (instruction) instruction.style.opacity = '1';
    
    // Reset probabilities
    document.querySelectorAll('.probability-item').forEach(item => {
        item.classList.remove('winner');
        item.querySelector('.probability-bar').style.height = '0px';
    });
}

/**
 * Undo last action
 */
function undoDrawing() {
    if (drawingHistory.length > 0) {
        const lastState = drawingHistory.pop();
        const img = new Image();
        img.src = lastState;
        img.onload = () => {
            ctx.fillStyle = BG_COLOR;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0);
            predict();
        };
    } else {
        clearCanvas();
    }
}

/**
 * Preprocess image for MNIST (expects white on black, centered, 20x20 inside 28x28)
 */
function preprocessImage() {
    // 1. Find the bounding box of the drawing
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;
    let minX = canvas.width, minY = canvas.height, maxX = 0, maxY = 0;
    let found = false;

    for (let y = 0; y < canvas.height; y++) {
        for (let x = 0; x < canvas.width; x++) {
            const i = (y * canvas.width + x) * 4;
            // Since it's white on black, checking any channel is enough
            if (data[i] > 20) { 
                minX = Math.min(minX, x);
                minY = Math.min(minY, y);
                maxX = Math.max(maxX, x);
                maxY = Math.max(maxY, y);
                found = true;
            }
        }
    }

    if (!found) return new Float32Array(MODEL_SIZE * MODEL_SIZE);

    // 2. Extract and rescale to 20x20
    const boxW = maxX - minX + 1;
    const boxH = maxY - minY + 1;
    
    const tempCanvas = document.createElement('canvas');
    const tempCtx = tempCanvas.getContext('2d');
    
    // Calculate scale to fit in 20x20
    const scale = 20 / Math.max(boxW, boxH);
    const sw = boxW * scale;
    const sh = boxH * scale;

    // 3. Center in 28x28
    tempCanvas.width = MODEL_SIZE;
    tempCanvas.height = MODEL_SIZE;
    tempCtx.fillStyle = BG_COLOR;
    tempCtx.fillRect(0, 0, MODEL_SIZE, MODEL_SIZE);
    
    // Draw centered
    const dx = (MODEL_SIZE - sw) / 2;
    const dy = (MODEL_SIZE - sh) / 2;
    tempCtx.drawImage(canvas, minX, minY, boxW, boxH, dx, dy, sw, sh);

    // 4. Final normalization
    const finalData = tempCtx.getImageData(0, 0, MODEL_SIZE, MODEL_SIZE).data;
    const input = new Float32Array(MODEL_SIZE * MODEL_SIZE);
    
    for (let i = 0; i < finalData.length; i += 4) {
        // Luminosity method (already grayscale from our drawing)
        input[i / 4] = finalData[i] / 255;
    }
    
    return input;
}

/**
 * Make prediction
 */
async function predict() {
    if (!session) {
        console.warn('Inference skipped: Model not loaded');
        return;
    }

    const startTime = performance.now();
    
    try {
        const input = preprocessImage();
        const tensor = new ort.Tensor('float32', input, [1, 1, MODEL_SIZE, MODEL_SIZE]);
        
        // Dynamically map input/output names from the session
        const inputName = session.inputNames[0];
        const outputName = session.outputNames[0];
        
        const feeds = {};
        feeds[inputName] = tensor;
        
        const results = await session.run(feeds);
        const output = results[outputName].data;
        const probabilities = softmax(Array.from(output));
        
        const maxIdx = probabilities.indexOf(Math.max(...probabilities));
        const confidence = probabilities[maxIdx];
        
        displayResults({
            digit: maxIdx,
            confidence: confidence,
            probabilities: probabilities
        });
        
        const endTime = performance.now();
        if (inferenceTimeText) {
            inferenceTimeText.textContent = `${(endTime - startTime).toFixed(1)}ms`;
        }
        
    } catch (error) {
        console.error('❌ Inference error:', error);
    }
}

function softmax(arr) {
    const maxVal = Math.max(...arr);
    const exps = arr.map(x => Math.exp(x - maxVal));
    const sumExps = exps.reduce((a, b) => a + b);
    return exps.map(x => x / sumExps);
}

function generateDemoPrediction() {
    const digit = Math.floor(Math.random() * 10);
    const probabilities = new Array(10).fill(0).map(() => Math.random() * 0.1);
    probabilities[digit] = 0.8 + Math.random() * 0.19;
    const sum = probabilities.reduce((a, b) => a + b);
    return {
        digit,
        confidence: probabilities[digit] / sum,
        probabilities: probabilities.map(p => p / sum)
    };
}

/**
 * Display results in UI
 */
function displayResults(results) {
    const { digit, confidence, probabilities } = results;
    
    predictionDigit.textContent = digit;
    predictionConfidence.textContent = (confidence * 100).toFixed(1) + '%';
    
    const items = document.querySelectorAll('.probability-item');
    const maxBarHeight = 100; // px
    
    items.forEach((item, index) => {
        const prob = probabilities[index];
        const bar = item.querySelector('.probability-bar');
        
        bar.style.height = (prob * maxBarHeight) + 'px';
        
        if (index === digit) {
            item.classList.add('winner');
        } else {
            item.classList.remove('winner');
        }
    });
}
