#!/bin/bash

echo "Starting Ollama initialization script..."
# Baixar o modelo LLaMA 3.1


ollama serve & ollama pull llama3.1
echo "LLaMA 3.1 model downloaded successfully!"

ollama serve

# Executar o servidor Ollama