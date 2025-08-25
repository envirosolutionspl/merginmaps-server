import click
from flask import Flask
import random
import string
from datetime import datetime, timezone


def _echo_title(title):
    click.echo("")
    click.echo(f"# {title}")
    click.echo()


def _echo_error(msg):
    click.secho("Error: ", fg="red", nl=False, bold=True)
    click.secho(msg, fg="bright_red")


def add_commands(app: Flask):
    from .app import db
    from mergin.auth.models import UserProfile

    def _check_celery():
        from celery import current_app

        ping_celery = current_app.control.inspect().ping()
        if not ping_celery:
            _echo_error(
                "Proces Celery nie działa poprawnie. Skonfiguruj celery worker oraz celery beat. Powoduje to również problem z wysyłaniem wiadomości e-mail z systemu.",
            )
            return
        click.secho("Celery działa poprawnie.", fg="green")
        return True

    def _send_statistics():
        from .stats.tasks import send_statistics, save_statistics

        _echo_title("Wysyłanie statystyk.")
        # save rows to MerginStatistics table
        save_statistics.delay()

        if not app.config.get("COLLECT_STATISTICS"):
            click.secho(
                "Wysyłanie statystyk jest wyłączone.",
            )
            return

        if not _check_celery():
            return
        send_statistics.delay()
        click.secho("Statystyki zostały wysłane.", fg="green")

    def _send_email(email: str):
        """Send check email to specified email address."""
        from .celery import send_email_async

        _echo_title(f"Wysyłanie wiadomości testowej na podany adres e-mail {email}.")
        if app.config["MAIL_SUPPRESS_SEND"]:
            _echo_error(
                "Wysyłanie wiadomości e-mail jest wyłączone. Ustaw MAIL_SUPPRESS_SEND=False, aby włączyć wysyłanie wiadomości."
            )
            return
        default_sender = app.config.get("MAIL_DEFAULT_SENDER")
        if not default_sender:
            _echo_error(
                "Nie ustawiono domyślnego nadawcy. Ustaw zmienną środowiskową MAIL_DEFAULT_SENDER",
            )
            return
        email_data = {
            "subject": "Sprawdzanie serwera Mergin Maps",
            "html": "Świetnie, konfiguracja poczty serwera Mergin Maps działa poprawnie.",
            "recipients": [email],
            "sender": default_sender,
        }
        try:
            is_celery_running = _check_celery()
            if not is_celery_running:
                return
            send_email_async.delay(**email_data)
        except Exception as e:
            _echo_error(
                f"Błąd podczas wysyłania wiadomości e-mail: {e}",
            )

    def _check_server():  # pylint: disable=W0612
        """Check server configuration."""

        _echo_title("Server health check")
        edition_map = {
            "ce": "Wersja Community",
            "ee": "Wersja Enterprise",
        }
        edition = edition_map.get(app.config["SERVER_TYPE"])
        if edition:
            click.echo(f"Wersja Mergin Maps: {edition}")
        click.echo(f"Wersja Mergin Maps: {app.config['VERSION']}")

        base_url = app.config["MERGIN_BASE_URL"]
        if not base_url:
            _echo_error(
                "Nie ustawiono podstawowego adresu URL. Ustaw zmienną środowiskową MERGIN_BASE_URL",
            )
        else:
            click.secho(f"Base URL of server is {base_url}", fg="green")

        contact_email = app.config["CONTACT_EMAIL"]
        if not contact_email:
            _echo_error(
                "Nie ustawiono adresu e-mail kontaktowego. Ustaw zmienną środowiskową CONTACT_EMAIL",
            )
        else:
            click.secho(f"Twój adres e-mail kontaktowy to {contact_email}.", fg="green")

        tables = db.engine.table_names()
        if not tables:
            _echo_error("Baza danych nie została zainicjalizowana. Uruchom polecenie flask init-db")
        else:
            click.secho("Baza danych została poprawnie zainicjalizowana", fg="green")

        _check_celery()

    def _init_db():
        """Create database tables."""
        from .stats.models import MerginInfo

        _echo_title("Inicjalizacja bazy danych")
        with click.progressbar(
            label="Tworzenie bazy danych", length=4, show_eta=False
        ) as progress_bar:
            progress_bar.update(0)
            db.drop_all(bind=None)
            progress_bar.update(1)
            db.create_all(bind=None)
            progress_bar.update(2)
            db.session.commit()
            progress_bar.update(3)
            info = MerginInfo.query.first()
            if not info and app.config.get("COLLECT_STATISTICS"):
                # create new info with random service id
                service_id = app.config.get("SERVICE_ID", None)
                info = MerginInfo(service_id)
                db.session.add(info)
                db.session.commit()
            progress_bar.update(4)

        click.secho("Tabele zostały utworzone.", fg="green")

    @app.cli.command()
    def init_db():
        """Re-create database tables."""
        _init_db()

    @app.cli.command()
    @click.option("--email", "-e", required=True, envvar="CONTACT_EMAIL")
    @click.option(
        "--recreate",
        "-r",
        help="Odtwórz bazę danych oraz użytkownika administracyjnego.",
        is_flag=True,
        required=False,
    )
    def init(email: str, recreate: bool):
        """Initialize database if does not exist or -r is provided. Perform check of server configuration. Send statistics, respecting your setup."""

        from .auth.models import User

        tables = db.engine.table_names()
        if recreate and tables:
            click.confirm(
                "Czy na pewno chcesz odtworzyć bazę danych i użytkownika administracyjnego? Spowoduje to usunięcie wszystkich danych!",
                default=False,
                abort=True,
            )

        if not tables or recreate:
            _init_db()

            _echo_title("Tworzenie użytkownika administracyjnego. Skopiuj wygenerowane hasło.")
            username = User.generate_username(email)
            password_chars = string.ascii_letters + string.digits
            password = "".join(random.choice(password_chars) for i in range(12))
            user = User(username=username, passwd=password, email=email, is_admin=True)
            user.profile = UserProfile()
            user.active = True
            db.session.add(user)
            db.session.commit()
            click.secho(
                "Użytkownik administracyjny został utworzony. Zapisz wygenerowane hasło.", fg="green"
            )
            click.secho(f"Email: {email}")
            click.secho(f"Nazwa użytkownika: {username}")
            click.secho(f"Hasło: {password}")
        _check_server()
        _send_email(email)
        _send_statistics()

    @app.cli.group()
    def server():
        """Server management commands."""
        pass

    @server.command()
    @click.option("--email", required=True)
    def send_check_email(email: str):  # pylint: disable=W0612
        """Send check email to specified email address."""
        _send_email(email)

    @server.command()
    def check():
        """Check server configuration."""
        _check_server()
