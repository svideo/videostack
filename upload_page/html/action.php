<?php
var_dump($_FILES);
if (empty($_FILES['upload']['name'])) {
	echo "请选择文件";
	exit;
}

$upload_dir = '/tmp/name.jpg';
if (move_uploaded_file($_FILES['upload']['tmp_name'], $upload_dir)) {
		echo "文件上传成功";
} else {
		echo "文件上传失败";
		exit;
}

?>
