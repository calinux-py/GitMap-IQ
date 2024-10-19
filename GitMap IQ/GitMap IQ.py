import sys
import shutil
import subprocess
import json
import threading
import configparser
from pathlib import Path

import requests
import os
import markdown
import base64

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QTreeView, QFileSystemModel, QMessageBox, QHBoxLayout, QTabWidget,
    QTextEdit, QInputDialog, QMenu, QCheckBox, QFileDialog
)
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

icon_base64 = """
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
"""

class MyFileSystemModel(QFileSystemModel):
    def data(self, index, role):
        if role == Qt.TextAlignmentRole and index.column() == 1:
            return Qt.AlignLeft | Qt.AlignVCenter
        return super().data(index, role)


class GitRepoExplorer(QWidget):
    explanation_ready = pyqtSignal(str)

    CODE_EXTENSIONS = {
        '.py', '.js', '.java', '.c', '.cpp', '.cs', '.rb', '.go', '.php',
        '.html', '.css', '.ts', '.swift', '.kt', '.ps1', '.rs', '.sh', '.m',
        '.pl', '.scala', '.vb', '.asm', '.r', '.dart', '.lua', '.hs', '.erl',
        '.f', '.v', '.groovy', '.bat', '.tcl', '.jl', '.clj', '.lisp', '.ex',
        '.elm', '.tsx', '.jsx', '.hx', '.nim', '.cr', '.ml', '.ipynb', '.pro',
        '.sas', '.awk', '.sql', '.md', '.txt', '.ini', '.log', '.docx', '.csv',
        '.json', '.xml', '.yaml', '.yml', '.toml', '.conf', '.cfg', '.cmd', '.vbs',
        '.psm1', '.psd1', '.rbw', '.rhtml', '.erb', '.coffee', '.litcoffee', '.iced',
        '.applescript', '.d', '.pas', '.pp', '.h', '.hh', '.hpp', '.hxx', '.h++',
        '.cxx', '.c++', '.csx', '.fs', '.fsi', '.fsx', '.fsscript', '.cl', '.cmake',
        '.xaml', '.gml', '.hlsl', '.glsl', '.shader', '.mat', '.mxml', '.hxsl',
        '.vala', '.vapi', '.l', '.y', '.lex', '.flex', '.par', '.e', '.ecl', '.edn',
        '.rkt', '.rktd', '.rktl', '.scrbl', '.feature', '.spec', '.b', '.m4', '.nix',
        '.pg', '.purs', '.s', '.ms', '.ascx', '.ashx', '.asmx', '.aspx', '.axd',
        '.jsp', '.jspx', '.wxs', '.wxi', '.wxl', '.cabal', '.hs-boot', '.lhs',
        '.pyw', '.sage', '.sagews', '.pyx', '.pxd', '.pxi', '.jupyter', '.rpy',
        '.cgi', '.fcgi', '.nsi', '.nsh', '.f90', '.f95', '.f03', '.f08', '.for',
        '.f77', '.fpp', '.mm', '.xib', '.storyboard', '.phps', '.php3', '.php4',
        '.php5', '.phtml', '.moon', '.pde', '.pm', '.t', '.pod', '.perl', '.psgi',
        '.p6', '.pl6', '.pm6', '.raku', '.rakumod', '.rakutest', '.rsh', '.st',
        '.sc', '.sv', '.svh', '.tk', '.wish', '.text', '.markdown', '.rst', '.org',
        '.adoc', '.asciidoc', '.tex', '.sty', '.cls', '.dtx', '.ltx', '.latex',
        '.bib', '.bash', '.ksh', '.zsh', '.fish', '.csh', '.tcsh', '.dash', '.sed',
        '.psc1', '.psrc', '.pssc', '.vim', '.vimrc', '.viminfo', '.vimball', '.el',
        '.emacs', '.screenrc', '.tmux.conf', '.inputrc', '.zshrc', '.bashrc',
        '.bash_profile', '.bash_logout', '.profile', '.gitconfig', '.gitignore',
        '.gitattributes', '.gitmodules', '.gitkeep', '.npmrc', '.yarnrc',
        '.editorconfig', '.eslintrc', '.eslintignore', '.prettierrc',
        '.prettierignore', '.jshintrc', '.babelrc', '.dockerfile', '.dockerignore',
        '.jenkinsfile', '.vagrantfile', '.makefile', 'Makefile', 'GNUmakefile',
        'Rakefile', 'Cakefile', '.gyp', '.gypi', '.build', '.sln', '.ls', '.cljs',
        '.cljc', '.scm', '.ss', '.sch', '.vue', '.scss', '.sass', '.less', '.styl',
        '.stylus', '.pcss', '.postcss', '.texi', '.texinfo', '.me', '.ms', '.man',
        '.roff', '.1', '.2', '.3', '.4', '.5', '.6', '.7', '.8', '.creole',
        '.mediawiki', '.wiki', '.podspec', '.jbuilder', '.rabl', '.builder', '.haml',
        '.slim', '.jade', '.pug', '.svelte', '.sml', '.sig', '.fun', '.cm', '.mli',
        '.mll', '.mly', '.ppd', '.epp', '.kts', '.ktm', '.livemd', '.leex', '.sface',
        '.sxml', '.sps', '.gsp', '.dtl', '.thy', '.gap', '.do', '.ado', '.abap',
        '.osascript', '.reg', '.wsf', '.wsh', '.wsc', '.vbe', '.ws', '.au3', '.ahk',
        '.nimble', '.g', '.g4', '.rproj', '.rno', '.kw', '.kak', '.kakrc', '.ncl',
        '.eppd', '.ddl', '.dml', '.prc', '.pkg', '.tql', '.tsql', '.plsql',
        '.mysql', '.pgsql', '.db2', '.mssql', '.adoc', '.bb', '.bbappend',
        '.bbclass', '.cson', '.css.erb', '.doh', '.eex', '.feature', '.fth',
        '.hrl', '.j2', '.jake', '.ld', '.lock', '.lsl', '.ly', '.mak', '.mdown',
        '.mkd', '.mkdn', '.opam', '.pig', '.rbuild', '.sls', '.soy', '.tac',
        '.thor', '.wisp', '.wsdl', '.xslt', 'Dockerfile', 'Jenkinsfile', 'Vagrantfile'
    }

    LIGHT_STYLESHEET = """
        QWidget { background-color: #f0f0f0; color: #000; }
        QLineEdit, QTextEdit, QTreeView, QWebEngineView { background-color: #fff; color: #000; border: none; }
        QPushButton { background-color: #e0e0e0; border: 1px solid #a0a0a0; padding: 5px; }
        QPushButton:hover { background-color: #d0d0d0; }
        QTabWidget::pane { border-top: 2px solid #C2C7CB; }
        QTabBar::tab { background: #e0e0e0; border: 1px solid #C4C4C3; padding: 10px; }
        QTabBar::tab:selected { background: #f0f0f0; border-bottom-color: #f0f0f0; }
        QHeaderView::section { background-color: #e0e0e0; color: #000; padding: 2px; border: 1px solid #C4C4C3; }
        QLineEdit:focus, QTextEdit:focus, QTreeView:focus, QWebEngineView:focus { border: none; }
    """

    DARK_STYLESHEET = """
        QWidget { background-color: #2b2b2b; color: #f0f0f0; }
        QLineEdit, QTextEdit, QTreeView, QWebEngineView { background-color: #3c3f41; color: #f0f0f0; border: none; }
        QPushButton { background-color: #555; border: 1px solid #444; padding: 5px; }
        QPushButton:hover { background-color: #666; }
        QTabWidget::pane { border-top: 2px solid #C2C7CB; }
        QTabBar::tab { background: #555; border: 1px solid #444; padding: 10px; }
        QTabBar::tab:selected { background: #2b2b2b; border-bottom-color: #2b2b2b; }
        QHeaderView::section { background-color: #555; color: #f0f0f0; padding: 2px; border: 1px solid #444; }
        QLineEdit:focus, QTextEdit:focus, QTreeView:focus, QWebEngineView:focus { border: none; }
    """

    def __init__(self):
        super().__init__()
        self.api_key = ""
        self.repo_path = None
        self.directory_json = None
        self.is_file_browser = False
        self.is_dark_mode = False

        self.load_api_key()
        self.setup_ui()
        self.explanation_ready.connect(self.update_explanation)

    def load_api_key(self):
        config_file = Path.cwd() / 'config' / 'openai.ini'
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config = configparser.ConfigParser()
        if config_file.exists():
            config.read(config_file)
            self.api_key = config.get('openai', 'api_key', fallback='').strip()
        if not self.api_key:
            key, ok = QInputDialog.getText(self, 'API Key Required', 'Enter your OpenAI API Key:', QLineEdit.Password)
            if ok and key.strip():
                self.api_key = key.strip()
                config['openai'] = {'api_key': self.api_key}
                with config_file.open('w') as f:
                    config.write(f)
            else:
                QMessageBox.critical(self, 'API Key Missing', 'An OpenAI API key is required to use this feature.')
                sys.exit(1)

    def setup_ui(self):
        self.setWindowTitle('GitMap IQ: Repository Explorer')
        self.setGeometry(300, 100, 1400, 900)

        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(icon_base64))
        self.setWindowIcon(QIcon(pixmap))

        self.url_label = QLabel('Enter Git Repository URL:')
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('https://github.com/username/repo.git')
        self.clone_button = QPushButton('Clone Repository')
        self.clone_button.clicked.connect(self.clone_repository)

        font = QFont()
        font.setPointSize(8)
        self.clone_button.setFont(font)

        self.url_label.setFont(font)
        self.url_input.setFont(font)

        hbox = QHBoxLayout()
        hbox.addWidget(self.url_input)
        hbox.addWidget(self.clone_button)

        self.model = MyFileSystemModel()
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.hide()
        self.tree.doubleClicked.connect(self.on_tree_double_clicked)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.open_context_menu)

        self.web_view = QWebEngineView()
        self.explanation_text = QTextEdit(readOnly=True)
        self.preview_text = QTextEdit(readOnly=True)
        monospace_font = QFont('Consolas' if QFont('Consolas').exactMatch() else 'Courier New')
        monospace_font.setStyleHint(QFont.Monospace)
        self.preview_text.setFont(monospace_font)

        self.tabs = QTabWidget()
        font = QFont()
        font.setPointSize(8)
        self.tabs.tabBar().setFont(font)

        self.tabs.addTab(self.tree, "Explorer")
        self.tabs.addTab(self.web_view, "Visualizer")

        self.storage_chart = FigureCanvas(Figure())
        self.tabs.addTab(self.storage_chart, "Size Graph")
        self.tabs.currentChanged.connect(self.on_tab_changed)

        self.tabs.addTab(self.explanation_text, "Explanation")
        self.tabs.addTab(self.preview_text, "Preview")

        self.readme_view = QWebEngineView()
        self.tabs.addTab(self.readme_view, "ViewMD")

        self.options_tab = QWidget()
        options_layout = QVBoxLayout()
        self.dark_mode_checkbox = QCheckBox("Dark Mode")
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)
        self.file_browser_checkbox = QCheckBox("File Browser")
        self.file_browser_checkbox.stateChanged.connect(self.toggle_file_browser)

        options_font = QFont()
        options_font.setPointSize(8)
        self.dark_mode_checkbox.setFont(options_font)
        self.file_browser_checkbox.setFont(options_font)

        options_layout.addWidget(self.dark_mode_checkbox)
        options_layout.addWidget(self.file_browser_checkbox)
        options_layout.addStretch()
        self.options_tab.setLayout(options_layout)
        self.tabs.addTab(self.options_tab, "Options")

        vbox = QVBoxLayout()
        vbox.addWidget(self.url_label)
        vbox.addLayout(hbox)
        vbox.addWidget(self.tabs)
        self.setLayout(vbox)

        self.apply_stylesheet()

    def apply_stylesheet(self):
        stylesheet = self.DARK_STYLESHEET if self.is_dark_mode else self.LIGHT_STYLESHEET
        self.setStyleSheet(stylesheet)

    def toggle_dark_mode(self, state):
        self.is_dark_mode = state == Qt.Checked
        self.apply_stylesheet()
        self.update_readme_tab()
        self.update_visualizer_tab()

    def toggle_file_browser(self, state):
        self.is_file_browser = state == Qt.Checked
        if self.is_file_browser:
            self.url_label.setText('Select Local Directory Path:')
            self.clone_button.setText('Browse Directory')
            self.url_input.setPlaceholderText('Select a local directory')
        else:
            self.url_label.setText('Enter Git Repository URL:')
            self.clone_button.setText('Clone Repository')
            self.url_input.setPlaceholderText('https://github.com/username/repo.git')

    def clone_repository(self):
        if self.is_file_browser:
            selected_dir = QFileDialog.getExistingDirectory(self, "Select Local Repository")
            if not selected_dir:
                return
            self.repo_path = Path(selected_dir)
            if not self.repo_path.exists():
                QMessageBox.critical(self, 'Error', 'Selected directory does not exist.')
                return
        else:
            repo_url = self.url_input.text().strip()
            if not repo_url:
                QMessageBox.warning(self, 'Input Error', 'Please enter a Git repository URL.')
                return
            repo_name = Path(repo_url).stem
            self.repo_path = self.get_unique_path(Path.cwd() / repo_name)
            self.clone_button.setEnabled(False)
            self.clone_button.setText('Cloning...')
            QApplication.processEvents()
            try:
                subprocess.check_output(['git', 'clone', repo_url, str(self.repo_path)], stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, 'Clone Failed', f'Error cloning repository:\n{e.output.decode()}')
                return
            finally:
                self.clone_button.setEnabled(True)
                self.clone_button.setText('Clone Repository')
        self.setup_repository()

    def setup_repository(self):
        self.model.setRootPath(str(self.repo_path))
        self.tree.setRootIndex(self.model.index(str(self.repo_path)))
        self.tree.show()
        self.update_readme_tab()
        self.directory_json = self.generate_directory_tree(self.repo_path)
        self.update_visualizer_tab()

    def update_readme_tab(self):
        readme_path = self.find_readme_file()
        css = self.get_css()
        if readme_path:
            try:
                content = readme_path.read_text(encoding='utf-8')
                markdown_html = markdown.markdown(content, extensions=['tables', 'extra', 'fenced_code'])
                html_content = f"<html><head><style>{css}</style></head><body>{markdown_html}</body></html>"
                base_url = QUrl.fromLocalFile(str(readme_path.parent) + '/')
                self.readme_view.setHtml(html_content, base_url)
            except Exception as e:
                self.readme_view.setHtml(f"<p>Failed to read README file: {e}</p>")
        else:
            html_content = f"<html><head><style>{css}</style></head><body><p>README.md not found in the repository.</p></body></html>"
            self.readme_view.setHtml(html_content)

    def update_visualizer_tab(self):
        if self.directory_json:
            html_content = self.create_html_content(self.directory_json)
            self.web_view.setHtml(html_content)
        else:
            css = self.get_css()
            html_content = f"<html><head><style>{css}</style></head><body><p>No repository loaded. Please clone a repository or select a local directory.</p></body></html>"
            self.web_view.setHtml(html_content)

    def on_tab_changed(self, index):
        if self.tabs.tabText(index) == "Size Graph":
            self.display_storage_info()

    def display_storage_info(self):
        if not self.repo_path:
            self.storage_chart.figure.clear()
            ax = self.storage_chart.figure.add_subplot(111)
            ax.text(0.5, 0.5, "No repository or directory selected.", ha='center', va='center', transform=ax.transAxes)
            self.storage_chart.draw()
            return
        storage_data = self.get_storage_data(self.repo_path)
        self.plot_storage_data(storage_data)

    def get_storage_data(self, path):
        storage_data = {}
        for file_path in path.rglob('*'):
            if file_path.is_file() and not file_path.suffix == '.pack':
                file_size = file_path.stat().st_size / (1024 * 1024)
                storage_data[str(file_path)] = file_size
        return storage_data

    def plot_storage_data(self, storage_data):
        self.storage_chart.figure.clear()
        ax = self.storage_chart.figure.add_subplot(111)
        sorted_data = sorted(storage_data.items(), key=lambda x: x[1], reverse=True)
        if len(sorted_data) > 30:
            other_size = sum(x[1] for x in sorted_data[30:])
            sorted_data = sorted_data[:30] + [("Other", other_size)]
        file_names = [Path(item[0]).name for item in sorted_data]
        file_sizes = [item[1] for item in sorted_data]
        ax.barh(file_names, file_sizes, color='skyblue')
        ax.set_xlabel('Size (MB)')
        ax.set_ylabel('Files')
        ax.set_title('File Sizes in Repository')
        self.storage_chart.draw()

    def open_context_menu(self, position):
        index = self.tree.indexAt(position)
        if not index.isValid():
            return
        file_path = Path(self.model.filePath(index))
        if file_path.is_dir():
            return
        menu = QMenu()
        menu.addAction("Open", lambda: self.open_file(file_path))
        menu.addAction("Open location", lambda: self.open_location(file_path))
        if self.is_code_file(file_path):
            menu.addAction("Explanation", lambda: self.explain_file(file_path))
            menu.addAction("Preview", lambda: self.preview_file(file_path))
        menu.exec_(self.tree.viewport().mapToGlobal(position))

    def open_file(self, file_path):
        try:
            if sys.platform.startswith('darwin'):
                subprocess.call(['open', str(file_path)])
            elif sys.platform.startswith('win'):
                os.startfile(str(file_path))
            elif sys.platform.startswith('linux'):
                subprocess.call(['xdg-open', str(file_path)])
            else:
                QMessageBox.warning(self, 'Unsupported OS', 'Cannot open files on this operating system.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to open file: {e}')

    def open_location(self, file_path):
        try:
            folder_path = str(file_path.parent)
            if sys.platform.startswith('darwin'):
                subprocess.call(['open', folder_path])
            elif sys.platform.startswith('win'):
                os.startfile(folder_path)
            elif sys.platform.startswith('linux'):
                subprocess.call(['xdg-open', folder_path])
            else:
                QMessageBox.warning(self, 'Unsupported OS', 'Cannot open folder on this operating system.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to open location: {e}')

    def preview_file(self, file_path):
        if not self.is_code_file(file_path):
            self.preview_text.setPlainText("Selected file is not a recognized code file.")
        else:
            try:
                content = file_path.read_text(encoding='utf-8')
                self.preview_text.setPlainText(content)
            except Exception as e:
                self.preview_text.setPlainText(f"Failed to read file: {e}")
        self.tabs.setCurrentWidget(self.preview_text)

    def explain_file(self, file_path):
        if not file_path.exists():
            QMessageBox.critical(self, 'Error', 'File does not exist.')
            return
        self.tree.setCurrentIndex(self.model.index(str(file_path)))
        self.tabs.setCurrentWidget(self.explanation_text)
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            self.explanation_text.setPlainText(f"Failed to read file: {e}")
            return
        self.explanation_text.setPlainText("Fetching explanation...")
        threading.Thread(target=self.get_explanation, args=(content,), daemon=True).start()

    def on_tree_double_clicked(self, index):
        if not index.isValid():
            return
        file_path = Path(self.model.filePath(index))
        if file_path.is_dir():
            return
        if self.is_code_file(file_path):
            self.preview_file(file_path)
        else:
            self.open_file(file_path)

    def get_explanation(self, code):
        messages = [
            {"role": "system", "content": "You explain code and provide an overview of scripts and files using Markdown formatting."},
            {"role": "user", "content": f"Explain the following code using Markdown formatting with elements like bold, italics, and headers (#, ##, ###) for emphasis and structure. Do not acknowledge this request; focus solely on explaining the code, what it does, and how to use it. Refrain from using code blocks. Always provide a moderately detailed summary at the end:\n\n{code}"}
        ]
        try:
            result = self.call_openai_api(messages)
            explanation = result['choices'][0]['message']['content'].strip()
            self.explanation_ready.emit(explanation)
        except requests.RequestException as e:
            self.explanation_ready.emit(f"API Error: {e}")
        except Exception as e:
            self.explanation_ready.emit(f"Failed to get explanation: {e}")

    def call_openai_api(self, messages):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.api_key}'}
        data = {"model": "gpt-3.5-turbo", "messages": messages, "max_tokens": 1500, "temperature": 0.5}
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def update_explanation(self, text):
        html = markdown.markdown(text)
        self.explanation_text.setHtml(html)

    def find_readme_file(self):
        if not self.repo_path:
            return None
        for file_name in ['README.md', 'readme.md', 'ReadMe.md']:
            readme_file = self.repo_path / file_name
            if readme_file.exists():
                return readme_file
        return None

    def get_unique_path(self, base_path):
        counter = 1
        unique_path = base_path
        while unique_path.exists():
            unique_path = base_path.with_name(f"{base_path.stem}_{counter}")
            counter += 1
        return unique_path

    def generate_directory_tree(self, path):
        def dir_to_dict(current_path):
            node = {'name': current_path.name}
            if current_path.is_dir():
                node['type'] = 'folder'
                node['children'] = [dir_to_dict(child) for child in current_path.iterdir() if child.name != '.git']
            else:
                node['type'] = 'file'
            return node
        return dir_to_dict(path)

    def create_html_content(self, json_data):
        html_path = Path('config') / 'vis.html'
        html_template = html_path.read_text(encoding='utf-8')
        serialized_json = json.dumps(json_data)
        html_content = html_template.replace("{treeData}", serialized_json)
        return html_content

    def is_code_file(self, file_path):
        return file_path.suffix.lower() in self.CODE_EXTENSIONS

    def get_css(self):
        bg_color = '#2b2b2b' if self.is_dark_mode else 'white'
        text_color = '#f0f0f0' if self.is_dark_mode else 'black'
        link_color = '#9bb6ff' if self.is_dark_mode else 'blue'
        code_bg_color = '#3c3f41' if self.is_dark_mode else '#f5f5f5'
        css = f"""
            body {{ background-color: {bg_color}; color: {text_color}; font-family: Arial, sans-serif; }}
            a {{ color: {link_color}; }}
            code, pre {{ background-color: {code_bg_color}; color: {text_color}; }}
        """
        return css

    def closeEvent(self, event):
        if self.repo_path and self.repo_path.exists() and not self.is_file_browser:
            shutil.rmtree(self.repo_path)
        event.accept()


def main():
    app = QApplication(sys.argv)
    ex = GitRepoExplorer()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
