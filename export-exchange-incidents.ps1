param(
    [string]$EnvFile = ".env"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Show-Banner {
    Write-Host "========================================"
    Write-Host "            SkyhighMonitor"
    Write-Host "========================================"
}

function Get-EnvMap {
    param(
        [string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        throw "Arquivo .env nao encontrado em: $Path"
    }

    $values = @{}
    foreach ($rawLine in Get-Content -LiteralPath $Path) {
        $line = $rawLine.Trim()
        if (-not $line -or $line.StartsWith("#") -or -not $line.Contains("=")) {
            continue
        }

        $parts = $line.Split("=", 2)
        $key = $parts[0].Trim()
        if (-not $key) {
            continue
        }

        $value = $parts[1].Trim().Trim("'`"")
        if (-not $values.ContainsKey($key)) {
            $values[$key] = $value
        }
    }

    return $values
}

function Get-RequiredValue {
    param(
        [hashtable]$Values,
        [string]$Name
    )

    if (-not $Values.ContainsKey($Name) -or [string]::IsNullOrWhiteSpace([string]$Values[$Name])) {
        throw "Variavel obrigatoria ausente no .env: $Name"
    }

    return [string]$Values[$Name]
}

function Get-OptionalValue {
    param(
        [hashtable]$Values,
        [string]$Name,
        [string]$Default = ""
    )

    if ($Values.ContainsKey($Name) -and -not [string]::IsNullOrWhiteSpace([string]$Values[$Name])) {
        return [string]$Values[$Name]
    }

    return $Default
}

function Get-BasicAuthHeaderValue {
    param(
        [string]$Email,
        [string]$Password
    )

    $bytes = [System.Text.Encoding]::UTF8.GetBytes("${Email}:${Password}")
    $token = [Convert]::ToBase64String($bytes)
    return "Basic $token"
}

function Get-StartTimeForOneDay {
    $utcNow = [DateTime]::UtcNow
    $utcStart = Get-Date -Date $utcNow.Date -Format "yyyy-MM-ddTHH:mm:ss.000Z"
    return $utcStart
}

function Get-ObjectPropertyValue {
    param(
        [object]$InputObject,
        [string]$PropertyName
    )

    if ($null -eq $InputObject) {
        return $null
    }

    $property = $InputObject.PSObject.Properties[$PropertyName]
    if ($null -eq $property) {
        return $null
    }

    return $property.Value
}

function Get-NextStartTime {
    param(
        [object]$Response
    )

    $responseInfo = Get-ObjectPropertyValue -InputObject $Response -PropertyName "responseInfo"
    $topLevelNextStartTime = Get-ObjectPropertyValue -InputObject $responseInfo -PropertyName "nextStartTime"
    if ($topLevelNextStartTime) {
        return [string]$topLevelNextStartTime
    }

    $body = Get-ObjectPropertyValue -InputObject $Response -PropertyName "body"
    $nestedResponseInfo = Get-ObjectPropertyValue -InputObject $body -PropertyName "responseInfo"
    $nestedNextStartTime = Get-ObjectPropertyValue -InputObject $nestedResponseInfo -PropertyName "nextStartTime"
    if ($nestedNextStartTime) {
        return [string]$nestedNextStartTime
    }

    return $null
}

function Get-IncidentItems {
    param(
        [object]$Response
    )

    if ($Response -is [System.Array]) {
        return @($Response)
    }

    foreach ($propertyName in @("incidents", "items", "results", "data")) {
        $propertyValue = Get-ObjectPropertyValue -InputObject $Response -PropertyName $propertyName
        if ($null -ne $propertyValue) {
            return @($propertyValue)
        }
    }

    $body = Get-ObjectPropertyValue -InputObject $Response -PropertyName "body"
    $nestedIncidents = Get-ObjectPropertyValue -InputObject $body -PropertyName "incidents"
    if ($null -ne $nestedIncidents) {
        return @($nestedIncidents)
    }

    return @()
}

function Get-IncidentKey {
    param(
        [object]$Incident
    )

    if ($Incident.incidentId) {
        return "incidentId:$($Incident.incidentId)"
    }

    if ($Incident.id) {
        return "id:$($Incident.id)"
    }

    return ($Incident | ConvertTo-Json -Depth 20 -Compress)
}

function Get-ToFieldValue {
    param(
        [object]$Incident
    )

    if ($null -eq $Incident.information -or $null -eq $Incident.information.internalCollaborators) {
        return ""
    }

    $collaborators = $Incident.information.internalCollaborators
    if ($collaborators -is [System.Array]) {
        return (($collaborators | ForEach-Object { "$_" }) -join ";")
    }

    return [string]$collaborators
}

function Invoke-IncidentsPage {
    param(
        [string]$BaseUrl,
        [string]$IncidentsPath,
        [string]$Email,
        [string]$Password,
        [int]$PageSize,
        [string]$StartTime
    )

    $normalizedBase = $BaseUrl.TrimEnd("/")
    $normalizedPath = $IncidentsPath.TrimStart("/")
    $uri = "{0}/{1}?limit={2}" -f $normalizedBase, $normalizedPath, $PageSize
    $headers = @{
        Accept = "application/json"
        Authorization = Get-BasicAuthHeaderValue -Email $Email -Password $Password
    }
    $body = @{
        startTime = $StartTime
    } | ConvertTo-Json -Depth 10

    return Invoke-RestMethod -Method Post -Uri $uri -Headers $headers -ContentType "application/json" -Body $body
}

function Get-ExchangeIncidents {
    param(
        [string]$BaseUrl,
        [string]$IncidentsPath,
        [string]$Email,
        [string]$Password,
        [int]$PageSize,
        [int]$MaxPages,
        [string]$StartTime
    )

    $allIncidents = New-Object System.Collections.Generic.List[object]
    $seenKeys = New-Object System.Collections.Generic.HashSet[string]
    $currentStartTime = $StartTime

    for ($page = 0; $page -lt $MaxPages; $page++) {
        $response = Invoke-IncidentsPage `
            -BaseUrl $BaseUrl `
            -IncidentsPath $IncidentsPath `
            -Email $Email `
            -Password $Password `
            -PageSize $PageSize `
            -StartTime $currentStartTime
        $pageItems = @(Get-IncidentItems -Response $response)

        foreach ($incident in $pageItems) {
            $serviceNames = @($incident.serviceNames)
            if ($serviceNames -notcontains "Microsoft Exchange Online") {
                continue
            }

            if ([string]$incident.instanceName -ne "Exchange Online") {
                continue
            }

            $key = Get-IncidentKey -Incident $incident
            if ($seenKeys.Add($key)) {
                [void]$allIncidents.Add($incident)
            }
        }

        if ($pageItems.Count -lt $PageSize) {
            break
        }

        $nextStartTime = Get-NextStartTime -Response $response
        if ([string]::IsNullOrWhiteSpace($nextStartTime) -or $nextStartTime -eq $currentStartTime) {
            break
        }

        $currentStartTime = $nextStartTime
    }

    return $allIncidents.ToArray()
}

function Export-IncidentsCsv {
    param(
        [object[]]$Incidents,
        [string]$OutputPath
    )

    $rows = foreach ($incident in $Incidents) {
        [PSCustomObject]@{
            incident_id = if ($incident.incidentId) { [string]$incident.incidentId } else { [string]$incident.id }
            from = if ($incident.actorId) { [string]$incident.actorId } else { "" }
            to = Get-ToFieldValue -Incident $incident
        }
    }

    $rows | Export-Csv -LiteralPath $OutputPath -NoTypeInformation -Encoding UTF8
}

$executionDir = (Get-Location).Path
$envPath = if ([System.IO.Path]::IsPathRooted($EnvFile)) {
    $EnvFile
} else {
    Join-Path $executionDir $EnvFile
}

Show-Banner
Write-Host "Diretorio de execucao: $executionDir"
Write-Host "Arquivo .env: $envPath"

$envValues = Get-EnvMap -Path $envPath
$email = Get-RequiredValue -Values $envValues -Name "SKY_EMAIL"
$password = Get-RequiredValue -Values $envValues -Name "SKY_PASSWORD"
$baseUrl = Get-OptionalValue -Values $envValues -Name "SKY_BASE_URL" -Default "https://www.myshn.net"
$incidentsPath = Get-OptionalValue `
    -Values $envValues `
    -Name "SKY_INCIDENTS_PATH" `
    -Default "/shnapi/rest/external/api/v1/queryIncidents"
$pageSize = [int](Get-OptionalValue -Values $envValues -Name "SKY_PAGE_SIZE" -Default "200")
$maxPages = [int](Get-OptionalValue -Values $envValues -Name "SKY_MAX_PAGES" -Default "1000")
$startTime = Get-StartTimeForOneDay
$outputPath = Join-Path $executionDir ("exchange_incidents_{0}.csv" -f (Get-Date).ToUniversalTime().ToString("yyyyMMdd"))

Write-Host "Consultando incidentes Exchange Online desde: $startTime"

$incidents = Get-ExchangeIncidents `
    -BaseUrl $baseUrl `
    -IncidentsPath $incidentsPath `
    -Email $email `
    -Password $password `
    -PageSize $pageSize `
    -MaxPages $maxPages `
    -StartTime $startTime

Export-IncidentsCsv -Incidents $incidents -OutputPath $outputPath

Write-Host "Total de incidentes exportados: $($incidents.Count)"
Write-Host "CSV exportado em: $outputPath"
