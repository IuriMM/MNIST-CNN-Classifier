"""
Evaluation Module for MNIST CNN

This module contains evaluation and inference functionality for the trained model.
"""

import torch
import torch.nn as nn
from typing import Tuple


def evaluate_model(
    model: nn.Module,
    loader,
    criterion: nn.Module,
    device: torch.device,
) -> Tuple[float, float]:
    """
    Evaluate the model on a dataset.
    
    Args:
        model (nn.Module): The neural network model
        loader: DataLoader for evaluation data
        criterion: Loss function
        device (torch.device): Device to run evaluation on
        
    Returns:
        Tuple[float, float]: Average loss and accuracy (%)
    """
    # Disable Dropout and BatchNorm layers
    model.eval()

    correct = 0
    total = 0
    running_loss = 0.0

    # Disable gradient computation and backpropagation
    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)

            # Forward pass
            outputs = model(images)

            # Calculate loss
            loss = criterion(outputs, labels)
            running_loss += loss.item() * images.size(0)

            # Get predictions
            _, predicted = torch.max(outputs, 1)

            # Update metrics
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    avg_loss = running_loss / total
    accuracy = 100.0 * correct / total

    return avg_loss, accuracy


def predict_single(
    model: nn.Module,
    image: torch.Tensor,
    device: torch.device,
) -> Tuple[int, float]:
    """
    Make prediction on a single image.
    
    Args:
        model (nn.Module): The neural network model
        image (torch.Tensor): Input image tensor of shape (1, 28, 28)
        device (torch.device): Device to run inference on
        
    Returns:
        Tuple[int, float]: Predicted class and confidence
    """
    model.eval()

    with torch.no_grad():
        image = image.unsqueeze(0).to(device)  # Add batch dimension
        output = model(image)
        probabilities = torch.softmax(output, dim=1)
        confidence, prediction = torch.max(probabilities, 1)

    return prediction.item(), confidence.item()


def print_evaluation_results(
    train_loss: float,
    train_acc: float,
    val_loss: float = None,
    val_acc: float = None,
    test_loss: float = None,
    test_acc: float = None,
) -> None:
    """
    Print evaluation results in a formatted table.
    
    Args:
        train_loss (float): Training loss
        train_acc (float): Training accuracy
        val_loss (float): Validation loss (optional)
        val_acc (float): Validation accuracy (optional)
        test_loss (float): Test loss (optional)
        test_acc (float): Test accuracy (optional)
    """
    print("\n" + "=" * 60)
    print("EVALUATION RESULTS")
    print("=" * 60)

    print(f"Training Loss: {train_loss:.4f} | Training Accuracy: {train_acc:.2f}%")

    if val_loss is not None and val_acc is not None:
        print(f"Validation Loss: {val_loss:.4f} | Validation Accuracy: {val_acc:.2f}%")

    if test_loss is not None and test_acc is not None:
        print(f"Test Loss: {test_loss:.4f} | Test Accuracy: {test_acc:.2f}%")

    print("=" * 60 + "\n")
