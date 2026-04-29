#requires -RunAsAdministrator
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock" `
    -Name AllowDevelopmentWithoutDevLicense `
    -Value 1