<?php
declare(strict_types=1);

// ---------------------------------------------------------------------
// Jardin de Gironde — traitement des demandes de devis
//
// Enregistre chaque demande dans storage/devis.json et envoie un e-mail
// de notification. Utilisé par assets/js/main.js lorsque le site est
// hébergé sur un serveur PHP (hébergement mutualisé Hostinger).
// ---------------------------------------------------------------------

header('Content-Type: application/json; charset=utf-8');

const NOTIFICATION_EMAIL = 'jardindegironde@gmail.com';
const STORAGE_FILE = __DIR__ . '/storage/devis.json';

function respond(bool $success, string $message = ''): void {
    echo json_encode(['success' => $success, 'message' => $message], JSON_UNESCAPED_UNICODE);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    respond(false, 'Méthode non autorisée.');
}

$raw = file_get_contents('php://input');
$input = json_decode((string) $raw, true);
if (!is_array($input)) {
    $input = $_POST;
}

function clean(string $key, array $input, int $maxLength = 500): string {
    $value = isset($input[$key]) ? (string) $input[$key] : '';
    $value = trim(strip_tags($value));
    $value = preg_replace('/[\r\n]+/', ' ', $value) ?? $value;
    return mb_substr($value, 0, $maxLength);
}

// Pot de miel : un robot remplit le champ caché, on répond OK sans rien faire.
if (clean('site', $input, 50) !== '') {
    respond(true);
}

$nom       = clean('nom', $input, 120);
$telephone = clean('telephone', $input, 40);
$email     = clean('email', $input, 160);
$ville     = clean('ville', $input, 100);
$service   = clean('service', $input, 80);
$origine   = clean('origine', $input, 120);
$message   = isset($input['message'])
    ? mb_substr(trim(strip_tags((string) $input['message'])), 0, 2000)
    : '';

if ($nom === '' || $telephone === '' || $email === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(422);
    respond(false, 'Merci de compléter le nom, le téléphone et une adresse e-mail valide.');
}

$campagne = [];
foreach (['gclid', 'gbraid', 'wbraid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'] as $key) {
    $value = clean($key, $input, 200);
    if ($value !== '') {
        $campagne[$key] = $value;
    }
}

$entry = [
    'date_soumission' => date('Y-m-d H:i:s'),
    'nom'             => $nom,
    'telephone'       => $telephone,
    'email'           => $email,
    'ville'           => $ville,
    'service'         => $service,
    'message'         => $message,
    'origine'         => $origine,
    'campagne'        => $campagne,
];

// --- Enregistrement dans storage/devis.json ---
if (!is_dir(__DIR__ . '/storage')) {
    @mkdir(__DIR__ . '/storage', 0755, true);
}
$fp = @fopen(STORAGE_FILE, 'c+');
if ($fp && flock($fp, LOCK_EX)) {
    $records = json_decode((string) stream_get_contents($fp), true);
    if (!is_array($records)) {
        $records = [];
    }
    $records[] = $entry;
    ftruncate($fp, 0);
    rewind($fp);
    fwrite($fp, json_encode($records, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
    flock($fp, LOCK_UN);
    fclose($fp);
}

// --- Notification par e-mail ---
$subject = 'Demande de devis — ' . $nom . ($ville !== '' ? ' (' . $ville . ')' : '');

$body = "Nouvelle demande de devis — Jardin de Gironde\n\n"
    . "Nom : {$nom}\n"
    . "Téléphone : {$telephone}\n"
    . "E-mail : {$email}\n"
    . "Ville : " . ($ville !== '' ? $ville : '—') . "\n"
    . "Prestation : " . ($service !== '' ? $service : '—') . "\n"
    . "Page d'origine : " . ($origine !== '' ? $origine : '—') . "\n\n"
    . "Projet :\n" . ($message !== '' ? $message : '—') . "\n";

if ($campagne !== []) {
    $body .= "\nCampagne :\n";
    foreach ($campagne as $key => $value) {
        $body .= "  {$key} : {$value}\n";
    }
}

$domain = $_SERVER['SERVER_NAME'] ?? 'jardindegironde.fr';
$headers = "From: Jardin de Gironde <no-reply@{$domain}>\r\n";
$headers .= "Reply-To: {$nom} <{$email}>\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

@mail(NOTIFICATION_EMAIL, $subject, $body, $headers);

respond(true);
