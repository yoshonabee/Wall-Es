# Wall-Es

A real time route planning system for multi-agents

## Init

```sh
# download the model weight
wget https://github.com/yoshonabee/Wall-Es/releases/download/0.0.1/weight.pkl -P backend/lib/torch/state_dict
pip install -r requirements.txt
```

## Run

```sh
./run.sh
```

Open `127.0.0.1:5000` on the browser.

## Test

```sh
python3 backend/test/test_game.py
python3 backend/test/test_game_print.py
```