<?php
$want = $_GET['want'];

if ( !isset($want) ) {
	echo "need what you want";
	exit(1);
}

$imgs = [];
if ($want == 'img') {
	#$img_url = "http://www.speed.com/images/" . $max;
	$fh   = fopen('../images/1.jpg', 'rb');
	$size = filesize($imgFile);
	$content = fread($fh, $size);
	fclose($fh);

	$encoder = base64_encode($content);

	$img_str = "data:image/jpeg;base64," . $encoder;
	echo json_encode(array(
		"imgBinStr" => $img_str
	));
}
else {
	echo "invalid reqeust";
	exit(1);	
}
