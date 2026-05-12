"""
Configuration and Constants for MNIST CNN Project
"""

import torch
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
NOTEBOOK_DIR = PROJECT_ROOT / "notebooks"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
NOTEBOOK_DIR.mkdir(exist_ok=True)

# Model hyperparameters (defaults)
MODEL_CONFIG = {
    'filters1': 32,
    'filters2': 64,
    'kernel_size': (3, 3),
    'activation': 'relu',
    'dense_units': 128,
    'dropout': 0.25,
}

# Training hyperparameters (defaults)
TRAINING_CONFIG = {
    'batch_size': 64,
    'optimizer': 'adam',
    'lr': 0.001,
    'epochs': 32,
}

# Data configuration
DATA_CONFIG = {
    'train_size': 60000,
    'test_size': 10000,
    'val_split': 0.1,
    'image_size': (28, 28),
    'n_classes': 10,
}

# Device configuration
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# File paths
MODEL_WEIGHTS_PATH = OUTPUT_DIR / "model_weights.pth"
TRAINING_LOSS_PATH = OUTPUT_DIR / "training_loss.png"
METRICS_PATH = OUTPUT_DIR / "metrics.txt"
