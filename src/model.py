"""
CNN Model Architecture for MNIST Digit Classification

This module defines the Convolutional Neural Network architecture used for
classifying handwritten digits from the MNIST dataset.
"""

import torch
import torch.nn as nn


class MNIST_CNN(nn.Module):
    """
    Convolutional Neural Network for MNIST Digit Classification.
    
    Architecture:
    - Feature Extractor: 2 convolutional blocks with max pooling
    - Classifier: Fully connected layers with dropout regularization
    
    Args:
        filters1 (int): Number of filters in first convolutional layer. Default: 32
        filters2 (int): Number of filters in second convolutional layer. Default: 64
        kernel_size (tuple or int): Kernel size for convolutional operations. Default: (3, 3)
        activation (str): Activation function ('relu' or 'tanh'). Default: 'relu'
        dense_units (int): Number of units in dense layer. Default: 128
        dropout (float): Dropout probability. Default: 0.25
    """
    
    def __init__(
        self,
        filters1=32,
        filters2=64,
        kernel_size=(3, 3),
        activation='relu',
        dense_units=128,
        dropout=0.25,
    ):
        super().__init__()

        # Select activation function
        if activation == 'relu':
            activation_layer = nn.ReLU()
        elif activation == 'tanh':
            activation_layer = nn.Tanh()
        else:
            raise ValueError(f"Unknown activation function: {activation}")

        # Calculate padding to maintain spatial dimensions
        if isinstance(kernel_size, int):
            padding = kernel_size // 2
        else:
            padding = (kernel_size[0] // 2, kernel_size[1] // 2)

        # Feature Extractor: Learns spatial patterns (edges, strokes, shapes)
        # Input: (1, 28, 28) -> Output: (64, 7, 7) after 2 conv blocks with 2x2 max pooling
        self.features = nn.Sequential(
            nn.Conv2d(
                in_channels=1,
                out_channels=filters1,
                kernel_size=kernel_size,
                padding=padding
            ),
            activation_layer,
            nn.MaxPool2d(kernel_size=2, stride=2),  # 28x28 -> 14x14

            nn.Conv2d(
                in_channels=filters1,
                out_channels=filters2,
                kernel_size=kernel_size,
                padding=padding
            ),
            activation_layer.__class__() if activation == 'relu' else nn.Tanh(),
            nn.MaxPool2d(kernel_size=2, stride=2)  # 14x14 -> 7x7
        )

        # Classifier: Maps extracted features to class scores (10 digits)
        # Input: 64 * 7 * 7 = 3136 -> Output: 10 (digit classes)
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(filters2 * 7 * 7, dense_units),
            activation_layer.__class__() if activation == 'relu' else nn.Tanh(),
            nn.Dropout(dropout),
            nn.Linear(dense_units, 10)  # 10 digit classes (0-9)
        )

    def forward(self, x):
        """
        Forward pass through the network.
        
        Args:
            x (torch.Tensor): Input tensor of shape (batch_size, 1, 28, 28)
            
        Returns:
            torch.Tensor: Output logits of shape (batch_size, 10)
        """
        x = self.features(x)
        x = self.classifier(x)
        return x
