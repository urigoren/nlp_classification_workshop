<?php
if (array_key_exists("submission", $_REQUEST) && array_key_exists("user",$_REQUEST)) //Record submission
{
        // See submission client: https://github.com/urigoren/nlp_classification/blob/master/python/submit.py
        $user=preg_replace("/[^a-zA-Z0-9_]+/", "", $_REQUEST["user"]);
        $submission=json_decode($_REQUEST["submission"],true);
        $truth=json_decode(file_get_contents("holdout.data"),true);
        // Calculate the accuracy of the submission
        $n=0;$score=0;
        foreach($truth as $x=>$y) {
            $n +=1;
            $score += array_key_exists($x, $submission) && $submission[$x]==$y ? 1 : 0;
        }
        $score /= $n;
        $submission["score"]=$score;
        $submission["user"]=$user;
        // Save submission as json file
        file_put_contents("$user.json",json_encode($submission));
        echo $score;
}
else // Show leaderboard
{
        // flat files to "user"=>"score" array
        $scores = array();
        $files = scandir('.');
        foreach ($files as $index=>$fname) {
                if (substr($fname,-5)=='.json') {
                        $json= json_decode(file_get_contents($fname),true);
                        $scores[$json["user"]]=$json["score"];
                }
        }
        arsort($scores);
        // Format the leaderboard
        echo "<html><head><meta http-equiv=\"refresh\" content=\"30\" /></head>";
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <title>NLP Classification Workshop</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js"></script>
  <meta http-equiv="refresh" content="30" />
</head>
<body><div class="container" align="center">
<h1>Leader board</h1>
  <table class="table table-striped">
    <thead>
      <tr>
        <th>Submission_id</th>
        <th>Accuracy</th>
      </tr>
    </thead>
    <tbody>
<?php
        foreach($scores as $user=>$score) {
                echo "<tr><th>$user</th><td>$score</td></tr>";
        }
?>
</tbody></table>
<br />
Made by <a href="http://www.goren4u.com">Uri Goren</a>.
</div></body></html>
<?php
}
?>
