{

	description = "Twitter scraper and streamer.";

	inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
	inputs.flake-utils.url = "github:numtide/flake-utils";

	outputs = { self, nixpkgs, flake-utils, }:
	flake-utils.lib.eachDefaultSystem (system: let
		pkgs = nixpkgs.legacyPackages.${system};
	in rec {

		twitter = {lib, buildPythonApplication, docopt, requests}:
			buildPythonApplication rec {
				pname = "twitter";
				version = "2.2.3";
				src = lib.cleanSource ./.;
				doCheck = false;
				propagatedBuildInputs = [
					docopt
					requests
				];
			};

		defaultPackage = pkgs.python3Packages.callPackage twitter {};

		defaultApp = {
			type = "app";
			program = "${self.defaultPackage.${system}}/bin/twitter";
		};

	});

}
