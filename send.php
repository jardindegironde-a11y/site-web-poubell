<?php
declare(strict_types=1);

// ---------------------------------------------------------------------
// BACNIFIQUE — traitement du formulaire de rendez-vous
// Enregistre chaque demande dans storage/rendezvous.json et envoie
// un e-mail de notification à l'adresse ci-dessous.
// ---------------------------------------------------------------------

header('Content-Type: application/json; charset=utf-8');

const NOTIFICATION_EMAIL = 'bacnifique@gmail.com';
const PRICE_PER_BIN = 25;
const STORAGE_FILE = __DIR__ . '/storage/rendezvous.json';

function respond(bool $success, string $message = ''): void {
    echo json_encode(['success' => $success, 'message' => $message], JSON_UNESCAPED_UNICODE);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    respond(false, 'Méthode non autorisée.');
}

$raw = file_get_contents('php://input');
$input = json_decode($raw, true);
if (!is_array($input)) {
    $input = $_POST;
}

function clean(string $key, array $input, int $maxLength = 500): string {
    $value = isset($input[$key]) ? (string) $input[$key] : '';
    $value = trim($value);
    $value = strip_tags($value);
    $value = preg_replace('/[\r\n]+/', ' ', $value) ?? $value;
    return mb_substr($value, 0, $maxLength);
}

$fullName   = clean('fullName', $input, 120);
$phone      = clean('phone', $input, 40);
$address    = clean('address', $input, 200);
$postalCode = clean('postalCode', $input, 10);
$city       = clean('city', $input, 100);
$binCount   = (int) ($input['binCount'] ?? 0);
$notes      = isset($input['notes']) ? mb_substr(trim(strip_tags((string) $input['notes'])), 0, 1000) : '';

if ($fullName === '' || $phone === '' || $address === '' || $postalCode === '' ||
    $city === '' || $binCount < 1) {
    http_response_code(422);
    respond(false, 'Merci de compléter tous les champs obligatoires.');
}

$binCount = min($binCount, 50);
$total = $binCount * PRICE_PER_BIN;

$entry = [
    'date_soumission' => date('Y-m-d H:i:s'),
    'nom'              => $fullName,
    'telephone'        => $phone,
    'adresse'          => $address,
    'code_postal'      => $postalCode,
    'commune'          => $city,
    'nombre_poubelles' => $binCount,
    'notes'            => $notes,
    'total_estime'     => $total . ' €',
];

// --- Enregistrement dans storage/rendezvous.json (append) ---
$fp = fopen(STORAGE_FILE, 'c+');
if ($fp && flock($fp, LOCK_EX)) {
    $contents = stream_get_contents($fp);
    $records = json_decode((string) $contents, true);
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

// --- Envoi de l'e-mail de notification ---
$subject = 'Nouvelle demande de nettoyage BACNIFIQUE - ' . $fullName;

$body = "Nouvelle demande de nettoyage BACNIFIQUE\n"
    . "A rappeler pour fixer la date de collecte.\n\n"
    . "Nom : {$fullName}\n"
    . "Téléphone : {$phone}\n"
    . "Adresse : {$address}\n"
    . "Code postal : {$postalCode}\n"
    . "Commune : {$city}\n"
    . "Nombre de poubelles : {$binCount}\n"
    . "Total estimé : {$total} €\n"
    . "Informations complémentaires : " . ($notes !== '' ? $notes : '—') . "\n";

$headers = "From: BACNIFIQUE <no-reply@" . ($_SERVER['SERVER_NAME'] ?? 'bacnifique.fr') . ">\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

@mail(NOTIFICATION_EMAIL, $subject, $body, $headers);

respond(true);
