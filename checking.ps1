param (
    [switch]$DisableRealTimeProtection,
    [switch]$DisableFileUpload,
    [switch]$DisableDefender
)

# Function to get the status of Microsoft Defender
function Get-DefenderStatus {
    $serviceStatus = Get-Service -Name "WinDefend" -ErrorAction SilentlyContinue

    if ($null -eq $serviceStatus) {
        Write-Host "Microsoft Defender Antivirus service is not installed on this system."
        return
    }

    if ($serviceStatus.Status -eq 'Running') {
        Write-Host "Microsoft Defender Antivirus service is running."
    } else {
        Write-Host "Microsoft Defender Antivirus service is not running."
    }

    $defenderStatus = Get-MpComputerStatus

    if ($defenderStatus.AntivirusEnabled) {
        Write-Host "Microsoft Defender Antivirus is enabled."
    } else {
        Write-Host "Microsoft Defender Antivirus is disabled."
    }

    $lastUpdate = $defenderStatus.AntivirusSignatureLastUpdated
    Write-Host "Last update installed on: $lastUpdate"

    $updateStatus = Get-MpPreference | Select-Object -ExpandProperty SignatureUpdateInterval
    $timeSinceUpdate = (Get-Date) - $lastUpdate

    if ($timeSinceUpdate.TotalDays -le $updateStatus) {
        Write-Host "Microsoft Defender Antivirus signatures are up to date."
    } else {
        Write-Host "Microsoft Defender Antivirus signatures are outdated."
    }

    $scanStatus = $defenderStatus.RealTimeProtectionEnabled

    if ($scanStatus) {
        Write-Host "Real-time protection is enabled."
    } else {
        Write-Host "Real-time protection is disabled."
    }
}

# Function to disable real-time protection
function Disable-RealTimeProtection {
    Set-MpPreference -DisableRealtimeMonitoring $true
    Write-Host "Real-time protection has been disabled."
}

# Function to disable file upload
function Disable-FileUpload {
    Set-MpPreference -SubmitSamplesConsent 2
    Write-Host "File upload for sample submission has been disabled."
}

# Function to disable Microsoft Defender
function Disable-Defender {
    Stop-Service -Name "WinDefend" -Force
    Set-Service -Name "WinDefend" -StartupType Disabled
    Write-Host "Microsoft Defender Antivirus has been disabled."
}

# Execute functions based on switches
Get-DefenderStatus

if ($DisableRealTimeProtection) {
    Disable-RealTimeProtection
}

if ($DisableFileUpload) {
    Disable-FileUpload
}

if ($DisableDefender) {
    Disable-Defender
}
