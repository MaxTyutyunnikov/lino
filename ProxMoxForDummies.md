# Proxmox für Hobby-Systemadministratoren #

**Januar 2010**

Also ich habe die Proxmox-CD runtergeladen und gebrannt, und damit meinen nagelneuen Server gebootet, auf dem ich zuvor zwar schon ein
Debian laufen hatte, aber ohne wichtige Daten. Also bare-metal installation.

Ich zögerte lediglich bei der Frage, was ich als FQDN haben will. Er schlug "proxmox.domain.tld" vor, und ich habe daraus auf gut Glück mal "proxmox.saffre-rumma.ee" gemacht. Die vorgeschlagene IP-Adresse 192.168.1.160 habe ich gelassen (Gateway, Netmask und DNS-Server auch).

Jetzt läuft der Server, und unter 192.168.1.160 habe ich jetzt Zugriff auf das Web-Interface von Proxmox. Habe auch schon ein Template "Debian 6.0" runtergeladen und erstelle damit einen erste virtuelle Maschine. Siehe beiliegenden Screenshot. (Nach dem Screenshot habe ich noch mit den Parametern
gespielt, u.a. die IP-Adresse 127.0.0.1 nach 192.168.1.161 geändert.)

Mit `ssh root@192.168.1.161` kann ich mich auf dem virtuellen Server
einloggen.

Dort kriege ich allerdings selbst auf `ping google.com` keine Antwort
(sondern "unknown host google.com"). Keine Ahnung, woran das liegt.

Ich sehe noch nicht klar, wie ich Hostnamen, IP-Adressen und
Domain-Namen auf welche Server verteilen muss.

Mein Router meldet unsere dynamische IP-Adresse brav an dyndns, wo sie
unter "jaama.dyndns.org" abgefragt werden kann.

Domain saffre-rumma.ee soll noch eine Zeitlang unverändert nach Tallinn
gehen, aber wenn ich den Rechner dort abgeholt habe, will ich ihn
natürlich so schnell wie möglich auf dem Proxmox mit neuer Hardware
auferstehen lassen.

Mit `ssh root@192.168.1.160` kann ich mich auf die Hauptmaschine einloggen::

proxmox:~# less /etc/network/interfaces
auto lo
iface lo inet loopback

auto vmbr0
iface vmbr0 inet static
> address 192.168.1.160
> netmask 255.255.255.0
> gateway 192.168.1.254
> bridge\_ports eth0
> bridge\_stp off
> bridge\_fd 0