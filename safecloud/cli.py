import click
from rich.console import Console
from safecloud import scanner


console = Console()


@click.group()
def cli():
    pass


@cli.command()
@click.argument("bucket_name")
def s3check(bucket_name):
    result = scanner.check_s3(bucket_name)
    if "error" in result:
        console.print(f"[red]Hata:[/red] {result['error']}")
    elif result["public"]:
        console.print(f"[red]UYARI:[/red] {bucket_name} herkese açık!")
    else:
        console.print(f"[green]Güvenli:[/green] {bucket_name} erişime kapalı.")

@cli.command()
@click.argument("ip")
def portscan(ip):
    open_ports = scanner.scan_ports(ip)
    if open_ports:
        console.print(f"[yellow]Açık Portlar:[/yellow] {open_ports}")
    else:
        console.print("[green]Açık port bulunamadı[/green]")