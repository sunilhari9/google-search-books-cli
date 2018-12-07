import click
import requests
import json
import os
from operator import itemgetter
from pyfiglet import Figlet
f = Figlet(font='big')

@click.group()
def main():
    """
    Simple CLI for querying books on Google Books
    """
    pass

@main.command()
@click.argument('query',default='',metavar='<Max Results>')
@click.argument('max', default=20,metavar='<Book Name>')
def search(query,max):
    """Return list of Book Available based on <Book Name> entered with <Max Results> defaulted to 20
    """
    print(f.renderText("CLI Search"))
    if not query:
        click.echo("Popular search strings 'HTML','PHP','Python', ‘Java’")
        query = click.prompt('Please enter a Book Name to Search')       
    else:
        click.echo("List of books available for given Search: "+query)
    
        
    url_format = 'https://www.googleapis.com/books/v1/volumes'
    query = "+".join(query.split())

    query_params = {
        'q': query,
        'maxResults':max
    }
    response = requests.get(url_format, params=query_params)
    for response in response.json()['items']:        # traversal of List Books
        click.echo("Book Name: "+ response['volumeInfo']['title']+" Id: "+response['id'])
    
@main.command()
@click.argument('id',default='',metavar='<Book ID>')
def add(id):
    """This add the Book in to your shelf"""
    url_format = 'https://www.googleapis.com/books/v1/volumes/{}'
    if not id:
        id = click.prompt('Please enter a Book Id to add it in to your shelf')       
    bookDetails = requests.get(url_format.format(id))
    if('error' not in bookDetails.json()):
        if os.path.exists("bookshelf.json"):
            jsonFile = open("bookshelf.json", "r") # Open the JSON file for reading
            data = json.load(jsonFile) # Read the JSON into the buffer
            jsonFile.close()
            for response in data:        # traversal of local List Books
                available = False
                if (response['id'] == id):
                    available = True            
            if(not available):
                with open('bookshelf.json', 'w') as outfile:
                    data.append(bookDetails.json())
                    json.dump(data, outfile)
                    print(f.renderText("Added Sucessfully"))
            else:
                click.echo("Already in your shelf..!")   
        else:
            with open('bookshelf.json', 'w') as outfile:
                data = []
                data.append(bookDetails.json())
                json.dump(data, outfile)
                print(f.renderText("Added Sucessfully"))                
    else:
        click.echo("Not Valid Book please enter valid ID..!") 
        
@main.command()
@click.argument('id')
def read(id):
    """This return Description of the Book"""
    url_format = 'https://www.googleapis.com/books/v1/volumes/{}'
    response = requests.get(url_format.format(id))        
    click.echo(response.json()['volumeInfo']['description'])
    
@main.command()
def clearbooks():
    """This will remove all books from shelf"""
    os.remove("bookshelf.json")
    print(f.renderText("Cleared"))
    
@main.command()
@click.argument('sortby',default='',metavar='<Sort by>')
def mybooks(sortby):
    """This return a List of books in your shelf"""
    if os.path.exists("bookshelf.json"):
        jsonFile = open("bookshelf.json", "r") # Open the JSON file for reading
        data = json.load(jsonFile) # Read the JSON into the buffer
        jsonFile.close()
        if not sortby:
            newlist = data
        else:
            newlist = sorted(data, key=lambda e: e.get('volumeInfo', {}).get(sortby))
        #newlist = sorted(data, key=lambda x: ([x]['title']))
        #print(newList)
        for response in newlist:        # traversal of local List Books
            #print(response['volumeInfo']['pageCount'])
            click.echo("Book Name: "+ response['volumeInfo']['title'] + ", No Of Pages: " +str(response['volumeInfo']['pageCount']))
    else:      
        click.echo("No Books..!")

if __name__ == "__main__":
    main()
