# Quick Start Guide

Comece com o MNIST CNN Classifier em 5 minutos!

## 1. Instalação Rápida

```bash
# Clone ou navegue até o diretório do projeto
cd MNIST-CNN-Classifier

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# Instale dependências
pip install -r requirements.txt
```

## 2. Treine o Modelo (seu primeira execução)

```bash
# Execute com configuração padrão
python main.py
```

**O que acontece:**
- Dataset MNIST é baixado automaticamente (~20 MB)
- Modelo é treinado por 32 épocas
- Resultados são salvos em `outputs/`
- Tempo estimado: ~10-15 minutos (varia com hardware)

## 3. Visualize os Resultados

```bash
# Gere visualizações adicionais
python visualize.py
```

**Arquivos gerados:**
- `outputs/training_loss.png` - Curva de loss
- `outputs/predictions_visualization.png` - Predições de amostra
- `outputs/confusion_matrix.png` - Matriz de confusão
- `outputs/per_class_accuracy.png` - Acurácia por classe
- `outputs/conv_filters.png` - Filtros da primeira camada

## 4. Faça Predições

```bash
# Execute inferência em imagens de teste
python inference.py
```

## Exemplos de Uso

### Treinar com Parâmetros Customizados

```bash
# Treinamento rápido (5 épocas)
python main.py --epochs 5

# Treinar com SGD e learning rate mais alto
python main.py --optimizer sgd --lr 0.01 --epochs 20

# Modelo com menos regularização
python main.py --dropout 0.1

# Treinar com batches maiores (mais rápido)
python main.py --batch-size 128
```

### Grid Search de Hiperparâmetros

```bash
# Encontre a melhor configuração automaticamente
python hyperparameter_tuning.py
```

Isso vai testar múltiplas combinações de hiperparâmetros e salvar resultados em:
`outputs/hyperparameter_search_results.csv`

## Estrutura de Arquivos

```
outputs/
├── model_weights.pth           # Pesos do modelo treinado
├── training_loss.png           # Gráfico da curva de loss
├── metrics.txt                 # Métricas em formato texto
├── predictions_visualization.png
├── confusion_matrix.png
├── per_class_accuracy.png
└── conv_filters.png
```

## Próximos Passos

1. **Explore o código**: Veja `src/model.py` para entender a arquitetura
2. **Modifique o modelo**: Tente adicionar mais layers
3. **Experimente hiperparâmetros**: Use `--help` para todas as opções
4. **Crie um notebook**: Use Jupyter para exploração interativa
5. **Implemente Data Augmentation**: Melhore ainda mais o desempenho

## Troubleshooting

### Erro: "CUDA out of memory"
```bash
# Reduza o batch size
python main.py --batch-size 32
```

### Erro: "No module named torch"
```bash
# Reinstale dependências
pip install --upgrade -r requirements.txt
```

### Modelos anteriores sendo sobrescrito
```bash
# Especifique um novo diretório de saída
python main.py --output-dir outputs_v2
```

## Dicas de Performance

| Ação | Tempo economizado |
|------|------------------|
| Usar GPU em vez de CPU | ~10x mais rápido |
| Aumentar batch size | 20-30% mais rápido |
| Reduzir número de epochs | Proporcional à redução |

## Recursos Adicionais

- [README completo](README.md) - Documentação detalhada
- [PyTorch Documentation](https://pytorch.org/) - Referência PyTorch
- [MNIST Paper](http://yann.lecun.com/exdb/publis/pdf/lecun-98.pdf) - Artigo original

## Próximos Desafios

1. Alcance 99% de acurácia em menos de 5 épocas
2. Implemente validação cruzada
3. Adicione data augmentation
4. Crie um modelo que roda em tempo real em webcam
5. Compare com outras arquiteturas (ResNet, etc.)

---

**Dúvidas?** Veja o [README.md](README.md) para documentação completa!
