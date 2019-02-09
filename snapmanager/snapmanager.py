import boto3
import click

session = boto3.Session(profile_name='barkay_wolfsohn')
ec2 = session.resource('ec2')

def filter_instances(project):

    instances = []
    if project:
        filters = [{'Name':'tag:project' , 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances


@click.group()
def cli():
    """Tool-manager-snapshot mamag snapshots"""

@cli.group('snapshots')
def snapshots():
    """ Commands for snapshots"""

@snapshots.command('list')

@click.option('--project', default=None,
        help="Only volumes for the progect(tag Progect:<name>)")
def list_volumes(project):
    "List EC2 snapshots"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime("%c")
                )))
    return


@cli.group('volumes')
def volumes():
    """ Commands for volumes"""

@volumes.command('list')
@click.option('--project', default=None,
        help="Only volumes for the progect(tag Progect:<name>)")
def list_volumes(project):
    "List EC2 volumes"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(", ".join((
                v.id,
                i.id,
                v.state,
                str(v.size) + "GiB",
                v.encrypted and "Encrypted" or "Not Encrypted"
            )))

    return

@cli.group('instances')
def instances():
        """Commands for instences"""

@instances.command('snapshot',
        help="Criate snapshots for all volumes")
@click.option('--project', default=None,
        help="Only instances for the progect(tag Progect:<name>)")

def create_snapshots(project):
    "Create snapshot for EC2 instances"

    instances = filter_instances(project)

    for i in instances:

        i.stop()
        i.wait_until_stopped()

        for v in i.volumes.all():
            print('create snapshot for {0}'.format(v.id))
            v.create_snapshot(Description="Created by Snapshot Script")
        print("Strating {0}...".format(i.id))

        i.start()
        i.wait_until_running()

    print("Job's done!")
    return


@instances.command('list')
@click.option('--project', default=None,
        help="Only instances for the progect(tag Progect:<name>)")
def list_instances(project):
    "List EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        tags = { t['Key']: t['Value'] for t in  i.tags or [] }
        print(', '.join((
        i.id,
        i.instance_type,
        i.placement['AvailabilityZone'],
        i.state['Name'],
        i.public_dns_name,
        tags.get('project', '<no project>')
        )))
    return

@instances.command('stop')
@click.option('--project', default=None,
        help="only instances from the project")
def stop_instances(project):
    "stop EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("Stoping {0}...".format(i.id))
        i.stop()

    return

@instances.command('start')
@click.option('--project', default=None,
        help="only instances from the project")
def start_instances(project):
    "stop EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("Starting {0}...".format(i.id))
        i.start()

    return

if __name__ == '__main__':
    cli()
