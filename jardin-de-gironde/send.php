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

// ---------------------------------------------------------------------
// Envoi SMTP authentifié — RECOMMANDÉ.
//
// La fonction mail() de l'hébergement part sans authentification : Gmail
// la classe en indésirable ou la jette. Avec une vraie boîte aux lettres,
// le message arrive dans la boîte de réception à tous les coups.
//
// Renseignez les quatre valeurs ci-dessous et l'envoi bascule
// automatiquement sur SMTP. Laissées vides, on retombe sur mail().
//
//   Hostinger  : smtp.hostinger.com, port 465, votre adresse complète
//   Gmail      : smtp.gmail.com, port 465, mot de passe d'application
//
// Les identifiants vivent dans smtp-config.php, à côté de ce fichier.
// Ce fichier n'est pas versionné : le mot de passe ne part donc jamais
// sur GitHub. Modèle fourni dans smtp-config.exemple.php.
// ---------------------------------------------------------------------
$smtp = ['host' => '', 'port' => 465, 'user' => '', 'pass' => ''];
if (is_file(__DIR__ . '/smtp-config.php')) {
    $charge = require __DIR__ . '/smtp-config.php';
    if (is_array($charge)) {
        $smtp = array_merge($smtp, $charge);
    }
}
define('SMTP_HOST', (string) $smtp['host']);
define('SMTP_PORT', (int) $smtp['port']);
define('SMTP_USER', (string) $smtp['user']);
define('SMTP_PASS', (string) $smtp['pass']);
// ---------------------------------------------------------------------
// Relais vers l'ancien formulaire Hostinger Horizons.
//
// C'est ce canal qui envoyait les notifications jusqu'ici : le site
// Horizons de jardindegironde.fr enregistre la demande dans sa collection
// « devis_requests » et Hostinger prévient le propriétaire du compte.
// On continue donc à y déposer une copie de chaque demande.
//
// ATTENTION : ce relais ne fonctionne que tant que le site Horizons reste
// en ligne sur jardindegironde.fr. Le jour où le domaine bascule sur cette
// version statique, il s'éteint — d'où l'envoi SMTP ci-dessus, qui est la
// solution durable. Laisser vide pour désactiver le relais.
// ---------------------------------------------------------------------
const HORIZONS_ENDPOINT = 'https://jardindegironde.fr/hcgi/platform/api/collections/devis_requests/records';

const STORAGE_FILE = __DIR__ . '/storage/devis.json';
const MAIL_LOG = __DIR__ . '/storage/mail.log';

// Expéditeur : doit appartenir au domaine qui héberge le site, sinon les
// serveurs destinataires rejettent le message (SPF).
function sender_domain(): string {
    $host = $_SERVER['HTTP_HOST'] ?? ($_SERVER['SERVER_NAME'] ?? 'jardindegironde.fr');
    return preg_replace('/^www\./', '', strtok($host, ':'));
}

/**
 * Envoi via SMTP authentifié (TLS implicite, port 465).
 * Retourne true si le serveur a accepté le message.
 */
function smtp_send(string $to, string $subject, string $body, string $replyTo): bool {
    $host = SMTP_HOST !== '' ? SMTP_HOST : null;
    if ($host === null || SMTP_USER === '' || SMTP_PASS === '') {
        return false;
    }

    $scheme = (int) SMTP_PORT === 465 ? 'ssl://' : 'tcp://';
    $socket = @stream_socket_client($scheme . $host . ':' . SMTP_PORT, $errno, $errstr, 12);
    if (!$socket) {
        return false;
    }
    stream_set_timeout($socket, 12);

    $read = static function () use ($socket): string {
        $out = '';
        while (($line = fgets($socket, 1024)) !== false) {
            $out .= $line;
            if (strlen($line) < 4 || $line[3] !== '-') {
                break;
            }
        }
        return $out;
    };
    $cmd = static function (string $line, string $expect) use ($socket, $read): bool {
        fwrite($socket, $line . "\r\n");
        return str_starts_with(trim($read()), $expect);
    };

    $ok = str_starts_with(trim($read()), '220');
    $ok = $ok && $cmd('EHLO ' . sender_domain(), '250');

    if ($ok && (int) SMTP_PORT !== 465) {
        $ok = $cmd('STARTTLS', '220')
            && @stream_socket_enable_crypto($socket, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)
            && $cmd('EHLO ' . sender_domain(), '250');
    }

    $ok = $ok && $cmd('AUTH LOGIN', '334')
        && $cmd(base64_encode(SMTP_USER), '334')
        && $cmd(base64_encode(SMTP_PASS), '235')
        && $cmd('MAIL FROM:<' . SMTP_USER . '>', '250')
        && $cmd('RCPT TO:<' . $to . '>', '250')
        && $cmd('DATA', '354');

    if ($ok) {
        $headers = "From: Jardin de Gironde <" . SMTP_USER . ">\r\n"
            . "To: <{$to}>\r\n"
            . "Reply-To: {$replyTo}\r\n"
            . 'Subject: =?UTF-8?B?' . base64_encode($subject) . "?=\r\n"
            . "MIME-Version: 1.0\r\n"
            . "Content-Type: text/plain; charset=UTF-8\r\n"
            . "Content-Transfer-Encoding: base64\r\n"
            . 'Date: ' . date('r') . "\r\n\r\n";
        fwrite($socket, $headers . chunk_split(base64_encode($body)) . "\r\n.\r\n");
        $ok = str_starts_with(trim($read()), '250');
    }

    $cmd('QUIT', '221');
    fclose($socket);
    return $ok;
}

