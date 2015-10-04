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

$sql = "SELECT * FROM `temperature` WHERE date > DATE_SUB(NOW(), INTERVAL 7 DAY)";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    $rows = array();
    while($row = $result->fetch_assoc()) {
         $rows[] = $row;
    }
	print json_encode($rows);
} else {
    echo "0 results";
}



$conn->close();

?>