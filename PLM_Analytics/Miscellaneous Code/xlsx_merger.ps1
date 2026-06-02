# MasterXLSX + UTF8 CSV

$FolderPath = "C:\Your\Folder\Path"

$MasterXlsx = Join-Path $FolderPath "MasterCombined.xlsx"
$MasterCsv  = Join-Path $FolderPath "MasterCombined.csv"

# Excel Constants

$xlOpenXMLWorkbook = 51
$xlCSVUTF8         = 62
$xlCalculationManual = -4135

# Start Excel
$Excel = New-Object -ComObject Excel.Application

$Excel.Visible       = $false
$Excel.DisplayAlerts = $false
$Excel.ScreenUpdating = $false
$Excel.EnableEvents   = $false
$Excel.Calculation    = $xlCalculationManual

# Workbook

$MasterWorkbook = $Excel.Workbooks.Add()
$MasterSheet    = $MasterWorkbook.Sheets.Item(1)

$CurrentRow     = 1
$HeaderCopied   = $false
$ExpectedColumns = $null
$ExpectedHeaders = $null

# Retrieve XLSX

$Files = Get-ChildItem -Path $FolderPath -Filter *.xlsx |
    Where-Object {
        $_.Name -ne "MasterCombined.xlsx" -and
        $_.Name -notlike '~$*'
    } |
    Sort-Object Name

# Process XLSX

foreach ($File in $Files)
{
    Write-Host ""
    Write-Host "Processing: $($File.Name)"

    $Workbook      = $null
    $Sheet         = $null
    $UsedRange     = $null
    $HeaderRange   = $null
    $TargetHeader  = $null
    $DataRange     = $null
    $TargetRange   = $null

    try
    {
        # Open Read Only

        $Workbook = $Excel.Workbooks.Open(
            $File.FullName,
            3,
            $true
        )

        # First worksheet
        $Sheet = $Workbook.Sheets.Item(1)

        # Used range
        $UsedRange = $Sheet.UsedRange

        $RowCount = $UsedRange.Rows.Count
        $ColCount = $UsedRange.Columns.Count

        # Skip Empty

        if ($RowCount -lt 2)
        {
            Write-Host "  Skipped (no data rows)"
        }
        else
        {
            # Validate Column Count

            if ($null -eq $ExpectedColumns)
            {
                $ExpectedColumns = $ColCount
            }

            if ($ColCount -ne $ExpectedColumns)
            {
                Write-Host "  Skipped (column mismatch)"
            }
            else
            {
                # Validate Headers

                $CurrentHeaders = @()

                for ($c = 1; $c -le $ColCount; $c++)
                {
                    $HeaderText = $Sheet.Cells.Item(1, $c).Text

                    if ($null -eq $HeaderText)
                    {
                        $HeaderText = ""
                    }

                    $CurrentHeaders += $HeaderText.Trim().ToLower()
                }

                if ($null -eq $ExpectedHeaders)
                {
                    $ExpectedHeaders = $CurrentHeaders
                }

                $HeaderMismatch = $false

                for ($i = 0; $i -lt $ExpectedHeaders.Count; $i++)
                {
                    if ($ExpectedHeaders[$i] -ne $CurrentHeaders[$i])
                    {
                        $HeaderMismatch = $true
                        break
                    }
                }

                if ($HeaderMismatch)
                {
                    Write-Host "  Skipped (header mismatch)"
                }
                else
                {
                    # Copy Header

                    if (-not $HeaderCopied)
                    {
                        $HeaderRange = $Sheet.Range(
                            $Sheet.Cells.Item(1,1),
                            $Sheet.Cells.Item(1,$ColCount)
                        )

                        $TargetHeader = $MasterSheet.Range(
                            $MasterSheet.Cells.Item($CurrentRow,1),
                            $MasterSheet.Cells.Item($CurrentRow,$ColCount)
                        )

                        $TargetHeader.Value2 = $HeaderRange.Value2

                        $CurrentRow++
                        $HeaderCopied = $true
                    }

                    # Copy Data

                    $DataRange = $Sheet.Range(
                        $Sheet.Cells.Item(2,1),
                        $Sheet.Cells.Item($RowCount,$ColCount)
                    )

                    $TargetRange = $MasterSheet.Range(
                        $MasterSheet.Cells.Item($CurrentRow,1),
                        $MasterSheet.Cells.Item(
                            $CurrentRow + $RowCount - 2,
                            $ColCount
                        )
                    )

                    # Fast bulk transfer
                    $TargetRange.Value2 = $DataRange.Value2

                    # Advance row pointer
                    $RowsAdded = $RowCount - 1
                    $CurrentRow += $RowsAdded

                    Write-Host "  Added $RowsAdded rows"
                }
            }
        }
    }
    catch
    {
        Write-Host "  ERROR: $($_.Exception.Message)"
    }
    finally
    {
        # Close Workbook

        if ($Workbook)
        {
            $Workbook.Close($false)
        }

        # Release COM Objects

        foreach ($Object in @(
            $TargetRange,
            $DataRange,
            $TargetHeader,
            $HeaderRange,
            $UsedRange,
            $Sheet,
            $Workbook
        ))
        {
            if ($Object)
            {
                [System.Runtime.InteropServices.Marshal]::ReleaseComObject($Object) | Out-Null
            }
        }

        # Null references
        $TargetRange  = $null
        $DataRange    = $null
        $TargetHeader = $null
        $HeaderRange  = $null
        $UsedRange    = $null
        $Sheet        = $null
        $Workbook     = $null
    }
}

