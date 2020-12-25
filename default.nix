{ lib, buildPythonPackage, docopt, twint, pymongo, nest-asyncio }:
buildPythonPackage rec {
	pname = "twitter";
	version = "1.2.2";

	src = ./.;
	doCheck = false;
	propagatedBuildInputs = [
		twint
		docopt
		pymongo
		nest-asyncio
	];

	meta = with lib; {
		description = "Twitter scraper, streamer";
		homepage = "https://github.com/ihsanturk/twitter";
		license = licenses.mit;
		# maintainers = [ maintainers.ihsanturk ];
	};

}
