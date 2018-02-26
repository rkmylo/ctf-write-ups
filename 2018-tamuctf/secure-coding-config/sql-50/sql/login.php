<?php
  ini_set('display_errors', 'On');
  error_reporting(E_ALL | E_STRICT);
  echo "<html>";
  if (isset($_POST["username"]) && isset($_POST["password"])) {
    $servername = "localhost";
    $username = "sqli-server";
    $password = 'Bx117@$YaML**!';
    $dbname = "SqliDB";
    // Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);
    if ($conn->connect_error)
        die("Connection failed: " . $conn->connect_error);
    // User and pass that were passed to us.
    // NOTE: The fact that the password is plaintext is not part of the challenge. It just makes testing much easier
    $user = $_POST['username'];
    $pass = $_POST['password']; 

    // Ensure admin will always be the first record, though really unnecessary
    $sql = "SELECT * FROM Users WHERE User='$user' AND Password='$pass' ORDER BY ID";
    if ($result = $conn->query($sql)) // Query
    {
      if ($result->num_rows >= 1)
      {
        $row = $result->fetch_assoc();
        if ($row["User"] == "admin")
          echo "You logged in as " . $row["User"];
      }
      else {
        echo "Dat be invalid login info!";
      }
    }
    $conn->close();
  }
  else
    echo "Must supply username and password...";
  echo "</html>";
?>

