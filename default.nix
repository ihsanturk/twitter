{ lib, buildPythonPackage, docopt, twint }:
buildPythonPackage rec {
	pname = "twitter";
	version = "1.0.0";

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
