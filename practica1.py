#!/usr/bin/python3

import webapp
from urllib.parse import unquote


class MyApp (webapp.webApp):

    urlsLargas = {}
    urlsAcortadas = {}

    def parse(self, request):
        return (request.split(' ', 1)[0], request.split(' ', 2)[1],
                request.split('=')[-1])

    def process(self, parsed):
        self.urlsContador = len(self.urlsLargas)
        method, resource, content = parsed
        form = ("<form method = 'POST'>" +
                "<b>Introduce la URL que se quiera acortar: </b><br>" +
                "<input type='text' name='url'><br>" +
                "<input type='submit' value='Enviar'></form>")
        if method == "GET":
            if resource == "/favicon.ico":
                returnCode = "HTTP/1.1 404 Not Found"
                htmlAnswer = ("<html><body><h1>Not Found</h1></body></html>")

            elif resource == "/":
                returnCode = "HTTP/1.1 200 OK"
                htmlAnswer = ("<html><body>" + form +
                              str(self.urlsAcortadas) + "</body></html>")
            else:
                resource = int(resource[1:])
                if resource in self.urlsAcortadas:
                    returnCode = "HTTP/1.1 302 Found"
                    htmlAnswer = ("<html><body><meta http-equiv='refresh'" +
                                  "content='1 url=" +
                                  self.urlsAcortadas[resource] + "'>" +
                                  "</p>" + "</body></html>")
                else:
                    returnCode = "HTTP/1.1 404 Not Found"
                    htmlAnswer = ("<html><body><h1>" +
                                  "Ha surgido un problema:</h1>" +
                                  "Recurso no encontrado.</body></html>")

        elif method == "POST":
            if content == "":
                returnCode = "HTTP/1.1 400 Bad Request"
                htmlAnswer = ("<html><body><h1>" +
                              "Ha surgido un problema:</h1>" +
                              "El formulario esta vacio" +
                              "<p><small>(Se debe introducir una url que" +
                              " se quiera acortar)</small></p></body></html>")

            else:
                if (content[0:14] == "https%3A%2F%2F" or
                        content[0:13] == "http%3A%2F%2F"):
                    content = unquote(content)
                else:
                    content = "http://" + content
                if content in self.urlsLargas:
                    enlace = str(self.urlsLargas[content])
                    enlace = "http://localhost:1234/" + enlace
                    returnCode = "HTTP/1.1 200 Ok"
                    htmlAnswer = ("<html><body>" + "<a href=" + enlace + ">" +
                                  enlace + "</a>" + "</body></html>")
                else:
                    self.urlsLargas[content] = self.urlsContador
                    enlace = "http://localhost:1234/" + str(self.urlsContador)
                    self.urlsAcortadas[self.urlsContador] = content
                    self.urlsContador = self.urlsContador + 1
                    returnCode = "HTTP/1.1 200 Ok"
                    htmlAnswer = ("<html><body>" + "<a href=" + enlace + ">" +
                                  enlace + "</a>" + "</body></html>")

        else:
            returnCode = "HTTP/1.1 405 Method Not Allowed"
            htmlAnswer = ("<html><body><h1>" +
                          "Ha surgido un problema:</h1>" +
                          "Metodo no permitido.</body></html>")
        return (returnCode, htmlAnswer)

if __name__ == "__main__":
    try:
        testWebApp = MyApp("localhost", 1234)
    except KeyboardInterrupt:
        print("Closing binded socket")
