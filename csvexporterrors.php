<?php

$connection = new PDO('mysql:host=localhost;dbname=engineering_thesis', 'root', '', array(
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
));

$data_to_export = $connection
->prepare("SELECT COUNT(*) AS count, message 
FROM `errors` 
GROUP BY message 
ORDER BY count DESC", [PDO::FETCH_ASSOC]);
$data_to_export->execute();

$csvFilename = 'export_errors_' . date('Y-m-d_H-i-s') . '.csv';
$path = fopen($csvFilename, 'w');
fputcsv($path, array_keys((array)$data_to_export->fetchObject()));
while ($row = $data_to_export->fetchObject()) {
    fputcsv($path, [
        $row->count,
        $row->message
    ]);
}
fclose($path);
header('Content-Type: text/csv');
header('Content-Disposition: attachment; filename="' . $csvFilename . '"');
readfile($csvFilename);
unlink($csvFilename);
exit;