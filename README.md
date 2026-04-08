# TockyCode 🧠💻

> **TockyCode** - Ferramenta de IA para geração de código 100% local e gratuita.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Android%20%7C%20Windows-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Recursos

- 🧠 **IA Local** - Funciona 100% offline, sem necessidade de internet
- 💰 **Gratuito** - Sem assinaturas, sem custos ocultos
- 🌐 **Multi-Plataforma** - Available as DEB, AppImage, and APK
- 🔤 **Múltiplas Linguagens** - Suporta 15+ linguagens de programação

## Supported Languages

| Categoria | Linguagens |
|-----------|------------|
| **Web** | JavaScript, TypeScript, HTML, CSS |
| **Backend** | Python, Go, Rust, Java, C++, C#, PHP, Ruby |
| **Mobile** | Swift, Kotlin |
| **Data** | SQL |
| **Config** | JSON, YAML |

## 📦 Distribuições

### Linux (DEB)
```bash
sudo dpkg -i tockycode_1.0.0_all.deb
tockycode --help
```

### Linux (AppImage)
```bash
chmod +x TockyCode-1.0.0.AppImage
./TockyCode-1.0.0.AppImage
```

### Android (APK)
```
Instale o arquivo TockyCode-android.apk no seu dispositivo Android
```

## 🚀 Uso via CLI

### Gerar código
```bash
tockycode generate -p "create a REST API in python with flask" -l python
```

### Opções
```
-p, --prompt <prompt>    Descrição do código a gerar (obrigatório)
-l, --language <lang>    Linguagem de programação (padrão: javascript)
-h, --help               Mostrar ajuda
```

## 📱 Interface Android

O aplicativo Android oferece:
- Interface gráfica intuitiva
- Seleção de linguagem de programação
- Campo de entrada para descrição do código
- Visualização e cópia do código gerado
- Tema escuro moderno com cores accent

## 🛠️ Desenvolvimento

### Estrutura do Projeto
```
Tocky/
├── tockycode-cli/       # Ferramenta CLI em Python
├── tockycode-appimage/  # Script AppImage
├── tockycode_app/       # Aplicativo Flutter (Android/iOS/Web)
├── deb-package/         # Pacote Debian
└── dist/               # Arquivos de distribuição prontos
```

### Requisitos
- **CLI**: Python 3.8+
- **AppImage**: Linux com suporte a AppImage
- **Android**: Android 5.0+ (API 21)

## 📄 Licença

MIT License - See [LICENSE](LICENSE) for details.

---

Feito com ❤️ por [DaviGayDaSilva](https://github.com/DaviGayDaSilva)

*Este projeto foi desenvolvido com assistência de IA.*