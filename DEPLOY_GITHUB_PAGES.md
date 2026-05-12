# Guia de Deploy - Hospedando no GitHub Pages

Siga este guia passo-a-passo para hospedar a interface web MNIST no GitHub Pages **gratuitamente**.

---

## 📋 Pré-requisitos

✅ Conta GitHub  
✅ Git instalado  
✅ Modelo MNIST treinado e convertido para ONNX  

---

## 🔧 Passo 1: Converter Modelo para ONNX

**Por que?** O navegador não consegue executar arquivos `.pth` do PyTorch. Precisamos converter para ONNX.

```bash
# No diretório do projeto
python convert_to_onnx.py
```

**Resultado esperado:**
```
✅ Model converted successfully
✓ Saved to: web/models/mnist_cnn.onnx
```

Se falhar:
```bash
# Instale ONNX (opcional mas recomendado)
pip install onnx

# Treine o modelo se ainda não fez
python main.py --epochs 10
```

---

## 📁 Passo 2: Estrutura de Pastas

Após a conversão, sua pasta deverá ter:

```
MNIST-CNN-Classifier/
├── web/
│   ├── index.html
│   ├── css/style.css
│   ├── js/app.js
│   └── models/mnist_cnn.onnx  ← Esse arquivo é importante!
├── .github/
│   └── workflows/deploy-pages.yml
└── ...outros arquivos...
```

---

## 🌐 Passo 3: Criar Repositório GitHub

### Opção A: GitHub Web (Mais Fácil)

