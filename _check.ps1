$root = 'c:\Users\darius\Documents\ntrlv'
$specs = @(
  @{g='A. God wills all, the world, every person'; s=@(
    '43-john\john-ch-001.md|29|John 1:29',
    '43-john\john-ch-003.md|16-17|John 3:16-17',
    '43-john\john-ch-004.md|42|John 4:42',
    '43-john\john-ch-006.md|37-40|John 6:37-40',
    '43-john\john-ch-011.md|52|John 11:52',
    '43-john\john-ch-012.md|32|John 12:32',
    '43-john\john-ch-012.md|47|John 12:47',
    '43-john\john-ch-017.md|2|John 17:2',
    '42-luke\luke-ch-002.md|10|Luke 2:10',
    '42-luke\luke-ch-003.md|6|Luke 3:6',
    '40-matthew\matthew-ch-018.md|14|Matt 18:14',
    '54-1-timothy\1-timothy-ch-002.md|3-4|1 Tim 2:3-4',
    '54-1-timothy\1-timothy-ch-002.md|6|1 Tim 2:6',
    '54-1-timothy\1-timothy-ch-004.md|10|1 Tim 4:10',
    '56-titus\titus-ch-002.md|11|Titus 2:11',
    '61-2-peter\2-peter-ch-003.md|9|2 Pet 3:9',
    '62-1-john\1-john-ch-002.md|2|1 John 2:2',
    '62-1-john\1-john-ch-004.md|14|1 John 4:14'
  )}
  @{g='B. All reconciled, all in Christ'; s=@(
    '45-romans\romans-ch-003.md|23-24|Rom 3:23-24',
    '45-romans\romans-ch-005.md|18-19|Rom 5:18-19',
    '45-romans\romans-ch-005.md|20|Rom 5:20',
    '45-romans\romans-ch-011.md|15|Rom 11:15',
    '45-romans\romans-ch-011.md|32|Rom 11:32',
    '45-romans\romans-ch-011.md|36|Rom 11:36',
    '46-1-corinthians\1-corinthians-ch-015.md|22|1 Cor 15:22',
    '46-1-corinthians\1-corinthians-ch-015.md|26-28|1 Cor 15:26-28',
    '47-2-corinthians\2-corinthians-ch-005.md|14-15|2 Cor 5:14-15',
    '47-2-corinthians\2-corinthians-ch-005.md|19|2 Cor 5:19',
    '51-colossians\colossians-ch-001.md|15-20|Col 1:15-20',
    '51-colossians\colossians-ch-001.md|23|Col 1:23',
    '49-ephesians\ephesians-ch-001.md|9-10|Eph 1:9-10',
    '49-ephesians\ephesians-ch-004.md|6|Eph 4:6',
    '50-philippians\philippians-ch-002.md|9-11|Phil 2:9-11',
    '58-hebrews\hebrews-ch-002.md|8-9|Heb 2:8-9',
    '44-acts\acts-ch-003.md|21|Acts 3:21',
    '48-galatians\galatians-ch-003.md|8|Gal 3:8',
    '01-genesis\genesis-ch-012.md|3|Gen 12:3'
  )}
  @{g='C. Creation, nations, and the wide promises'; s=@(
    '45-romans\romans-ch-008.md|19-22|Rom 8:19-22',
    '45-romans\romans-ch-014.md|11|Rom 14:11',
    '66-revelation\revelation-ch-005.md|13|Rev 5:13',
    '66-revelation\revelation-ch-021.md|4-5|Rev 21:4-5',
    '66-revelation\revelation-ch-022.md|2|Rev 22:2',
    '23-isaiah\isaiah-ch-025.md|8|Isa 25:8',
    '23-isaiah\isaiah-ch-045.md|22-25|Isa 45:22-25',
    '23-isaiah\isaiah-ch-052.md|10|Isa 52:10',
    '23-isaiah\isaiah-ch-055.md|10-11|Isa 55:10-11',
    '23-isaiah\isaiah-ch-002.md|2-4|Isa 2:2-4',
    '23-isaiah\isaiah-ch-019.md|22-25|Isa 19:22-25',
    '36-zephaniah\zephaniah-ch-003.md|9|Zeph 3:9',
    '38-zechariah\zechariah-ch-014.md|9|Zech 14:9',
    '19-psalms\psalms-ch-022.md|27-28|Ps 22:27-28',
    '19-psalms\psalms-ch-065.md|2|Ps 65:2',
    '19-psalms\psalms-ch-086.md|9|Ps 86:9',
    '19-psalms\psalms-ch-098.md|2-3|Ps 98:2-3',
    '19-psalms\psalms-ch-145.md|9-10|Ps 145:9-10',
    '02-exodus\exodus-ch-034.md|6-7|Ex 34:6-7'
  )}
  @{g='D. Mercy that outlasts the anger'; s=@(
    '25-lamentations\lamentations-ch-003.md|22-33|Lam 3:22-33',
    '19-psalms\psalms-ch-030.md|5|Ps 30:5',
    '19-psalms\psalms-ch-103.md|8-14|Ps 103:8-14',
    '19-psalms\psalms-ch-139.md|8|Ps 139:8',
    '28-hosea\hosea-ch-011.md|8-9|Hos 11:8-9',
    '28-hosea\hosea-ch-013.md|14|Hos 13:14',
    '33-micah\micah-ch-007.md|18-20|Micah 7:18-20',
    '26-ezekiel\ezekiel-ch-016.md|53-55|Ezek 16:53-55',
    '23-isaiah\isaiah-ch-054.md|7-8|Isa 54:7-8',
    '18-job\job-ch-033.md|29-30|Job 33:29-30',
    '32-jonah\jonah-ch-004.md|11|Jonah 4:11'
  )}
  @{g='E. The warning texts, for comparison'; s=@(
    '40-matthew\matthew-ch-003.md|12|Matt 3:12',
    '40-matthew\matthew-ch-013.md|42|Matt 13:42',
    '40-matthew\matthew-ch-018.md|8|Matt 18:8',
    '40-matthew\matthew-ch-025.md|41|Matt 25:41',
    '40-matthew\matthew-ch-025.md|46|Matt 25:46',
    '41-mark\mark-ch-009.md|43-49|Mark 9:43-49',
    '42-luke\luke-ch-003.md|17|Luke 3:17',
    '42-luke\luke-ch-012.md|47-48|Luke 12:47-48',
    '53-2-thessalonians\2-thessalonians-ch-001.md|9|2 Thess 1:9',
    '65-jude\jude-ch-001.md|7|Jude 7',
    '66-revelation\revelation-ch-014.md|11|Rev 14:11',
    '66-revelation\revelation-ch-020.md|10|Rev 20:10',
    '66-revelation\revelation-ch-020.md|14-15|Rev 20:14-15',
    '66-revelation\revelation-ch-021.md|8|Rev 21:8',
    '27-daniel\daniel-ch-012.md|2|Dan 12:2',
    '23-isaiah\isaiah-ch-066.md|22-24|Isa 66:22-24',
    '46-1-corinthians\1-corinthians-ch-003.md|15|1 Cor 3:15',
    '46-1-corinthians\1-corinthians-ch-013.md|8|1 Cor 13:8',
    '58-hebrews\hebrews-ch-006.md|2|Heb 6:2'
  )}
)
$out = New-Object System.Collections.Generic.List[string]
foreach ($grp in $specs) {
  $out.Add('=== ' + $grp.g + ' ===')
  foreach ($item in $grp.s) {
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
    } else {
      $out.Add($label + ' MISSING FILE ' + $path)
    }
  }
  $out.Add('')
}
[System.IO.File]::WriteAllLines((Join-Path $root '_report.txt'), $out, (New-Object System.Text.UTF8Encoding($false)))
'lines=' + $out.Count
