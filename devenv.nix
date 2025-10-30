{ pkgs
, lib
, config
, inputs
, ...
}: {
  languages.python = {
    enable = true;
    version = "3.13";
    uv = {
      enable = true;
      sync.enable = true;
    };
  };

  packages = [
    pkgs.age
  ];

  git-hooks.hooks = {
    shellcheck = {
      enable = true;
      files = "bin";
    };
    nixpkgs-fmt.enable = true;
    mypy = {
      enable = true;
      entry = ".devenv/state/venv/bin/mypy";
    };
    ruff.enable = true;
    ruff-format.enable = true;
  };

  dotenv.enable = true;

  scripts.deploy.exec = "bin/deploy";
  scripts.run-server.exec = ''
    flask --app dax --debug run
  '';
}
