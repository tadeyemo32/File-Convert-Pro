import os
import subprocess
import sys
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFileDialog, QComboBox, QTextEdit,
                             QProgressBar, QMessageBox, QGroupBox, QSizePolicy)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor, QLinearGradient, QPainter


class DarkTheme:
    @staticmethod
    def apply(app):
        app.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(18, 18, 18))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.AlternateBase, QColor(40, 40, 40))
        palette.setColor(QPalette.ToolTipBase, QColor(40, 40, 40))
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(40, 40, 40))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Highlight, QColor(0, 122, 204))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(palette)
        app.setStyleSheet("""
            QToolTip { 
                background-color: #2a2a2a; 
                color: white; 
                border: 1px solid #404040; 
            }
            QGroupBox { 
                border: 1px solid #404040;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #404040;
                border-radius: 4px;
                background: #252525;
            }
            QComboBox::drop-down {
                border: none;
            }
            QTextEdit {
                background: #252525;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 5px;
            }
        """)


class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.normal_style = """
            QPushButton {
                background-color: #2a2a2a;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 500;
            }
        """
        self.hover_style = """
            QPushButton {
                background-color: #404040;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 500;
            }
        """
        self.setStyleSheet(self.normal_style)
        
    def enterEvent(self, event):
        self.animate_hover(True)
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.animate_hover(False)
        super().leaveEvent(event)
        
    def animate_hover(self, hover):
        animation = QPropertyAnimation(self, b"geometry")
        animation.setDuration(150)
        animation.setEasingCurve(QEasingCurve.OutQuad)
        rect = self.geometry()
        if hover:
            animation.setEndValue(rect.adjusted(-2, -2, 2, 2))
        else:
            animation.setEndValue(rect.adjusted(2, 2, -2, -2))
        animation.start()


class FileConverterGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Converter Pro")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(700, 500)
        self.setWindowIcon(QIcon.fromTheme("document-convert"))
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        self.setup_ui()
        self.conversion_process = None
        self.desktop_path = os.path.expanduser("~/Desktop")
        
    def setup_ui(self):
        self.create_header()
        self.create_file_selection()
        self.create_conversion_section()
        
    def create_header(self):
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("File Converter Pro")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff;")
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        self.main_layout.addWidget(header)
        
    def create_file_selection(self):
        file_group = QGroupBox("File Selection")
        file_layout = QVBoxLayout()
        file_layout.setSpacing(10)
        
        self.input_label = QLabel("No file selected")
        self.input_label.setWordWrap(True)
        self.input_label.setStyleSheet("color: #42a2d8; font-size: 12px;")
        
        browse_btn = AnimatedButton("Browse File")
        browse_btn.clicked.connect(self.select_input_file)
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["jpg", "png", "webp", "bmp", "tiff", "mp3", "gif", "pdf", "docx"])
        self.format_combo.setCurrentIndex(1)
        
        self.output_name = QLabel("Output will be saved to Desktop")
        self.output_name.setWordWrap(True)
        self.output_name.setStyleSheet("color: #aaaaaa; font-size: 12px;")
        
        file_layout.addWidget(QLabel("Input File:"))
        file_layout.addWidget(self.input_label)
        file_layout.addWidget(browse_btn)
        file_layout.addWidget(QLabel("Convert to:"))
        file_layout.addWidget(self.format_combo)
        file_layout.addWidget(self.output_name)
        file_group.setLayout(file_layout)
        
        self.main_layout.addWidget(file_group)
        
    def create_conversion_section(self):
        convert_group = QGroupBox("Conversion")
        convert_layout = QVBoxLayout()
        convert_layout.setSpacing(15)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #404040;
                border-radius: 4px;
                text-align: center;
                background: #252525;
            }
            QProgressBar::chunk {
                background-color: #007acc;
                border-radius: 4px;
            }
        """)
        
        self.convert_btn = AnimatedButton("Convert")
        self.convert_btn.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:disabled {
                background-color: #505050;
            }
        """)
        self.convert_btn.clicked.connect(self.start_conversion)
        self.convert_btn.setEnabled(False)
        
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("""
            QTextEdit {
                background-color: #252525;
                color: #e0e0e0;
                border: 1px solid #404040;
                padding: 8px;
                font-family: 'Courier New', monospace;
                font-size: 11px;
            }
        """)
        
        convert_layout.addWidget(self.progress_bar)
        convert_layout.addWidget(self.convert_btn)
        convert_layout.addWidget(QLabel("Conversion Log:"))
        convert_layout.addWidget(self.log_output)
        convert_group.setLayout(convert_layout)
        
        self.main_layout.addWidget(convert_group)
        
    def select_input_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select File", "", 
            "All Supported Files (*.png *.jpg *.jpeg *.webp *.bmp *.tiff *.mp4 *.pdf *.docx);;"
            "Image Files (*.png *.jpg *.jpeg *.webp *.bmp *.tiff);;"
            "Video Files (*.mp4);;"
            "Document Files (*.pdf *.docx);;"
            "All Files (*)"
        )
        
        if file_path:
            self.input_file = file_path
            self.input_label.setText(file_path)
            self.update_output_name()
            self.convert_btn.setEnabled(True)
            self.update_supported_formats(os.path.splitext(file_path)[1].lower())
            self.log_output.append(f"Selected file: {file_path}")
            
    def update_supported_formats(self, input_ext):
        format_map = {
            '.png': ['jpg', 'jpeg', 'webp', 'bmp', 'tiff'],
            '.jpg': ['png', 'jpeg', 'webp', 'bmp', 'tiff'],
            '.jpeg': ['png', 'jpg', 'webp', 'bmp', 'tiff'],
            '.webp': ['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
            '.bmp': ['png', 'jpg', 'jpeg', 'webp', 'tiff'],
            '.tiff': ['png', 'jpg', 'jpeg', 'webp', 'bmp'],
            '.mp4': ['mp3', 'gif'],
            '.pdf': ['docx'],
            '.docx': ['pdf']
        }
        
        current_text = self.format_combo.currentText()
        self.format_combo.clear()
        
        if input_ext in format_map:
            self.format_combo.addItems(format_map[input_ext])
            if current_text in format_map[input_ext]:
                self.format_combo.setCurrentText(current_text)
        else:
            self.convert_btn.setEnabled(False)
            QMessageBox.warning(self, "Unsupported File", f"File extension '{input_ext}' is not supported for conversion.")
    
    def update_output_name(self):
        if hasattr(self, 'input_file'):
            base_name = os.path.splitext(os.path.basename(self.input_file))[0]
            output_ext = self.format_combo.currentText()
            output_path = os.path.join(self.desktop_path, f"{base_name}_converted.{output_ext}")
            self.output_name.setText(f"Output will be saved to:\n{output_path}")
    
    def start_conversion(self):
        if not hasattr(self, 'input_file'):
            return
            
        output_format = self.format_combo.currentText()
        input_file = self.input_file
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(self.desktop_path, f"{base_name}_converted.{output_format}")
        
        self.log_output.append(f"\nStarting conversion to {output_format}...")
        self.progress_bar.setValue(10)
        QApplication.processEvents()
        
        try:
            if output_format in ['mp3', 'gif'] and input_file.lower().endswith('.mp4'):
                self.convert_with_ffmpeg(input_file, output_file, output_format)
            else:
                self.convert_with_cpp_tool(input_file, output_format, output_file)
                
            self.progress_bar.setValue(100)
            self.log_output.append("Conversion completed successfully!")
            
            reply = QMessageBox.question(
                self, 'Success', 
                'Conversion completed successfully!\nWould you like to open the output file?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            
            if reply == QMessageBox.Yes:
                if sys.platform == "win32":
                    os.startfile(output_file)
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, output_file])
                    
        except Exception as e:
            self.log_output.append(f"Error: {str(e)}")
            self.progress_bar.setValue(0)
            QMessageBox.critical(self, "Conversion Failed", f"An error occurred:\n{str(e)}")
    
    def convert_with_cpp_tool(self, input_file, output_format, output_file):
        if not os.path.exists("./fileconvert"):
            raise FileNotFoundError("The fileconvert executable was not found in the current directory")
            
        cmd = ["./fileconvert", input_file, output_format]
        self.log_output.append(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd, 
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.stdout:
                self.log_output.append(result.stdout)
            if result.stderr:
                self.log_output.append(result.stderr)
                
            self.progress_bar.setValue(70)
            
            if os.path.exists(f"{os.path.splitext(input_file)[0]}_converted.{output_format}"):
                os.rename(f"{os.path.splitext(input_file)[0]}_converted.{output_format}", output_file)
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"Conversion failed with error:\n{e.stderr}")
    
    def convert_with_ffmpeg(self, input_file, output_file, output_format):
        if output_format == "mp3":
            cmd = [
                "ffmpeg", "-i", input_file,
                "-q:a", "0", "-map", "a",
                output_file
            ]
        else:
            cmd = [
                "ffmpeg", "-i", input_file,
                "-vf", "fps=10,scale=640:-1:flags=lanczos",
                output_file
            ]
            
        self.log_output.append(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.stdout:
                self.log_output.append(result.stdout)
            if result.stderr:
                self.log_output.append(result.stderr)
                
            self.progress_bar.setValue(70)
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"FFmpeg conversion failed with error:\n{e.stderr}")
        except FileNotFoundError:
            raise Exception("FFmpeg is not installed or not in system PATH")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    DarkTheme.apply(app)
    
    font = QFont()
    font.setFamily("Segoe UI" if sys.platform == "win32" else "Helvetica")
    font.setPointSize(10)
    app.setFont(font)
    
    window = FileConverterGUI()
    window.show()
    sys.exit(app.exec_())