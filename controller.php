<?php

include 'debug.php';

$connection = new PDO('mysql:host=localhost;dbname=engineering_thesis', 'root', '', array(
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
));

if (!$connection) {

  die("Connection failed: " . mysqli_connect_error());

}else{

  $mostCommonErrors = $connection->prepare("SELECT COUNT(*) AS count, message FROM `errors` GROUP BY message ORDER BY count DESC");
  $mostCommonErrors->execute();
  $errors = [];

  while ($row = $mostCommonErrors->fetchObject()) {

    $errors[] = $row;

  }

  $sessionSummaries = $connection->prepare("SELECT entries, errors, correct_sequences, SEC_TO_TIME(TIMESTAMPDIFF(second, start, end)) AS duration, start, end FROM session_summaries");
  $sessionSummaries->execute();
  $summaries = [];

  while ($row = $sessionSummaries->fetchObject()) {

    $summaries[] = $row;

  }

  // dump($summaries);
}