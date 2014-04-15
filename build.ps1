Param(
    [string]$op
)

IF ($op -eq "deploy")
{
    appcfg.py .
}
ELSE
{
    dev_appserver.py .
}