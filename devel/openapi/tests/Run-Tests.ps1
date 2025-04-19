[CmdletBinding(DefaultParameterSetName = "Run")]
param
(
    [Parameter(ParameterSetName = "NoRun")]
    [ValidateScript({$_})]
    [switch]$NoRun,

    [Parameter(ParameterSetName = "Run")]
    [switch]$Quiet,

    [Parameter(ParameterSetName = "Run")]
    [ArgumentCompleter({
        param ($commandName, $parameterName, $wordToComplete, $commandAst, $fakeBoundParameters)
        $Urls = (Get-Content "$PSScriptRoot/urls.py") -match '^\s*"' -replace '\s|"|,$' -replace '/\{\w*\}'
        (@($Urls) -like "$wordToComplete*"), (@($Urls) -like "/$wordToComplete*"), (@($Urls) -like "*$wordToComplete*") | Write-Output | Select-Object -Unique
    })]
    [string[]]$Url,

    [Parameter(ParameterSetName = "Run")]
    [int[]]$Slice,

    $TestFile = "./test_api.py",

    $LogPath = "./pytest.log"
)


if (-not ($NoRun -and (Test-Path $LogPath)))
{
    $_args = @($TestFile, "--log-path", $LogPath, "--no-header")

    if ($VerbosePreference -in (0, 4)) {
        $_args += "--tb=no", "-q", "--no-summary"
    } else {
        $_args += "--tb=short"
    }

    if ($Url) {$_args += "--url", ($Url -join ",")}
    if ($Slice) {$_args += "--slice", "[$($Slice -join ":")]"}

    pytest @_args
}


$AddProp = "Additional properties are not allowed"
$NotType = "is not of type"

enum Change
{
    NoChange = 0
    Fixed = 1
    Broken = -1
}

class Prop
{
    [string]$Path
    [string]$Value

    [string] ToString() {return $this.Path, $this.Value -join ": "}
}

class TestResult
{
    [string]$Url
    [string]$Content
    [bool]$Pass
    [Change]$Change
    [string]$Message
    [string]$Category
    [Prop]$Response
    [string]$Model
    [Prop]$Schema
    [string]$XmlString
    [xml]$Xml
    [string]$FieldType = ""

    [string] ToString() {return $this.Url, $this.Category -join ": "}
}

Update-TypeData -Force -TypeName TestResult -DefaultDisplayPropertySet "Url", "Category", "Message"

Remove-Variable Url
$LogsByUrl = [ordered]@{}
$LastUrl = $null
$Result = $null

$Content = Get-Content $LogPath -Raw -ErrorAction Stop
if (-not $Content) {return}

$BaseLogger = [System.IO.Path]::GetFileNameWithoutExtension("test_api.py")
$LogLines = $Content.Trim() -split "\n(?=$BaseLogger)"
$LogLines | % {
    $Logger, $Message = $_ -split ": ", 2

    $LogParts = $Logger -split '\.' | Select-Object -Skip 2
    $Url, $Key, $ModelName = $LogParts
    $ModelName = $ModelName -join '.'

    if ($Url -ne $LastUrl) {
        if ($Result -and $LastUrl) {$LogsByUrl[$LastUrl] += @($Result)}
        # $Result = 1 | Select-Object Url, Pass, Message, ResponsePath, Response, SchemaPath, Schema, Xml
        # $Result = 1 | Select-Object Url, Pass, Message, Category, Response, Schema, Xml
        $Result = [TestResult]::new()
        $Result.Url = $Url
        $Result.Pass = $false
        $LastUrl = $Url
    }

    if ($Key -in ("response", "schema")) {
        $Path, $Value = $Message -split ': ', 2
        $Value = $Value -replace '\n\s*', ' '
        $Result.$Key = [Prop]@{Path = $Path; Value = $Value}
        if ($ModelName) {$Result.Model = $ModelName}

    } elseif ($Key -eq "message") {
        $Result.Message = $Message
        if ($Message -match $AddProp) {
            $Result.Category = "AddProps"
        } elseif ($Message -match $NotType) {
            $Type = $Message -replace ".* " -replace "'"
            $Type = (Get-Culture).TextInfo.ToTitleCase($Type)
            $Result.Category = "Not$Type"
        } elseif ($Message -eq "pass") {
            $Result.Category = "Pass"
            $Result.Pass = $true
        } else {
            $Result.Category = $Message
            $Result.Pass = $false
        }
    } elseif ($Key -eq "xml") {
        if ($Message -ne "no_xml") {
            $Result.XmlString = $Message
            $Xml = [xml]$Message
            $Result.Xml = $Xml
            $Type = $Xml.type, $Xml.ChildNodes.type | Write-Output | Where-Object {$_} | Select-Object -First 1
            $Result.FieldType = $Type -replace '^\.\\'
        }
    } else {
        try {
            $Result.$Key = $Message
        } catch {
            $_.ErrorDetails = "Unidentified key: '$Key': $_"
            Write-Error -ErrorRecord $_
        }
    }

}
$LogsByUrl[$Url] += @($Result)

$Global:Results = $LogsByUrl.Values | Write-Output

$Global:ByUrl = $Results | group Url -AsHashTable

if ($ByUrl -and $_PreviousRun) {
    foreach ($Url in $ByUrl.Keys) {
        $Current = $ByUrl[$Url]
        $Global:Previous = $_PreviousRun[$Url]

        if (-not $Previous) {continue}

        if ("Pass" -eq $Previous.Category) {
            if ("Pass" -ne $Current.Category) {
                $Current | % {$_.Change = "Broken"}
                continue
            }
        }
        if ("Pass" -eq $Current.Category) {
            if ("Pass" -ne $Previous.Category) {
                $Current | % {$_.Change = "Fixed"}
                continue
            }
        }

        $PreviousByMessage = $Previous | sort Message | group Message -AsHashTable
        if (-not $PreviousByMessage) {
            $Previous
            return
        }
        $Current | % {
            $prev = $PreviousByMessage[$_.Message]
            if ($prev.Pass) {
                if (-not $_.Pass) {$_.Change = "Broken"}
            } else {
                if ($_.Pass) {$_.Change = "Fixed"}
            }
        }
    }
}

if ($ByUrl)
{
    $Global:_PreviousRun = $ByUrl.Clone()
}


$Global:ByError = $Results | group Category
$Global:Diff = $Results | group Change
$Global:Failed = $ByError | ? Name -ne "Pass" | % Group | Write-Output | sort Url

$CategorySummary = @{
    Name = "CategorySummary"
    Expression = {$_.Group | group Category | sort Name | % {"$($_.Name): $($_.Count)"} | join ", "}
}
$Global:ByFieldType = $Results |
    group FieldType |
    select Name, Count, $CategorySummary, Group

$Diff
