<?php

  require 'controller.php';

?>
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="pico.min.css">
  <link rel="stylesheet" href="pico.colors.min.css">
  <link rel="stylesheet" href="style.css">
  <title>Panel Inżyniera</title>
</head>
<body>
  <header class="container-fluid">
    <h1>Panel inżyniera</h1>
  </header>
  <main class="container">

    <div class="grid">
      <div>
        <h2>Podsumowanie sesji</h2>
        <table class="striped">
          <thead>
            <tr>
              <th>Wejścia</th>
              <th>Błędy</th>
              <th>Poprawne sekwencje</th>
              <th>Czas trwania</th>
              <th>Rozpoczęto</th>
              <th>Zakończono</th>
            </tr>
          </thead>
          <tbody>
            <?php foreach($summaries as $summary): ?>
              <tr>
                <td><?= htmlspecialchars($summary->entries); ?></td>
                <td><?= htmlspecialchars($summary->errors); ?></td>
                <td><?= htmlspecialchars($summary->correct_sequences); ?></td>
                <td><?= htmlspecialchars($summary->duration); ?></td>
                <td><?= htmlspecialchars($summary->start); ?></td>
                <td><?= htmlspecialchars($summary->end); ?></td>
              </tr>
            <?php endforeach;?>
          </tbody>


        </table>
        <button class="pico-background-jade-500">Eksportuj do csv</button>

        <h2>Najczęstsze błędy</h2>
        <table class="striped">   
          <thead>
            <tr>
              <th>Liczba wystąpień</th>
              <th>Treść błędu</th>
            </tr>
          </thead>     
          <?php foreach($errors as $error): ?>
            <tr>
              <td><?= htmlspecialchars($error->count); ?></td>
              <td><?= htmlspecialchars($error->message); ?></td>
            </tr>
          <?php endforeach;?>
        </table>
        <button class="pico-background-jade-500">Eksportuj do csv</button>

      </div>        
    </div>
    <div class="grid">
      <div>1</div>
      <div>2</div>
      <div>3</div>
      <div>4</div>
    </div>
  </main>

  
</body>
</html>