param (
    [string]$parentDirectory
)

# Comprobar si el directorio existe
if (-not (Test-Path -Path $parentDirectory -PathType Container)) {
    Write-Host "El directorio no existe: $parentDirectory"
    exit
}

# Cambiar al directorio especificado
Set-Location $parentDirectory

# Obtener todos los subdirectorios
$subdirectories = Get-ChildItem -Directory

foreach ($subdir in $subdirectories) {
    # Reemplazar 'max_steps' por 'maxSteps'
    $newName = $subdir.Name -replace 'max_steps', 'maxSteps'
    if ($newName -ne $subdir.Name) {
        # Renombrar el directorio
        Rename-Item -Path $subdir.FullName -NewName $newName
    }
}

Write-Host "Se han renombrado los directorios correctamente."
