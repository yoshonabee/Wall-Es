if [[ -z "${python3}" ]]; then
  python3 backend/main.py
else
  python backend/main.py
fi