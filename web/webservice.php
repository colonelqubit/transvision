<?php

// Variable allowing includes
$valid = true;

// Init application
require_once 'init.php';

header('Content-type: application/json; charset=UTF-8');

// include the search options.
require_once 'search_options.php';

// include the locale name finder
// include 'locale_find.php';

// include the cache files.
require_once 'cache_import.php';

// fonction de recherche
require_once'recherche.php';


foreach ($keys as $key => $chaine) {
    $ken[$key][$chaine] = $l_fr[$key];
}
foreach ($keys2 as $key => $chaine) {
    $kfr[$key][$chaine] = $l_en[$key];
}

$json_en = json_encode($ken);
$json_fr = json_encode($kfr);

if (isset($_GET['callback'])) {
    if ($_GET['return_loc'] == 'loc') {
        echo $_GET['callback'] . '(' . $json_fr . ');';
    } else{
        echo $_GET['callback'] . '(' . $json_en . ');';
    }
} else {
    if ($_GET['return_loc'] == 'loc'){
        echo $json_fr;
    } else {
        echo $json_en;
    }
}