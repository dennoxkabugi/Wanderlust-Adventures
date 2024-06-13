# cli.py
import click
import sqlite3
from datetime import datetime

DATABASE = 'tourists.db'

def connect_db():
    return sqlite3.connect(DATABASE)

@click.group()
def cli():
    pass

@cli.command()
@click.option('--first-name', prompt='First name', help='The first name of the tourist.')
@click.option('--last-name', prompt='Last name', help='The last name of the tourist.')
def add_tourist(first_name, last_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Tourist (first_name, last_name) VALUES (?, ?)', (first_name, last_name))
    conn.commit()
    conn.close()
    click.echo(f'Tourist {first_name} {last_name} added successfully!')

@cli.command()
def view_tourists():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name FROM Tourist')
    tourists = cursor.fetchall()
    conn.close()
    if tourists:
        for tourist in tourists:
            click.echo(f'ID: {tourist[0]}, Name: {tourist[1]} {tourist[2]}')
    else:
        click.echo('No tourists found.')

@cli.command()
@click.option('--tourist-id', prompt='Tourist ID', help='The ID of the tourist.')
@click.option('--destination', prompt='Destination', help='The destination of the trip.')
@click.option('--arrival-date', prompt='Arrival date (YYYY-MM-DD)', help='The arrival date.')
@click.option('--departure-date', prompt='Departure date (YYYY-MM-DD)', help='The departure date.')
@click.option('--accommodation', prompt='Accommodation (single/double)', help='The type of accommodation.')
def add_trip(tourist_id, destination, arrival_date, departure_date, accommodation):
    conn = connect_db()
    cursor = conn.cursor()
    
    arrival_date_obj = datetime.strptime(arrival_date, '%Y-%m-%d')
    departure_date_obj = datetime.strptime(departure_date, '%Y-%m-%d')
    days = (departure_date_obj - arrival_date_obj).days
    total = days * 10000 if accommodation == 'single' else days * 13000

    cursor.execute('''
        INSERT INTO Trip (tourist_id, destination, arrival_date, departure_date, days, accommodation, total)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (tourist_id, destination, arrival_date, departure_date, days, accommodation, total))
    
    conn.commit()
    conn.close()
    click.echo(f'Trip to {destination} for tourist ID {tourist_id} added successfully!')

@cli.command()
def view_trips():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Trip')
    trips = cursor.fetchall()
    conn.close()
    if trips:
        for trip in trips:
            click.echo(f'ID: {trip[0]}, Tourist ID: {trip[1]}, Destination: {trip[2]}, Arrival Date: {trip[3]}, Departure Date: {trip[4]}, Days: {trip[5]}, Accommodation: {trip[6]}, Total: {trip[7]}')
    else:
        click.echo('No trips found.')

@cli.command()
@click.option('--trip-id', prompt='Trip ID', help='The ID of the trip to delete.')
def delete_trip(trip_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Trip WHERE id = ?', (trip_id,))
    conn.commit()
    conn.close()
    click.echo(f'Trip with ID {trip_id} deleted successfully!')

if __name__ == '__main__':
    cli()
