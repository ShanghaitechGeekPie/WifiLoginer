# powershell login for shanghaitech
Clear-Host

$version = "2.1"
$loginurl = "https://controller1.net.shanghaitech.edu.cn:8445/PortalServer//Webauth/webAuthAction!login.action"
#loginurl = "https://10.15.44.172:8445/PortalServer//Webauth/webAuthAction!login.action"

Write-Host "----------------------------------------------" -ForegroundColor "green"
Write-Host "ShanghaiTech Login Script Powershell Beta $version" -ForegroundColor "cyan"
Write-Host "Writen By Dengqi<dengqi@shanghaitech.edu.cn>"    -ForegroundColor "cyan"
Write-Host "----------------------------------------------" -ForegroundColor "green"
Write-Host "Determine the configuration file" -ForegroundColor "green"
$isConfig = Test-Path ".\login_config.json"
If($isConfig -eq $true)
{
    Write-Host "Okay, find the config file."    -ForegroundColor "cyan"
}else {
    while($true){
        $readAccount = Read-Host "Please input your name:"
        Write-Host "Okay, your account is $readAccount. Right?(Y/N)" -ForegroundColor "cyan"
        $readInput = Read-Host "Y for yes, others for no:"
        if($readInput -eq "Y") {
            break;
        }
    }
    while($true){
        $readPassword = Read-Host "Please input your password:" 
        Write-Host "Okay, your password is $readPassword. Right?(Y/N)"  -ForegroundColor "cyan"
        $readInput = Read-Host "Y for yes, others for no:" 
        if($readInput -eq "Y") {
            break;
        }
    }
    $config = @{user=$readAccount;password=$readPassword}
    $configJson = $config | ConvertTo-Json
    $configJson | Set-Content ".\login_config.json"
    $configJson | Out-File ".\login_config.json"
    Write-Host "Okay, write the config file"    -ForegroundColor "cyan"
}

$readConfig = Get-Content ".\login_config.json" | ConvertFrom-Json
$account = $readConfig.user
$password = $readConfig.password

Write-Host "Hello, let's login" -ForegroundColor "cyan"
$postdata = @{userName="$account";password="$password";hasValidateCode="false";authLan="zh_CN"}

$count = 0
While($true)
{
$ha = Invoke-RestMethod -Uri "$loginurl"  -Method Post -Body $postdata 
$dateNow = Get-DAte
If($count -gt 5){
    Write-Host "You have try more than 5 times, script will exit." -ForegroundColor "red"
    Write-Host "You can delete the login_config.json file to re-input the account and password" -ForegroundColor "red"
    break
}
Write-Host "----------------------------------------------" -ForegroundColor "green"
Write-Host "You have try $count times" -ForegroundColor "cyan"
Write-Host "Current time is $dateNow"  -ForegroundColor "cyan"
Write-Host "Login status" -ForegroundColor "cyan"
Write-Host   $ha.success -foregroundcolor "magenta"
If($ha.success -eq $false){
    Write-Host "Retry" -foregroundcolor "red"
    Start-Sleep -s 5
    $count = $count + 1
    continue
}
$count = 0 
Write-Host "----------------------------------------------" -ForegroundColor "green"
Write-Host "Your login account is" -ForegroundColor "cyan"
Write-Host   $ha.data.account -foregroundcolor "magenta"
Write-Host "----------------------------------------------" -ForegroundColor "green"
Write-Host "Your ip is" -ForegroundColor "cyan"
Write-Host   $ha.data.ip -foregroundcolor "magenta"
Write-Host "----------------------------------------------" -ForegroundColor "green"
Start-Sleep -s 1800
}