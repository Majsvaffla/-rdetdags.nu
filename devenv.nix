{
  pkgs,
  lib,
  config,
  inputs,
  ...
}: {
  languages.python = {
    enable = true;
    version = "3.13";
    uv = {
      enable = true;
      sync.enable = true;
    };
  };

  services.postgres = {
    enable = true;
    package = pkgs.postgresql_17;
    initialDatabases = [
      {
        name = "ärdetdags";
      }
    ];
  };

  git-hooks.hooks = {
    shellcheck = {
      enable = true;
      files = "bin";
    };
    alejandra.enable = true;
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
    flask --app dags --debug run
  '';
}
