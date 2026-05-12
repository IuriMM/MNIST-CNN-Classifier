# Contribuindo para MNIST CNN Classifier

Agradecemos seu interesse em contribuir! Este documento fornece diretrizes e instruções para contribuir com este projeto.

## Como Contribuir

### Reportar Bugs

Se você encontrar um bug, por favor crie uma issue com:

1. **Título descritivo**: Descreva o problema brevemente
2. **Descrição detalhada**: Explique o problema com máximo detalhe possível
3. **Passos para reproduzir**: Lista exata de passos para reproduzir o bug
4. **Comportamento esperado**: O que deveria acontecer
5. **Comportamento atual**: O que realmente acontece
6. **Screenshots/Logs**: Se aplicável, inclua evidências
7. **Ambiente**: Python version, OS, packages versions

### Sugerir Melhorias

Sugestões de recursos ou melhorias são sempre bem-vindas! Ao criar uma issue de sugestão:

1. Use um título descritivo
2. Forneça uma descrição detalhada da sugestão
3. Explique por que essa melhoria seria útil
4. Liste exemplos de como a melhoria seria usada

### Pull Requests

1. **Fork** o repositório
2. **Clone** seu fork: `git clone https://github.com/seu-usuario/MNIST-CNN.git`
3. **Crie uma branch** para sua feature: `git checkout -b feature/nome-da-feature`
4. **Faça suas mudanças** seguindo as guidelines abaixo
5. **Teste** suas mudanças
6. **Commit** com mensagens claras: `git commit -m 'descrição clara da mudança'`
7. **Push** para sua branch: `git push origin feature/nome-da-feature`
8. **Abra um Pull Request** com descrição detalhada das mudanças

## Guidelines

### Código

- **Python Style**: Siga [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- **Docstrings**: Use docstrings no estilo Google (como nos arquivos existentes)
- **Type Hints**: Use type hints para melhor documentação
- **Testes**: Inclua testes para novas funcionalidades
- **Comentários**: Adicione comentários explicativos para código complexo

### Commits

- Use mensagens descritivas: `git commit -m 'Adicionar feature X'` não `git commit -m 'Update'`
- Um commit por feature/fix lógico
- Referência issues quando relevante: `Fixes #123`

### Documentação

- Atualize o README.md se fizer mudanças significativas
- Documente novas funcionalidades
- Mantenha exemplos atualizados

### Testes

Antes de fazer um PR, certifique-se de que:

```bash
# Seu código roda sem erros
python main.py --help

# Treinamento funciona
python main.py --epochs 2

# Inferência funciona
python inference.py
```

## Áreas de Contribuição

### Código

- [ ] Implementar Data Augmentation
- [ ] Adicionar mais arquiteturas (ResNet, VGG, etc.)
- [ ] Melhorar performance
- [ ] Adicionar técnicas de regularização
- [ ] Implementar visualizações adicionais

### Documentação

- [ ] Expandir README com mais exemplos
- [ ] Criar tutorials Jupyter
- [ ] Documentar parâmetros detalhadamente
- [ ] Adicionar troubleshooting guide

### Testes

- [ ] Adicionar unit tests
- [ ] Adicionar integration tests
- [ ] Testar em múltiplas versões de Python

### Experimentação

- [ ] Experimentar com diferentes arquiteturas
- [ ] Testar diferentes datasets
- [ ] Comparar com outros modelos

## Processo de Review

Seu PR será revisado por maintainers. Eles podem:

- Fazer perguntas sobre sua implementação
- Sugerir mudanças
- Solicitar testes adicionais
- Pedir correções antes de merge

Por favor, seja respeitoso e construtivo durante o processo de review.

## Código de Conduta

### Nossas Expectativas

- Respeito mútuo
- Comunicação inclusiva
- Foco construtivo
- Sem discriminação

### Comportamento Inaceitável

- Assédio em qualquer forma
- Linguagem ofensiva
- Bullying
- Discriminação

### Aplicação

Violações do código de conduta devem ser reportadas para os maintainers. Ações apropriadas serão tomadas.

## Dúvidas?

- Abra uma issue com a tag `[QUESTION]`
- Verifique issues já abertas
- Consulte a documentação

## Reconhecimento

Contribuidores serão reconhecidos no README e neste arquivo.

---

**Obrigado por contribuir! 🎉**
