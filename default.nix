{ lib, buildPythonPackage, docopt, twint }:
buildPythonPackage rec {
	pname = "twitter";
	version = "0.0.1";

	src = ./.;
	doCheck = false;
	propagatedBuildInputs = [
		docopt
		twint
	];

	meta = with lib; {
		description = "Twitter scraper, streamer";
		homepage = "https://github.com/ihsanturk/twitter";
		license = licenses.mit;
		# maintainers = [ maintainers.ihsanturk ];
	};

}
