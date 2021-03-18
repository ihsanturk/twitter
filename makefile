default:
	nix build

sync:
	rsync -avr . ihsan@do-arch:~/twitter
