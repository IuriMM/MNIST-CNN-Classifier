"""
Convert PyTorch MNIST CNN Model to ONNX Format

This script converts the trained PyTorch model to ONNX format,
which can be used in web browsers with ONNX Runtime JS.
"""

import torch
import torch.onnx
from pathlib import Path

from src.model import MNIST_CNN
from src.utils import get_device


def convert_to_onnx(
    model_path: str,
    output_path: str = "web/models/mnist_cnn.onnx",
) -> None:
    """
    Convert PyTorch model to ONNX format.
    
    Args:
        model_path (str): Path to PyTorch model weights
        output_path (str): Path to save ONNX model
    """
    print(f"\n{'='*70}")
    print("Converting PyTorch Model to ONNX")
    print(f"{'='*70}\n")
    
    # Setup
    device = get_device()
    
    # Load model
    print(f"1. Loading model from {model_path}...")
    model = MNIST_CNN().to(device)
    
    try:
        model.load_state_dict(torch.load(model_path, map_location=device))
        print("   ✓ Model loaded successfully")
    except FileNotFoundError:
        print(f"   ✗ Error: Model not found at {model_path}")
        print(f"   Please train the model first: python main.py")
        return
    
    model.eval()
    
    # Create dummy input (1 image, 1 channel, 28x28)
    print("\n2. Creating dummy input...")
    dummy_input = torch.randn(1, 1, 28, 28).to(device)
    print(f"   Input shape: {dummy_input.shape}")
    
    # Convert to ONNX
    print("\n3. Converting to ONNX format...")
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    torch.onnx.export(
        model,
        dummy_input,
        output_path,
        export_params=True,
        opset_version=12,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={
            'input': {0: 'batch_size'},
            'output': {0: 'batch_size'}
        },
        verbose=False,
    )
    
    print(f"   ✓ Model converted successfully")
    print(f"   ✓ Saved to: {output_path}")
    
    # Verify
    print("\n4. Verifying ONNX model...")
    try:
        import onnx
        model_onnx = onnx.load(output_path)
        onnx.checker.check_model(model_onnx)
        print("   ✓ ONNX model is valid")
    except ImportError:
        print("   ⚠ ONNX library not installed (install with: pip install onnx)")
    except Exception as e:
        print(f"   ✗ Verification failed: {e}")
    
    # File size
    file_size = Path(output_path).stat().st_size / (1024 * 1024)
    print(f"\n5. Model file size: {file_size:.2f} MB")
    
    print(f"\n{'='*70}")
    print("✓ Conversion Complete!")
    print(f"{'='*70}")
    print("\nNext steps:")
    print("1. Deploy to GitHub Pages: push the 'web' folder")
    print("2. Open index.html in a browser")
    print("3. Start drawing numbers and get predictions!")
    print()


if __name__ == "__main__":
    # Convert model
    convert_to_onnx(
        model_path="outputs/model_weights.pth",
        output_path="web/models/mnist_cnn.onnx",
    )
