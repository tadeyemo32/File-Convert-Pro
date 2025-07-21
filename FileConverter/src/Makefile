# Makefile for file converter using Magick++

CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2
MAGICK_CFLAGS = $(shell Magick++-config --cxxflags)
MAGICK_LDFLAGS = $(shell Magick++-config --ldflags --libs)

SRC = main.cpp
OUT = fileconvert

all: $(OUT)

$(OUT): $(SRC)
	$(CXX) $(CXXFLAGS) $(MAGICK_CFLAGS) -o $(OUT) $(SRC) $(MAGICK_LDFLAGS)

clean:
	rm -yf $(OUT)
