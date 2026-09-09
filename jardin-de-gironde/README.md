# Jardin de Gironde — refonte du site

Site statique (HTML + CSS + un fichier JS), sans framework ni dépendance.
Il remplace la version React générée par Hostinger Horizons.

## Ce qui change par rapport à l'ancien site

| Ancien site | Nouveau site |
|---|---|
| 10 vidéos MP4 en lecture automatique, dont une plein écran en accueil | **1 seule vidéo** : le partenariat Villaverde, chargée uniquement quand on arrive dessus |
| Sections à défilement bloqué (`min-h-[280vh]`), texte qui apparaît mot à mot | Défilement normal, apparitions douces, désactivées si l'utilisateur préfère moins d'animations |
| Bundle React de 410 Ko + Framer Motion | ~25 Ko de CSS + 6 Ko de JS |
| Vidéos de services au rendu « IA » | 7 illustrations façon sérigraphie, avec la mascotte du site, dessinées en SVG (~3 Ko pièce) + photos réelles de chantiers |
| Note « 4,9/5 sur 48 avis » dans les données structurées, invérifiable | Retirée — voir « Points d'attention » |
| Aucune page dédiée aux campagnes publicitaires | 2 landing pages Google Ads |
| Pas de mentions légales ni de politique de confidentialité | Les deux pages présentes |

## Structure

```
index.html                     Accueil
entretien-jardin.html          Landing page Google Ads — campagne « jardinage / entretien »
creation-paysagisme.html       Landing page Google Ads — campagne « paysagisme / création »
merci.html                     Page de confirmation (déclenche la conversion Ads)
tonte-pelouse.html             Pages de service (6)
taille-haies.html
debroussaillage.html
entretien-jardins.html
creation-espaces-verts.html
nettoyage-haute-pression.html
nettoyage-toiture-gouttiere.html
mentions-legales.html
politique-confidentialite.html
send.php                       Réception du formulaire (SMTP, repli mail())
smtp-config.exemple.php        Modèle des identifiants d'envoi (à copier)
demandes.php                   Consultation des demandes reçues (mot de passe)
illus.py                       Générateur des illustrations SVG
logo.py                        Générateur du logo vectorisé
storage/                       Demandes enregistrées (non servi publiquement)
sitemap.xml  robots.txt
build.py                       Générateur : produit tous les fichiers .html ci-dessus
assets/css/style.css
assets/js/main.js
assets/img/                    Photos réelles en WebP + illustrations SVG
assets/video/                  villaverde-cestas.mp4
```

## Modifier le contenu

Les pages HTML sont **générées**. Ne les éditez pas à la main : modifiez `build.py`
(textes, services, FAQ, villes, coordonnées) puis relancez :

```bash
cd jardin-de-gironde
python3 build.py
```

Aucune dépendance : Python 3 suffit.

## Prévisualiser en local

```bash
cd jardin-de-gironde
php -S localhost:8000        # avec le formulaire fonctionnel
# ou : python3 -m http.server 8000   (le formulaire affichera le repli téléphone/e-mail)
```

## Aperçu en ligne

**https://mediumpurple-boar-934886.hostingersite.com**

Adresse de test Hostinger créée pour valider la refonte. `jardindegironde.fr`,
`vedurastudio.com` et les sites BACNIFIQUE n'ont pas été touchés. Les balises
`canonical` pointent vers `www.jardindegironde.fr`, cette adresse ne sera donc
pas indexée par Google.

## Mise en ligne

Le site est entièrement statique : il suffit de déposer le contenu du dossier
`jardin-de-gironde/` à la racine du domaine (`public_html`).

`jardindegironde.fr` pointe aujourd'hui vers **Hostinger Horizons**. Pour publier
cette version, il faut rattacher le domaine à l'hébergement mutualisé du compte
(`u853872532`) puis y téléverser les fichiers. Le formulaire utilisera alors
`send.php`.

Vérifier après mise en ligne :

- `storage/` n'est pas accessible depuis le web (un `.htaccess` le bloque déjà) ;
- une demande de test arrive bien sur `jardindegironde@gmail.com` ;
- le certificat HTTPS est actif sur `www.jardindegironde.fr` **et** `jardindegironde.fr`.

## Notifications par e-mail

Chaque demande part par **trois canaux**, pour qu'aucune ne se perde :

1. **Enregistrement local** dans `storage/devis.json`, consultable sur
   `demandes.php` (mot de passe en haut du fichier, à changer).
2. **Relais vers l'ancien formulaire Horizons** — c'est le canal qui envoyait
   les notifications jusqu'ici. `send.php` dépose une copie de la demande dans
   la collection `devis_requests` du site Horizons de `jardindegironde.fr`, et
   Hostinger prévient le propriétaire du compte comme avant.
   **Ce relais s'éteindra le jour où `jardindegironde.fr` basculera sur cette
   version statique** : le site Horizons ne sera plus en ligne. C'est pourquoi
   le point 3 reste nécessaire.
3. **Envoi direct** par SMTP si configuré, sinon par `mail()`.

Le résultat de chaque tentative est journalisé dans `storage/mail.log`
(`canal`, `envoye`, `relais_horizons`).

### Rendre l'envoi direct fiable

`mail()` part sans authentification : le message quitte bien le serveur
(vérifié, `mail()` renvoie `true`), mais Gmail le classe en indésirable ou le
refuse, car rien ne prouve que l'expéditeur est légitime.
La fonction `mail()` de l'hébergement envoie sans authentification : le
message part bien (vérifié, `mail()` renvoie `true`), mais Gmail le classe en
indésirable ou le refuse, car rien ne prouve que l'expéditeur est légitime.

