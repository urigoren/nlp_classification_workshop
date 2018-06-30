<?php
if (array_key_exists("submission", $_REQUEST) && array_key_exists("user",$_REQUEST)) //Record submission
{
        $user=preg_replace("/[^a-zA-Z0-9_]+/", "", $_REQUEST["user"]);
        $submission=json_decode($_REQUEST["submission"],true);
        $truth=json_decode(file_get_contents("holdout.data"),true);
        $n=0;$score=0;
        foreach($truth as $x=>$y) {
            $n +=1;
            $score += array_key_exists($x, $submission) && $submission[$x]==$y ? 1 : 0;
        }
        $score /= $n;
        $submission["score"]=$score;
        $submission["user"]=$user;
        file_put_contents($user.".json",json_encode($submission));
        echo $score;
}
else // Show leaderboard
{
        $scores=array_reduce(array_map(function ($f) {
                $json= json_decode(file_get_contents($f),true);
                return array(str_replace(".json","",$f)=>$json["score"]);
        },array_filter(scandir('.'), function ($x) {
                return substr($x,-5)=='.json';
        })),array_merge,array());
        arsort($scores);
        echo "<html><body><div align=\"center\"><h1>Leader board</h1>";
        echo "<table border =\"0\">";
        echo "<tr><th>User</th><th>Accuracy</th></tr>";
        foreach($scores as $user=>$score) {
                echo "<tr><th>$user</th><td>$score</td></tr>";
        }
        echo "</table></div></body></html>";
}
?>
