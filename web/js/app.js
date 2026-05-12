/**
 * MNIST Digit Classifier - JavaScript Application
 * Main application logic for drawing and real-time prediction
 */

// Constants
const CANVAS_SIZE = 280;
const MODEL_SIZE = 28;
const DRAW_COLOR = '#000000';
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
const confidenceFill = document.getElementById('confidenceFill');
const confidenceText = document.getElementById('confidenceText');
const probabilitiesGrid = document.getElementById('probabilitiesGrid');
const brushSizeSlider = document.getElementById('brushSize');
const brushSizeValue = document.getElementById('brushSizeValue');
const statusText = document.getElementById('status');
const inferenceTimeText = document.getElementById('inferenceTime');
const gallery = document.getElementById('gallery');
const loadingOverlay = document.getElementById('loadingOverlay');

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    await init();
});

/**
 * Initialize the application
 */
async function init() {
    console.log('🚀 Initializing MNIST Digit Classifier...');
    
    // Setup canvas
    setupCanvas();
    
    // Load ONNX model
    await loadModel();
    
    // Setup event listeners
    setupEventListeners();
    
    // Initialize probability display
    initProbabilities();
    
    // Hide loading overlay
    loadingOverlay.classList.add('hidden');
    
    console.log('✅ Application initialized successfully!');
    updateStatus('Pronto! Comece a desenhar');
}

/**
 * Setup canvas properties and context
 */
function setupCanvas() {
    console.log('📐 Setting up canvas...');
    
    canvas = drawingCanvas;
    ctx = canvas.getContext('2d', { willReadFrequently: true });
    
    // Set actual dimensions
    const rect = canvas.getBoundingClientRect();
    canvas.width = Math.min(rect.width, CANVAS_SIZE);
    canvas.height = canvas.width;
    
    // Configure canvas context
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.lineWidth = 15;
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

/**
 * Load ONNX model
 */
async function loadModel() {
    console.log('🤖 Loading ONNX model...');
    updateStatus('Carregando modelo...');
    
    try {
        const ortConfig = {
            executionProviders: ['webassembly'],
            graphOptimizationLevel: 'all',
        };
        
        ort.env.wasm.wasmPaths = 'https://cdn.jsdelivr.net/npm/onnxruntime-web/dist/';
        
        // Try to load from local path first, fallback to CDN
        const modelPath = './models/mnist_cnn.onnx';
        
        try {
            session = await ort.InferenceSession.create(modelPath, ortConfig);
            console.log('✅ Model loaded from local path');
        } catch (e) {
            console.warn('⚠ Local model not found, using placeholder mode');
            console.warn('To enable predictions, run: python convert_to_onnx.py');
            updateStatus('Modelo não encontrado - modo demonstração');
            session = null;
        }
    } catch (error) {
        console.error('❌ Error loading model:', error);
        updateStatus('Erro ao carregar modelo');
        session = null;
    }
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    console.log('🎮 Setting up event listeners...');
    
    // Canvas events
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);
    
    // Touch events for mobile
    canvas.addEventListener('touchstart', handleTouch);
    canvas.addEventListener('touchmove', handleTouch);
    canvas.addEventListener('touchend', stopDrawing);
    
    // Button events
    clearBtn.addEventListener('click', clearCanvas);
    undoBtn.addEventListener('click', undoDrawing);
    predictBtn.addEventListener('click', predict);
    
    // Brush size slider
    brushSizeSlider.addEventListener('input', (e) => {
        const size = e.target.value;
        brushSizeValue.textContent = size + 'px';
        ctx.lineWidth = size;
    });
}

/**
 * Initialize probability display
 */
