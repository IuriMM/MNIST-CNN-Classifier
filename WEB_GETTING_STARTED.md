# 🎨 Web Interface - Getting Started

Interface web interativa para o MNIST Classifier - Desenhe números e deixe a IA adivinhar!

---

## 🚀 Começar em 3 Minutos

### 1️⃣ Converter Modelo

```bash
# Certifique-se que o modelo foi treinado
python main.py --epochs 10

# Converta para ONNX (necessário para JavaScript)
python convert_to_onnx.py
```

✅ Criará `web/models/mnist_cnn.onnx`

### 2️⃣ Testar Localmente

```bash
# Opção 1: Python (mais fácil)
cd web
python -m http.server 8000

# Opção 2: Node.js
npx http-server web

# Opção 3: VS Code Live Server
# Clique "Go Live" (canto inferior direito)
```

Abra seu navegador: **`http://localhost:8000`**

### 3️⃣ Começar a Desenhar!

- ✏️ Desenhe um número no canvas
- 🧠 Veja a IA fazer predição em tempo real
- 📊 Confira probabilidades de cada dígito
- 🎨 Experimente diferentes estilos

---

## 📁 O que foi Criado

```
web/
├── 📄 index.html              Interface bonita
├── 🎨 css/style.css          Design responsivo
├── 🧠 js/app.js             Lógica completa
├── 🤖 models/mnist_cnn.onnx Modelo (você precisa gerar)
└── 📖 README.md             Documentação
```

---

## 🎯 Features da Interface

| Feature | Descrição |
|---------|-----------|
| **Canvas 280x280** | Desenhe como MNIST espera |
| **Real-time Prediction** | Predição automática enquanto desenha |
| **Brush Size** | Ajuste de 5 a 25 pixels |
| **Gallery** | Últimas 20 predições com thumbnail |
| **Confidence Bar** | Visualize nível de certeza |
| **Probability Matrix** | Veja probabilidade de cada dígito |
| **Mobile Support** | Funciona em celulares |
| **Offline** | Roda 100% no navegador |

---

## 📊 Exemplos

### Desenhando Número 5

```
Canvas (280x280)                     Resultado
┌─────────────────┐                ┌────────────┐
│                 │                │ Predição:5 │
│   ╱╱╱╱╱╱        │    ===>        │  99.5%     │
│   │   │         │                └────────────┘
│   ╲╲╲╲╲         │
│     │           │
│   ╱╱╱╱╱╱        │
└─────────────────┘
```

### Resultados em Tempo Real

Enquanto desenha, a interface atualiza:

```
Época 1: ?
Época 2: 5? (50%)
Época 3: 5 (75%)
Época 4: 5 (85%)
Época 5: 5 (92%)
Final:   5 (99.5%) ✓
```

---

## 🌍 Deploy no GitHub Pages

### Opção 1: Automático (Recomendado)

```bash
# Já tem GitHub Actions configurado!
git push
# Deployment acontece automaticamente
```

Acesse em: `https://seu-usuario.github.io/MNIST-CNN-Classifier`

### Opção 2: Manual

Veja [DEPLOY_GITHUB_PAGES.md](../DEPLOY_GITHUB_PAGES.md) para instruções detalhadas.

---

## 💡 Debugging

Abra **Console do Navegador** (F12) para:

```javascript
// Ver histórico de predições
app.getPredictions()

// Fazer predição manualmente
app.predict()

// Limpar canvas
app.clearCanvas()

// Verificar se modelo carregou
console.log(app.session())
```

---

## ⚠️ Problemas Comuns

### "Modelo não carrega"

```bash
# Reconverter
python convert_to_onnx.py

# Verificar arquivo existe
ls -lh web/models/mnist_cnn.onnx
# Deve ter ~400 KB
```

### "Predições não funcionam"

1. Abra Console (F12)
2. Procure erros em vermelho
3. Se vir "Model not found" → reconverter
4. Se vir ONNX error → reinstalar dependencies

### "Canvas não responde"

```bash
# Recarregar página
Ctrl+R (Windows/Linux)
Cmd+R (Mac)

# Ou "hard refresh"
Ctrl+Shift+R
```

---

## 📱 Mobile

Funciona perfeitamente em celulares!

- ✅ Toque no canvas para desenhar
- ✅ Predição automática
- ✅ Interface responsiva
- ✅ Sem lags em dispositivos modernos

**Testar em mobile:**

```bash
# No seu computador (onde roda o servidor):
ipconfig getifaddr en0    # Mac
hostname -I               # Linux
ipconfig                  # Windows (procure IPv4 Address)

# No celular, acesse:
http://192.168.1.XXX:8000
# (substitua XXX pelo seu IP)
```

---

## 🎨 Customizar Cores

Edite `web/css/style.css`:

```css
:root {
    --primary-color: #2E86AB;      /* Azul */
    --secondary-color: #A23B72;    /* Rosa */
    --accent-color: #F18F01;       /* Laranja */
}
```

Seu novo tema aparece instantaneamente!

---

## 📈 Performance

| Métrica | Valor |
|---------|-------|
| Tempo de Carregamento | ~2 seg (primeira), <100ms (cache) |
| Inferência | 50-100ms |
| Tamanho Total | ~465 KB |
| Tamanho do Modelo | ~400 KB |

---

## 🔄 Workflow Típico

```
┌─────────────────────────────────┐
│ 1. Treinar Modelo               │
│    python main.py               │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│ 2. Converter para ONNX          │
│    python convert_to_onnx.py    │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│ 3. Testar Localmente            │
│    python -m http.server 8000   │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│ 4. Deploy no GitHub             │
│    git push                     │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│ 5. Compartilhar URL             │
│    https://seu-site.github.io   │
└─────────────────────────────────┘
```

---

## 🎁 Extra: Adicionar Mais Features

### 1. Salvar Predições Localmente

```javascript
// Em app.js, procure "localStorage"
// Descomente as linhas com localStorage
```

### 2. Exportar como Imagem

```javascript
// Botão para baixar desenho
function downloadDrawing() {
    const link = document.createElement('a');
    link.href = canvas.toDataURL();
    link.download = 'mnist_drawing.png';
    link.click();
}
```

### 3. Compartilhar no Twitter

```javascript
// Crie URL com predição
const text = `Desenhei o número ${prediction.digit} e a IA acertou com ${confidence}%!`;
const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}`;
window.open(url, '_blank');
```

---

## 📚 Documentação Completa

Veja [README.md](README.md) para:
- ✅ Explicação detalhada
- ✅ Troubleshooting completo
- ✅ Customizações avançadas
- ✅ Deploy em domínio próprio

---

## 🌟 Dicas Pro

1. **Desenhe Centralizado**: Números no meio do canvas são reconhecidos melhor
2. **Traços Contínuos**: Desenhos com linhas contínuas são melhores que pontilhados
3. **Tamanho Confortável**: Use brush 15-20px para melhor resultado
4. **Teste Vários**: Experimente diferentes estilos de número 5, 8, etc.

---

## 🚀 Próximo Passo

```bash
# 1. Gere o modelo ONNX
python convert_to_onnx.py

# 2. Teste localmente
cd web
python -m http.server 8000

# 3. Abra http://localhost:8000 e comece a desenhar!
```

---

**Divirta-se! 🎨🧠**

Feito com ❤️ usando PyTorch + JavaScript

Última atualização: 2024
