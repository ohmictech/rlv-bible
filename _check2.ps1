$root = 'c:\Users\darius\Documents\ntrlv'
$specs = @(
  '40-matthew\matthew-ch-005.md|25-26|Matt 5:25-26',
  '40-matthew\matthew-ch-012.md|31-32|Matt 12:31-32',
  '42-luke\luke-ch-012.md|58-59|Luke 12:58-59',
  '43-john\john-ch-003.md|36|John 3:36',
  '45-romans\romans-ch-009.md|22-23|Rom 9:22-23',
  '45-romans\romans-ch-010.md|11-13|Rom 10:11-13',
  '56-titus\titus-ch-002.md|11-14|Titus 2:11-14',
  '60-1-peter\1-peter-ch-003.md|18-20|1 Pet 3:18-20',
  '60-1-peter\1-peter-ch-004.md|6|1 Pet 4:6',
  '23-isaiah\isaiah-ch-057.md|16-18|Isa 57:16-18',
  '66-revelation\revelation-ch-015.md|4|Rev 15:4',
  '19-psalms\psalms-ch-136.md|1|Ps 136:1',
  '23-isaiah\isaiah-ch-026.md|19|Isa 26:19',
  '25-lamentations\lamentations-ch-003.md|31-33|Lam 3:31-33',
  '58-hebrews\hebrews-ch-010.md|12-14|Heb 10:12-14',
  '44-acts\acts-ch-010.md|34-35|Acts 10:34-35',
  '52-1-thessalonians\1-thessalonians-ch-005.md|9-10|1 Thess 5:9-10'
)
$out = New-Object System.Collections.Generic.List[string]
foreach ($item in $specs) {
  $parts = $item -split '\|'
  $path = Join-Path $root $parts[0]
  $label = $parts[2]
  if (Test-Path $path) {
    $lines = [System.IO.File]::ReadAllLines($path)
    $range = $parts[1] -split '-'
    $start = [int]$range[0]
    if ($range.Count -gt 1) { $end = [int]$range[1] } else { $end = $start }
    for ($i = $start; $i -le $end; $i++) {
      $out.Add(('{0} [{1}] {2}' -f $label, $i, $lines[$i-1].Trim()))
    }
  } else { $out.Add($label + ' MISSING ' + $path) }
}
[System.IO.File]::WriteAllLines((Join-Path $root '_report2.txt'), $out, (New-Object System.Text.UTF8Encoding($false)))
'lines=' + $out.Count
