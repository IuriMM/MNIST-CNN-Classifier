"""
Visualization Script for MNIST CNN

This script creates visualizations of model predictions and performance.
"""

import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from torchvision import datasets, transforms

from src.model import MNIST_CNN
from src.utils import get_device


def visualize_predictions(
    model: MNIST_CNN,
    test_loader,
    device: torch.device,
    num_samples: int = 12,
    save_path: str = "outputs/predictions_visualization.png",
) -> None:
    """
    Visualize model predictions on test images.
    
    Args:
        model (MNIST_CNN): Trained model
        test_loader: DataLoader for test data
        device (torch.device): Device to run on
        num_samples (int): Number of samples to visualize
        save_path (str): Path to save the figure
    """
    model.eval()
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    
    images, labels = next(iter(test_loader))
    images, labels = images.to(device), labels.to(device)
    
    with torch.no_grad():
        outputs = model(images)
        _, predictions = torch.max(outputs, 1)
    
    # Plot
    fig, axes = plt.subplots(3, 4, figsize=(14, 10))
    fig.suptitle('MNIST CNN - Model Predictions', fontsize=16, fontweight='bold')
    
    axes = axes.ravel()
    
    for idx in range(min(num_samples, len(images))):
        img = images[idx].cpu().numpy().squeeze()
        true_label = labels[idx].item()
        pred_label = predictions[idx].item()
        
        axes[idx].imshow(img, cmap='gray')
        
        # Color: green if correct, red if incorrect
        color = 'green' if true_label == pred_label else 'red'
        axes[idx].set_title(
            f'True: {true_label}\nPred: {pred_label}',
            color=color,
            fontweight='bold'
        )
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ Predictions visualization saved to {save_path}")
    plt.close()


def create_confusion_matrix(
    model: MNIST_CNN,
    test_loader,
    device: torch.device,
    save_path: str = "outputs/confusion_matrix.png",
) -> np.ndarray:
    """
    Create and visualize confusion matrix.
    
    Args:
        model (MNIST_CNN): Trained model
        test_loader: DataLoader for test data
        device (torch.device): Device to run on
        save_path (str): Path to save the figure
        
    Returns:
        np.ndarray: Confusion matrix
    """
    model.eval()
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Initialize confusion matrix
    cm = np.zeros((10, 10))
    
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predictions = torch.max(outputs, 1)
            
            for true, pred in zip(labels, predictions):
                cm[true.item(), pred.item()] += 1
    
    # Plot
    plt.figure(figsize=(12, 10))
    sns.heatmap(
        cm,
        annot=True,
        fmt='.0f',
        cmap='Blues',
        cbar_kws={'label': 'Number of Predictions'}
    )
    plt.xlabel('Predicted Label', fontsize=12, fontweight='bold')
    plt.ylabel('True Label', fontsize=12, fontweight='bold')
    plt.title('Confusion Matrix - MNIST CNN', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ Confusion matrix saved to {save_path}")
    plt.close()
    
    return cm


def plot_per_class_accuracy(
    confusion_matrix: np.ndarray,
    save_path: str = "outputs/per_class_accuracy.png",
) -> None:
    """
    Plot per-class accuracy from confusion matrix.
    
    Args:
        confusion_matrix (np.ndarray): Confusion matrix (10x10)
        save_path (str): Path to save the figure
    """
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Calculate per-class accuracy
    accuracies = []
    for i in range(10):
        correct = confusion_matrix[i, i]
        total = confusion_matrix[i].sum()
        accuracy = (correct / total * 100) if total > 0 else 0
        accuracies.append(accuracy)
    
    # Plot
    plt.figure(figsize=(12, 6))
    bars = plt.bar(range(10), accuracies, color='#2E86AB', alpha=0.8)
    
    # Add value labels on bars
    for i, (bar, acc) in enumerate(zip(bars, accuracies)):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{acc:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.xlabel('Digit Class', fontsize=12, fontweight='bold')
    plt.ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
    plt.title('Per-Class Accuracy - MNIST CNN', fontsize=14, fontweight='bold')
    plt.xticks(range(10))
    plt.ylim([0, 105])
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ Per-class accuracy plot saved to {save_path}")
    plt.close()
    
    # Print statistics
    print(f"\nPer-Class Accuracy Statistics:")
    print(f"  Mean: {np.mean(accuracies):.2f}%")
    print(f"  Min:  {np.min(accuracies):.2f}%")
    print(f"  Max:  {np.max(accuracies):.2f}%")
    print(f"  Std:  {np.std(accuracies):.2f}%")


def visualize_filters(
    model: MNIST_CNN,
    save_path: str = "outputs/conv_filters.png",
) -> None:
    """
    Visualize convolutional filters from the first layer.
    
    Args:
        model (MNIST_CNN): Trained model
        save_path (str): Path to save the figure
    """
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Get first conv layer weights
    first_conv_weight = model.features[0].weight.data.cpu()  # (32, 1, 3, 3)
    
    # Normalize to [0, 1]
    first_conv_weight = (first_conv_weight - first_conv_weight.min()) / \
                        (first_conv_weight.max() - first_conv_weight.min())
    
    # Plot first 16 filters
    fig, axes = plt.subplots(4, 4, figsize=(10, 10))
    fig.suptitle('First Layer Convolutional Filters', fontsize=14, fontweight='bold')
    
    axes = axes.ravel()
    
    for idx in range(16):
        filter_img = first_conv_weight[idx, 0].numpy()
        axes[idx].imshow(filter_img, cmap='viridis')
        axes[idx].axis('off')
        axes[idx].set_title(f'Filter {idx}', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ Conv filters visualization saved to {save_path}")
    plt.close()


def main():
    """Main visualization script."""
    print("\n" + "=" * 70)
    print("MNIST CNN - Visualization")
    print("=" * 70 + "\n")
    
    # Setup
    device = get_device()
    
    # Load model
    model_path = "outputs/model_weights.pth"
    model = MNIST_CNN().to(device)
    
    try:
        model.load_state_dict(torch.load(model_path, map_location=device))
        print(f"✓ Model loaded from {model_path}\n")
    except FileNotFoundError:
        print(f"⚠ Model not found at {model_path}")
        print("Please train the model first using: python main.py")
        return
    
    # Load test data
    print("Loading test data...")
    test_data = datasets.MNIST(
        root="data",
        train=False,
        download=True,
        transform=transforms.ToTensor()
    )
    test_loader = torch.utils.data.DataLoader(test_data, batch_size=64, shuffle=False)
    print(f"✓ Test data loaded ({len(test_data)} samples)\n")
    
    # Generate visualizations
    print("Generating visualizations...")
    print("-" * 70)
    
    visualize_predictions(model, test_loader, device)
    cm = create_confusion_matrix(model, test_loader, device)
    plot_per_class_accuracy(cm)
    visualize_filters(model)
    
    print("\n" + "=" * 70)
    print("✓ All visualizations completed!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
