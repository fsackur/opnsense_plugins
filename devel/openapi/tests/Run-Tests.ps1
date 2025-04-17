param
(
    [switch]$NoRun,

    [int[]]$Slice,

    $LogPath = "./pytest.log"
)

if (-not ($NoRun -and (Test-Path $LogPath)))
{
    Remove-Item $LogPath -ErrorAction Ignore

    $_args = "test_api.py", "--tb=no"
    if ($Slice)
    {
        $_args += "--slice", "[$($Slice -join ":")]"
    }
    pytest @_args | Out-Null
}

$LogLines = Get-Content $LogPath -ErrorAction Stop

$AddProp = "Additional properties are not allowed"
$NotType = "is not of type"

$Results = $LogLines | % {
    $url, $result = $_ -split ': ', 2
    $pass = $result -eq "pass"
    $err = $msg = $null
    if (-not $pass) {
        $err, $msg = $result -split ': ', 2
    }

    $data = $null
    if ($msg) {
        if ($msg.StartsWith($AddProp)) {
            $data = $msg.Substring(38)
            $msg = $AddProp
        } else {
            $data = $msg -replace " $NotType.*"
            $msg = $msg -replace ".*(?=$NotType)"
        }
    } elseif (-not $pass) {
        $msg = "Failed"
    }

    [pscustomobject]@{
        Url = $url
        Pass = $pass
        Error = $err
        Message = $msg
        Data = $data
    }
}

$Global:ByUrl = $Results | group Url -AsHashTable
$Global:ByError = $Results | group {$_.Message -replace '(?<=^\w.*)[\(\{].*|.*[\(\}]'}

$ByError