# Ensure Data Exists

if (-not $HeaderCopied)
{
    Write-Host ""
    Write-Host "No valid XLSX files found."

    $MasterWorkbook.Close($false)
    $Excel.Quit()

    foreach ($Object in @(
        $MasterSheet,
        $MasterWorkbook,
        $Excel
    ))
    {
        if ($Object)
        {
            [System.Runtime.InteropServices.Marshal]::ReleaseComObject($Object) | Out-Null
        }
    }

    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()

    exit
}

# Auto-Fit Columns

$MasterSheet.Columns.AutoFit() | Out-Null

# Save Master XLSX

Write-Host ""
Write-Host "Saving XLSX..."

$MasterWorkbook.SaveAs(
    $MasterXlsx,
    $xlOpenXMLWorkbook
)

# Save UTF8 CSV

Write-Host "Saving UTF8 CSV..."

$CsvWorkbook   = $null
$CsvSheet      = $null
$SourceRange   = $null
$TargetCsvRange = $null

try
{
    $CsvWorkbook = $Excel.Workbooks.Add()
    $CsvSheet    = $CsvWorkbook.Sheets.Item(1)

    $SourceRange = $MasterSheet.UsedRange

    $TargetCsvRange = $CsvSheet.Range("A1").Resize(
        $SourceRange.Rows.Count,
        $SourceRange.Columns.Count
    )

    $TargetCsvRange.Value2 = $SourceRange.Value2

    $CsvWorkbook.SaveAs(
        $MasterCsv,
        $xlCSVUTF8
    )
}
finally
{
    if ($CsvWorkbook)
    {
        $CsvWorkbook.Close($false)
    }

    foreach ($Object in @(
        $TargetCsvRange,
        $SourceRange,
        $CsvSheet,
        $CsvWorkbook
    ))
    {
        if ($Object)
        {
            [System.Runtime.InteropServices.Marshal]::ReleaseComObject($Object) | Out-Null
        }
    }

    $TargetCsvRange = $null
    $SourceRange    = $null
    $CsvSheet       = $null
    $CsvWorkbook    = $null
}

# Close All

$MasterWorkbook.Close($true)
$Excel.Quit()

foreach ($Object in @(
    $MasterSheet,
    $MasterWorkbook,
    $Excel
))
{
    if ($Object)
    {
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($Object) | Out-Null
    }
}

$MasterSheet    = $null
$MasterWorkbook = $null
$Excel          = $null

# Force Cleanup

[GC]::Collect()
[GC]::WaitForPendingFinalizers()
[GC]::Collect()
[GC]::WaitForPendingFinalizers()

# Finish

Write-Host ""
Write-Host "====================================="
Write-Host "DONE!"
Write-Host "====================================="
Write-Host ""

Write-Host "Created XLSX:"
Write-Host "  $MasterXlsx"

Write-Host ""
Write-Host "Created UTF8 CSV:"
Write-Host "  $MasterCsv"

Write-Host ""
