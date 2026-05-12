"""
Inference Script for MNIST CNN

This script demonstrates how to load a trained model and make predictions
on new images.
"""

import torch
import torch.nn as nn
import numpy as np
from pathlib import Path
from PIL import Image
from torchvision import transforms

from src.model import MNIST_CNN
from src.evaluate import predict_single
from src.utils import get_device


def load_trained_model(
    model_path: str,
    device: torch.device,
) -> MNIST_CNN:
    """
    Load a trained model from disk.
    
    Args:
        model_path (str): Path to saved model weights
        device (torch.device): Device to load model on
        
    Returns:
        MNIST_CNN: Loaded model ready for inference
    """
    model = MNIST_CNN().to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    print(f"✓ Model loaded from {model_path}")
    return model


def predict_from_image(
    model: MNIST_CNN,
    image_path: str,
    device: torch.device,
) -> tuple:
    """
    Make prediction on a single image file.
    
    Args:
        model (MNIST_CNN): Trained model
        image_path (str): Path to image file (must be 28x28 grayscale)
        device (torch.device): Device to run inference on
        
    Returns:
        tuple: (prediction, confidence)
    """
    # Load image
    image = Image.open(image_path).convert('L')  # Convert to grayscale
    image = image.resize((28, 28))  # Ensure correct size
    
    # Convert to tensor
    transform = transforms.ToTensor()
    image_tensor = transform(image)
    
    # Make prediction
    prediction, confidence = predict_single(model, image_tensor, device)
    
    return prediction, confidence


def predict_batch(
    model: MNIST_CNN,
    image_paths: list,
    device: torch.device,
) -> list:
    """
    Make predictions on multiple images.
    
    Args:
        model (MNIST_CNN): Trained model
        image_paths (list): List of image paths
        device (torch.device): Device to run inference on
        
    Returns:
        list: List of (prediction, confidence) tuples
    """
    results = []
    
    for image_path in image_paths:
        pred, conf = predict_from_image(model, image_path, device)
        results.append((pred, conf))
        
    return results


def predict_from_array(
    model: MNIST_CNN,
    image_array: np.ndarray,
    device: torch.device,
) -> tuple:
    """
    Make prediction on numpy array.
    
    Args:
        model (MNIST_CNN): Trained model
        image_array (np.ndarray): Image as numpy array (28x28)
        device (torch.device): Device to run inference on
        
    Returns:
        tuple: (prediction, confidence)
    """
    # Normalize if needed
    if image_array.max() > 1.0:
        image_array = image_array / 255.0
    
    # Convert to tensor
    image_tensor = torch.FloatTensor(image_array).unsqueeze(0)
    
    # Make prediction
    prediction, confidence = predict_single(model, image_tensor, device)
    
    return prediction, confidence


def main():
    """Main inference example."""
    print("\n" + "=" * 70)
    print("MNIST CNN - Inference Example")
    print("=" * 70 + "\n")
    
    # Setup
    device = get_device()
    
    # Load model
    model_path = "outputs/model_weights.pth"
    
    if not Path(model_path).exists():
        print(f"⚠ Model not found at {model_path}")
        print("Please train the model first using: python main.py")
        return
    
    model = load_trained_model(model_path, device)
    
    # Example 1: Inference on a random batch from test data
    print("\nExample 1: Random test images")
    print("-" * 70)
    
    from torchvision import datasets, transforms
    
    test_data = datasets.MNIST(
        root="data",
        train=False,
        download=True,
        transform=transforms.ToTensor()
    )
    
    # Get a batch of test images
    indices = np.random.choice(len(test_data), 5, replace=False)
    
    for idx in indices:
        image, label = test_data[idx]
        image_np = image.squeeze().cpu().numpy()
        
        prediction, confidence = predict_from_array(model, image_np, device)
        
        status = "✓" if prediction == label else "✗"
        print(f"{status} Predicted: {prediction}, Actual: {label}, "
              f"Confidence: {confidence:.2%}")
    
    print("\n" + "=" * 70)
    print("✓ Inference completed!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