1. Acesse [github.com/new](https://github.com/new)
2. Preencha:
   - **Repository name**: `MNIST-CNN-Classifier`
   - **Description**: "MNIST Digit Classifier - Draw and Predict"
   - **Public** (para habilitar GitHub Pages)
   - **Add .gitignore**: Python
3. Clique **Create repository**

### Opção B: GitHub CLI

```bash
# Instale: https://cli.github.com/

gh repo create MNIST-CNN-Classifier \
  --public \
  --source=. \
  --remote=origin \
  --push
```

---

## 📤 Passo 4: Fazer Push do Código

### Primeira vez (sem Git local):

```bash
# Navegue até a pasta do projeto
cd MNIST-CNN-Classifier

# Inicie repositório Git
git init

# Adicione seu repositório remoto
git remote add origin https://github.com/SEU-USUARIO/MNIST-CNN-Classifier.git

# Configure seu nome e email (primeira vez)
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@example.com"

# Adicione todos os arquivos
git add .

# Faça commit
git commit -m "Initial commit: MNIST Classifier with Web Interface"

# Faça push (substitua main por master se necessário)
git branch -M main
git push -u origin main
```

### Próximas vezes (depois de mudanças):

```bash
git add .
git commit -m "Sua mensagem de commit"
git push
```

---

## ⚙️ Passo 5: Ativar GitHub Pages

### Método 1: GitHub Actions (Automático) ⭐ Recomendado

O arquivo `.github/workflows/deploy-pages.yml` já está configurado!

1. Vá para seu repositório no GitHub
2. Clique em **Actions**
3. Se vir "Deploy Web Interface to GitHub Pages", está tudo certo!
4. Faça um push para disparar o deploy:

```bash
git add .
git commit -m "Trigger deploy"
git push
```

5. Volte para **Actions** e veja o workflow rodar
6. Aguarde conclusão (verde ✅)

### Método 2: Manual (Se GitHub Actions não funcionar)

1. Vá para **Settings** do seu repositório
2. Clique em **Pages** (esquerda)
3. Sob "Build and deployment":
   - **Source**: Deploy from a branch
   - **Branch**: `main` (ou `master`)
   - **Folder**: `/ (root)` se moveu web/* para raiz, ou `/web` se deixou em pasta
4. Clique **Save**

---

## 🔗 Passo 6: Acessar Sua Aplicação

Após deploy, sua aplicação estará disponível em:

```
https://SEU-USUARIO.github.io/MNIST-CNN-Classifier
```

**Exemplo:**
```
https://john-doe.github.io/MNIST-CNN-Classifier
```

---

## ✅ Checklist de Verificação

Após deploy, verifique:

- [ ] Site carrega sem erros (F12 para ver console)
- [ ] Canvas é renderizado (área para desenho)
- [ ] Botões funcionam (Limpar, Desfazer, Predizer)
- [ ] Console não mostra erros em vermelho
- [ ] Predições funcionam (mesmo que lentamente)

Se algo falhar:

```javascript
// No console (F12):
// 1. Verifique o modelo
app.session()

// Deve retornar um objeto (modelo carregado)
// Se null, o modelo não foi convertido/uploaded
```

---

## 🔄 Troubleshooting

### ❌ "404 Not Found"

**Problema**: Página não encontrada  
**Solução**:
1. Verifique se o repositório é **público**
2. Espere 5 minutos após push (GitHub Pages demora um pouco)
3. Verifique se os arquivos estão em `/web` ou na raiz
4. Limpe cache: Ctrl+Shift+R

### ❌ "Could not load model"

**Problema**: ONNX model não carrega  
**Solução**:
```bash
# Reconverter e fazer upload novamente
python convert_to_onnx.py

# Verificar arquivo
ls -lh web/models/mnist_cnn.onnx

# Fazer push
git add web/models/mnist_cnn.onnx
git commit -m "Update model"
git push
```

### ❌ GitHub Actions não dispara

**Problema**: Workflow não roda  
**Solução**:
1. Vá para **Settings > Actions > General**
2. Selecione **Allow all actions and reusable workflows**
3. Faça um novo push

### ❌ "Predições não funcionam"

**Problema**: Clica em "Predizer" mas nada acontece  
**Solução**:
1. Abra Console (F12)
2. Verifique se há erros
3. Se vir "Model not found" → reconverter modelo
4. Se vir ONNX errors → verificar versão do ONNX

---

## 🎨 Customizações Pós-Deploy

Você pode personalizar tudo após deploy!

### Mudar Título
Edite `web/index.html`:
```html
<title>Seu Nome - MNIST Classifier</title>
```

### Mudar Cores
Edite `web/css/style.css`:
```css
--primary-color: #SUA-COR;
```

### Adicionar seu nome
Edite `web/index.html`:
```html
<p>Criado por <strong>Seu Nome</strong></p>
```

### Fazer push das mudanças
```bash
git add web/
git commit -m "Customize interface"
git push
```

Deploy atualizado em minutos!

---

## 📊 URLs Compartilháveis

Agora você pode compartilhar sua aplicação!

**Compartilhar:**
```
Acesse meu classificador MNIST: https://seu-usuario.github.io/MNIST-CNN-Classifier
```

**Em redes sociais:**
- Twitter/X: "Criei um classificador de números com IA que roda no seu navegador! 🤖✏️"
- LinkedIn: "Implementei uma interface web para MNIST usando PyTorch e JavaScript"
- Discord: Cole o link nos canais de projetos

---

## 🔐 Privacidade e Segurança

✅ **Totalmente Seguro:**
- Nenhum dado é enviado para servidores
- Inferência acontece 100% no seu navegador
- Nenhum histórico é armazenado (a menos que você add localStorage)
- GitHub Pages usa HTTPS automático

---

## 🚀 Melhorando o Deploy

### Adicionar Domínio Customizado

Se você tem um domínio próprio:

1. Aponte DNS para GitHub Pages
2. Crie arquivo `web/CNAME`:
   ```
   seu-dominio.com
   ```
3. Settings > Pages > Custom domain
4. Enforce HTTPS

### Adicionar Badge ao README

```markdown
[![Deployed on GitHub Pages](https://img.shields.io/badge/deployed%20on-GitHub%20Pages-blue?style=for-the-badge)](https://seu-usuario.github.io/MNIST-CNN-Classifier)
```

### Adicionar Analytics

Instale [GoAccess](https://goaccess.io/) ou configure Google Analytics (já integrado em muitos temas).

---

## 📚 Próximas Etapas

Depois de fazer deploy:

1. ✅ Compartilhe o link com amigos
2. ✅ Peça feedback
3. ✅ Considere adicionar features:
   - [ ] Salvar predições em localStorage
   - [ ] Exportar como imagem
   - [ ] Tema escuro
   - [ ] Suporte a múltiplos idiomas

---

## 🆘 Precisa de Ajuda?

- **GitHub Pages Docs**: https://pages.github.com/
- **GitHub Actions**: https://docs.github.com/actions
- **ONNX Runtime JS**: https://onnxruntime.ai/docs/
- **Crie uma Issue** no repositório

---

## 🎉 Sucesso!

Se chegou aqui, parabéns! Sua aplicação MNIST está rodando **gratuitamente** no GitHub Pages! 🚀

**Agora é sua vez:**
- Experimente desenhar diferentes estilos
- Compartilhe com a comunidade
- Contribua com melhorias
- Inspire outras pessoas!

---

**Made with ❤️**

Última atualização: 2024
