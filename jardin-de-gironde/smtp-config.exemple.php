<?php
// ---------------------------------------------------------------------
// Identifiants d'envoi des e-mails.
//
// Copiez ce fichier sous le nom smtp-config.php et complétez-le.
// smtp-config.php n'est pas versionné : le mot de passe reste sur le
// serveur et ne part jamais sur GitHub.
//
// Gmail      : hôte smtp.gmail.com, port 465, utilisateur votre adresse
//              Gmail, mot de passe = « mot de passe d'application »
//              (compte Google -> Sécurité -> Validation en deux étapes
//              -> Mots de passe des applications). Ce n'est PAS le mot
//              de passe habituel du compte, et il est révocable à tout
//              moment sans changer le reste.
// Hostinger  : hôte smtp.hostinger.com, port 465, votre adresse complète
//              et son mot de passe.
// ---------------------------------------------------------------------

return [
    // Mot de passe de la page /demandes.php
    'admin_pass' => 'choisissez-un-mot-de-passe',

    'host' => 'smtp.gmail.com',
    'port' => 465,
    'user' => 'jardindegironde@gmail.com',
    'pass' => 'xxxx xxxx xxxx xxxx',
];
