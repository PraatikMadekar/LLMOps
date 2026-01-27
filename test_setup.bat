@echo off
cd /d "C:\Users\MIRACLE\Desktop\LLMOps"
call venv\Scripts\activate.bat
echo Testing model loader...
python -m multi_doc_chat.utils.model_loader
pause
