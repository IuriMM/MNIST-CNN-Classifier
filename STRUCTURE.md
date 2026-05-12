# Estrutura do Projeto

Este documento descreve a organização e propósito de cada arquivo no repositório.

## Hierarquia de Diretórios

```
MNIST-CNN-Classifier/
│
├── src/                           # Código principal do projeto
│   ├── __init__.py               # Pacote Python
│   ├── model.py                  # Arquitetura CNN
│   ├── train.py                  # Pipeline de treinamento
│   ├── evaluate.py               # Avaliação e inferência
│   └── utils.py                  # Funções auxiliares
│
├── data/                          # Dataset MNIST (criado automaticamente)
│   └── MNIST/
│       └── raw/
│           ├── train-images-idx3-ubyte
│           ├── train-labels-idx1-ubyte
│           ├── t10k-images-idx3-ubyte
│           └── t10k-labels-idx1-ubyte
│
├── outputs/                       # Resultados do treinamento
│   ├── model_weights.pth         # Pesos do modelo
│   ├── training_loss.png         # Gráfico da curva de loss
│   ├── metrics.txt               # Métricas em texto
│   ├── metrics_comparison.png    # Comparação de modelos
│   ├── predictions_visualization.png
│   ├── confusion_matrix.png
│   ├── per_class_accuracy.png
│   └── conv_filters.png
│
├── notebooks/                     # Jupyter Notebooks (opcional)
│   └── (análises adicionais)
│
├── main.py                        # Script principal - COMECE AQUI
├── inference.py                  # Fazer predições com modelo treinado
├── visualize.py                  # Gerar visualizações
├── hyperparameter_tuning.py      # Grid search de hiperparâmetros
├── config.py                     # Configurações e constantes
│
├── requirements.txt              # Dependências Python
├── README.md                     # Documentação completa
├── QUICKSTART.md                 # Guia rápido
├── CONTRIBUTING.md               # Guia de contribuição
├── LICENSE                       # Licença MIT
├── .gitignore                    # Arquivos ignorados no git
└── STRUCTURE.md                  # Este arquivo
```

## Descrição dos Arquivos Principais

### `/src/model.py`
**Propósito**: Define a arquitetura CNN

**Classes**:
- `MNIST_CNN`: Modelo com 2 camadas convolucionais e 2 camadas densas

**Uso**:
```python
from src.model import MNIST_CNN
model = MNIST_CNN()
```

---

### `/src/train.py`
**Propósito**: Implementa o loop de treinamento

**Funções principais**:
- `train_model()`: Treina o modelo por N épocas
- `get_optimizer()`: Cria o optimizer especificado

**Uso**:
```python
from src.train import train_model, get_optimizer
loss_curve = train_model(model, train_loader, criterion, optimizer, n_epochs, device)
```

---

### `/src/evaluate.py`
**Propósito**: Avaliação do modelo e inferência

**Funções principais**:
- `evaluate_model()`: Calcula loss e acurácia em um dataset
- `predict_single()`: Predição em uma única imagem
- `print_evaluation_results()`: Exibe resultados formatados

**Uso**:
```python
from src.evaluate import evaluate_model
loss, accuracy = evaluate_model(model, test_loader, criterion, device)
```

---

### `/src/utils.py`
**Propósito**: Funções auxiliares compartilhadas

**Funções principais**:
- `get_device()`: Detecta GPU/CPU disponível
- `load_mnist_data()`: Carrega dataset e cria dataloaders
- `save_model()`: Salva pesos do modelo
- `load_model_weights()`: Carrega pesos salvos
- `plot_training_loss()`: Cria gráfico da curva de loss
- `print_model_summary()`: Exibe arquitetura

**Uso**:
```python
from src.utils import get_device, load_mnist_data, plot_training_loss
device = get_device()
train_loader, val_loader, test_loader, _, _, _ = load_mnist_data()
```

---

### `main.py`
**Propósito**: Script principal - orquestra todo o pipeline

