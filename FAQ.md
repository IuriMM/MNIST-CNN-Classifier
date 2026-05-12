# FAQ - Perguntas Frequentes

## Instalação e Setup

### P: Como instalar as dependências?
**R:** Execute:
```bash
pip install -r requirements.txt
```

### P: Preciso de GPU?
**R:** Não, mas é recomendado para treinamento mais rápido.
- **Com GPU (CUDA)**: ~2-3 minutos por 10 épocas
- **Com CPU**: ~10-15 minutos por 10 épocas
- **Com DirectML**: ~5-7 minutos por 10 épocas

### P: Como usar GPU?
**R:** O projeto detecta automaticamente. Se você tem GPU NVIDIA:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### P: Python 3.7 funciona?
**R:** Não. Requer Python 3.8+. Verifique com:
```bash
python --version
```

---

## Treinamento

### P: Por que o treinamento demora tanto?
**R:** Depende do seu hardware:
- **GPU**: Esperado (rápido)
- **CPU**: Normal para 10 épocas
- **Dicas**: Reduza batch_size ou epochs

### P: Como acelerar o treinamento?
**R:** Várias opções:
```bash
# Aumentar batch size
python main.py --batch-size 128

# Reduzir épocas
python main.py --epochs 5

# Usar GPU se disponível (automático)
```

### P: O modelo não treina bem. O que fazer?
**R:** Tente:
1. Aumentar número de épocas: `--epochs 50`
2. Reduzir learning rate: `--lr 0.0001`
3. Usar SGD: `--optimizer sgd`

### P: Posso interromper e retomar o treinamento?
**R:** Atualmente não (seria uma boa feature!). 
Workaround: Aumente `--epochs` da próxima vez.

### P: Como mudador a arquitetura?
**R:** Edite `src/model.py`:
- `filters1`: Primeiro layer
- `filters2`: Segundo layer
- `dense_units`: Camada densa
- `dropout`: Regularização

---

## Resultados e Avaliação

### P: Por que meu modelo tem acurácia diferente?
**R:** Fatores que influenciam:
- Inicialização aleatória dos pesos
- Ordem dos dados (shuffle)
- Hardware (pequenas diferenças)

### P: 99% de acurácia é bom?
**R:** Sim! MNIST é relativamente fácil. 
- Humanos: ~99.5%
- Estado-da-arte: ~99.5%+
- Este modelo: **99.03%** ✓

### P: Como comparar com outro modelo?
**R:** Use diferentes `--output-dir`:
```bash
python main.py --optimizer adam --output-dir outputs_adam
python main.py --optimizer sgd --output-dir outputs_sgd
```

### P: O modelo sofre de overfitting?
**R:** Não significativamente. Sinais de overfitting:
- Train accuracy: ~99.78%
- Test accuracy: ~99.03%
- Diferença: ~0.75% (pequena!)

---

## Hiperparâmetros

### P: Quais hiperparâmetros devo ajustar?
**R:** Ordem de importância:
1. Learning rate (`--lr`)
2. Batch size (`--batch-size`)
3. Número de épocas (`--epochs`)
4. Dropout (`--dropout`)

### P: Como fazer grid search?
**R:** Use o script dedicado:
```bash
python hyperparameter_tuning.py
```

### P: Qual é o melhor learning rate?
**R:** Depende do otimizador:
- Adam: 0.001 (padrão) a 0.0001
- SGD: 0.01 a 0.1
- RMSprop: 0.001 a 0.01

### P: Quanto dropout usar?
**R:** Comece com 0.25 (padrão):
- Sem dropout: Pode overfittar
- 0.1-0.3: Bom para MNIST
- 0.5+: Muito agressivo

---

## Dados e Inferência

### P: Onde fica o dataset MNIST?
**R:** Em `data/MNIST/raw/` após primeira execução.
Automáticamente baixado de:
http://yann.lecun.com/exdb/mnist/

### P: Posso usar meu próprio dataset?
**R:** Sim! Modifique `src/utils.py`:
```python
# Substitua load_mnist_data() com sua função
```

### P: Como fazer predição em nova imagem?
**R:** Use `inference.py`:
```bash
python inference.py
```

### P: Qual é o tamanho de imagem esperado?
**R:** 28×28 pixels em escala de cinza.

### P: Preciso normalizar as imagens?
**R:** Sim, as imagens devem estar em [0, 1].
Feito automaticamente pela pipeline!

---

## Troubleshooting

### P: Erro "No module named torch"
**R:** Instale dependências:
```bash
pip install -r requirements.txt
```

### P: Erro "CUDA out of memory"
**R:** Reduza batch size:
```bash
python main.py --batch-size 32
```

### P: Erro "FileNotFoundError: MNIST/raw/..."
**R:** Baixe o dataset manualmente:
```bash
python -c "from torchvision import datasets, transforms; datasets.MNIST(root='data', train=True, download=True)"
```

### P: Script não inicia
**R:** Verifique:
```bash
python main.py --help  # Mostra ajuda
python -c "import torch; print(torch.__version__)"  # Verifica versão
```

### P: Resultados muito diferentes entre execuções
**R:** Adicione seed para reprodutibilidade:
```python
torch.manual_seed(42)
np.random.seed(42)
```

---

## Performance e Otimização

### P: Como melhorar acurácia além de 99%?
**R:** Técnicas avançadas:
1. Data Augmentation
2. Batch Normalization
3. Arquitetura mais profunda
4. Ensemble methods

### P: Qual é o modelo mais rápido?
**R:** 
- Mais rápido: Batch size grande (128+)
- Mais preciso: Batch size menor (32)
- Equilíbrio: 64 (padrão)

### P: Posso usar quantização?
**R:** Sim, para deployment. Não está implementado.
Seria uma ótima contribuição!

---

## Contribuição

### P: Como contribuir?
**R:** Veja [CONTRIBUTING.md](CONTRIBUTING.md)

### P: Posso corrigir bugs?
**R:** Sim! Envie um PR com:
1. Descrição do bug
2. Passos para reproduzir
3. Sua solução

### P: Que features vocês querem?
**R:** Ideias bem-vindas!
- Data Augmentation
- Transfer Learning
- Quantização
- Deployment guides

---

## Licença e Uso

### P: Posso usar em projeto comercial?
**R:** Sim! Licença MIT permite.
Apenas cite a fonte.

### P: Preciso fazer algo especial?
**R:** Não, apenas respeite a licença MIT.

### P: Posso modificar o código?
**R:** Sim, é open source!

---

## Conceitos

### P: O que é CNN?
**R:** Rede Neural Convolucional. Excelente para imagens.

### P: Por que convolução?
**R:** Explora padrões locais em imagens.

### P: O que é Max Pooling?
**R:** Reduz dimensionalidade mantendo features importantes.

### P: O que é Dropout?
**R:** Regularização que previne overfitting.

---

## Referências

### P: Onde aprender mais sobre CNN?
**R:** Recursos recomendados:
- [PyTorch Documentation](https://pytorch.org/)
- [Deep Learning Book](https://www.deeplearningbook.org/)
- [MNIST Paper](http://yann.lecun.com/exdb/publis/pdf/lecun-98.pdf)

### P: Como citar este projeto?
**R:** 
```
MNIST CNN Classifier
https://github.com/seu-usuario/MNIST-CNN-Classifier
```

---

## Não encontrou sua dúvida?

- Verifique [README.md](README.md)
- Verifique [QUICKSTART.md](QUICKSTART.md)
- Abra uma [Issue](../../issues)
- Envie um [PR](../../pulls)

---

**Última atualização**: 2024
**Mantém**: Comunidade
