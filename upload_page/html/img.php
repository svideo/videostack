<?php

header('Content-type: image/jpeg'); 
$imgFile = '../images/1.jpg';
$fh   = fopen('../images/1.jpg', 'rb');
$size = filesize($imgFile);
$content = fread($fh, $size);
fclose($fh);

$encoder = base64_encode($content);

$img_str = "data:image/jpeg;base64," . $encoder;
echo $img_str;
?>
