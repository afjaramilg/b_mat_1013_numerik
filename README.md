# b\_mat\_1013\_numerik
## setup
vom root des projektes:
```bash
python3 -m venv .b_mat_1013_numerik
source .b_mat_1013_numerik/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user \
       --name="b_mat_1013_numerik-kernel" \
       --display-name="b_mat_1013_numerik"
```

fuer nix-os user:
```bash
nix-shell shell.nix
```
Im Browser oeffnet sich daraufhin die Jupyter Notebook Seite unter localhost:8888
