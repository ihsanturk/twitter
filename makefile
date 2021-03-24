default:
	nix build

sync:
	rsync -avr . --delete --filter=':- .gitignore' ihsan@do-arch:~/twitter
