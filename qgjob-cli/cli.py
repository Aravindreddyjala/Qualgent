import click, requests

BACKEND_URL = "http://localhost:8000"

@click.group()
def cli():
    pass

@cli.command()
@click.option('--org-id', required=True)
@click.option('--app-version-id', required=True)
@click.option('--test', required=True)
def submit(org_id, app_version_id, test):
    payload = {
        "org_id": org_id,
        "app_version_id": app_version_id,
        "test_path": test
    }
    resp = requests.post(f"{BACKEND_URL}/submit-job", json=payload)
    if resp.ok:
        click.echo(f"Job submitted successfully, Job ID: {resp.json()['job_id']}")
    else:
        click.echo(f"Failed to submit job: {resp.text}")

@cli.command()
@click.option('--job-id', required=True)
def status(job_id):
    resp = requests.get(f"{BACKEND_URL}/status/{job_id}")
    if resp.ok:
        data = resp.json()
        click.echo(f"Job Status for {data['job_id']}: {data['status']}")
    else:
        click.echo(f"Job not found: {resp.text}")

if __name__ == "__main__":
    cli()

