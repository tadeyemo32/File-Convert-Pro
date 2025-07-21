# FileConverter Pro

FileConverter Pro is a modern, cross-platform desktop application for converting images, videos, and documents between popular formats. It combines a high-performance native C++ backend with a polished PyQt5 GUI to deliver fast conversions and an intuitive user experience. It supports a wide range of file types and is designed for users who need a reliable and efficient conversion tool on macOS, Windows, and Linux.
![App Icon](/assets/1.png)
---

## Features

- Convert between major image formats: PNG, JPG, JPEG, WEBP, BMP, TIFF
- Extract audio from MP4 videos (MP4 to MP3)
- Convert MP4 videos to GIFs
- Convert between PDF and DOCX documents
- GUI built with PyQt5 featuring a responsive dark theme and animated interface
- Native performance using ImageMagick and FFmpeg
- Intelligent validation of supported input/output formats
- Built for desktop platforms with standalone builds available

---

## Architecture

**C++ CLI Tool (Backend)**

- Written in C++17
- Uses `Magick++` (ImageMagick C++ bindings) for image processing
- Invokes FFmpeg via `system()` for media conversions (MP4 to MP3/GIF)
- Uses the standard C++ library for path handling (`<filesystem>`), data structures (`<unordered_map>`), and string manipulation

**Python GUI (Frontend)**

- Built with PyQt5
- Interfaces with the C++ backend via `subprocess`
- Automatically handles file browsing, supported format selection, progress bar updates, and error reporting
- Applies a consistent dark theme using `QPalette` and Qt stylesheet customization

---

## Supported Conversions

| Input Format | Supported Output Formats              |
|--------------|----------------------------------------|
| .png         | jpg, jpeg, webp, bmp, tiff             |
| .jpg         | png, jpeg, webp, bmp, tiff             |
| .jpeg        | png, jpg, webp, bmp, tiff              |
| .webp        | png, jpg, jpeg, bmp, tiff              |
| .bmp         | png, jpg, jpeg, webp, tiff             |
| .tiff        | png, jpg, jpeg, webp, bmp              |
| .mp4         | mp3, gif                               |
| .pdf         | docx                                   |
| .docx        | pdf                                    |

---

## Build Instructions

### Requirements

- C++17-compatible compiler (g++ or clang++)
- ImageMagick development libraries (`Magick++`)
- FFmpeg installed and available in PATH
- Python 3.8+ with PyQt5
- CMake or Make (optional for build automation)

### Build C++ CLI Tool

#### macOS / Linux

```bash
cd cpp
g++ -std=c++17 fileconvert.cpp -o fileconvert `Magick++-config --cppflags --cxxflags --ldflags --libs`