function initProbabilities() {
    probabilitiesGrid.innerHTML = '';
    
    for (let i = 0; i < 10; i++) {
        const div = document.createElement('div');
        div.className = 'probability-item';
        div.innerHTML = `
            <div class="probability-digit">${i}</div>
            <div class="probability-bar">
                <div class="probability-bar-fill" style="width: 0%;"></div>
            </div>
            <div class="probability-value">0%</div>
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
    
    // Save state for undo
    drawingHistory.push(canvas.toDataURL());
    
    ctx.beginPath();
    ctx.moveTo(x, y);
    
    updateStatus('Desenhando...');
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
    e.preventDefault();
    
    const touch = e.touches[0];
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
        updateStatus('Pronto! Desenhe outro número ou clique predizer');
    }
}

/**
 * Clear canvas
 */
function clearCanvas() {
    console.log('🗑 Clearing canvas...');
    
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    drawingHistory = [];
    
    // Reset prediction display
    predictionDigit.textContent = '?';
    predictionConfidence.textContent = '0%';
    confidenceFill.style.width = '0%';
    confidenceText.textContent = 'Desenhe um número!';
    
    // Reset probabilities
    document.querySelectorAll('.probability-item').forEach(item => {
        item.querySelector('.probability-bar-fill').style.width = '0%';
        item.querySelector('.probability-value').textContent = '0%';
    });
    
    updateStatus('Canvas limpo!');
}

/**
 * Undo last drawing action
 */
function undoDrawing() {
    console.log('↶ Undoing drawing...');
    
    if (drawingHistory.length > 0) {
        drawingHistory.pop();
        
        if (drawingHistory.length > 0) {
            const imageData = new Image();
            imageData.src = drawingHistory[drawingHistory.length - 1];
            imageData.onload = () => {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(imageData, 0, 0);
            };
        } else {
            clearCanvas();
        }
        
        updateStatus('Ação desfeita!');
    }
}

/**
 * Preprocess canvas image for model
 */
function preprocessImage() {
    console.log('🔄 Preprocessing image...');
    
    // Create a temporary canvas for preprocessing
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = MODEL_SIZE;
    tempCanvas.height = MODEL_SIZE;
    const tempCtx = tempCanvas.getContext('2d');
    
    // Fill with white background
    tempCtx.fillStyle = '#ffffff';
    tempCtx.fillRect(0, 0, MODEL_SIZE, MODEL_SIZE);
    
    // Draw the canvas image scaled to 28x28
    tempCtx.drawImage(canvas, 0, 0, MODEL_SIZE, MODEL_SIZE);
    
    // Get image data
    const imageData = tempCtx.getImageData(0, 0, MODEL_SIZE, MODEL_SIZE);
    const data = imageData.data;
    
    // Convert to grayscale and normalize to [0, 1]
    const input = new Float32Array(MODEL_SIZE * MODEL_SIZE);
    
    for (let i = 0; i < data.length; i += 4) {
        const r = data[i];
        const g = data[i + 1];
        const b = data[i + 2];
        
        // Convert to grayscale using luminosity method
        const gray = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
        
        // Invert (MNIST expects white on black)
        input[i / 4] = 1 - gray;
    }
    
    return input;
}

/**
 * Make prediction
 */
async function predict() {
    console.log('🧠 Making prediction...');
    updateStatus('Analisando...');
    
    const startTime = performance.now();
    
    if (!session) {
        console.warn('⚠ Model not loaded');
        
        // Demo prediction
        const demoResults = generateDemoPrediction();
        displayResults(demoResults);
        
        updateStatus('Modo demonstração (modelo não carregado)');
        return;
    }
    
    try {
        // Preprocess image
        const input = preprocessImage();
        
        // Create tensor
        const tensor = new ort.Tensor('float32', input, [1, 1, MODEL_SIZE, MODEL_SIZE]);
        
        // Run inference
        const feeds = { input: tensor };
        const results = await session.run(feeds);
        
        // Get output
        const output = results.output.data;
        
        // Convert to probabilities
        const probabilities = softmax(Array.from(output));
        
        // Get top prediction
        const maxIdx = probabilities.indexOf(Math.max(...probabilities));
        const confidence = probabilities[maxIdx];
        
        // Store results
        predictions.push({
            digit: maxIdx,
            confidence: confidence,
            probabilities: probabilities,
            timestamp: new Date().toLocaleTimeString()
        });
        
        // Display results
        displayResults({
            digit: maxIdx,
            confidence: confidence,
            probabilities: probabilities
        });
        
        // Add to gallery
        addToGallery(maxIdx, confidence);
        
        const endTime = performance.now();
        const inferenceTime = (endTime - startTime).toFixed(2);
        
        console.log(`✅ Prediction: ${maxIdx} (${(confidence * 100).toFixed(2)}%)`);
        console.log(`⏱ Inference time: ${inferenceTime}ms`);
        
        inferenceTimeText.textContent = `${inferenceTime}ms`;
        updateStatus(`Predição concluída!`);
        
    } catch (error) {
        console.error('❌ Error during inference:', error);
        updateStatus('Erro durante a predição');
    }
}

/**
 * Softmax function
 */
function softmax(arr) {
    const maxVal = Math.max(...arr);
    const exps = arr.map(x => Math.exp(x - maxVal));
    const sumExps = exps.reduce((a, b) => a + b);
    return exps.map(x => x / sumExps);
}

/**
 * Generate demo prediction (for when model is not loaded)
 */
function generateDemoPrediction() {
    const digit = Math.floor(Math.random() * 10);
    const probabilities = new Array(10).fill(0);
    
    // Concentrate probability around the chosen digit
    probabilities[digit] = 0.85 + Math.random() * 0.14;
    
    // Distribute remaining probability
    const remaining = 1 - probabilities[digit];
    for (let i = 0; i < 10; i++) {
        if (i !== digit) {
            probabilities[i] = remaining / 9;
        }
    }
    
    return {
        digit: digit,
        confidence: probabilities[digit],
        probabilities: probabilities
    };
}

/**
 * Display prediction results
 */
function displayResults(results) {
    const { digit, confidence, probabilities } = results;
    
    // Update main prediction
    predictionDigit.textContent = digit;
    predictionConfidence.textContent = (confidence * 100).toFixed(1) + '%';
    
    // Update confidence bar
    const confidencePercent = confidence * 100;
    confidenceFill.style.width = confidencePercent + '%';
    confidenceText.textContent = `${confidencePercent.toFixed(1)}% de confiança`;
    
    // Update probability items
    const probabilityItems = document.querySelectorAll('.probability-item');
    probabilityItems.forEach((item, index) => {
        const prob = probabilities[index] * 100;
        const barFill = item.querySelector('.probability-bar-fill');
        const valueText = item.querySelector('.probability-value');
        
        barFill.style.width = prob + '%';
        valueText.textContent = prob.toFixed(0) + '%';
    });
}

/**
 * Add prediction to gallery
 */
function addToGallery(digit, confidence) {
    // Remove empty message if exists
    const emptyGallery = gallery.querySelector('.empty-gallery');
    if (emptyGallery) {
        emptyGallery.remove();
    }
    
    // Create gallery item
    const item = document.createElement('div');
    item.className = 'gallery-item';
    
    // Create canvas for thumbnail
    const thumbCanvas = document.createElement('canvas');
    thumbCanvas.width = 100;
    thumbCanvas.height = 100;
    const thumbCtx = thumbCanvas.getContext('2d');
    
    // Draw thumbnail
    thumbCtx.drawImage(canvas, 0, 0, 100, 100);
    
    // Add canvas to item
    item.appendChild(thumbCanvas);
    
    // Add info
    const info = document.createElement('div');
    info.className = 'gallery-item-info';
    info.innerHTML = `
        <div style="font-size: 1.3em;">${digit}</div>
        <div style="font-size: 0.8em;">${(confidence * 100).toFixed(0)}%</div>
    `;
    item.appendChild(info);
    
    // Limit gallery to 20 items
    if (gallery.children.length >= 20) {
        gallery.removeChild(gallery.firstChild);
    }
    
    gallery.appendChild(item);
    
    // Scroll to end
    item.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Update status text
 */
function updateStatus(message) {
    statusText.textContent = message;
    console.log(`📝 Status: ${message}`);
}

// Make functions available globally for debugging
window.app = {
    predict,
    clearCanvas,
    session: () => session,
    getDrawingData: () => canvas.toDataURL(),
    getPredictions: () => predictions,
};

console.log('💡 Dicas de debug:');
console.log('  app.predict() - Fazer predição manual');
console.log('  app.clearCanvas() - Limpar canvas');
console.log('  app.getPredictions() - Ver histórico de predições');
console.log('  app.getDrawingData() - Obter desenho como imagem base64');
