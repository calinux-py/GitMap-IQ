# GitMapIQ

GitMap IQ is a GUI application designed to help you explore Git repositories interactively and visually. Features like repository cloning, file browsing, code previews, and AI-powered code explanations--GitMap IQ simplifies understanding repositories and directories.

![Windows](https://img.shields.io/badge/platform-Windows-blue) ![Python](https://img.shields.io/badge/language-Python-darkgreen) ![HTML](https://img.shields.io/badge/language-HTML-orange) ![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white)

[<img src="https://github.com/calinux-py/GitMap-IQ/blob/main/GitMap%20IQ/config/Screenshot%202024-10-19%20161600.png?raw=true" alt="UniUI" width="63%">](https://github.com/calinux-py/GitMap-IQ/blob/main/GitMap%20IQ/config/Screenshot%202024-10-19%20161600.png)

## Features

- **Clone and Browse Repositories**: Clone Git repositories directly from URLs or browse local directories.
- **File Explorer**: Navigate through the repository's file structure with a tree view.
- **Code Preview**: View the content of code files within the application.
- **AI-Powered Code Explanation**: Get detailed explanations of code files using OpenAI's GPT-3.5-turbo model.
- **Repository Visualization**: Visualize the directory structure of the repository.
- **Size Graph**: Analyze file sizes within the repository using interactive graphs.
- **Markdown Rendering**: View rendered `README.md` files.
- **Dark Mode**: Toggle between light and dark themes.
- **File Operations**: Open files or their containing folders directly from the application.

[<img src="https://github.com/calinux-py/GitMap-IQ/blob/main/GitMap%20IQ/config/Screenshot%202024-10-19%20161810.png?raw=true" alt="UniUI" width="63%">](https://github.com/calinux-py/GitMap-IQ/blob/main/GitMap%20IQ/config/Screenshot%202024-10-19%20161810.png)

## Installation

### Prerequisites

- **Python 3.6 or higher**
- **Git** (for cloning repositories)
- **OpenAI API Key** (for AI-powered code explanations)

### Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

*Alternatively, install packages manually:*

```bash
pip install PyQt5 requests matplotlib markdown
```

## Setup

### OpenAI API Key

GitMapIQ uses OpenAI's GPT-3.5-turbo model to generate code explanations. You need an API key to enable this feature.

1. Obtain your API key from [OpenAI](https://platform.openai.com/account/api-keys).
2. On first run, the application will prompt you to enter your API key.
3. The key will be saved in a configuration file at `config/openai.ini`.

## Usage

Run the application using the following command:

```bash
python gitmap.py
```

[<img src="https://github.com/calinux-py/GitMap-IQ/blob/main/GitMap%20IQ/config/Screenshot%202024-10-19%20161732.png?raw=true" alt="UniUI" width="63%">](https://github.com/calinux-py/GitMap-IQ/blob/main/GitMap%20IQ/config/Screenshot%202024-10-19%20161732.png)

## User Interface Overview

- **Repository Input**: Enter a Git repository URL to clone or select a local directory.
- **Clone/Browse Button**: Clone the repository or open the local directory.
- **Tabs**:
  - **Explorer**: Navigate the repository's file structure.
  - **Visualizer**: View a visual representation of the directory tree.
  - **Size Graph**: Analyze file sizes within the repository.
  - **Explanation**: Get AI-generated explanations for code files.
  - **Preview**: Preview the content of code files.
  - **ViewMD**: Render and view `README.md` files.
  - **Options**: Toggle dark mode and switch between repository and local directory modes.

## Features in Detail

### Clone and Browse Repositories

- **Clone Repository**: Enter a Git URL and click "Clone Repository" to clone and explore a remote repository.
- **Browse Directory**: Switch to file browser mode to select and explore a local directory.

### File Explorer

- **Navigate Files**: Use the tree view to browse through directories and files.
- **Context Menu**: Right-click on files to access options like "Open", "Open location", "Explanation", and "Preview".

### AI-Powered Code Explanation

- **Explain Code**: Right-click on a code file and select "Explanation" to receive a detailed explanation generated by AI.
- **OpenAI Integration**: Utilizes the GPT-3.5-turbo model for generating explanations.

### Repository Visualization

- **Visualizer Tab**: Provides a visual representation of the repository's directory structure.
- **Size Graph Tab**: Displays a graph of file sizes to help identify large files.

### Code Preview

- **Preview Files**: View the content of code files within the application without opening external editors.

### Markdown Rendering

- **ViewMD Tab**: Renders `README.md` files for easy reading within the application.

### Options

- **Dark Mode**: Toggle between light and dark themes for better visibility.
- **File Browser Mode**: Switch between cloning repositories and browsing local directories.

## Configuration

### Settings

- **Dark Mode**: Enable or disable dark mode in the "Options" tab.
- **File Browser**: Switch between repository URL input and local directory browsing.

### OpenAI API Key Management

- **First-Time Setup**: Enter your OpenAI API key when prompted on the first run.
- **Configuration File**: The API key is stored in `config/openai.ini`. You can edit or replace this file to update the key.

## Troubleshooting

- **Clone Failures**: Ensure the Git repository URL is correct and that you have internet connectivity.
- **OpenAI Errors**: Verify that your API key is valid and that you have an active OpenAI subscription.
- **File Not Opening**: Check that the file exists and that you have the necessary permissions.

## License

[MIT License](LICENSE).
