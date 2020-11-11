{ pkgs ? import <nixpkgs> {} }: with pkgs;
let
	lib = pkgs.lib;
	mach-nix = import (builtins.fetchGit {
		url = "https://github.com/DavHau/mach-nix";
		ref = "refs/heads/master";
		rev = "3acbfc2ebd0b826cd046925493714a5e2f146d73";
	}) {};
	twint = mach-nix.buildPythonPackage {
		src = "https://github.com/twintproject/twint/tarball/ae5e7e1189be1cf319bbd55b921aca6bfb899f8c";
		# src = "https://github.com/ihsanturk/twint/tarball/master";
		# src = ~/code/github.com/ihsanturk/twint;
		overridesPre = [( pySelf: pySuper: { dateutil = null; })];
	};
	twitter = pkgs.callPackage ./default.nix {
		inherit twint lib;
		docopt = pkgs.python38Packages.docopt;
		buildPythonPackage = pkgs.python38Packages.buildPythonPackage;
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
		python38Packages.pymongo
	];
}
