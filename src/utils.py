"""
Utility Functions for MNIST CNN

This module contains helper functions for data loading, visualization, and device management.
"""

import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import seaborn as sns
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split
from pathlib import Path


def get_device() -> torch.device:
    """
    Get the appropriate computing device (GPU/CPU).
    
    Returns:
        torch.device: PyTorch device object
    """
    try:
        import torch_directml
        if torch_directml.is_available():
            device = torch_directml.device()
            print("✓ Using DirectML GPU device")
            return device
    except ImportError:
        pass

    if torch.cuda.is_available():
        device = torch.device("cuda")
        print("✓ Using CUDA GPU device")
        return device

    device = torch.device("cpu")
    print("⚠ Using CPU device (slower)")
    return device


def load_mnist_data(
    data_dir: str = "data",
    batch_size: int = 64,
    val_split: float = 0.1,
) -> tuple:
    """
    Load MNIST dataset and create data loaders.
    
    Args:
        data_dir (str): Directory to store MNIST data
        batch_size (int): Batch size for training and testing
        val_split (float): Fraction of training data to use for validation
        
    Returns:
        tuple: (train_loader, val_loader, test_loader, train_data, val_data, test_data)
    """
    # Define transforms
    transform = transforms.ToTensor()

    # Load datasets
    print("Loading MNIST dataset...")
    train_data = datasets.MNIST(
        root=data_dir,
        train=True,
        download=True,
        transform=transform
    )

    test_data = datasets.MNIST(
        root=data_dir,
        train=False,
        download=True,
        transform=transform
    )

    # Split training data into train and validation
    val_size = int(len(train_data) * val_split)
    train_size = len(train_data) - val_size
    train_subset, val_subset = random_split(
        train_data,
        [train_size, val_size],
        generator=torch.Generator().manual_seed(42)
    )

    # Create data loaders
    train_loader = DataLoader(
        train_subset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=0
    )

    val_loader = DataLoader(
        val_subset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0
    )

    test_loader = DataLoader(
        test_data,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0
    )

    print(f"✓ Train set size: {len(train_subset)}")
    print(f"✓ Validation set size: {len(val_subset)}")
    print(f"✓ Test set size: {len(test_data)}")

    return train_loader, val_loader, test_loader, train_subset, val_subset, test_data


def save_model(model: nn.Module, filepath: str) -> None:
    """
    Save model weights to file.
    
    Args:
        model (nn.Module): The model to save
        filepath (str): Path to save the model weights
    """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), filepath)
    print(f"✓ Model saved to {filepath}")


def load_model_weights(model: nn.Module, filepath: str) -> nn.Module:
    """
    Load model weights from file.
    
    Args:
        model (nn.Module): The model to load weights into
        filepath (str): Path to load the model weights from
        
    Returns:
        nn.Module: Model with loaded weights
    """
    model.load_state_dict(torch.load(filepath))
    print(f"✓ Model loaded from {filepath}")
    return model


def plot_training_loss(
    loss_curve: list,
    save_path: str = "outputs/training_loss.png",
) -> None:
    """
    Plot and save the training loss curve.
    
    Args:
        loss_curve (list): List of loss values for each epoch
        save_path (str): Path to save the figure
    """
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.plot(loss_curve, linewidth=2.5, color='#2E86AB', label='Training Loss')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.xlabel('Epoch', fontsize=12, fontweight='bold')
    plt.ylabel('Loss', fontsize=12, fontweight='bold')
    plt.title('Training Loss Curve - MNIST CNN', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ Loss curve saved to {save_path}")
    plt.close()


def plot_multiple_metrics(
    metrics: dict,
    save_path: str = "outputs/metrics_comparison.png",
) -> None:
    """
    Plot multiple metrics for comparison.
    
    Args:
        metrics (dict): Dictionary with metric names and values
        save_path (str): Path to save the figure
    """
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Accuracy comparison
    accuracies = {k: v[1] for k, v in metrics.items() if len(v) >= 2}
    axes[0].bar(accuracies.keys(), accuracies.values(), color='#06A77D', alpha=0.8)
    axes[0].set_ylabel('Accuracy (%)', fontsize=11, fontweight='bold')
    axes[0].set_title('Model Accuracy Comparison', fontsize=12, fontweight='bold')
    axes[0].grid(True, alpha=0.3, axis='y')
    axes[0].set_ylim([0, 105])
    for i, (k, v) in enumerate(accuracies.items()):
        axes[0].text(i, v + 1, f'{v:.2f}%', ha='center', fontsize=10, fontweight='bold')

    # Plot 2: Loss comparison
    losses = {k: v[0] for k, v in metrics.items() if len(v) >= 2}
    axes[1].bar(losses.keys(), losses.values(), color='#D62839', alpha=0.8)
    axes[1].set_ylabel('Loss', fontsize=11, fontweight='bold')
    axes[1].set_title('Model Loss Comparison', fontsize=12, fontweight='bold')
    axes[1].grid(True, alpha=0.3, axis='y')
    for i, (k, v) in enumerate(losses.items()):
        axes[1].text(i, v + 0.01, f'{v:.4f}', ha='center', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ Metrics comparison saved to {save_path}")
    plt.close()


def print_model_summary(model: nn.Module) -> None:
    """
    Print model architecture summary.
    
    Args:
        model (nn.Module): The model to summarize
    """
    print("\n" + "=" * 70)
    print("MODEL ARCHITECTURE")
    print("=" * 70)
    print(model)
    print("=" * 70 + "\n")
