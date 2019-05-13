
<?php 
  // create curl resource
  $ch = curl_init();
  // set url 
  curl_setopt($ch, CURLOPT_URL, "localhost:5000/register");
  // $output contains the output json
  $output = curl_exec($ch);
  // close curl resource to free up system resources 
  curl_close($ch);
  // {"name":"Baron","gender":"male","probability":0.88,"count":26}
  //var_dump(json_decode($output, true));
?>