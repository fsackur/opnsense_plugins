param
(
    [switch]$NoRun,

    [int[]]$Slice,

    $LogPath = "./pytest.log",

    $SpecPath = "./openapi.yml"
)


if (-not $Spec)
{
    $Global:Spec = gc $SpecPath | ConvertFrom-Yaml -AsHashtable
}


if (-not ($NoRun -and (Test-Path $LogPath)))
{
    Remove-Item $LogPath -ErrorAction Ignore

    $_args = "test_api.py", "--tb=no" #, "--rootdir", $PSScriptRoot
    if ($Slice)
    {
        $_args += "--slice", "[$($Slice -join ":")]"
    }
    pytest @_args | Out-Null
}

$LogLines = Get-Content $LogPath -ErrorAction Stop

$AddProp = "Additional properties are not allowed"
$NotType = "is not of type"

$Global:Results = $LogLines | % {
    $url, $result = $_ -split ': ', 2
    $pass = $result -eq "pass"
    $err = $msg = $null
    if (-not $pass) {
        $err, $msg = $result -split ': ', 2
    }

    $methodOp = $Spec.paths[$url]
    $op = $methodOp.GetEnumerator() | ? Key -ne "description" | % Value
    $schema = $op.responses."200".content.'application/json'.schema
    while ($schema.Keys.Count -and -not $schema['$ref']) {
        $schema = $schema.GetEnumerator() | ? Key -ne "type" | select -First 1 | % Value
    }
    $ref = $schema.'$ref' -replace '^#/components/schemas/'

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

    $change = $null
    if ($_PreviousRun)
    {
        $PreviousPass = $_PreviousRun[$url].Pass
        $changed = $pass -xor $PreviousPass
        $change = if ($changed) {if ($pass) {"Fixed"} else {"Broken"}} else {"NoChange"}
    }

    [pscustomobject]@{
        Url = $url
        Pass = $pass
        Error = $err
        Message = $msg
        Data = $data
        Model = $ref
        Changed = $change
    }
}

$Global:ByUrl = $Results | group Url -AsHashTable
$Global:ByError = $Results | group {$_.Message -replace '(?<=^\w.*)[\(\{].*|.*[\(\}]'}
$Global:Diff = $Results | group Changed
if ($ByUrl)
{
    $Global:_PreviousRun = $ByUrl.Clone()
}
$Diff
