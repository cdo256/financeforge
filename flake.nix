{
  description = "FinanceForge";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    pyproject.url = "github:nix-community/pyproject.nix";
  };

  outputs = { self, nixpkgs, flake-utils, pyproject }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python3;
        project = pyproject.lib.project.loadPyproject {
          projectRoot = ./.;
          format = "pyproject";
        };
      in {
        devShells.default = pkgs.mkShell {
          packages = [ python.withPackages (ps: [ ps.flask ps.setuptools ]) ];
        };

        packages.default = pkgs.python3Packages.buildPythonApplication {
          pname = "financeforge";
          version = "0.1.0";
          src = ./.;
          format = "pyproject";
          propagatedBuildInputs = [ pkgs.python3Packages.flask ];
        };
      }
    );
}
