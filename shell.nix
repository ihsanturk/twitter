with import <nixpkgs> {};
let
	mach-nix = import (builtins.fetchGit {
		url = "https://github.com/DavHau/mach-nix";
		ref = "refs/heads/master";
		rev = "3acbfc2ebd0b826cd046925493714a5e2f146d73";
	}) {};
	twint = mach-nix.buildPythonPackage {
		# src = "https://github.com/twintproject/twint/tarball/master";
		src = "https://github.com/ihsanturk/twint/tarball/master";
		overridesPre = [( pySelf: pySuper: { dateutil = null; })];
	};
	twitter = pkgs.callPackage ./default.nix {
		inherit twint lib;
		docopt = pkgs.python38Packages.docopt;
		buildPythonPackage = pkgs.python38Packages.buildPythonPackage;
	};
in
mkShell {
	name = "twitter";
	buildInputs = [ twitter ];
}
