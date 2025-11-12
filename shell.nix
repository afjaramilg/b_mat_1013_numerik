let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.numpy
      python-pkgs.matplotlib
      python-pkgs.ipykernel
    ]))
  ];
    shellHook = ''
    alias configure-jupyter="python -m ipykernel install --user \
       --name="b_mat_1013_numerik-kernel" \
       --display-name="b_mat_1013_numerik""
    '';
}
