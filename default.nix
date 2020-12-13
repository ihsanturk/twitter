{ lib, buildPythonPackage, docopt, twint, pymongo }:
buildPythonPackage rec {
	pname = "twitter";
	version = "1.0.1";

	src = ./.;
	doCheck = false;
	propagatedBuildInputs = [
		twint
		docopt
		pymongo
	];

	meta = with lib; {
		description = "Twitter scraper, streamer";
		homepage = "https://github.com/ihsanturk/twitter";
		license = licenses.mit;
		# maintainers = [ maintainers.ihsanturk ];
	};

}
