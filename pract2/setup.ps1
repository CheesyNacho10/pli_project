param (
  [string]$primerArchivo,
  [string]$segundoArchivo,
  [string]$rutaDestino
)

# Obtener el nombre base del primer archivo (sin extensión)
$nombreBase = [System.IO.Path]::GetFileNameWithoutExtension($primerArchivo)

# Construir la ruta de destino para el primer archivo
$rutaDestinoPrimerArchivo = Join-Path $rutaDestino (Split-Path -Leaf $primerArchivo)

# Construir la ruta de destino para el segundo archivo (incluyendo la nueva carpeta)
$nuevaCarpeta = Join-Path $rutaDestino $nombreBase
$rutaDestinoSegundoArchivo = Join-Path $nuevaCarpeta (Split-Path -Leaf $segundoArchivo)

# Verificar si la nueva carpeta existe, si no, crearla
if (-not (Test-Path $nuevaCarpeta)) {
  New-Item -ItemType Directory -Path $nuevaCarpeta
}

# Copiar los archivos a sus respectivas rutas de destino
Copy-Item $primerArchivo -Destination $rutaDestinoPrimerArchivo
Copy-Item $segundoArchivo -Destination $rutaDestinoSegundoArchivo
