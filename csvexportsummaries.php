<?php

$connection = new PDO('mysql:host=localhost;dbname=engineering_thesis', 'root', '', array(
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
));


$data_to_export = $connection->prepare("SELECT entries, errors, correct_sequences, SEC_TO_TIME(TIMESTAMPDIFF(second, start, end)) AS duration, start, end FROM session_summaries", [PDO::FETCH_ASSOC]);
$data_to_export->execute();

$csvFilename = 'export_session_summaries_' . date('Y-m-d_H-i-s') . '.csv';

$path = fopen($csvFilename, 'w');

fputcsv($path, array_keys((array)$data_to_export->fetchObject()));
while ($row = $data_to_export->fetchObject()) {
    fputcsv($path, [
        $row->entries,
        $row->errors,
        $row->correct_sequences,
        $row->duration,
        $row->start,
        $row->end
    ]);
}
fclose($path);
header('Content-Type: text/csv');
header('Content-Disposition: attachment; filename="' . $csvFilename . '"');
readfile($csvFilename);
unlink($csvFilename);
exit;
