$Path = "./log.txt"
$c = gc $Path -ea Stop
$Results = $c | % {
    $url, $result = $_ -split ': ', 2
    $pass = $result -eq "pass"
    $err = $msg = $null
    if (-not $pass) {
        $err, $msg = $result -split ': ', 2
    }
    [pscustomobject]@{
        Url = $url
        Pass = $pass
        Error = $err
        Message = $msg
    }
}

$Results
