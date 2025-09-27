import click
from rich.console import Console
from rich.table import Table
from safecloud import scanner, utils
from safecloud import crypto
import os
import sys
import urllib.request

from gpt4all import GPT4All

console = Console()

MODEL_URL = "https://the-eye.eu/public/AI/models/nomic-ai/gpt4all/gpt4all-lora-quantized.bin"
MODEL_PATH = os.path.expanduser("~/.safecloud/gpt4all-lora-quantized.bin")


@click.group()
def cli():
    pass


def ensure_ai_model():
    try:
        import gpt4all
    except ImportError:
        console.print("[yellow]gpt4all not found, installing...[/yellow]")
        os.system(f"{sys.executable} -m pip install gpt4all")

    if not os.path.exists(MODEL_PATH) or os.path.getsize(MODEL_PATH) < 1024 * 1024:
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        console.print("[yellow]Model file not found or too small. Downloading GPT4All model...[/yellow]")
        try:
            urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
            console.print("[green]Model downloaded successfully![/green]")
        except Exception as e:
            console.print(f"[red]Failed to download model: {e}[/red]")
            sys.exit(1)
    else:
        console.print("[green]Model file exists. Proceeding...[/green]")


def ai_log_analysis(log_file):
    ensure_ai_model()
    model = GPT4All(MODEL_PATH)
    with open(log_file, "r") as f:
        logs = f.read()
    prompt = f"Analyze the following logs for security threats or anomalies:\n\n{logs}\n\nProvide a summary and potential issues."
    response = model.generate(prompt)
    console.print(f"[cyan]AI Analysis Result:[/cyan]\n{response}")


@cli.command()
@click.argument("logfile")
def logai(logfile):
    ai_log_analysis(logfile)


@cli.command()
@click.argument("bucket_name")
def s3check(bucket_name):
    result = scanner.check_s3(bucket_name)
    if "error" in result:
        console.print(f"[red]Error:[/red] {result['error']}")
    elif result["public"]:
        console.print(f"[red]WARNING:[/red] {bucket_name} is publicly accessible!")
    else:
        console.print(f"[green]Safe:[/green] {bucket_name} is private.")


@cli.command()
@click.argument("ip")
def portscan(ip):
    open_ports = scanner.scan_ports(ip)
    if open_ports:
        console.print(f"[yellow]Open ports:[/yellow] {open_ports}")
    else:
        console.print("[green]Not found: Open ports[/green]")


@cli.command()
@click.argument("target")
@click.option("--ports", "-p", default=None, help="Ports to scan, e.g., 22,80,443 or 20-25")
@click.option("--timeout", "-t", default=1.0, type=float, help="Connection timeout in seconds (not used in current scan)")
@click.option("--banner/--no-banner", default=False, help="Try to grab banner from open ports")
@click.option("--blacklist/--no-blacklist", default=False, help="Perform DNSBL (blacklist) check")
def ipcheck(target, ports, timeout, banner, blacklist):
    console.rule(f"IP CHECK — {target}")

    ip = target
    try:
        import socket as _socket
        if not utils.is_valid_ip(target):
            ip = _socket.gethostbyname(target)
            console.print(f"[cyan]Hostname resolved:[/cyan] {target} -> {ip}")
    except Exception:
        ip = target

    if not utils.is_valid_ip(ip):
        console.print(f"[red]Invalid IP/hostname could not be resolved:[/red] {target}")
        raise SystemExit(1)

    console.print(f"[green]Target IP:[/green] {ip}")

    try:
        rdns = _socket.gethostbyaddr(ip)[0]
        console.print(f"[cyan]Reverse DNS:[/cyan] {rdns}")
    except Exception:
        console.print("[yellow]Reverse DNS not found.[/yellow]")

    port_list = utils.parse_ports(ports)
    if port_list:
        console.print(f"[cyan]Ports to scan:[/cyan] {port_list}")
    else:
        console.print("[cyan]Ports to scan: default (quick scan)[/cyan]")

    open_ports = scanner.scan_ports(ip, ports=port_list)
    if open_ports:
        t = Table(title="Open Ports")
        t.add_column("Port", justify="right")
        t.add_column("Service / Banner", justify="left")
        for p in open_ports:
            b = ""
            if banner and hasattr(scanner, "grab_banner"):
                b = scanner.grab_banner(ip, p)
            t.add_row(str(p), b or "-")
        console.print(t)
    else:
        console.print("[green]No open ports found (limited to quick scan).[/green]")

    if blacklist:
        console.print("[magenta]Starting DNSBL check...[/magenta]")
        bl = scanner.dnsbl_check(ip)
        any_listed = False
        for provider, result in bl.items():
            if isinstance(result, dict) and result.get("listed"):
                any_listed = True
                console.print(f"[red]{provider} => LISTED[/red] {result.get('txt', [])}")
            elif isinstance(result, dict) and not result.get("listed"):
                console.print(f"[green]{provider} => not listed[/green]")
            else:
                console.print(f"[yellow]{provider} => {result}[/yellow]")
        if any_listed:
            console.print("[bold red]WARNING: IP is listed in one or more blacklists![/bold red]")
        else:
            console.print("[green]Blacklist check clear.[/green]")

    console.rule("IP CHECK completed")


@cli.command()
@click.option("--out", "-o", default=None, help="Path to save the generated key (default ~/.safecloud/safecloud.key)")
def keygen(out):
    key = crypto.generate_key(out)
    console.print(f"[green]Key generated and saved:[/green] {out or crypto.DEFAULT_KEY_PATH}")


@cli.command()
@click.argument("infile")
@click.option("--out", "-o", default=None, help="Encrypted output file path (default infile + .enc)")
@click.option("--keyfile", "-k", default=None, help="Key file path (default ~/.safecloud/safecloud.key)")
def encrypt(infile, out, keyfile):
    try:
        path = crypto.encrypt_file(infile, outfile=out, key_path=keyfile)
        console.print(f"[green]Encrypted:[/green] {path}")
    except Exception as e:
        console.print(f"[red]Error encrypting file:[/red] {e}")


@cli.command()
@click.argument("infile")
@click.option("--out", "-o", default=None, help="Decrypted output file path (default removes .enc suffix)")
@click.option("--keyfile", "-k", default=None, help="Key file path (default ~/.safecloud/safecloud.key)")
def decrypt(infile, out, keyfile):
    try:
        path = crypto.decrypt_file(infile, outfile=out, key_path=keyfile)
        console.print(f"[green]Decrypted:[/green] {path}")
    except Exception as e:
        console.print(f"[red]Error decrypting file:[/red] {e}")