La solution fiable est l'envoi **SMTP authentifié**. Copiez
`smtp-config.exemple.php` sous le nom `smtp-config.php` et complétez-le :

```php
return [
    'host' => 'smtp.gmail.com',
    'port' => 465,
    'user' => 'jardindegironde@gmail.com',
    'pass' => 'mot de passe d\'application',
];
```

`smtp-config.php` n'est **pas versionné** : le mot de passe reste sur le
serveur et ne part jamais sur GitHub.

Deux façons d'obtenir ces identifiants :

- **Boîte Hostinger** sur `jardindegironde.fr` — le domaine est déjà préparé
  (enregistrements MX, SPF et DKIM en place), il ne manque qu'un abonnement
  e-mail et la création d'une adresse ;
- **Gmail** — dans le compte Google, activer la validation en deux étapes puis
  générer un « mot de passe d'application » ; hôte `smtp.gmail.com`, port 465,
  utilisateur `jardindegironde@gmail.com`.

Tant que ces valeurs restent vides, `send.php` retombe sur `mail()` et
journalise chaque tentative dans `storage/mail.log`.

## Configuration Google Ads

L'identifiant `AW-18308555635` est déjà présent dans le `<head>` de chaque page.
Il reste **deux libellés de conversion à renseigner** — sans eux, Google Ads ne
comptabilise aucune conversion.

1. Dans Google Ads : *Objectifs → Conversions → Nouvelle action de conversion → Site Web*.
2. Créer deux actions :
   - **Demande de devis** (principale) — page de destination `/merci.html` ;
   - **Appel téléphonique depuis le site** (secondaire).
3. Pour chacune, relever le `send_to` de la forme `AW-18308555635/AbC-D_efGhIjKlMnOp`.
4. Les reporter dans `assets/js/main.js`, en haut du fichier :

```js
conversions: {
  devis: 'AW-18308555635/xxxxxxxxxxxxxxxxxxx',
  appel: 'AW-18308555635/yyyyyyyyyyyyyyyyyyy'
}
```

### Ce que le site fait déjà pour les campagnes

- **Deux landing pages dédiées**, une par campagne, avec en-tête allégée (pas de
  menu de navigation : moins de sorties, meilleur taux de conversion) et le
  formulaire visible sans défiler sur ordinateur.
- **Correspondance mot-clé / annonce / page** : titre et sous-titre reprennent le
  vocabulaire de chaque campagne (« jardinier », « entretien » d'un côté ;
  « paysagiste », « création » de l'autre).
- **Capture du `gclid`** (et `gbraid`, `wbraid`, UTM) à l'arrivée, conservé pendant
  la session et transmis avec la demande : vous savez quelle campagne a produit
  quel devis, y compris dans l'e-mail de notification.
- **Barre d'action fixe sur mobile** (Appeler / Devis gratuit) — l'essentiel du
  trafic Ads est mobile.
- **Suivi des clics téléphone** comme conversion secondaire.
- **Pages exigées par Google Ads** pour la validation des annonces : mentions
  légales, politique de confidentialité, coordonnées visibles.
- **`merci.html` en `noindex`** et exclue de `robots.txt`.

### Suggestion de structure de campagnes

| Campagne | Page de destination | Exemples de mots-clés |
|---|---|---|
| Jardinage & entretien | `entretien-jardin.html` | jardinier gironde, entretien jardin bordeaux, tonte pelouse, taille de haies, débroussaillage, nettoyage gouttière |
| Paysagisme & création | `creation-paysagisme.html` | paysagiste gironde, création jardin bordeaux, aménagement paysager, engazonnement, pose de clôture |

Utilisez un suffixe d'URL de campagne du type
`utm_source=google&utm_medium=cpc&utm_campaign={campaignid}&utm_term={keyword}`.

## Points d'attention

- **Note et avis** : l'ancien site déclarait « 4,9/5 sur 48 avis » dans ses données
  structurées. Une note affichée sans avis publics vérifiables est contraire aux
  règles de Google sur les données structurées et nuit à la crédibilité — c'est
  précisément ce qui donne l'impression d'un site « monté à la va-vite ». Elle a
  été retirée. Dès que vous avez des avis Google réels, on peut afficher la note
  réelle et lier vers la fiche.
- **Crédit d'impôt** : le site précise que les 50 % concernent l'entretien courant
  et **pas** les travaux de création. C'est la règle applicable aux services à la
  personne, et le dire clairement évite les litiges (et les réclamations Ads).
- **Mentions légales** : le SIRET, la forme juridique, l'adresse du siège et le
  numéro de déclaration « services à la personne » sont à compléter dans
  `build.py` (constante `MENTIONS`) avant la mise en ligne. Google Ads peut
  demander ces informations lors de la vérification de l'annonceur.
- **Logo** : `assets/img/logo-jdg.svg` est une **reproduction vectorielle** de
  votre écusson, tracée d'après l'image que vous avez fournie — texte converti
  en courbes, aucune dépendance à une police, ~6 Ko, net à toutes les tailles.
  Le script `logo.py` permet de la régénérer et d'en ajuster la géométrie.
  Ce n'est pas votre fichier d'origine : pour l'utiliser, déposez-le dans
  `assets/img/` sous le nom `logo.png`, `logo.webp` ou `logo.svg` et relancez
  `python3 build.py`. Il est détecté et prend automatiquement le dessus.
- **Photos** : uniquement des prises de vue réelles de vos chantiers, ré-encodées
  en WebP (de 3 Mo à 100–450 Ko). L'image « poignée de main en jardinerie » de
  l'ancien site, visiblement générée par IA, a été retirée.
