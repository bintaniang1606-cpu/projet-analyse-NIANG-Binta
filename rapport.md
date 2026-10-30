# Rapport — Analyse des journaux du pare-feu

## Résumé
(3 à 5 phrases, à écrire avec tes mots : combien de lignes après nettoyage,
port le plus utilisé, taux de DENY, et le fait que deux comportements
anormaux ressortent.)

## Comportement suspect 1 : scan de ports depuis 192.168.1.99
- 328 ports distincts contactés, contre 8 pour les autres IP
  (figure `figures/ports_distincts_par_ip.png`).
- 400 connexions vers 10.0.0.5 en 15 minutes, dont 383 bloquées (DENY).

## Comportement suspect 2 : exfiltration depuis 192.168.1.11
- Environ 260 Mo envoyés, les autres IP sont sous 1 Mo
  (figures `figures/octets_par_ip.png` et `figures/octets_par_appareil.png`).
- Presque tout vers 8.8.8.8 sur le port 8080, depuis une caméra IoT.

## Recommandations
1. Isoler la caméra 192.168.1.11 et changer ses identifiants.
2. Segmenter le réseau : mettre les objets IoT dans un VLAN dédié.
3. Fermer Telnet (port 23), utiliser SSH.
4. Détecter et bloquer automatiquement les scans de ports.
5. Alerter quand un appareil envoie un volume anormal vers l'extérieur.

