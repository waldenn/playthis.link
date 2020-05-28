<?php

$url = ltrim($_SERVER['REQUEST_URI'], '/');
$hi = 'Hi 👋 <br>Prefix any URL with playthis.link to instantly listen to it as audio.<br><br>Made by <a href="https://twitter.com/soheil">@soheil</a>';
if ($url == '') {
  echo $hi;
  exit();
}
$out_file = md5($url) . '.mp3';

`python3 synthesize.py --text "$url" --out $out_file 2>&1`;

if (!file_exists($out_file)) {
  echo $hi;
  exit();
}

header("location: /$out_file");
