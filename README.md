# b\_mat\_1013\_numerik
## setup (linux)
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

Daraufhin kann entweder der Jupyter Server gestartet werden oder die Datei ueber nvim geoffnet werden.