/**
 * Dépose une copie de la demande dans la collection Horizons, qui déclenche
 * la notification déjà en place. Ne renvoie que l'état, sans jamais bloquer.
 */
function horizons_forward(array $payload): bool {
    if (HORIZONS_ENDPOINT === '') {
        return false;
    }
    $json = json_encode($payload, JSON_UNESCAPED_UNICODE);

    if (function_exists('curl_init')) {
        $ch = curl_init(HORIZONS_ENDPOINT);
        curl_setopt_array($ch, [
            CURLOPT_POST           => true,
            CURLOPT_POSTFIELDS     => $json,
            CURLOPT_HTTPHEADER     => ['Content-Type: application/json'],
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT        => 12,
        ]);
        curl_exec($ch);
        $code = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        return $code >= 200 && $code < 300;
    }

    $ctx = stream_context_create(['http' => [
        'method'        => 'POST',
        'header'        => "Content-Type: application/json\r\n",
        'content'       => $json,
        'timeout'       => 12,
        'ignore_errors' => true,
    ]]);
    $res = @file_get_contents(HORIZONS_ENDPOINT, false, $ctx);
    if ($res === false) {
        return false;
    }
    foreach ($http_response_header ?? [] as $line) {
        if (preg_match('#^HTTP/\S+\s+(\d{3})#', $line, $m)) {
            return (int) $m[1] >= 200 && (int) $m[1] < 300;
        }
    }
    return false;
}

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

$domain = sender_domain();
$from = 'no-reply@' . $domain;

$headers = "From: Jardin de Gironde <{$from}>\r\n";
$headers .= "Reply-To: {$nom} <{$email}>\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$headers .= "Content-Transfer-Encoding: 8bit\r\n";

// Le 5e paramètre fixe l'expéditeur d'enveloppe : sans lui, l'hébergeur
// utilise l'utilisateur système et le message part en indésirable.
$canal = 'smtp';
$sent = smtp_send(NOTIFICATION_EMAIL, $subject, $body, "{$nom} <{$email}>");
if (!$sent) {
    $canal = 'mail()';
    $sent = @mail(NOTIFICATION_EMAIL, $subject, $body, $headers, '-f' . $from);
}

// Copie vers l'ancien formulaire Horizons — canal de notification historique.
$relais = horizons_forward([
    'nom'       => $nom,
    'email'     => $email,
    'telephone' => $telephone,
    'ville'     => $ville,
    'service'   => $service,
    'message'   => $message,
]);

// Journal : permet de distinguer « mail() indisponible » de « mail parti
// mais non distribué ». Consultable dans storage/mail.log.
@file_put_contents(
    MAIL_LOG,
    sprintf("%s | canal=%s | envoye=%s | relais_horizons=%s | from=%s | to=%s\n",
        date('Y-m-d H:i:s'),
        $canal,
        $sent ? 'true' : 'false',
        $relais ? 'true' : 'false',
        $canal === 'smtp' ? SMTP_USER : $from,
        NOTIFICATION_EMAIL),
    FILE_APPEND | LOCK_EX
);

// La demande est enregistrée quoi qu'il arrive : même si l'e-mail échoue,
// elle reste consultable sur /demandes.php.
respond(true);
