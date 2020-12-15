{ pkgs ? import <nixpkgs> {} }: with pkgs;
let
	lib = pkgs.lib;
	mach-nix = import (builtins.fetchGit {
		url = "https://github.com/DavHau/mach-nix";
		ref = "refs/heads/master";
		rev = "3acbfc2ebd0b826cd046925493714a5e2f146d73";
	}) {};
	twint = mach-nix.buildPythonPackage {
		# src = "git+https://github.com/twintproject/twint.git@origin/master#egg=twint";
		src = "https://github.com/ihsanturk/twint/tarball/master";
		# src = ~/code/github.com/ihsanturk/twint;
		overridesPre = [( pySelf: pySuper: { dateutil = null; })];
	};
	twitter = pkgs.callPackage ./default.nix {
		inherit twint lib;
		docopt = pkgs.python37Packages.docopt;
		pymongo = pkgs.python37Packages.pymongo;
		nest-asyncio = python38Packages.nest-asyncio;
		buildPythonPackage = pkgs.python37Packages.buildPythonPackage;
	};
	# confusables = mach-nix.buildPythonPackage {
	# 	src = "https://github.com/woodgern/confusables/tarball/master";
	# };
in
mkShell {
	name = "twitter";
	buildInputs = [
		mongodb
		twitter
		# confusables
		mongodb-tools
	];
}
