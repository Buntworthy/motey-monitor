<?php
$servername = "mysql.cutsquash.com";
$username = "cutsquashcom";
$password = "PASSWORD_GOES_HERE";
$dbname = "cutsquash_house_data";
$key = 'KEY_GOES_HERE';

// Check the key is what we expect
if ($_GET["key"] != $key) {
	die("Incorrect key");
}

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// add the current reading to the database
$sql = "INSERT INTO temperature (date, ID, temp)
			VALUES ('" .
				$_GET["datetime"] . "','" .
				$_GET["id"] . "', '" .
				$_GET["temp"] .
				"')";

if ($conn->query($sql) === TRUE) {
	echo("OK");
} else {
    die("Connection failed: " . $conn->error);
}

$conn->close();

?>