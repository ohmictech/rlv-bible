$root = 'c:\Users\darius\Documents\ntrlv'
$enc = New-Object System.Text.UTF8Encoding($true)
# order matters: longer corrupted forms first, plain driftg last
$fixes = @(
  @('driftsging','singing'),
  @('driftsgers','singers'),
  @('driftging','singing'),
  @('driftsews','sinews'),
  @('driftsg','sings'),
  @('driftged','singed'),
  @('driftsk','sink'),
  @('driftg','sing')
)
$files = Get-ChildItem -Path $root -Recurse -Filter '*-ch-*.md'
$total = 0
foreach ($f in $files) {
  $text = [System.IO.File]::ReadAllText($f.FullName)
  $orig = $text
  foreach ($pair in $fixes) {
    $pattern = '\b' + $pair[0] + '\b'
    $text = [regex]::Replace($text, $pattern, $pair[1])
  }
  if ($text -ne $orig) {
    [System.IO.File]::WriteAllText($f.FullName, $text, $enc)
    $n = 0
    foreach ($pair in $fixes) { $n += ([regex]::Matches($orig, '\b' + $pair[0] + '\b')).Count }
    $total += $n
    $f.Name + ' fixed ' + $n
  }
}
'TOTAL FIXED ' + $total
