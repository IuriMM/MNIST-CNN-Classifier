# 🌐 MNIST Digit Classifier - Web Interface

Interface web interativa para classificação de dígitos MNIST com predições em tempo real!

## 🎯 Features

✅ **Drawing Canvas** - Desenhe dígitos com mouse ou toque  
✅ **Real-time Prediction** - Predições automáticas enquanto desenha  
✅ **ONNX Runtime JS** - Inferência no navegador (sem servidor)  
✅ **Beautiful UI** - Design moderno e responsivo  
✅ **Gallery** - Histórico de predições  
✅ **Mobile Support** - Funciona em smartphones e tablets  
✅ **GitHub Pages Ready** - Deploy gratuito no GitHub Pages  

---

## 🚀 Quick Start

### 1. Converter Modelo PyTorch para ONNX

```bash
# Certifique-se de que o modelo foi treinado
python main.py --epochs 10

# Converter para ONNX (necessário para rodar no navegador)
python convert_to_onnx.py
```

Isso criará `web/models/mnist_cnn.onnx` (~400 KB).

### 2. Testar Localmente

```bash
# Opção 1: Usar Python http.server
cd web
python -m http.server 8000

# Opção 2: Usar Node.js http-server
npm install -g http-server
http-server web

# Opção 3: Usar VS Code Live Server
# Extension: ritwickdey.LiveServer
# Clique em "Go Live" na barra de status
```

Abra em seu navegador: `http://localhost:8000`

### 3. Deploy no GitHub Pages

#### Opção A: Repository Pages (main branch)

```bash
# 1. Crie um repositório no GitHub
git init
git remote add origin https://github.com/seu-usuario/MNIST-Classifier.git

# 2. Mude o arquivo de deploy
mv web/* .
rm -r web

# 3. Push para main branch
git add .
git commit -m "Initial commit"
git push -u origin main

# 4. Vá para Settings > Pages
# - Source: main branch
# - Folder: / (root)
# - Save

# 5. Acesse: https://seu-usuario.github.io/MNIST-Classifier
```

#### Opção B: Separate Docs Folder

```bash
# 1. Crie pasta docs
mkdir docs
cp web/* docs/
rm -r web

# 2. Git push
git add .
git commit -m "Add web interface"
git push

# 3. Settings > Pages
# - Source: main branch
# - Folder: /docs
# - Save

# 4. Acesse: https://seu-usuario.github.io/seu-repo
```

#### Opção C: GitHub Actions (Automático)

Crie `.github/workflows/deploy.yml`:

```yaml
name: Deploy Web Interface

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./web
          cname: seu-dominio.com  # Opcional
```

---

## 📁 Estrutura de Arquivos

```
web/
├── index.html          # Página principal
├── css/
│   └── style.css       # Estilos (1000+ linhas)
├── js/
│   └── app.js          # Lógica da aplicação (400+ linhas)
└── models/
    └── mnist_cnn.onnx  # Modelo convertido (400 KB)
```

---

## 🎨 Interface

### Canvas
- **Tamanho**: 280×280 pixels (mesmo tamanho que MNIST treina)
- **Cor**: Preto (invertido para branco internamente)
- **Pincel**: Ajustável (5-25px)
- **Suporte**: Mouse, toque, tablet

### Resultados
- **Predição Principal**: Dígito identificado + confiança
- **Barra de Confiança**: Visualização do nível de certeza
- **Matriz de Probabilidades**: Probabilidade para cada dígito (0-9)
- **Tempo de Inferência**: Velocidade da predição

### Controles
- **Predizer**: Fazer predição manual
- **Limpar**: Apagar o canvas
- **Desfazer**: Remover último traço

---

## 🔧 Tecnologia

### Frontend
- **HTML5 Canvas** - Renderização e desenho
- **CSS3** - Animações e design responsivo
- **Vanilla JavaScript** - Sem dependências externas

### Inferência
- **ONNX Runtime JS** - Execução do modelo no navegador
- **WebAssembly** - Performance otimizada

### Deployment
- **GitHub Pages** - Hosting estático gratuito
- **CDN** - ONNX Runtime via CDN

---

## 🖼️ Funcionalidades

### Drawing
```javascript
// Desenhe com mouse ou toque
// Canvas detecta automaticamente
```

### Real-time Prediction
```javascript
// Predição automática a cada 500ms
// Ou clique o botão "Predizer"
autoPredict = true;  // Ativar/desativar
```

### Gallery
```javascript
// Últimas 20 predições aparece em galeria
// Mostra dígito e confiança
// Thumbnail do desenho ao hover
```

### Brush Size
```javascript
// Ajuste o tamanho do pincel
// Slider de 5 a 25 pixels
// Atualiza em tempo real
```

---

## 📊 Preprocessing

A imagem passa por preprocessing antes da predição:

1. **Resize**: Canvas 280×280 → Modelo 28×28
2. **Grayscale**: Conversão para escala de cinza
3. **Normalize**: Normalização para [0, 1]
4. **Invert**: Inversão (MNIST usa branco em preto)

```javascript
// Implementado em preprocessImage()
// Usa Canvas Context 2D para transformações
```

---

## 🚀 Performance

- **Tempo de Carregamento**: ~2-3 segundos (primeira vez, caches depois)
- **Inferência**: ~50-100ms (dependendo do dispositivo)
- **Tamanho do Modelo**: ~400 KB (ONNX comprimido)
- **Suporte**: Chrome, Firefox, Safari, Edge

