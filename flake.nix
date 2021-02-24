{

	description = "Twitter scraper and streamer.";

	inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
	inputs.flake-utils.url = "github:numtide/flake-utils";

	outputs = { self, nixpkgs, flake-utils, ... }:
	flake-utils.lib.eachDefaultSystem (system:
	let
		pkgs = nixpkgs.legacyPackages.${system};
	in rec {

		twitter = pkgs.python3Packages.callPackage
			({ lib, buildPythonPackage, docopt }:
			buildPythonPackage rec {
				pname = "twitter";
				version = "2.0.0-alpha";
				src = lib.cleanSource ./.;
				doCheck = false;
				propagatedBuildInputs = [
					docopt
				];
			}) {
			inherit (pkgs) lib buildPythonPackage docopt;
		};

		defaultPackage.${system} = twitter;

		defaultApp = {
			type = "app";
			program = "${defaultPackage}/bin/twitter";
		};

	});

}
