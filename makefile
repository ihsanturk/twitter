default:
	nix build

sync:
	rsync -avr . --delete ihsan@do-arch:~/twitter
