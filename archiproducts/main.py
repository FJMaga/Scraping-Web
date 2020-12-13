import requests
from bs4 import BeautifulSoup
import iluminacion

def main():


    scraping_iluminacion = iluminacion.Iluminacion()
    scraping_iluminacion.Scraping()


if __name__ == '__main__':
    # iniciamos juego

    #requests.init()
    #BeautifulSoup.init()
    main()