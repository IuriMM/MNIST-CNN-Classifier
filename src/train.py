"""
Training Module for MNIST CNN

This module contains the training pipeline for the MNIST digit classifier.
"""

import torch
import torch.nn as nn
import torch.optim as optim
import time
import datetime
from tqdm import tqdm
from typing import Tuple, List


def train_model(
    model: nn.Module,
    train_loader,
    criterion: nn.Module,
    optimizer: optim.Optimizer,
    n_epochs: int,
    device: torch.device,
) -> List[float]:
    """
    Train the neural network model.
    
    Args:
        model (nn.Module): The neural network model to train
        train_loader: DataLoader for training data
        criterion: Loss function
        optimizer: Optimization algorithm
        n_epochs (int): Number of training epochs
        device (torch.device): Device to run training on (CPU or GPU)
        
    Returns:
        List[float]: Training loss values for each epoch
    """
    # Enable layers specific to training (Dropout, BatchNorm)
    model.train()

    # Measure training duration
    start = time.time()
    train_loss_curve = []

    # Create progress bar
    pbar = tqdm(range(1, n_epochs + 1), desc="Training Progress")

    for epoch in pbar:
        train_loss = 0.0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            # Clear old gradients
            optimizer.zero_grad()

            # Forward pass
            outputs = model(images)

            # Calculate loss
            loss = criterion(outputs, labels)

            # Backpropagation
            loss.backward()

            # Update weights
            optimizer.step()

            # Accumulate loss
            train_loss += loss.item() * images.size(0)

        # Calculate average loss for the epoch
        train_loss = train_loss / len(train_loader.dataset)
        train_loss_curve.append(train_loss)
        
        pbar.set_description(
            f'Epoch {epoch}/{n_epochs} | Training Loss: {train_loss:.4f}'
        )

    end = time.time()
    elapsed_time = str(datetime.timedelta(seconds=round(end - start)))
    print(f"\n✓ Training completed in {elapsed_time}")

    return train_loss_curve


def get_optimizer(
    optimizer_name: str,
    model_params,
    lr: float,
) -> optim.Optimizer:
    """
    Get the specified optimizer.
    
    Args:
        optimizer_name (str): Name of the optimizer ('adam', 'sgd', 'rmsprop')
        model_params: Model parameters to optimize
        lr (float): Learning rate
        
    Returns:
        optim.Optimizer: The optimizer instance
    """
    if optimizer_name == 'adam':
        return optim.Adam(model_params, lr=lr)
    elif optimizer_name == 'sgd':
        return optim.SGD(model_params, lr=lr)
    elif optimizer_name == 'rmsprop':
        return optim.RMSprop(model_params, lr=lr)
    else:
        raise ValueError(f"Unknown optimizer: {optimizer_name}")