---

## 🐛 Debugging

### Console do Navegador
Pressione `F12` e vá para "Console"

```javascript
// Comandos disponíveis:
app.predict()              // Predizer manualmente
app.clearCanvas()          // Limpar
app.getPredictions()       // Ver histórico
app.getDrawingData()       // Obter imagem
app.session()              // Ver info do modelo
```

### Verificar Se o Modelo Carregou
```javascript
// No console:
console.log(app.session());

// Se null = modelo não foi convertido
// Se objeto = modelo carregado com sucesso
```

---

## ⚠️ Troubleshooting

### Modelo não carrega
**Problema**: ONNX Runtime JS encontra erro  
**Solução**:
```bash
# Reconverter modelo
python convert_to_onnx.py

# Verificar arquivo
ls -lh web/models/mnist_cnn.onnx

# Deve ter ~400KB
```

### Predições incorretas
**Problema**: Predições não fazem sentido  
**Solução**:
- Desenhe números mais claramente
- Inteiro o número dentro do canvas
- Tente usar outro dígito

### Lentidão em mobile
**Problema**: Predições lentas em smartphone  
**Solução**:
- Use WebAssembly (padrão)
- Reduza tamanho do brush
- Limite gallery a 10 itens

### Canvas não responde
**Problema**: Cliques não funcionam  
**Solução**:
```javascript
// Verifique no console
app.session()

// Recarregue a página (Ctrl+R ou Cmd+R)
```

---

## 📱 Responsividade

A interface adapta-se para:
- 🖥️ **Desktop** (1200px+)
- 💻 **Laptop** (768px-1200px)
- 📱 **Mobile** (320px-768px)

Teste em diferentes tamanhos:
```bash
# Chrome DevTools
F12 → Ctrl+Shift+M  # Toggle device mode
```

---

## 🎓 Customizações

### Mudar Cores
Edite `web/css/style.css`:

```css
:root {
    --primary-color: #2E86AB;      /* Azul */
    --secondary-color: #A23B72;    /* Rosa */
    --accent-color: #F18F01;       /* Laranja */
}
```

### Mudar Tamanho do Canvas
Edite `web/js/app.js`:

```javascript
const CANVAS_SIZE = 280;  // Aumentar/diminuir
const MODEL_SIZE = 28;    // Não mude (fixo para MNIST)
```

### Adicionar Sons
Inclua biblioteca como Howler.js e adicione:

```javascript
// em predict():
const sound = new Howl({ src: ['predict.mp3'] });
sound.play();
```

### Salvar Predições
Adicione localStorage:

```javascript
// Em addToGallery():
localStorage.setItem('predictions', JSON.stringify(predictions));

// Em init():
predictions = JSON.parse(localStorage.getItem('predictions') || '[]');
```

---

## 🌍 Deploying para Domínio Próprio

### Com Domínio Customizado

1. **Compre domínio** (ex: namecheap.com)

2. **Aponte para GitHub Pages**:
   ```
   CNAME Record: seu-dominio.com → seu-usuario.github.io
   A Records: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
   ```

3. **Crie arquivo CNAME** em `web/CNAME`:
   ```
   seu-dominio.com
   ```

4. **Settings > Pages**:
   - Source: main / /docs folder
   - Custom domain: seu-dominio.com
   - Enforce HTTPS: ✓

---

## 📈 Estatísticas

| Métrica | Valor |
|---------|-------|
| Linhas de Código | 1,500+ |
| Tamanho do HTML | 15 KB |
| Tamanho do CSS | 25 KB |
| Tamanho do JS | 12 KB |
| Tamanho do Modelo | 400 KB |
| **Total** | **~465 KB** |

Depois do cache do navegador, carrega em <100ms.

---

## 🤝 Contribuindo

Ideias para melhorias:

- [ ] Suporte para múltiplos modelos
- [ ] Análise de confiança mais detalhada
- [ ] Export de predições (CSV, JSON)
- [ ] Tema escuro
- [ ] Integração com Twitter/Discord
- [ ] Histórico persistente
- [ ] Comparação com modelos anteriores

---

## 📞 Support

### Dúvidas Frequentes

**P: Preciso de servidor backend?**  
R: Não! Tudo roda no navegador com ONNX Runtime JS.

**P: Funciona offline?**  
R: Sim, após primeira carga (exceto primeiro carregamento do ONNX).

**P: Quanto custa hospedar no GitHub Pages?**  
R: Totalmente grátis! Até 1GB de armazenamento.

**P: Posso usar meu próprio modelo?**  
R: Sim! Treine com `main.py`, converta com `convert_to_onnx.py`, substitua `mnist_cnn.onnx`.

---

## 📝 Licença

MIT License - Use livremente em projetos pessoais e comerciais

---

## 🎉 Próximos Passos

1. ✅ Treinar modelo (`python main.py`)
2. ✅ Converter para ONNX (`python convert_to_onnx.py`)
3. ✅ Testar localmente (`cd web && python -m http.server 8000`)
4. ✅ Deploy no GitHub Pages (seguir instruções acima)
5. ✅ Compartilhar com amigos! 🚀

---

**Divirta-se desenhando números e vendo a IA adivinhar! 🎨🧠**

Made with ❤️ using PyTorch and JavaScript
