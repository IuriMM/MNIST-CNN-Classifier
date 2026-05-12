"""
Hyperparameter Tuning Script for MNIST CNN

This script performs a grid search over various hyperparameters to find
the best configuration for the MNIST digit classifier.
"""

import torch
import torch.nn as nn
import pandas as pd
from itertools import product
from torch.utils.data import DataLoader, random_split

from src.model import MNIST_CNN
from src.train import train_model, get_optimizer
from src.evaluate import evaluate_model
from src.utils import get_device, load_mnist_data


def hyperparameter_search(
    train_data,
    val_data,
    device: torch.device,
    param_grid: dict,
    n_trials: int = None,
) -> pd.DataFrame:
    """
    Perform grid search over hyperparameters.
    
    Args:
        train_data: Training dataset
        val_data: Validation dataset
        device (torch.device): Device to run on
        param_grid (dict): Grid of hyperparameters to search
        n_trials (int): Limit number of trials (if None, search all combinations)
        
    Returns:
        pd.DataFrame: Results of grid search
    """
    criterion = nn.CrossEntropyLoss()
    results = []

    # Generate all combinations
    combinations = [
        dict(zip(param_grid.keys(), vals))
        for vals in product(*param_grid.values())
    ]

    if n_trials:
        combinations = combinations[:n_trials]

    total = len(combinations)
    print(f"\nStarting Grid Search: {total} combinations to test\n")
    print("=" * 80)

    for i, hp in enumerate(combinations, 1):
        print(f"\n[{i}/{total}] Testing hyperparameters:")
        print(f"  Optimizer: {hp['optimizer']}, LR: {hp['lr']}")
        print(f"  Batch Size: {hp['batch_size']}, Epochs: {hp['epochs']}")
        print(f"  Dropout: {hp['dropout']}")

        # Create data loaders
        train_loader = DataLoader(
            train_data,
            batch_size=hp['batch_size'],
            shuffle=True,
        )
        val_loader = DataLoader(
            val_data,
            batch_size=hp['batch_size'],
            shuffle=False,
        )

        # Create model
        model = MNIST_CNN(dropout=hp['dropout']).to(device)

        # Create optimizer
        optimizer = get_optimizer(
            hp['optimizer'],
            model.parameters(),
            hp['lr']
        )

        # Train
        train_model(
            model=model,
            train_loader=train_loader,
            criterion=criterion,
            optimizer=optimizer,
            n_epochs=hp['epochs'],
            device=device,
        )

        # Evaluate
        val_loss, val_acc = evaluate_model(
            model=model,
            loader=val_loader,
            criterion=criterion,
            device=device,
        )

        # Store results
        row = {**hp, 'val_loss': val_loss, 'val_acc': val_acc}
        results.append(row)

        print(f"  ✓ Val Loss: {val_loss:.4f} | Val Accuracy: {val_acc:.2f}%")

    print("\n" + "=" * 80)
    return pd.DataFrame(results)


def main():
    """Main execution function."""
    # Setup
    device = get_device()
    print(f"\n{'='*80}")
    print("MNIST CNN - Hyperparameter Tuning")
    print(f"{'='*80}\n")

    # Load data
    print("Loading data...")
    _, val_loader, _, train_subset, val_subset, _ = load_mnist_data(
        batch_size=64,
        val_split=0.1,
    )

    # Define hyperparameter grid
    param_grid = {
        'optimizer': ['adam', 'sgd'],
        'lr': [0.01, 0.001],
        'batch_size': [32, 64],
        'epochs': [10, 15],
        'dropout': [0.0, 0.25],
    }

    print("\nHyperparameter Grid:")
    for key, values in param_grid.items():
        print(f"  {key}: {values}")

    # Perform search
    results_df = hyperparameter_search(
        train_data=train_subset,
        val_data=val_subset,
        device=device,
        param_grid=param_grid,
        n_trials=None,  # Set to integer to limit trials
    )

    # Display results
    print("\n\nResults Summary:")
    print("=" * 80)
    results_sorted = results_df.sort_values(by='val_acc', ascending=False)

    print("\nTop 10 Configurations:")
    print(results_sorted[['optimizer', 'lr', 'batch_size', 'epochs', 'dropout', 'val_loss', 'val_acc']].head(10))

    # Save results
    results_sorted.to_csv('outputs/hyperparameter_search_results.csv', index=False)
    print(f"\n✓ Results saved to outputs/hyperparameter_search_results.csv")

    # Get best configuration
    best_config = results_sorted.iloc[0]
    print("\n" + "=" * 80)
    print("BEST CONFIGURATION FOUND:")
    print("=" * 80)
    print(f"Optimizer: {best_config['optimizer']}")
    print(f"Learning Rate: {best_config['lr']}")
    print(f"Batch Size: {int(best_config['batch_size'])}")
    print(f"Epochs: {int(best_config['epochs'])}")
    print(f"Dropout: {best_config['dropout']}")
    print(f"Validation Loss: {best_config['val_loss']:.4f}")
    print(f"Validation Accuracy: {best_config['val_acc']:.2f}%")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
