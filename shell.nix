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
    ]))
  ];
    shellHook = ''
            echo "Starting jupyter notebook server"
            jupyter notebook
       '';


}
