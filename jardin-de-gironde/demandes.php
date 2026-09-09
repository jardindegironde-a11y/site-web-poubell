<?php
declare(strict_types=1);

// ---------------------------------------------------------------------
// Jardin de Gironde — consultation des demandes de devis
//
// Filet de sécurité : même si l'e-mail de notification n'arrive pas,
// aucune demande n'est perdue. Page protégée par mot de passe.
//
// Changez MOT_DE_PASSE avant la mise en ligne.
// ---------------------------------------------------------------------

const MOT_DE_PASSE = 'jardin2026';
const STORAGE_FILE = __DIR__ . '/storage/devis.json';

session_start();

if (isset($_GET['sortie'])) {
    session_destroy();
    header('Location: demandes.php');
    exit;
}

if (isset($_POST['mdp'])) {
    if (hash_equals(MOT_DE_PASSE, (string) $_POST['mdp'])) {
        $_SESSION['jdg_admin'] = true;
    } else {
        $erreur = 'Mot de passe incorrect.';
    }
}

$autorise = !empty($_SESSION['jdg_admin']);

$style = '<style>
  body { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; background: #FBFAF7;
         color: #111A14; margin: 0; padding: 40px 20px; line-height: 1.6; }
  .wrap { max-width: 880px; margin: 0 auto; }
  h1 { font-size: 24px; letter-spacing: -.02em; }
  form.login { display: flex; gap: 10px; margin-top: 20px; flex-wrap: wrap; }
  input, button { font: inherit; padding: 12px 16px; border-radius: 10px;
                  border: 1px solid #E4E2DA; }
  button { background: #17662C; color: #fff; border-color: #17662C; cursor: pointer; }
  .item { background: #fff; border: 1px solid #E4E2DA; border-radius: 14px;
          padding: 20px 22px; margin-top: 16px; }
  .item h2 { font-size: 17px; margin: 0 0 4px; }
  .meta { color: #6B7670; font-size: 14px; }
  .msg { white-space: pre-wrap; margin-top: 12px; padding-top: 12px;
         border-top: 1px solid #EFEDE6; }
  a { color: #17662C; }
  .err { color: #A2371F; margin-top: 12px; }
</style>';

header('Content-Type: text/html; charset=utf-8');
header('X-Robots-Tag: noindex, nofollow');

echo '<!doctype html><html lang="fr"><head><meta charset="utf-8">',
     '<meta name="viewport" content="width=device-width, initial-scale=1">',
     '<meta name="robots" content="noindex, nofollow">',
     '<title>Demandes de devis — Jardin de Gironde</title>', $style,
     '</head><body><div class="wrap">';

if (!$autorise) {
    echo '<h1>Demandes de devis</h1>',
         '<form class="login" method="post">',
         '<input type="password" name="mdp" placeholder="Mot de passe" autofocus>',
         '<button type="submit">Entrer</button></form>';
    if (isset($erreur)) {
        echo '<p class="err">', htmlspecialchars($erreur), '</p>';
    }
    echo '</div></body></html>';
    exit;
}

$records = [];
if (is_file(STORAGE_FILE)) {
    $decoded = json_decode((string) file_get_contents(STORAGE_FILE), true);
    if (is_array($decoded)) {
        $records = array_reverse($decoded);
    }
}

echo '<h1>Demandes de devis <span class="meta">(', count($records), ')</span></h1>',
     '<p class="meta"><a href="?sortie=1">Se déconnecter</a></p>';

if ($records === []) {
    echo '<p class="meta">Aucune demande enregistrée pour le moment.</p>';
}

function e(?string $v): string {
    return htmlspecialchars((string) $v, ENT_QUOTES, 'UTF-8');
}

foreach ($records as $r) {
    echo '<div class="item">';
    echo '<h2>', e($r['nom'] ?? '—'), '</h2>';
    echo '<p class="meta">', e($r['date_soumission'] ?? ''), ' · ',
         e($r['service'] ?? '—'), ' · ', e($r['ville'] ?? '—'), '</p>';
    echo '<p><a href="tel:', e($r['telephone'] ?? ''), '">', e($r['telephone'] ?? ''), '</a>',
         ' — <a href="mailto:', e($r['email'] ?? ''), '">', e($r['email'] ?? ''), '</a></p>';
    if (!empty($r['message'])) {
        echo '<div class="msg">', e($r['message']), '</div>';
    }
    if (!empty($r['campagne'])) {
        $parts = [];
        foreach ($r['campagne'] as $k => $v) {
            $parts[] = e($k) . '=' . e((string) $v);
        }
        echo '<p class="meta">', implode(' · ', $parts), '</p>';
    }
    echo '</div>';
}

echo '</div></body></html>';
