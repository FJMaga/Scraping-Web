import csv

import requests
from bs4 import BeautifulSoup

import pandas as pd
from numpy.distutils.system_info import tmp


class Iluminacion:

    def __init__(self):

        # Peticion Web

        self.url_base = 'https://www.archiproducts.com'
        self.url_archivos = self.url_base + '/es/productos/iluminacion'

        self.page = requests.get(self.url_archivos, verify=False)

        self.j = 0

    def Scraping(self):
        if self.page.status_code == 200:

            self.j=0


            print("")
            print("DATOS EXTRAIDOS DE: " + str(self.url_archivos))
            print("")
            '''
            #print(self.page)
            #print(self.page.text)

            # Div contenedor enlaces datos Iluminacion interior
            soup_interiores = BeautifulSoup(self.page.text, 'html.parser')
            #print(soup_interiores.find(attrs = {"data-id": "794"}))
            #print(soup_interiores.find(attrs={"data-id": "794"}).find_all('a', href=True))

            href_archivos_iluminacion_interior = []
            for href in soup_interiores.find(attrs={"data-id": "794"}).find_all('a', href=True):
                href_archivos_iluminacion_interior.append(href['href'])

            href_archivos_iluminacion_interior.remove(href_archivos_iluminacion_interior[0])

            #print("")
            #print("Interior -> " + str(href_archivos_iluminacion_interior))
            #print("Cantidad de categorias encontrados en Iluminacion interior: " + str(len(href_archivos_iluminacion_interior)))
            #print("")

            #cont=0
            #i=0
            cont = 21618
            i = 5
            #cont = 24518
            #i = 9
            while i < len(href_archivos_iluminacion_interior):

                print("Interior --> "+str(i))

                #href_archivos_iluminacion_interior = href_archivos_iluminacion_interior[:2]
                categorias_interior=[]
                cantidad = []
                #for categoria in href_archivos_iluminacion_interior:
                page_categoria_interior = requests.get(self.url_base + href_archivos_iluminacion_interior[i])
                soup_categoria_interior = BeautifulSoup(page_categoria_interior.text, 'html.parser')

                href_archivos_iluminacion_interior_pag = [href_archivos_iluminacion_interior[i]]
                #print(soup_categoria_interior.find(class_='title-content-wrapper').find_all('span'))
                for n_pag in soup_categoria_interior.find(class_='title-content-wrapper').find_all('span'):

                    n_pag_sin_punto = (n_pag.text).replace(".", "")
                    int_n_pag = int(n_pag_sin_punto) / 60
                    print("nuemero articulos por categoria " + str(n_pag_sin_punto))
                    print("nuemero paginas por categoria " + str(int((int_n_pag))))

                    for pag in range(2, int(int_n_pag) + 2):
                        href_archivos_iluminacion_interior_pag.append(href_archivos_iluminacion_interior[i] + "/" + str(pag))
                    #print(href_archivos_iluminacion_interior_pag)
                for categoria in href_archivos_iluminacion_interior_pag:

                    page_categoria_interior_pag = requests.get(self.url_base + categoria)
                    soup_categoria_interior_pag = BeautifulSoup(page_categoria_interior_pag.text, 'html.parser')

                    #print(soup_categoria_interior_pag)

                    if not soup_categoria_interior_pag.find(id='productGrid').find_all('a', href=True) == None:

                        href_soup_categoria_interior_pag=[]

                        for href in soup_categoria_interior_pag.find(id='productGrid').find_all('a', href=True):

                            href_soup_categoria_interior_pag.append(href['href'])
                        #print(href_soup_categoria_interior_pag)
                        #print(str(len(href_soup_categoria_interior_pag)))

                    #print(href_soup_categoria_interior_pag)

                    #href_soup_categoria_interior_pag = href_soup_categoria_interior_pag[:3]
                    articulos_categoria_interior = []

                    for articulo in href_soup_categoria_interior_pag:
                        page_articulo_categoria_interior = requests.get(self.url_base + articulo)
                        soup_articulo_categoria_interior = BeautifulSoup(page_articulo_categoria_interior.text,'html.parser')
                        # print(soup_articulo_categoria_interior.find(id='product-image'))
                        # print(soup_articulo_categoria_interior.find(id='product-image').find_all('img', content=True))

                        articulo_categoria_interior = {}
                        imagenes_categoria_interior = []
                        b_categoria_interior = []
                        h_categoria_interior = []
                        b_h = {}
                        # print(i)
                        num = len(b_categoria_interior)
                        if soup_articulo_categoria_interior.find(class_="accordion-item is-active").find_all('b') is not None:
                            for b in soup_articulo_categoria_interior.find(class_="accordion-item is-active").find_all('b'):
                                b_categoria_interior.append(b.text)
                                # print(soup_articulo_categoria_interior.find(class_="accordion-item is-active"))

                            for h in soup_articulo_categoria_interior.find(class_="accordion-item is-active").find_all(
                                    'h2'):
                                h_categoria_interior.append(h.text)
                            h_categoria_interior.remove(h_categoria_interior[num])
                        else:
                            b_categoria_interior.append(None)
                            h_categoria_interior.append(None)

                        #itemprop = "description"

                        #print(soup_articulo_categoria_interior.find(itemprop="description"))
                        descripcion_categoria_interior = []
                        string_descrip = []
                        k=0
                        for item in soup_articulo_categoria_interior.find(itemprop="description"):
                            descripcion_categoria_interior.append(item)

                            #print(descripcion_categoria_interior.replace("\u200e",''))
                            string_descrip.append((str(descripcion_categoria_interior[k]).replace("\u200e",'')).replace("\xa0",''))
                            k += 1
                        #print(string_descrip)

                        #print(soup_articulo_categoria_interior.find(class_="callout box-product-info").find_all('h1'))

                        h1_item=[]
                        for fabricante in soup_articulo_categoria_interior.find(class_="callout box-product-info").find_all('a',title=True):
                            h1_item.append(fabricante.text)

                            articulo_categoria_interior['Id'] = cont
                        cont += 1
                        #print(h1_item)

                        if len(h1_item) == 3:
                            articulo_categoria_interior['Fabricante'] = str(h1_item[1])
                            articulo_categoria_interior['Nombre'] = str(h1_item[2])
                        if len(h1_item) == 4:
                            articulo_categoria_interior['Fabricante'] = str(h1_item[1])
                            articulo_categoria_interior['Nombre'] = str(h1_item[2])
                        if len(h1_item) == 5:
                            articulo_categoria_interior['Fabricante'] = str(h1_item[1])
                            articulo_categoria_interior['Nombre'] = str(h1_item[2] + ' ' + h1_item[3])

                        if not soup_articulo_categoria_interior.find(class_="price-distance price-group") == None:

                            if soup_articulo_categoria_interior.find(class_="text-info size-m through old-price") is not None:
                                for pvp in soup_articulo_categoria_interior.find(class_="text-info size-m through old-price"):
                                    articulo_categoria_interior['Pvp'] = ((pvp.replace("\n",'')).replace(" €\n",'')).replace(",",'.')
                            else:
                                articulo_categoria_interior['Pvp'] = None
                            if soup_articulo_categoria_interior.find(class_="title size-m text-price price float-left") is not None:
                                for pvp_descuento in soup_articulo_categoria_interior.find(class_="title size-m text-price price float-left"):
                                    articulo_categoria_interior['Pvp_descuento'] = ((pvp_descuento.replace("\n",'')).replace(" €\n",'')).replace(",",'.')
                            else:
                                articulo_categoria_interior['Pvp_descuento'] = None
                        else:
                            articulo_categoria_interior['Pvp'] = None
                            articulo_categoria_interior['Pvp_descuento'] = None
                            articulo_categoria_interior['Energia'] = None

                        for art in soup_articulo_categoria_interior.find(id='product-image').find_all('img', content=True):

                            #print(b_categoria_interior)
                            #print(h_categoria_interior)
                            #print(articulo_categoria_interior)
                            #print(b_h)
                            if imagenes_categoria_interior is not None:
                                imagenes_categoria_interior.append(art['content'])
                            else:
                                imagenes_categoria_interior.append('')
                            articulo_categoria_interior['categoria'] = 'Iluminación de interiores'
                            string_href_archivos_iluminacion_interior = str(href_archivos_iluminacion_interior[i])
                            articulo_categoria_interior['Subcategoria'] = str(string_href_archivos_iluminacion_interior[14:]).replace("-", " ")

                            if len(b_categoria_interior) == len(h_categoria_interior):
                                self.j = 0
                                for etiqueta_b in b_categoria_interior:
                                    b_h[b_categoria_interior[self.j]] = h_categoria_interior[self.j]
                                    articulo_categoria_interior[b_categoria_interior[self.j]] = h_categoria_interior[self.j]
                                    # articulos_categoria_interior.append(articulo_categoria_interior)
                                    # print(b_categoria_interior[self.j] + "  " + articulo_categoria_interior[etiqueta_b])
                                    self.j += 1
                            else:
                                pass
                                
                        lista_dimensiones=[]
                        lista_variantes=[]
                        imagen_dimensiones=[]
                        imagen_variantes=[]
                        for extras in soup_articulo_categoria_interior.find_all("div", attrs={"class":"accordion-content"}):
                            for extra in extras.find_all('img',alt=True):

                                #print(extra['alt'])
                                #print(str(extra['alt'])[:11])
                                #print(str(extra['alt'])[:20])
                                if str(extra['alt'])[:11] == 'Dimensiones':
                                    imagen_dimensiones.append(extra['alt'])
                                    if extras.find_all('img', alt=imagen_dimensiones):
                                        lista_dimensiones.append(extras.find_all('img', alt=imagen_dimensiones))
                                if str(extra['alt'])[:20] == 'Galería de variantes':
                                    imagen_variantes.append(extra['alt'])
                                    if extras.find_all('img', alt=imagen_variantes):
                                        lista_variantes.append(extras.find_all('img', alt=imagen_variantes))
                                else:
                                    pass


                        #print(lista_datos_proveedor)
                        lista_imagenes_dim=[]
                        for datos in lista_dimensiones:
                            #print(str(datos).replace('lazy-src','src'))
                            lista_imagenes_dim.append(str(datos).replace('lazy-src','src'))
                        lista_imagenes_var = []
                        for datos in lista_variantes:
                            # print(str(datos).replace('lazy-src','src'))
                            lista_imagenes_var.append(str(datos).replace('lazy-src', 'src'))

                        # print(b_categoria_exterior)
                        # print(h_categoria_exterior)
                        # print(b_h)

                        
                        articulo_categoria_interior['Descripcion'] = string_descrip
                        articulo_categoria_interior['imagenes'] = imagenes_categoria_interior
                        articulo_categoria_interior['imagenes_dimensiones'] = lista_imagenes_dim
                        articulo_categoria_interior['imagenes_variantes'] = lista_imagenes_var
                        articulos_categoria_interior.append(articulo_categoria_interior)

                        import json
                        import os

                        with open('articulos_categoria_interior.json', 'a+', encoding='utf-8') as f:
                            f.seek(0,2)  # Go to the end of file
                            print(f.tell())
                            if f.tell() == 0:  # Check if file is empty
                                json.dump([articulo_categoria_interior], f, ensure_ascii=False, indent=4)# If empty, write an array
                            else:
                                f.seek(0, 2)
                                f.truncate(f.tell() - 3)  # Remove the last character, open the array
                                f.write('},')  # Write the separator
                                json.dump(articulo_categoria_interior, f, ensure_ascii=False,
                                          indent=4)  # Dump the dictionary
                                f.write(']')  # Close the array
                                print(f)
                                

                df = pd.read_json('articulos_categoria_interior.json', encoding='utf-8')
                df.to_csv('articulos_categoria_interior.csv', index=False, header=True,
                          encoding='utf-8')


                    #print(articulos_categoria_interior)

                i += 1
                

                '''
            #df = pd.read_json('articulos_categoria_interior.json')
            #df.to_csv('articulos_categoria_interior.csv', index=False, header=True)

            # ----------------------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------

            # Div contenedor enlaces datos Iluminacion exterior
            soup_exteriores = BeautifulSoup(self.page.text, 'html.parser')
            #print(soup_exteriores.find(attrs={"data-id": "762"}))
            #print(soup_exteriores.find(attrs={"data-id": "762"}).find_all('a', href=True))
            href_archivos_iluminacion_exterior = []
            for href in soup_exteriores.find(attrs={"data-id": "762"}).find_all('a', href=True):
                if(href['href'] == '/es/productos/iluminacion-para-exteriores'):
                    href['href'] = '/es/productos/farolas'
                href_archivos_iluminacion_exterior.append(href['href'])

            href_archivos_iluminacion_exterior.remove(href_archivos_iluminacion_exterior[0])
            #print("Exterior -> " + str(href_archivos_iluminacion_exterior))
            articulosList =[]
            i = 0
            cont = 25690
            while i < len(href_archivos_iluminacion_exterior):

                print("Exterior --> " + str(i))

                # href_archivos_iluminacion_exterior = href_archivos_iluminacion_exterior[:2]
                categorias_exterior = []
                cantidad = []
                # for categoria in href_archivos_iluminacion_exterior:
                page_categoria_exterior = requests.get(self.url_base + href_archivos_iluminacion_exterior[i])
                soup_categoria_exterior = BeautifulSoup(page_categoria_exterior.text, 'html.parser')

                href_archivos_iluminacion_exterior_pag = [href_archivos_iluminacion_exterior[i]]
                #print(soup_categoria_exterior.find(class_='title-content-wrapper').find_all('span'))
                for n_pag in soup_categoria_exterior.find(class_='title-content-wrapper').find_all('span'):

                    n_pag_sin_punto = (n_pag.text).replace(".", "")
                    int_n_pag = int(n_pag_sin_punto) / 60
                    print("nuemero articulos por categoria " + str(n_pag_sin_punto))
                    print("nuemero paginas por categoria " + str(int((int_n_pag))))

                    for pag in range(2, int(int_n_pag) + 2):
                        href_archivos_iluminacion_exterior_pag.append(
                            href_archivos_iluminacion_exterior[i] + "/" + str(pag))
                    #print(href_archivos_iluminacion_exterior_pag)
                for categoria in href_archivos_iluminacion_exterior_pag:

                    page_categoria_exterior_pag = requests.get(self.url_base + categoria)
                    soup_categoria_exterior_pag = BeautifulSoup(page_categoria_exterior_pag.text, 'html.parser')

                    # print(soup_categoria_exterior_pag)

                    if not soup_categoria_exterior_pag.find(id='productGrid').find_all('a', href=True) == None:

                        href_soup_categoria_exterior_pag = []

                        for href in soup_categoria_exterior_pag.find(id='productGrid').find_all('a', href=True):
                            href_soup_categoria_exterior_pag.append(href['href'])
                        # print(href_soup_categoria_exterior_pag)
                        #print(str(len(href_soup_categoria_exterior_pag)))

                    # print(href_soup_categoria_exterior_pag)

                    # href_soup_categoria_exterior_pag = href_soup_categoria_exterior_pag[:3]
                    articulos_categoria_exterior = []

                    for articulo in href_soup_categoria_exterior_pag:
                        page_articulo_categoria_exterior = requests.get(self.url_base + articulo)
                        soup_articulo_categoria_exterior = BeautifulSoup(page_articulo_categoria_exterior.text,
                                                                         'html.parser')
                        # print(soup_articulo_categoria_exterior.find(id='product-image'))
                        # print(soup_articulo_categoria_exterior.find(id='product-image').find_all('img', content=True))

                        articulo_categoria_exterior = {}
                        imagenes_categoria_exterior = []
                        b_categoria_exterior = []
                        h_categoria_exterior = []
                        b_h = {}
                        # print(i)
                        num = len(b_categoria_exterior)
                        if soup_articulo_categoria_exterior.find(class_="accordion-item is-active").find_all(
                                'b') is not None:
                            for b in soup_articulo_categoria_exterior.find(class_="accordion-item is-active").find_all('b'):
                                b_categoria_exterior.append(b.text)
                                # print(soup_articulo_categoria_exterior.find(class_="accordion-item is-active"))

                            for h in soup_articulo_categoria_exterior.find(class_="accordion-item is-active").find_all(
                                    'h2'):
                                h_categoria_exterior.append(h.text)
                            h_categoria_exterior.remove(h_categoria_exterior[num])
                        else:
                            b_categoria_exterior.append(None)
                            h_categoria_exterior.append(None)
                        # itemprop = "description"

                        # print(soup_articulo_categoria_exterior.find(itemprop="description"))
                        descripcion_categoria_exterior = []
                        string_descrip = []
                        k = 0
                        for item in soup_articulo_categoria_exterior.find(itemprop="description"):
                            descripcion_categoria_exterior.append(item)

                            # print(descripcion_categoria_exterior.replace("\u200e",''))
                            string_descrip.append(
                                (str(descripcion_categoria_exterior[k]).replace("\u200e", '')).replace("\xa0", ''))
                            k += 1
                        # print(string_descrip)

                        # print(soup_articulo_categoria_exterior.find(class_="callout box-product-info").find_all('h1'))

                        h1_item = []
                        for fabricante in soup_articulo_categoria_exterior.find(
                                class_="callout box-product-info").find_all('a', title=True):
                            h1_item.append(fabricante.text)

                            # print(h1_item)
                            articulo_categoria_exterior['Id'] = cont
                        cont += 1

                        if len(h1_item) == 3:
                            articulo_categoria_exterior['Fabricante'] = str(h1_item[1])
                            articulo_categoria_exterior['Nombre'] = str(h1_item[2])
                        if len(h1_item) == 4:
                            articulo_categoria_exterior['Fabricante'] = str(h1_item[1])
                            articulo_categoria_exterior['Nombre'] = str(h1_item[2])
                        if len(h1_item) == 5:
                            articulo_categoria_exterior['Fabricante'] = str(h1_item[1])
                            articulo_categoria_exterior['Nombre'] = str(h1_item[2] + ' ' + h1_item[3])

                        if not soup_articulo_categoria_exterior.find(class_="price-distance price-group") == None:

                            if soup_articulo_categoria_exterior.find(
                                    class_="text-info size-m through old-price") is not None:
                                for pvp in soup_articulo_categoria_exterior.find(
                                        class_="text-info size-m through old-price"):
                                    articulo_categoria_exterior['Pvp'] = (
                                        (pvp.replace("\n", '')).replace("€\n", '')).replace(",", '.')
                            else:
                                articulo_categoria_exterior['Pvp'] = None
                            if soup_articulo_categoria_exterior.find(
                                    class_="title size-m text-price price float-left") is not None:
                                for pvp_descuento in soup_articulo_categoria_exterior.find(
                                        class_="title size-m text-price price float-left"):
                                    articulo_categoria_exterior['Pvp_descuento'] = (
                                        (pvp_descuento.replace("\n", '')).replace("€\n", '')).replace(",", '.')
                            else:
                                articulo_categoria_exterior['Pvp_descuento'] = None

                        else:
                            articulo_categoria_exterior['Pvp'] = None
                            articulo_categoria_exterior['Pvp_descuento'] = None
                            articulo_categoria_exterior['Energia'] = None


                        for art in soup_articulo_categoria_exterior.find(id='product-image').find_all('img',
                                                                                                      content=True):

                            # print(b_categoria_exterior)
                            # print(h_categoria_exterior)
                            # print(articulo_categoria_exterior)
                            # print(b_h)
                            if imagenes_categoria_exterior is not None:
                                imagenes_categoria_exterior.append(art['content'])
                            else:
                                imagenes_categoria_exterior.append('')
                            articulo_categoria_exterior['categoria'] = 'Iluminación de exteriores'
                            string_href_archivos_iluminacion_exterior = str(href_archivos_iluminacion_exterior[i])
                            articulo_categoria_exterior['Subcategoria'] = str(
                                string_href_archivos_iluminacion_exterior[14:]).replace("-", " ")

                            if len(b_categoria_exterior) == len(h_categoria_exterior):
                                self.j = 0
                                for etiqueta_b in b_categoria_exterior:
                                    b_h[b_categoria_exterior[self.j]] = h_categoria_exterior[self.j]
                                    articulo_categoria_exterior[b_categoria_exterior[self.j]] = h_categoria_exterior[
                                        self.j]
                                    # articulos_categoria_exterior.append(articulo_categoria_exterior)
                                    # print(b_categoria_exterior[self.j] + "  " + articulo_categoria_exterior[etiqueta_b])
                                    self.j += 1
                            else:
                                pass
                        #print(soup_articulo_categoria_exterior.find_all("div", attrs={"class":"accordion-content"}).find_all('img'))
                        lista_dimensiones = []
                        lista_variantes = []
                        imagen_dimensiones = []
                        imagen_variantes = []
                        for extras in soup_articulo_categoria_exterior.find_all("div",
                                                                                attrs={"class": "accordion-content"}):
                            for extra in extras.find_all('img', alt=True):

                                # print(extra['alt'])
                                # print(str(extra['alt'])[:11])
                                # print(str(extra['alt'])[:20])
                                if str(extra['alt'])[:11] == 'Dimensiones':
                                    imagen_dimensiones.append(extra['alt'])
                                    if extras.find_all('img', alt=imagen_dimensiones):
                                        lista_dimensiones.append(extras.find_all('img', alt=imagen_dimensiones))
                                if str(extra['alt'])[:20] == 'Galería de variantes':
                                    imagen_variantes.append(extra['alt'])
                                    if extras.find_all('img', alt=imagen_variantes):
                                        lista_variantes.append(extras.find_all('img', alt=imagen_variantes))
                                else:
                                    pass

                        # print(lista_datos_proveedor)
                        lista_imagenes_dim = []
                        for datos in lista_dimensiones:
                            # print(str(datos).replace('lazy-src','src'))
                            lista_imagenes_dim.append(str(datos).replace('lazy-src', 'src'))
                        lista_imagenes_var = []
                        for datos in lista_variantes:
                            # print(str(datos).replace('lazy-src','src'))
                            lista_imagenes_var.append(str(datos).replace('lazy-src', 'src'))


                        # print(b_categoria_exterior)
                        # print(h_categoria_exterior)
                        # print(b_h)
                        articulo_categoria_exterior['Descripcion'] = string_descrip
                        articulo_categoria_exterior['imagenes'] = imagenes_categoria_exterior
                        articulo_categoria_exterior['imagenes_dimensiones'] = lista_imagenes_dim
                        articulo_categoria_exterior['imagenes_variantes'] = lista_imagenes_var
                        articulos_categoria_exterior.append(articulo_categoria_exterior)

                        import json
                        import os

                        with open('articulos_categoria_exterior.json', 'a+', encoding='utf-8') as f:
                            f.seek(0, 2)  # Go to the end of file
                            print(f.tell())
                            if f.tell() == 0:  # Check if file is empty
                                json.dump([articulo_categoria_exterior], f, ensure_ascii=False,
                                          indent=4)  # If empty, write an array
                            else:
                                f.seek(0, 2)
                                f.truncate(f.tell() - 3)  # Remove the last character, open the array
                                f.write('},')  # Write the separator
                                json.dump(articulo_categoria_exterior, f, ensure_ascii=False,
                                          indent=4)  # Dump the dictionary
                                f.write(']')  # Close the array
                                print(f)

                df = pd.read_json('articulos_categoria_exterior.json', encoding='utf-8')
                df.to_csv('articulos_categoria_exterior.csv', index=False, header=True,
                          encoding='utf-8')
                            #print(articulo_categoria_exterior)


                    #print(articulos_categoria_exterior)
                i += 1


            '''
            from os import listdir

            filepaths = [f for f in listdir("./") if f.endswith('.csv')]
            df = pd.concat(map(pd.read_csv, filepaths))
            df.to_csv('scraping_web_archiproducts_iluminacion.csv', index=False, header=True)
            '''
        else:
            print("Error code %s" % self.page.status_code)



