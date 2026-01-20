let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.notebook
      python-pkgs.ipython
      python-pkgs.numpy
      python-pkgs.matplotlib
      python-pkgs.ipykernel
      python-pkgs.pynvim
      python-pkgs.jupyter-client
      python-pkgs.requests
      python-pkgs.websocket-client
    ]))
  ];
}
