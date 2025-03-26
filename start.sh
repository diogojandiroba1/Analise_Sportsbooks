#!/bin/bash

# Baixa os navegadores necessários para o Playwright funcionar
playwright install chromium

# Roda o script principal
python backend/main.py
