"""
Main Training and Evaluation Script for MNIST CNN

This script orchestrates the complete training and evaluation pipeline.
"""

import torch
import torch.nn as nn
import argparse
from pathlib import Path

from src.model import MNIST_CNN
from src.train import train_model, get_optimizer
from src.evaluate import evaluate_model, print_evaluation_results
from src.utils import (
    get_device,
    load_mnist_data,
    save_model,
    plot_training_loss,
    print_model_summary,
)


def main(args):
    """
    Main execution function.
    
    Args:
        args: Command-line arguments
    """
    # Setup
    device = get_device()
    print(f"\n{'='*70}")
    print("MNIST CNN - Handwritten Digit Classification")
    print(f"{'='*70}\n")

    # Load data
    print("Step 1: Loading Data")
    print("-" * 70)
    train_loader, val_loader, test_loader, _, _, _ = load_mnist_data(
        data_dir=args.data_dir,
        batch_size=args.batch_size,
    )

    # Create model
    print("\nStep 2: Building Model")
    print("-" * 70)
    model = MNIST_CNN(
        filters1=args.filters1,
        filters2=args.filters2,
        kernel_size=args.kernel_size,
        activation=args.activation,
        dense_units=args.dense_units,
        dropout=args.dropout,
    ).to(device)
    print_model_summary(model)

    # Setup training
    print("Step 3: Training Configuration")
    print("-" * 70)
    criterion = nn.CrossEntropyLoss()
    optimizer = get_optimizer(args.optimizer, model.parameters(), args.lr)
    print(f"✓ Loss Function: CrossEntropyLoss")
    print(f"✓ Optimizer: {args.optimizer.upper()}")
    print(f"✓ Learning Rate: {args.lr}")
    print(f"✓ Number of Epochs: {args.epochs}\n")

    # Train model
    print("Step 4: Training Model")
    print("-" * 70)
    train_loss_curve = train_model(
        model=model,
        train_loader=train_loader,
        criterion=criterion,
        optimizer=optimizer,
        n_epochs=args.epochs,
        device=device,
    )

    # Evaluate on training data
    print("\nStep 5: Evaluation")
    print("-" * 70)
    train_loss, train_acc = evaluate_model(
        model=model,
        loader=train_loader,
        criterion=criterion,
        device=device,
    )
    print(f"Training - Loss: {train_loss:.4f} | Accuracy: {train_acc:.2f}%")

    # Evaluate on validation data
    val_loss, val_acc = evaluate_model(
        model=model,
        loader=val_loader,
        criterion=criterion,
        device=device,
    )
    print(f"Validation - Loss: {val_loss:.4f} | Accuracy: {val_acc:.2f}%")

    # Evaluate on test data
    test_loss, test_acc = evaluate_model(
        model=model,
        loader=test_loader,
        criterion=criterion,
        device=device,
    )
    print(f"Test - Loss: {test_loss:.4f} | Accuracy: {test_acc:.2f}%")

    # Print summary
    print_evaluation_results(
        train_loss=train_loss,
        train_acc=train_acc,
        val_loss=val_loss,
        val_acc=val_acc,
        test_loss=test_loss,
        test_acc=test_acc,
    )

    # Save results
    print("Step 6: Saving Results")
    print("-" * 70)
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    # Save model
    save_model(model, f"{args.output_dir}/model_weights.pth")

    # Save training loss curve
    plot_training_loss(train_loss_curve, f"{args.output_dir}/training_loss.png")

    # Save metrics to file
    with open(f"{args.output_dir}/metrics.txt", "w") as f:
        f.write("MNIST CNN - Performance Metrics\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Training Loss: {train_loss:.4f}\n")
        f.write(f"Training Accuracy: {train_acc:.2f}%\n\n")
        f.write(f"Validation Loss: {val_loss:.4f}\n")
        f.write(f"Validation Accuracy: {val_acc:.2f}%\n\n")
        f.write(f"Test Loss: {test_loss:.4f}\n")
        f.write(f"Test Accuracy: {test_acc:.2f}%\n")

    print(f"✓ Metrics saved to {args.output_dir}/metrics.txt")
    print("\n" + "=" * 70)
    print("✓ Training Pipeline Completed Successfully!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train MNIST CNN Classifier",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Data arguments
    parser.add_argument(
        "--data-dir",
        type=str,
        default="data",
        help="Directory to store MNIST dataset"
    )

    # Model arguments
    parser.add_argument(
        "--filters1",
        type=int,
        default=32,
        help="Number of filters in first convolutional layer"
    )
    parser.add_argument(
        "--filters2",
        type=int,
        default=64,
        help="Number of filters in second convolutional layer"
    )
    parser.add_argument(
        "--kernel-size",
        type=int,
        default=3,
        help="Kernel size for convolutional operations"
    )
    parser.add_argument(
        "--activation",
        type=str,
        choices=["relu", "tanh"],
        default="relu",
        help="Activation function"
    )
    parser.add_argument(
        "--dense-units",
        type=int,
        default=128,
        help="Number of units in dense layer"
    )
    parser.add_argument(
        "--dropout",
        type=float,
        default=0.25,
        help="Dropout probability"
    )

    # Training arguments
    parser.add_argument(
        "--batch-size",
        type=int,
        default=64,
        help="Batch size for training"
    )
    parser.add_argument(
        "--optimizer",
        type=str,
        choices=["adam", "sgd", "rmsprop"],
        default="adam",
        help="Optimizer algorithm"
    )
    parser.add_argument(
        "--lr",
        type=float,
        default=1e-3,
        help="Learning rate"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=32,
        help="Number of training epochs"
    )

    # Output arguments
    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs",
        help="Directory to save results"
    )

    args = parser.parse_args()
    main(args)