**Funcionalidade**:
1. Carrega dados MNIST
2. Constrói modelo CNN
3. Realiza treinamento completo
4. Avalia em train/val/test sets
5. Salva resultados

**Uso**:
```bash
python main.py --epochs 32 --batch-size 64 --lr 0.001
```

---

### `inference.py`
**Propósito**: Fazer predições com modelo treinado

**Funções principais**:
- `load_trained_model()`: Carrega modelo de arquivo
- `predict_from_image()`: Predição em arquivo de imagem
- `predict_batch()`: Predições em múltiplas imagens
- `predict_from_array()`: Predição em array numpy

**Uso**:
```bash
python inference.py
```

---

### `visualize.py`
**Propósito**: Gerar visualizações detalhadas

**Visualizações geradas**:
- Predições de amostra
- Matriz de confusão
- Acurácia por classe
- Filtros convolucionais

**Uso**:
```bash
python visualize.py
```

---

### `hyperparameter_tuning.py`
**Propósito**: Busca de hiperparâmetros ótimos

**Funcionalidade**:
- Testa múltiplas combinações de parâmetros
- Calcula validação para cada combinação
- Salva resultados em CSV

**Uso**:
```bash
python hyperparameter_tuning.py
```

---

### `config.py`
**Propósito**: Configurações e constantes do projeto

**Conteúdo**:
- Caminhos de diretórios
- Configuração padrão de modelo
- Configuração padrão de treinamento
- Configuração de dados

**Uso**:
```python
from config import MODEL_CONFIG, TRAINING_CONFIG, DEVICE
```

---

## Fluxo de Execução Típico

### 1. Primeira Execução (Treinar Modelo)
```bash
python main.py
```

Executa:
- ✓ Carrega dados MNIST
- ✓ Cria modelo
- ✓ Treina modelo
- ✓ Avalia em todos os sets
- ✓ Salva pesos e gráficos

### 2. Visualizar Resultados
```bash
python visualize.py
```

Gera:
- Matriz de confusão
- Visualizações de predições
- Análise por classe

### 3. Fazer Inferência
```bash
python inference.py
```

Demonstra:
- Carregar modelo treinado
- Fazer predições em dados de teste

## Dependências Entre Módulos

```
main.py
├── src.model (MNIST_CNN)
├── src.train (train_model, get_optimizer)
├── src.evaluate (evaluate_model, print_evaluation_results)
└── src.utils (get_device, load_mnist_data, save_model, plot_training_loss)

inference.py
├── src.model (MNIST_CNN)
├── src.evaluate (predict_single)
└── src.utils (get_device)

visualize.py
├── src.model (MNIST_CNN)
└── (torch, matplotlib, seaborn)

hyperparameter_tuning.py
├── src.model (MNIST_CNN)
├── src.train (train_model, get_optimizer)
├── src.evaluate (evaluate_model)
└── src.utils (get_device, load_mnist_data)
```

## Convenções de Código

### Nomenclatura
- `snake_case` para funções e variáveis
- `CamelCase` para classes
- `UPPERCASE` para constantes

### Estrutura de Função
```python
def function_name(param1: type, param2: type) -> ReturnType:
    """
    Brief description.
    
    Args:
        param1 (type): Description
        param2 (type): Description
        
    Returns:
        ReturnType: Description
    """
```

### Type Hints
Sempre use type hints para melhor documentação e IDE support:
```python
from typing import Tuple, List, Optional

def my_function(x: int, y: str) -> Tuple[int, str]:
    pass
```

## Como Estender o Projeto

### Adicionar Novo Script
1. Crie arquivo em raiz do projeto
2. Importe classes/funções de `src/`
3. Siga as convenções de código

### Adicionar Nova Função à `utils.py`
1. Implemente a função
2. Adicione docstring completa
3. Atualize este documento

### Modificar Arquitetura CNN
1. Edite `src/model.py`
2. Atualize `src/utils.py` se necessário
3. Teste com `python main.py`

---

**Última atualização**: 2024
