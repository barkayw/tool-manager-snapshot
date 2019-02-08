# tool-manager-snapshot
Tool to manage AWS EC2 instance

## About

this project is uses BOTO3 to manage AWS EC2 instance snapshots.

### Configuring

Tool-manager-snapshot users the configuration file careated by the AWS cli e.g.

'aws configure --profile Tool-manager-snapshot'

## Running

'pipenv run python snapmanager/snapmanager.py <command> <subcommand> <--project = PROJECT>'

*command* is   instances , volumes or snapshots
*subcommand* depends on the command;  list, start , or stop 
* project is optional
