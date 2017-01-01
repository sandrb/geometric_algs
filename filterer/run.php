<?php
$input = file_get_contents("data.txt");
$lines = explode("\n",$input);

$n = $lines[0];
$m = $lines[1];
$ratio = explode(" ",$lines[2]);
$ratio = $ratio[0] / $ratio[1];
$vertices = array();
$curpos = 3;

//alle verkeerde punten wegfilteren
for($i = 0; $i < $n; $i++){
    $point = explode(" ",$lines[$i + $curpos]);
    if(($point[0] < 400 || $point[0] > 600) || ($point[1] < 400 || $point[1] > 600)){
        //als 1 van de coordinaten niet in de range 400-600 zit is het voldoende
        $vertices[] = array("x" => $point[0], "y" => $point[1]);
    }
}

//alle verkeerde objectpunten
$obstacles = array();
$curpos += $n;
for($i = 0; $i < $m; $i++){
    $point = explode(" ",$lines[$i + $curpos]);
    if($point[0] >= 400 && $point[0] <= 600 && $point[1] >= 400 && $point[1] <= 600){
        //alles binnen de range 400-600
        $obstacles[] = array("x" => $point[0], "y" => $point[1]);
    }
}

echo count($vertices) . "<br>";
echo count($obstacles) . "<br>";
echo $lines[2] . "<br>";
foreach($vertices as $vertex){
    echo $vertex["x"] . " " . $vertex["y"] . "<br>";
}
foreach($obstacles as $obstacle){
    echo $obstacle["x"] . " " . $obstacle["y"] . "<br>";
}
?>